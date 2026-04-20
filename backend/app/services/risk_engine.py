from app.models.credibility import CredibilityScore
from app.models.contradiction import Contradiction
from app.models.risk import EntityRiskScore, CaseRiskScore


def compute_risk(db, investigation_id):
    scores = db.query(CredibilityScore).filter(CredibilityScore.investigation_id == investigation_id).all()
    contradictions = db.query(Contradiction).filter(Contradiction.investigation_id == investigation_id).all()

    results = []

    for s in scores:
        risk = max(0, 100 - s.score)
        summary = f"Derived from credibility score {s.score}"

        rs = EntityRiskScore(
            investigation_id=investigation_id,
            entity_id=s.entity_id,
            score=risk,
            summary=summary
        )
        db.add(rs)
        results.append(rs)

    case_score = sum(r.score for r in results) // max(1, len(results))

    rating = "high" if case_score > 70 else "medium" if case_score > 40 else "low"

    case = CaseRiskScore(
        investigation_id=investigation_id,
        score=case_score,
        rating=rating,
        summary=f"Aggregated from {len(results)} entities"
    )

    db.add(case)
    db.commit()

    return {"entities": len(results), "case_score": case_score, "rating": rating}
