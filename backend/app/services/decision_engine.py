from collections import defaultdict
from app.models.entity import Claim
from app.models.contradiction import Contradiction
from app.models.credibility import CredibilityScore


def build_findings(db, investigation_id):
    claims = db.query(Claim).all()
    contradictions = db.query(Contradiction).filter(Contradiction.investigation_id == investigation_id).all()
    scores = db.query(CredibilityScore).filter(CredibilityScore.investigation_id == investigation_id).all()

    findings = []

    for s in scores:
        entity_claims = [c for c in claims if c.entity_id == s.entity_id]
        claim_ids = {ec.id for ec in entity_claims}
        entity_contradictions = [
            c for c in contradictions
            if c.claim_a_id in claim_ids or c.claim_b_id in claim_ids
        ]

        findings.append({
            "entity_id": str(s.entity_id),
            "credibility_score": s.score,
            "claim_count": len(entity_claims),
            "contradictions": len(entity_contradictions),
            "summary": s.summary,
        })

    findings.sort(key=lambda x: x["credibility_score"])
    return findings


def build_issue_analysis(db, investigation_id):
    claims = db.query(Claim).all()
    contradictions = db.query(Contradiction).filter(Contradiction.investigation_id == investigation_id).all()
    claim_type_groups = defaultdict(list)

    for claim in claims:
        claim_type_groups[claim.claim_type].append(claim)

    issues = []
    for claim_type, grouped_claims in claim_type_groups.items():
        issue_contras = []
        grouped_ids = {c.id for c in grouped_claims}
        for contra in contradictions:
            if contra.claim_a_id in grouped_ids or contra.claim_b_id in grouped_ids:
                issue_contras.append(contra)

        evidence = [
            {
                "claim_id": str(c.id),
                "entity_id": str(c.entity_id),
                "value": c.value,
                "source": c.source,
                "confidence": c.confidence,
            }
            for c in grouped_claims[:20]
        ]

        if issue_contras:
            conclusion = "disputed"
            analysis = f"This issue contains {len(issue_contras)} contradictions and requires careful weight assessment."
        else:
            conclusion = "stable"
            analysis = "This issue is internally consistent on the available machine-generated record."

        issues.append({
            "issue": claim_type,
            "evidence": evidence,
            "analysis": analysis,
            "conclusion": conclusion,
            "contradiction_count": len(issue_contras),
        })

    issues.sort(key=lambda x: (-x["contradiction_count"], x["issue"]))
    return issues


def decision_summary(db, investigation_id):
    findings = build_findings(db, investigation_id)
    issues = build_issue_analysis(db, investigation_id)

    high_risk = [f for f in findings if f["credibility_score"] < 50]
    stable = [f for f in findings if f["credibility_score"] >= 50]

    return {
        "high_risk_entities": high_risk,
        "stable_entities": stable,
        "issues": issues,
        "total_entities": len(findings)
    }
