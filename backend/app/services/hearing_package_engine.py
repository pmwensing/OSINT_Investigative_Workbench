from app.services.report_engine import build_report
from app.services.narrative_engine import build_narrative
from app.services.decision_engine import build_findings, decision_summary, build_issue_analysis
from app.models.contradiction import Contradiction
from app.models.timeline import TimelineEvent
from app.models.provenance import ClaimCitation
from app.models.freeze import FreezeSnapshot


def build_hearing_package(db, investigation_id):
    report = build_report(db, investigation_id)
    narrative = build_narrative(db, investigation_id)
    findings = build_findings(db, investigation_id)
    summary = decision_summary(db, investigation_id)
    issues = build_issue_analysis(db, investigation_id)

    contradictions = db.query(Contradiction).filter(Contradiction.investigation_id == investigation_id).all()
    timeline = db.query(TimelineEvent).filter(TimelineEvent.investigation_id == investigation_id).order_by(TimelineEvent.event_at).all()
    citations = db.query(ClaimCitation).all()
    freeze = db.query(FreezeSnapshot).filter(
        FreezeSnapshot.investigation_id == investigation_id,
        FreezeSnapshot.is_active == True
    ).order_by(FreezeSnapshot.created_at.desc()).first()

    exhibit_index = [
        {
            "exhibit_number": f"A-{i+1}",
            "claim_id": str(c.claim_id),
            "excerpt": c.excerpt,
            "locator": c.locator,
        }
        for i, c in enumerate(citations[:50])
    ]

    package = {
        "cover_sheet": {
            "title": f"Hearing Package for Investigation {investigation_id}",
            "status": "submission_ready" if freeze else "draft",
            "freeze_manifest_hash": freeze.manifest_hash if freeze else None,
        },
        "adjudicator_summary": narrative.get("narrative"),
        "issues": issues,
        "report": report,
        "findings": findings,
        "decision_summary": summary,
        "exhibit_index": exhibit_index,
        "contradiction_matrix": [
            {
                "claim_a_id": str(c.claim_a_id),
                "claim_b_id": str(c.claim_b_id),
                "summary": c.summary,
                "severity": c.severity,
            }
            for c in contradictions
        ],
        "timeline": [
            {
                "event_at": te.event_at.isoformat() if te.event_at else None,
                "title": te.title,
                "description": te.description,
            }
            for te in timeline
        ],
        "recommended_orders": report.get("recommended_orders", []),
        "table_of_contents": [
            "Cover Sheet",
            "Adjudicator Summary",
            "Issues for Determination",
            "Findings",
            "Exhibit Index",
            "Contradiction Matrix",
            "Timeline",
            "Credibility Table",
            "Evidence Citations",
            "Recommended Orders",
        ],
    }

    return package
