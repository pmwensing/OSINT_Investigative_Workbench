import hashlib
import json
from app.models.freeze import FreezeSnapshot, AuditEvent
from app.models.entity import Claim, Artifact, Relationship
from app.models.contradiction import Contradiction
from app.models.timeline import TimelineEvent
from app.models.provenance import ClaimCitation, ProvenanceRecord


def compute_manifest_hash(db, investigation_id):
    claims = db.query(Claim).all()
    artifacts = db.query(Artifact).filter(Artifact.investigation_id == investigation_id).all()
    relationships = db.query(Relationship).all()
    contradictions = db.query(Contradiction).filter(Contradiction.investigation_id == investigation_id).all()
    timeline = db.query(TimelineEvent).filter(TimelineEvent.investigation_id == investigation_id).all()
    citations = db.query(ClaimCitation).all()
    provenance = db.query(ProvenanceRecord).filter(ProvenanceRecord.investigation_id == investigation_id).all()

    payload = {
        "investigation_id": str(investigation_id),
        "claims": [
            {
                "id": str(c.id),
                "entity_id": str(c.entity_id),
                "claim_type": c.claim_type,
                "value": c.value,
                "source": c.source,
                "confidence": c.confidence,
            }
            for c in claims
        ],
        "artifacts": [
            {
                "id": str(a.id),
                "artifact_type": a.artifact_type,
                "location": a.location,
                "metadata": a.metadata,
            }
            for a in artifacts
        ],
        "relationships": [
            {
                "id": str(r.id),
                "source_entity_id": str(r.source_entity_id),
                "target_entity_id": str(r.target_entity_id),
                "relationship_type": r.relationship_type,
            }
            for r in relationships
        ],
        "contradictions": [
            {
                "id": str(c.id),
                "claim_a_id": str(c.claim_a_id),
                "claim_b_id": str(c.claim_b_id),
                "rule": c.rule,
                "summary": c.summary,
                "severity": c.severity,
            }
            for c in contradictions
        ],
        "timeline": [
            {
                "id": str(t.id),
                "title": t.title,
                "description": t.description,
                "event_type": t.event_type,
                "event_at": t.event_at.isoformat() if t.event_at else None,
            }
            for t in timeline
        ],
        "citations": [
            {
                "id": str(c.id),
                "claim_id": str(c.claim_id),
                "locator": c.locator,
                "excerpt": c.excerpt,
                "justification": c.justification,
            }
            for c in citations
        ],
        "provenance": [
            {
                "id": str(p.id),
                "record_type": p.record_type,
                "locator": p.locator,
                "content_hash": p.content_hash,
            }
            for p in provenance
        ],
    }

    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def freeze_investigation(db, investigation_id):
    manifest_hash = compute_manifest_hash(db, investigation_id)

    snapshot = FreezeSnapshot(
        investigation_id=investigation_id,
        manifest_hash=manifest_hash,
        audit_log=f"Freeze created with hash {manifest_hash}"
    )
    db.add(snapshot)

    audit = AuditEvent(
        investigation_id=investigation_id,
        event_type="freeze",
        details=f"Investigation frozen with hash {manifest_hash}"
    )
    db.add(audit)

    db.commit()
    db.refresh(snapshot)
    return snapshot


def log_event(db, investigation_id, event_type, details=None, object_type=None, object_id=None):
    audit = AuditEvent(
        investigation_id=investigation_id,
        event_type=event_type,
        object_type=object_type,
        object_id=object_id,
        details=details
    )
    db.add(audit)
    db.commit()
    return audit
