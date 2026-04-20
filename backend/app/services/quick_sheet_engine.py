from app.services.decision_engine import build_issue_analysis, decision_summary
from app.models.provenance import ClaimCitation


def build_quick_sheet(db, investigation_id):
    summary = decision_summary(db, investigation_id)
    issues = build_issue_analysis(db, investigation_id)
    citations = db.query(ClaimCitation).all()

    top_issues = issues[:5]
    top_exhibits = [
        {
            "exhibit_number": f"A-{i+1}",
            "claim_id": str(c.claim_id),
            "excerpt": c.excerpt,
            "locator": c.locator,
        }
        for i, c in enumerate(citations[:5])
    ]

    return {
        "title": f"Adjudicator Quick Sheet — {investigation_id}",
        "key_issues": top_issues,
        "key_exhibits": top_exhibits,
        "requested_orders": [
            "Prefer consistent, corroborated evidence over disputed assertions.",
            "Treat unresolved contradictions as reducing evidentiary weight.",
        ],
        "high_risk_entities": summary.get("high_risk_entities", []),
    }
