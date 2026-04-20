from app.services.hearing_package_engine import build_hearing_package


def _html_list(items):
    if not items:
        return "<p>None.</p>"
    return "<ul>" + "".join([f"<li>{item}</li>" for item in items]) + "</ul>"


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


def build_binder_html(db, investigation_id):
    pkg = build_hearing_package(db, investigation_id)

    toc_items = "".join([
        f'<li><a href="#sec-{i}">{item}</a></li>'
        for i, item in enumerate(pkg.get("table_of_contents", []), start=1)
    ])

    findings_items = [
        f'Entity {f["entity_id"]}: credibility {f["credibility_score"]}, claims {f["claim_count"]}, contradictions {f["contradictions"]}'
        for f in pkg.get("findings", [])
    ]
    contradiction_items = [
        f'{c["summary"]} (severity: {c["severity"]})'
        for c in pkg.get("contradiction_matrix", [])
    ]
    timeline_items = [
        f'{t["event_at"]}: {t["title"]} — {t["description"] or ""}'
        for t in pkg.get("timeline", [])
    ]
    order_items = pkg.get("recommended_orders", [])

    exhibit_links = _html_list([
        f'Exhibit placeholder for claim/artefact linkage {idx + 1}'
        for idx, _ in enumerate(pkg.get("contradiction_matrix", [])[:10])
    ])

    html = f'''<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>Hearing Package</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 36px; line-height: 1.4; }}
h1, h2 {{ page-break-after: avoid; }}
ul {{ margin-top: 0.4rem; }}
a {{ color: black; text-decoration: none; }}
.section {{ margin-bottom: 24px; }}
</style>
</head>
<body>
<h1>Hearing Package</h1>
<div class="section" id="sec-1">
  <h2>Cover Sheet</h2>
  <p><strong>Title:</strong> {pkg['cover_sheet']['title']}</p>
  <p><strong>Status:</strong> {pkg['cover_sheet']['status']}</p>
  <p><strong>Freeze Hash:</strong> {pkg['cover_sheet']['freeze_manifest_hash']}</p>
</div>
<div class="section" id="sec-2">
  <h2>Table of Contents</h2>
  <ul>{toc_items}</ul>
</div>
<div class="section" id="sec-3">
  <h2>Adjudicator Summary</h2>
  <p>{pkg.get('adjudicator_summary', '')}</p>
</div>
<div class="section" id="sec-4">
  <h2>Findings</h2>
  {_html_list(findings_items)}
</div>
<div class="section" id="sec-5">
  <h2>Contradiction Matrix</h2>
  {_html_list(contradiction_items)}
</div>
<div class="section" id="sec-6">
  <h2>Timeline</h2>
  {_html_list(timeline_items)}
</div>
<div class="section" id="sec-7">
  <h2>Recommended Orders</h2>
  {_html_list(order_items)}
</div>
<div class="section" id="sec-8">
  <h2>Exhibit Links</h2>
  {exhibit_links}
</div>
</body>
</html>'''

    return {
        "html": html,
        "suggested_filename": f"hearing_package_{investigation_id}.html",
        "pdf_render_hint": "Render this HTML with a bookmark-capable HTML-to-PDF engine or browser print-to-PDF pipeline.",
    }
