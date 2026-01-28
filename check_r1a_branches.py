#!/usr/bin/env python3
"""Search for samples in R1a-Z2124 branch and subbranches"""

import json
import csv


def search_aadna_by_haplogroup(csv_file, haplogroup_pattern):
    """Search AADNA CSV for samples with this haplogroup pattern"""
    results = []
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                hapl = row.get("Haplogroup", "")
                if hapl and haplogroup_pattern in hapl:
                    results.append(row)
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file}")
    return results


def search_aadna_by_r1a(csv_file):
    """Search for all R1a samples to see broader patterns"""
    results = []
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                hapl = row.get("Haplogroup", "")
                if hapl and ("R1a" in hapl or hapl.startswith("R-")):
                    results.append(row)
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file}")
    return results


def get_node_path(tree, target_id, current_path=None):
    """Get full path from root to target node"""
    if current_path is None:
        current_path = []

    if tree.get("id") == target_id:
        return current_path + [tree.get("id")]

    snps = tree.get("snps", "")
    if snps and target_id in snps:
        return current_path + [tree.get("id")]

    if "children" in tree:
        for child in tree["children"]:
            result = get_node_path(child, target_id, current_path + [tree.get("id")])
            if result:
                return result
    return None


def main():
    # Load tree
    with open("current_tree.json", "r", encoding="utf-8") as f:
        tree = json.load(f)

    # Search for samples in various branches
    print("=" * 60)
    print("Searching AADNA database for R1a-related samples")
    print("=" * 60)

    # Search for R1a and R- samples
    r1a_samples = search_aadna_by_r1a("aadna.ru.csv")

    if r1a_samples:
        print(f"\n✓ Found {len(r1a_samples)} R1a-related sample(s):\n")

        # Group by subethnos
        by_subethnos = {}
        for row in r1a_samples:
            subethnos = row.get("Субэтнос", "N/A")
            if subethnos not in by_subethnos:
                by_subethnos[subethnos] = []
            by_subethnos[subethnos].append(row)

        for subethnos, samples in sorted(by_subethnos.items()):
            print(f"\n{subethnos}:")
            for row in samples:
                print(
                    f"  - {row.get('Фамилия', 'N/A')} ({row.get('Haplogroup', 'N/A')})"
                )
                print(f"    Location: {row.get('Lacation', 'N/A')}")
                print(f"    Kit: {row.get('Kit Number', 'N/A')}")
    else:
        print("\n✗ No R1a samples found in AADNA database")

    # Check specific Z2124/Z2123 branches
    print("\n" + "=" * 60)
    print("Checking for Z2124/Z2123 branch samples")
    print("=" * 60)

    z2124_samples = search_aadna_by_haplogroup("aadna.ru.csv", "Z2124")
    z2123_samples = search_aadna_by_haplogroup("aadna.ru.csv", "Z2123")

    if z2124_samples:
        print(f"\n✓ Z2124 samples: {len(z2124_samples)}")
    if z2123_samples:
        print(f"✓ Z2123 samples: {len(z2123_samples)}")

    if not z2124_samples and not z2123_samples:
        print("✗ No Z2124/Z2123 samples found")


if __name__ == "__main__":
    main()
