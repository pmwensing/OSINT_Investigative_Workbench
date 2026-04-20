from collections import defaultdict
from app.models.entity import Claim
from app.models.contradiction import Contradiction
from app.models.credibility import CredibilityScore


def compute_credibility(db, investigation_id):
    claims = db.query(Claim).all()
    contradictions = db.query(Contradiction).all()

    entity_claims = defaultdict(list)
    for c in claims:
        entity_claims[c.entity_id].append(c)

    contradiction_map = defaultdict(int)
    for c in contradictions:
        contradiction_map[c.claim_a_id] += 1
        contradiction_map[c.claim_b_id] += 1

    results = []

    for entity_id, claim_list in entity_claims.items():
        base_score = 100
        contradiction_count = 0

        for c in claim_list:
            contradiction_count += contradiction_map.get(c.id, 0)

        penalty = contradiction_count * 10
        score = max(0, base_score - penalty)

        summary = f"{len(claim_list)} claims, {contradiction_count} contradictions"

        cs = CredibilityScore(
            investigation_id=investigation_id,
            entity_id=entity_id,
            score=score,
            contradiction_count=contradiction_count,
            supporting_claim_count=len(claim_list),
            summary=summary
        )
        db.add(cs)
        results.append(cs)

    db.commit()
    return results
