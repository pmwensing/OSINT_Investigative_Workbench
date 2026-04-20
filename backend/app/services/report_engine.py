from app.models.contradiction import Contradiction
from app.models.timeline import TimelineEvent
from app.models.credibility import CredibilityScore
from app.models.provenance import ClaimCitation
from app.services.decision_engine import decision_summary, build_findings


def build_report(db, investigation_id):
    summary = decision_summary(db, investigation_id)
    findings = build_findings(db, investigation_id)
    contradictions = db.query(Contradiction).filter(Contradiction.investigation_id == investigation_id).all()
    timeline = db.query(TimelineEvent).filter(TimelineEvent.investigation_id == investigation_id).order_by(TimelineEvent.event_at).all()
    credibility = db.query(CredibilityScore).filter(CredibilityScore.investigation_id == investigation_id).all()
    citations = db.query(ClaimCitation).all()

    contradiction_matrix = [
        {
            "claim_a_id": str(c.claim_a_id),
            "claim_b_id": str(c.claim_b_id),
            "rule": c.rule,
            "summary": c.summary,
            "severity": c.severity,
            "status": c.status,
        }
        for c in contradictions
    ]

    timeline_narrative = [
        {
            "event_at": te.event_at.isoformat() if te.event_at else None,
            "title": te.title,
            "description": te.description,
            "event_type": te.event_type,
        }
        for te in timeline
    ]

    credibility_table = [
        {
            "entity_id": str(cs.entity_id),
            "score": cs.score,
            "contradiction_count": cs.contradiction_count,
            "supporting_claim_count": cs.supporting_claim_count,
            "summary": cs.summary,
        }
        for cs in credibility
    ]

    evidence_citations = [
        {
            "claim_id": str(c.claim_id),
            "artifact_id": str(c.artifact_id) if c.artifact_id else None,
            "provenance_id": str(c.provenance_id) if c.provenance_id else None,
            "locator": c.locator,
            "excerpt": c.excerpt,
            "justification": c.justification,
        }
        for c in citations
    ]

    recommended_orders = []
    if summary["high_risk_entities"]:
        recommended_orders.append("Further scrutiny recommended for low-credibility entities.")
    if contradiction_matrix:
        recommended_orders.append("Resolve outstanding contradictions before relying on disputed claims.")
    if not recommended_orders:
        recommended_orders.append("Current record appears stable on available machine-generated analysis.")

    report = {
        "overview": f"Tribunal-grade investigation output for {investigation_id}",
        "findings": findings,
        "contradiction_matrix": contradiction_matrix,
        "timeline_narrative": timeline_narrative,
        "credibility_table": credibility_table,
        "evidence_citations": evidence_citations,
        "recommended_orders": recommended_orders,
        "summary": summary,
        "conclusion": "This report organizes findings, contradictions, chronology, credibility, and evidence linkage for decision support.",
    }

    return report
