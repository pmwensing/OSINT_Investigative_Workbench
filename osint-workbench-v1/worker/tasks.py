from __future__ import annotations
from datetime import datetime, timezone
from uuid import UUID
import json

from sqlalchemy import select

from worker.celery_app import celery_app
from worker.connectors.factory import get_connector
from worker.normalization import normalize_value
from api.db.session import SessionLocal
from api.db.models import Job, Target, Artifact, Entity, Observable, Relationship, Claim, Contradiction, TimelineEvent
from shared.storage import get_minio_client, put_json_bytes
from shared.neo4j_sync import sync_graph
from api.core.config import settings

@celery_app.task(name="worker.tasks.run_job")
def run_job(job_id: str) -> dict:
    db = SessionLocal()
    try:
        job = db.get(Job, UUID(job_id))
        if not job:
            raise RuntimeError("Job not found")

        target = db.get(Target, job.target_id)
        if not target:
            raise RuntimeError("Target not found")

        job.status = "running"
        job.started_at = datetime.now(timezone.utc)
        db.commit()

        connector = get_connector(job.connector)
        result = connector.run(target.target_type, target.value)

        raw = json.dumps(result.get("raw", result), indent=2, default=str).encode("utf-8")
        minio = get_minio_client()
        raw_key = f"investigation/{job.investigation_id}/job/{job.id}/{job.connector}.json"
        put_json_bytes(minio, settings.minio_bucket_raw, raw_key, raw)

        db.add(Artifact(
            investigation_id=job.investigation_id,
            job_id=job.id,
            artifact_type="raw_json",
            bucket=settings.minio_bucket_raw,
            object_key=raw_key,
            content_type="application/json",
        ))
        db.flush()

        entity_by_name = {}
        for item in result.get("entities", []):
            entity = Entity(
                investigation_id=job.investigation_id,
                entity_type=item["entity_type"],
                name=item["name"],
                confidence=item.get("confidence", 0.5),
                source_job_id=job.id,
            )
            db.add(entity)
            db.flush()
            entity_by_name[entity.name] = entity

        for item in result.get("observables", []):
            obs = Observable(
                investigation_id=job.investigation_id,
                observable_type=item["observable_type"],
                value=item["value"],
                normalized_value=normalize_value(item["observable_type"], item["value"]),
                confidence=item.get("confidence", 0.5),
                source_job_id=job.id,
            )
            db.add(obs)

        for item in result.get("relationships", []):
            src = entity_by_name.get(item["source_name"])
            dst = entity_by_name.get(item["target_name"])
            if src and dst:
                db.add(Relationship(
                    investigation_id=job.investigation_id,
                    source_entity_id=src.id,
                    target_entity_id=dst.id,
                    relationship_type=item["relationship_type"],
                    confidence=item.get("confidence", 0.5),
                    source_job_id=job.id,
                ))

        claim_rows = []
        for item in result.get("claims", []):
            claim = Claim(
                investigation_id=job.investigation_id,
                job_id=job.id,
                claim_type=item["claim_type"],
                subject=item["subject"],
                value=item["value"],
                confidence=item.get("confidence", 0.5),
            )
            db.add(claim)
            db.flush()
            claim_rows.append(claim)

        for idx, left in enumerate(claim_rows):
            for right in claim_rows[idx + 1:]:
                if left.claim_type == right.claim_type and left.subject == right.subject and left.value != right.value:
                    db.add(Contradiction(
                        investigation_id=job.investigation_id,
                        left_claim_id=left.id,
                        right_claim_id=right.id,
                        reason="Differing values within same claim type and subject",
                        score=0.7,
                    ))

        for item in result.get("timeline_events", []):
            db.add(TimelineEvent(
                investigation_id=job.investigation_id,
                job_id=job.id,
                title=item["title"],
                description=item.get("description"),
                event_type=item["event_type"],
            ))

        db.commit()

        nodes = [
            {"id": str(e.id), "label": e.name, "type": e.entity_type, "confidence": e.confidence}
            for e in db.scalars(select(Entity).where(Entity.investigation_id == job.investigation_id))
        ]
        edges = [
            {"id": str(r.id), "source": str(r.source_entity_id), "target": str(r.target_entity_id), "label": r.relationship_type, "confidence": r.confidence}
            for r in db.scalars(select(Relationship).where(Relationship.investigation_id == job.investigation_id))
        ]
        sync_graph(nodes, edges)

        graph_payload = json.dumps({"nodes": nodes, "edges": edges}, indent=2).encode("utf-8")
        graph_key = f"investigation/{job.investigation_id}/derived/graph.json"
        put_json_bytes(minio, settings.minio_bucket_artifacts, graph_key, graph_payload)
        db.add(Artifact(
            investigation_id=job.investigation_id,
            job_id=job.id,
            artifact_type="graph_json",
            bucket=settings.minio_bucket_artifacts,
            object_key=graph_key,
            content_type="application/json",
        ))

        timeline_rows = list(db.scalars(select(TimelineEvent).where(TimelineEvent.investigation_id == job.investigation_id).order_by(TimelineEvent.event_time.asc())))
        timeline_payload = json.dumps(
            [
                {"id": str(t.id), "event_time": t.event_time.isoformat(), "title": t.title, "description": t.description, "event_type": t.event_type}
                for t in timeline_rows
            ],
            indent=2,
        ).encode("utf-8")
        timeline_key = f"investigation/{job.investigation_id}/derived/timeline.json"
        put_json_bytes(minio, settings.minio_bucket_artifacts, timeline_key, timeline_payload)
        db.add(Artifact(
            investigation_id=job.investigation_id,
            job_id=job.id,
            artifact_type="timeline_json",
            bucket=settings.minio_bucket_artifacts,
            object_key=timeline_key,
            content_type="application/json",
        ))

        report_text = "\n".join([
            f"# Investigation Report",
            f"Investigation: {job.investigation_id}",
            f"Job: {job.id}",
            f"Connector: {job.connector}",
            "",
            f"Entities: {len(nodes)}",
            f"Relationships: {len(edges)}",
            f"Timeline events: {len(timeline_rows)}",
        ]).encode("utf-8")
        report_key = f"investigation/{job.investigation_id}/derived/report.md"
        put_json_bytes(minio, settings.minio_bucket_artifacts, report_key, report_text, content_type="text/markdown")
        db.add(Artifact(
            investigation_id=job.investigation_id,
            job_id=job.id,
            artifact_type="report_markdown",
            bucket=settings.minio_bucket_artifacts,
            object_key=report_key,
            content_type="text/markdown",
        ))

        job.status = "completed"
        job.finished_at = datetime.now(timezone.utc)
        db.commit()
        return {"status": "completed", "job_id": job_id}
    except Exception as exc:
        db.rollback()
        job = db.get(Job, UUID(job_id))
        if job:
            job.status = "failed"
            job.error_message = str(exc)
            job.finished_at = datetime.now(timezone.utc)
            db.commit()
        raise
    finally:
        db.close()
