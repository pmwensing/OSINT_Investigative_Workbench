import io
import json
import zipfile
from app.services.hearing_package_engine import build_hearing_package
from app.services.pdf_binder_engine import build_binder_html, build_binder_markdown


def build_zip_bundle(db, investigation_id):
    hearing = build_hearing_package(db, investigation_id)
    binder_md = build_binder_markdown(db, investigation_id)
    binder_html = build_binder_html(db, investigation_id)

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("hearing_package.json", json.dumps(hearing, indent=2))
        zf.writestr(binder_md["suggested_filename"], binder_md["markdown"])
        zf.writestr(binder_html["suggested_filename"], binder_html["html"])
        zf.writestr("README_EXPORT.txt", "Render the HTML binder to PDF with a bookmark-capable HTML-to-PDF tool.")

    return {
        "zip_base64_placeholder": buffer.getvalue().hex(),
        "filename": f"hearing_package_{investigation_id}.zip",
        "note": "Hex-encoded ZIP payload placeholder for transport; convert to binary in deployment runtime."
    }
