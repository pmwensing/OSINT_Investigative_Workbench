import csv
from collections import defaultdict

def build_hash_index(manifest_csv):
    groups = defaultdict(list)

    with open(manifest_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            groups[row["sha256"]].append(row)

    return groups
