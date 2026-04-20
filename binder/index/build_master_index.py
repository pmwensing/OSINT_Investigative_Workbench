import csv, uuid

def build_master_index(manifest_csv, out_dir):
    out_file = f"{out_dir}/MASTER_EXHIBIT_INDEX.csv"

    with open(manifest_csv) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with open(out_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "exhibit_id","title","source_path","category","sha256"
        ])
        writer.writeheader()

        for r in rows:
            writer.writerow({
                "exhibit_id": str(uuid.uuid4()),
                "title": r["basename"],
                "source_path": r["source_path"],
                "category": "Z_UNCLASSIFIED",
                "sha256": r["sha256"]
            })

    return out_file
