#!/usr/bin/env python3
"""Search for a specific haplogroup in current_tree.json"""

import json
import sys
import csv


def find_node(tree, target_id):
    """Recursively search for a node by id or snps"""
    # Check if id matches
    if tree.get("id") == target_id:
        return tree

    # Check if target is in snps list
    snps = tree.get("snps", "")
    if snps and target_id in snps:
        return tree

    # Search children
    if "children" in tree:
        for child in tree["children"]:
            result = find_node(child, target_id)
            if result:
                return result
    return None


def get_path(tree, target_id, current_path=None):
    """Get full path from root to target node"""
    if current_path is None:
        current_path = []

    # Check if this node is the target
    if tree.get("id") == target_id:
        return current_path + [tree.get("id")]

    # Check if target is in snps
    snps = tree.get("snps", "")
    if snps and target_id in snps:
        return current_path + [tree.get("id")]

    # Search children
    if "children" in tree:
        for child in tree["children"]:
            result = get_path(child, target_id, current_path + [tree.get("id")])
            if result:
                return result
    return None


def search_aadna(csv_file, haplogroup):
    """Search AADNA CSV for samples with this haplogroup"""
    results = []
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check multiple haplogroup fields
                hapl = row.get("Haplogroup", "")
                if hapl and haplogroup in hapl:
                    results.append(row)
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file}")
    return results


def main():
    target = "R-FT230328"

    print(f"Searching for: {target}")
    print("=" * 60)

    # Load tree
    try:
        with open("current_tree.json", "r", encoding="utf-8") as f:
            tree = json.load(f)
        print("✓ Tree loaded successfully")
    except Exception as e:
        print(f"✗ Error loading tree: {e}")
        return

    # Search for node
    node = find_node(tree, target)

    if node:
        print(f"✓ Node found: {target}")
        print("-" * 60)
        print(f"ID: {node.get('id')}")
        print(f"SNPs: {node.get('snps')}")
        print(f"Formed: {node.get('formed')} ybp")
        print(f"TMRCA: {node.get('tmrca')} ybp")
        if node.get("formed") != "-" and node.get("tmrca") != "-":
            gap = node.get("formed") - node.get("tmrca")
            print(f"Gap (Founder Effect): {gap} years")

        # Get full path
        path = get_path(tree, target)
        if path:
            print(f"\nFull Path:")
            print(" > ".join(path))
    else:
        print(f"✗ Node NOT found in local tree: {target}")
        print("\nNeed to search YFull.com for this haplogroup.")

    # Search AADNA database
    print("\n" + "=" * 60)
    print("Searching AADNA database...")
    results = search_aadna("aadna.ru.csv", target)

    if results:
        print(f"✓ Found {len(results)} sample(s) in AADNA database:")
        for i, row in enumerate(results, 1):
            print(f"\n  {i}. {row.get('Фамилия', 'N/A')} ({row.get('Name', 'N/A')})")
            print(f"     Subethnos: {row.get('Субэтнос', 'N/A')}")
            print(f"     Location: {row.get('Lacation', 'N/A')}")
            print(f"     Haplogroup: {row.get('Haplogroup', 'N/A')}")
            print(f"     Kit: {row.get('Kit Number', 'N/A')}")
    else:
        print(f"✗ No samples found for {target} in AADNA database")


if __name__ == "__main__":
    main()
