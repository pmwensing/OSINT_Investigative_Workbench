from app.models.contradiction import Contradiction
from app.models.timeline import TimelineEvent
from app.models.credibility import CredibilityScore
from app.services.decision_engine import build_findings, build_issue_analysis


def build_narrative(db, investigation_id):
    findings = build_findings(db, investigation_id)
    issues = build_issue_analysis(db, investigation_id)
    contradictions = db.query(Contradiction).filter(Contradiction.investigation_id == investigation_id).all()
    timeline = db.query(TimelineEvent).filter(TimelineEvent.investigation_id == investigation_id).order_by(TimelineEvent.event_at).all()
    credibility = db.query(CredibilityScore).filter(CredibilityScore.investigation_id == investigation_id).all()

    parts = []

    if issues:
        for issue in issues[:5]:
            parts.append(f"Issue: {issue['issue']}.")
            parts.append("Rule: The decision-maker should prefer consistent, corroborated, and better-supported evidence over disputed assertions.")
            parts.append(f"Analysis: {issue['analysis']}")
            parts.append(f"Conclusion: This issue is {issue['conclusion']}.")

    for event in timeline[:8]:
        when = event.event_at.isoformat() if event.event_at else "at an unspecified time"
        parts.append(f"Chronology: On {when}, {event.description or event.title}.")

    if contradictions:
        parts.append("Conflicts: The record contains material inconsistencies that reduce the weight of disputed assertions.")
        for c in contradictions[:5]:
            parts.append(f"Conflict detail: {c.summary}, under rule {c.rule}.")

    for cs in credibility[:5]:
        band = "low" if cs.score < 50 else "moderate" if cs.score < 75 else "high"
        parts.append(f"Credibility: Entity {cs.entity_id} has {band} credibility with score {cs.score}.")

    for f in findings[:5]:
        parts.append(f"Finding: Entity {f['entity_id']} has {f['claim_count']} claims and {f['contradictions']} contradictions.")

    narrative = " ".join(parts)
    return {
        "narrative": narrative,
        "length": len(narrative)
    }
