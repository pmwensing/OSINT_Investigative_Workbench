from app.models.entity import Claim
from app.models.contradiction import Contradiction
from app.models.credibility import CredibilityScore


def build_findings(db, investigation_id):
    claims = db.query(Claim).all()
    contradictions = db.query(Contradiction).all()
    scores = db.query(CredibilityScore).all()

    findings = []

    for s in scores:
        entity_claims = [c for c in claims if c.entity_id == s.entity_id]
        entity_contradictions = [c for c in contradictions if c.claim_a_id in [ec.id for ec in entity_claims] or c.claim_b_id in [ec.id for ec in entity_claims]]

        findings.append({
            "entity_id": str(s.entity_id),
            "credibility_score": s.score,
            "claim_count": len(entity_claims),
            "contradictions": len(entity_contradictions),
            "summary": s.summary,
        })

    findings.sort(key=lambda x: x["credibility_score"])
    return findings


def decision_summary(db, investigation_id):
    findings = build_findings(db, investigation_id)

    high_risk = [f for f in findings if f["credibility_score"] < 50]
    stable = [f for f in findings if f["credibility_score"] >= 50]

    return {
        "high_risk_entities": high_risk,
        "stable_entities": stable,
        "total_entities": len(findings)
    }
