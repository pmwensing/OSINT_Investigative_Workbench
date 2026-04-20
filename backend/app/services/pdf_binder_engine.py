from app.services.hearing_package_engine import build_hearing_package


def build_binder_markdown(db, investigation_id):
    pkg = build_hearing_package(db, investigation_id)

    toc = "\n".join([f"- {item}" for item in pkg.get("table_of_contents", [])])
    findings = "\n".join([
        f"- Entity {f['entity_id']}: credibility {f['credibility_score']}, claims {f['claim_count']}, contradictions {f['contradictions']}"
        for f in pkg.get("findings", [])
    ])
    contradictions = "\n".join([
        f"- {c['summary']} (severity: {c['severity']})"
        for c in pkg.get("contradiction_matrix", [])
    ])
    timeline = "\n".join([
        f"- {t['event_at']}: {t['title']} — {t['description'] or ''}"
        for t in pkg.get("timeline", [])
    ])
    orders = "\n".join([f"- {o}" for o in pkg.get("recommended_orders", [])])

    md = f'''# Hearing Package\n\n## Cover Sheet\n\n**Title:** {pkg['cover_sheet']['title']}\n\n**Status:** {pkg['cover_sheet']['status']}\n\n**Freeze Hash:** {pkg['cover_sheet']['freeze_manifest_hash']}\n\n## Table of Contents\n\n{toc}\n\n## Adjudicator Summary\n\n{pkg.get('adjudicator_summary', '')}\n\n## Findings\n\n{findings}\n\n## Contradiction Matrix\n\n{contradictions}\n\n## Timeline\n\n{timeline}\n\n## Recommended Orders\n\n{orders}\n'''
    return {
        "markdown": md,
        "suggested_filename": f"hearing_package_{investigation_id}.md"
    }
