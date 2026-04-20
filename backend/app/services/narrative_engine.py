from app.models.contradiction import Contradiction
from app.models.timeline import TimelineEvent
from app.models.credibility import CredibilityScore
from app.services.decision_engine import build_findings


def build_narrative(db, investigation_id):
    findings = build_findings(db, investigation_id)
    contradictions = db.query(Contradiction).filter(Contradiction.investigation_id == investigation_id).all()
    timeline = db.query(TimelineEvent).filter(TimelineEvent.investigation_id == investigation_id).order_by(TimelineEvent.event_at).all()
    credibility = db.query(CredibilityScore).filter(CredibilityScore.investigation_id == investigation_id).all()

    timeline_lines = []
    for event in timeline:
        when = event.event_at.isoformat() if event.event_at else "undated"
        timeline_lines.append(f"{when}: {event.title} — {event.description or ''}".strip())

    contradiction_lines = []
    for c in contradictions:
        contradiction_lines.append(f"Conflict detected under rule '{c.rule}': {c.summary} (severity: {c.severity}).")

    credibility_lines = []
    for cs in credibility:
        band = "high" if cs.score >= 75 else "moderate" if cs.score >= 50 else "low"
        credibility_lines.append(
            f"Entity {cs.entity_id} is assessed as {band} credibility with score {cs.score}; {cs.summary}."
        )

    findings_lines = []
    for f in findings:
        findings_lines.append(
            f"Entity {f['entity_id']} has {f['claim_count']} claims and {f['contradictions']} contradictions with credibility score {f['credibility_score']}."
        )

    what_happened = " ".join(timeline_lines[:10]) if timeline_lines else "No timeline narrative available."
    contradiction_summary = " ".join(contradiction_lines[:10]) if contradiction_lines else "No contradictions were detected."
    credibility_summary = " ".join(credibility_lines[:10]) if credibility_lines else "No credibility analysis is available."
    findings_summary = " ".join(findings_lines[:10]) if findings_lines else "No findings are available."

    adjudicator_summary = (
        f"What happened: {what_happened} "
        f"Key conflicts: {contradiction_summary} "
        f"Credibility: {credibility_summary} "
        f"Findings: {findings_summary}"
    )

    return {
        "what_happened": what_happened,
        "contradiction_summary": contradiction_summary,
        "credibility_summary": credibility_summary,
        "findings_summary": findings_summary,
        "adjudicator_summary": adjudicator_summary,
    }
