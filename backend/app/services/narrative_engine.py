from app.models.contradiction import Contradiction
from app.models.timeline import TimelineEvent
from app.models.credibility import CredibilityScore
from app.services.decision_engine import build_findings


def build_narrative(db, investigation_id):
    findings = build_findings(db, investigation_id)
    contradictions = db.query(Contradiction).filter(Contradiction.investigation_id == investigation_id).all()
    timeline = db.query(TimelineEvent).filter(TimelineEvent.investigation_id == investigation_id).order_by(TimelineEvent.event_at).all()
    credibility = db.query(CredibilityScore).filter(CredibilityScore.investigation_id == investigation_id).all()

    narrative_parts = []

    # WHAT HAPPENED (causal narrative)
    for event in timeline[:10]:
        when = event.event_at.isoformat() if event.event_at else "at an unspecified time"
        narrative_parts.append(f"On {when}, {event.description or event.title}.")

    # CONTRADICTIONS
    if contradictions:
        narrative_parts.append("However, the record contains material inconsistencies.")
        for c in contradictions[:5]:
            narrative_parts.append(f"Specifically, {c.summary}, indicating a conflict under rule {c.rule}.")

    # CREDIBILITY
    for cs in credibility[:5]:
        if cs.score < 50:
            narrative_parts.append(f"Entity {cs.entity_id} demonstrates low reliability with a credibility score of {cs.score}, undermined by contradictions.")
        else:
            narrative_parts.append(f"Entity {cs.entity_id} appears relatively reliable with a credibility score of {cs.score}.")

    # FINDINGS
    for f in findings[:5]:
        narrative_parts.append(f"The evidence shows {f['claim_count']} claims associated with entity {f['entity_id']}, with {f['contradictions']} inconsistencies.")

    adjudicator_narrative = " ".join(narrative_parts)

    return {
        "narrative": adjudicator_narrative,
        "length": len(adjudicator_narrative)
    }
