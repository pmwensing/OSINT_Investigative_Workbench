#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 INVESTIGATION_ID [API_BASE_URL]"
  exit 1
fi

INVESTIGATION_ID="$1"
API_BASE_URL="${2:-http://localhost:8000/api}"
OUTDIR="hearing_package_${INVESTIGATION_ID}"
mkdir -p "$OUTDIR"

curl -s "$API_BASE_URL/hearing/?investigation_id=$INVESTIGATION_ID" > "$OUTDIR/hearing_package.json"
curl -s "$API_BASE_URL/pdf/binder?investigation_id=$INVESTIGATION_ID" > "$OUTDIR/hearing_package_md.json"
curl -s "$API_BASE_URL/pdf/binder_html?investigation_id=$INVESTIGATION_ID" > "$OUTDIR/hearing_package_html.json"
curl -s "$API_BASE_URL/export/?investigation_id=$INVESTIGATION_ID" > "$OUTDIR/export_bundle.json"
curl -s "$API_BASE_URL/package/zip?investigation_id=$INVESTIGATION_ID" > "$OUTDIR/package_zip.json"

python3 - <<'PY'
import json, os, pathlib
outdir = pathlib.Path(os.environ.get('OUTDIR', '.'))
md_json = json.loads((outdir / 'hearing_package_md.json').read_text())
html_json = json.loads((outdir / 'hearing_package_html.json').read_text())
(outdir / md_json['suggested_filename']).write_text(md_json['markdown'])
(outdir / html_json['suggested_filename']).write_text(html_json['html'])
print('Wrote binder markdown/html files')
PY

if command -v wkhtmltopdf >/dev/null 2>&1; then
  HTML_FILE=$(python3 - <<'PY'
import json, pathlib
p = pathlib.Path('$OUTDIR') / 'hearing_package_html.json'
obj = json.loads(p.read_text())
print(pathlib.Path('$OUTDIR') / obj['suggested_filename'])
PY
)
  wkhtmltopdf --enable-internal-links "$HTML_FILE" "$OUTDIR/hearing_package.pdf" || true
elif command -v chromium >/dev/null 2>&1; then
  chromium --headless --print-to-pdf="$OUTDIR/hearing_package.pdf" "$OUTDIR/$(python3 - <<'PY'
import json, pathlib
p = pathlib.Path('$OUTDIR') / 'hearing_package_html.json'
obj = json.loads(p.read_text())
print(obj['suggested_filename'])
PY
)" || true
fi

echo "Done. Output directory: $OUTDIR"
