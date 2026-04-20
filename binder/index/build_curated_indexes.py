from __future__ import annotations
import argparse, csv
from pathlib import Path

HEADERS = [
    "exhibit_id","title","source_id","source_path","category","subcategory",
    "packet_flags","sha256","duplicate_group_id","canonical_preferred","notes"
]

def read_master(master_csv: str | Path) -> list[dict]:
    with Path(master_csv).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def filter_packet(rows: list[dict], packet_name: str) -> list[dict]:
    filtered = []
    for row in rows:
        flags = {f.strip() for f in row["packet_flags"].split(",") if f.strip()}
        if packet_name in flags:
            if row["canonical_preferred"] == "no":
                continue
            filtered.append(row)
    return filtered

def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    rows = read_master(args.master)
    disclosure = filter_packet(rows, "disclosure")
    adjudicator = filter_packet(rows, "adjudicator")

    write_csv(out / "DISCLOSURE_EXHIBIT_INDEX.csv", disclosure)
    write_csv(out / "ADJUDICATOR_EXHIBIT_INDEX.csv", adjudicator)

    print(f"Wrote {out / 'DISCLOSURE_EXHIBIT_INDEX.csv'}")
    print(f"Wrote {out / 'ADJUDICATOR_EXHIBIT_INDEX.csv'}")
    print(f"Disclosure rows: {len(disclosure)}")
    print(f"Adjudicator rows: {len(adjudicator)}")

if __name__ == "__main__":
    main()
