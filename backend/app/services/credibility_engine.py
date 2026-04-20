from collections import defaultdict
from app.models.entity import Claim, Relationship
from app.models.contradiction import Contradiction
from app.models.credibility import CredibilityScore
from app.models.timeline import TimelineEvent


CONFIDENCE_BONUS = {
    "high": 8,
    "medium": 3,
    "low": 0,
    None: 0,
}

SOURCE_BONUS = {
    "official": 10,
    "documentary": 6,
    "witness": 3,
    "hearsay": -4,
    None: 0,
}

SEVERITY_PENALTY = {
    "high": 18,
    "medium": 10,
    "low": 5,
    None: 10,
}


def compute_credibility(db, investigation_id):
    claims = db.query(Claim).all()
    contradictions = db.query(Contradiction).filter(Contradiction.investigation_id == investigation_id).all()
    timeline_events = db.query(TimelineEvent).filter(TimelineEvent.investigation_id == investigation_id).all()
    relationships = db.query(Relationship).all()

    entity_claims = defaultdict(list)
    for c in claims:
        entity_claims[c.entity_id].append(c)

    contradiction_map = defaultdict(list)
    for c in contradictions:
        contradiction_map[c.claim_a_id].append(c)
        contradiction_map[c.claim_b_id].append(c)

    degree_map = defaultdict(int)
    for r in relationships:
        degree_map[r.source_entity_id] += 1
        degree_map[r.target_entity_id] += 1

    timeline_sources = {te.source_id for te in timeline_events}

    results = []

    for entity_id, claim_list in entity_claims.items():
        base_score = 50
        contradiction_count = 0
        contradiction_penalty = 0
        confidence_bonus = 0
        source_bonus = 0
        timeline_bonus = 0
        graph_bonus = min(15, degree_map.get(entity_id, 0) * 2)

        for claim in claim_list:
            confidence_bonus += CONFIDENCE_BONUS.get(claim.confidence, 0)
            source_bonus += SOURCE_BONUS.get(claim.source, 0)

            if claim.id in timeline_sources:
                timeline_bonus += 2

            related_contras = contradiction_map.get(claim.id, [])
            contradiction_count += len(related_contras)
            contradiction_penalty += sum(SEVERITY_PENALTY.get(c.severity, 10) for c in related_contras)

        raw_score = base_score + confidence_bonus + source_bonus + timeline_bonus + graph_bonus - contradiction_penalty
        score = max(0, min(100, raw_score))

        summary = (
            f"claims={len(claim_list)}, contradictions={contradiction_count}, "
            f"confidence_bonus={confidence_bonus}, source_bonus={source_bonus}, "
            f"timeline_bonus={timeline_bonus}, graph_bonus={graph_bonus}, penalty={contradiction_penalty}"
        )

        cs = CredibilityScore(
            investigation_id=investigation_id,
            entity_id=entity_id,
            score=score,
            contradiction_count=contradiction_count,
            supporting_claim_count=len(claim_list),
            summary=summary,
        )
        db.add(cs)
        results.append(cs)

    db.commit()
    return results
