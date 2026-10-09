"""
CSV profiling script: prints basic statistics about a CSV file.
"""

import csv
import argparse
from collections import defaultdict

def detect_type(values):
    """Return 'int', 'float', or 'str' based on the given non‑empty values."""
    int_ok, float_ok = True, True
    for v in values:
        if int_ok:
            try:
                int(v)
            except ValueError:
                int_ok = False
        if float_ok:
            try:
                float(v)
            except ValueError:
                float_ok = False
    if int_ok: return 'int'
    if float_ok: return 'float'
    return 'str'

def main():
    parser = argparse.ArgumentParser(description="Profile a CSV file.")
    parser.add_argument("file", help="Path to the CSV file")
    args = parser.parse_args()

    with open(args.file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        if not headers:
            print("Empty CSV.")
            return

        stats = defaultdict(lambda: {"missing": 0, "values": set()})
        row_count = 0

        for row in reader:
            row_count += 1
            for h in headers:
                val = row.get(h, "")
                if val == "":
                    stats[h]["missing"] += 1
                else:
                    stats[h]["values"].add(val)

    print(f"Rows: {row_count}")
    print(f"Columns: {len(headers)}")
    print("\nColumn details:")
    for h in headers:
        col = stats[h]
        col_type = detect_type(col["values"])
        print(f"  {h}:")
        print(f"    Type: {col_type}")
        print(f"    Missing: {col['missing']}")
        print(f"    Unique: {len(col['values'])}")

if __name__ == "__main__":
    main()