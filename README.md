# Binder v2.0 Code Bundle

Ready-to-run local Binder v2.0 starter implementation.

## Included
- evidence scan + source manifest
- classification rules + classifier
- exact duplicate detection
- near-duplicate grouping heuristics
- master exhibit index builder
- curated disclosure/adjudicator index builder

## Run order

```bash
python -m binder.ingestion.scan_sources --root /path/to/evidence --out /path/to/output
python -m binder.index.build_master_index --manifest /path/to/output/SOURCE_MANIFEST.csv --out /path/to/output
python -m binder.index.build_curated_indexes --master /path/to/output/MASTER_EXHIBIT_INDEX.csv --out /path/to/output
```
