from app.services.decision_engine import decision_summary


def build_report(db, investigation_id):
    summary = decision_summary(db, investigation_id)

    report = {
        "overview": f"Investigation {investigation_id} analysis",
        "high_risk_entities": summary["high_risk_entities"],
        "stable_entities": summary["stable_entities"],
        "conclusion": "Based on current evidence and contradictions, high-risk entities require further scrutiny."
    }

    return report
