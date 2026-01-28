#!/usr/bin/env python3
import json
import csv
from typing import List, Dict, Optional


def load_tree(filepath: str) -> dict:
    """Load the current_tree.json"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def find_haplogroup(tree: dict, target_id: str) -> Optional[dict]:
    """Recursively find a haplogroup by id or SNP in snps field"""
    # Check id match
    if tree.get("id") == target_id:
        return tree

    # Check SNP synonyms
    if "snps" in tree:
        snp_list = [s.strip() for s in tree["snps"].split(",")]
        if target_id in snp_list:
            return tree

    # Recursively search children
    if "children" in tree:
        for child in tree["children"]:
            result = find_haplogroup(child, target_id)
            if result:
                return result
    return None


def get_path_to_root(
    tree: dict, target_id: str, path: List[str] = None
) -> Optional[List[str]]:
    """Get the path from Adam to the target haplogroup"""
    if path is None:
        path = []

    # Check if this is the target
    if tree.get("id") == target_id:
        return [tree["id"]] + path

    # Check SNP synonyms
    if "snps" in tree:
        snp_list = [s.strip() for s in tree["snps"].split(",")]
        if target_id in snp_list:
            return [tree["id"]] + path

    # Recursively search children
    if "children" in tree:
        for child in tree["children"]:
            result = get_path_to_root(child, target_id, path)
            if result:
                # Prepend current node id
                return [tree["id"]] + result

    return None


def get_all_descendants(
    tree: dict, target_id: str, descendants: List[str] = None
) -> List[str]:
    """Get all descendant IDs of a target haplogroup"""
    if descendants is None:
        descendants = []

    # If this is the target node, collect all children
    if tree.get("id") == target_id or (
        tree.get("snps") and target_id in [s.strip() for s in tree["snps"].split(",")]
    ):
        # Found target - collect all child IDs
        def collect_children(node, ids):
            ids.append(node["id"])
            if "children" in node:
                for child in node["children"]:
                    collect_children(child, ids)
            return ids

        collect_children(tree, [])
        return descendants

    # Otherwise keep searching
    if "children" in tree:
        for child in tree["children"]:
            result = get_all_descendants(child, target_id, descendants)
            if result:
                return result

    return None


def load_csv(filepath: str) -> List[dict]:
    """Load the AADNA CSV file"""
    data = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            data.append(row)
    return data


def find_samples_in_csv(csv_data: List[dict], haplogroup_ids: List[str]) -> List[dict]:
    """Find samples that match any of the haplogroup IDs"""
    matches = []
    for row in csv_data:
        # Check terminal haplogroup column
        terminal = row.get("Haplogroup", "")
        for hap_id in haplogroup_ids:
            if hap_id in terminal:
                matches.append(row)
                break
    return matches


def main():
    # Load tree
    tree = load_tree("current_tree.json")

    # Search for J-Y305471
    target = "J-Y305471"
    print(f"Searching for: {target}")
    print("=" * 60)

    # Find the haplogroup
    haplogroup = find_haplogroup(tree, target)

    if not haplogroup:
        print(f"❌ {target} NOT FOUND in current_tree.json")
        print(
            "\nYou may need to check YFull.com: https://www.yfull.com/tree/J-Y305471/"
        )
        return

    print(f"✅ Found: {haplogroup.get('id')}")
    print(f"   SNPs: {haplogroup.get('snps', 'N/A')}")
    print(f"   Formed: {haplogroup.get('formed', 'N/A')} ybp")
    print(f"   TMRCA: {haplogroup.get('tmrca', 'N/A')} ybp")

    # Get path from Adam
    print("\n" + "=" * 60)
    print("PATH FROM ADAM:")
    path = get_path_to_root(tree, target)
    if path:
        # Reverse to show Adam -> Target
        full_path = " > ".join(reversed(path))
        print(full_path)

    # Get all descendant IDs
    print("\n" + "=" * 60)
    descendants = [target]
    if "children" in haplogroup:

        def collect_all(node, ids):
            ids.append(node["id"])
            if "children" in node:
                for child in node["children"]:
                    collect_all(child, ids)

        collect_all(haplogroup, descendants)
    print(f"Descendant haplogroups ({len(descendants)}):")
    for i, desc in enumerate(descendants[:20], 1):  # Show first 20
        print(f"  {i}. {desc}")
    if len(descendants) > 20:
        print(f"  ... and {len(descendants) - 20} more")

    # Load CSV and find samples
    print("\n" + "=" * 60)
    csv_data = load_csv("aadna.ru.csv")
    samples = find_samples_in_csv(csv_data, descendants)

    if samples:
        print(f"✅ Found {len(samples)} samples in AADNA database:")
        for sample in samples:
            print(f"\n  Surname: {sample.get('Surname', 'N/A')}")
            print(f"  Subethnos: {sample.get('Субэтнос', 'N/A')}")
            print(
                f"  Location: {sample.get('Lacation', sample.get('Location', 'N/A'))}"
            )
            print(f"  Haplogroup: {sample.get('Haplogroup', 'N/A')}")
            print(f"  YFull: {sample.get('Yfull', 'N/A')}")
    else:
        print(f"❌ No samples found for {target} or its descendants")

    # Check specifically for Adyghe-Abkhaz samples
    print("\n" + "=" * 60)
    adyghe_samples = []
    for sample in samples:
        subethnos = sample.get("Субэтнос", "").lower()
        if any(
            term in subethnos
            for term in [
                "кабардинец",
                "абхаз",
                "адыг",
                "шапсуг",
                "абадзех",
                "бжедуг",
                "темиргоевец",
            ]
        ):
            adyghe_samples.append(sample)

    if adyghe_samples:
        print(f"✅ Found {len(adyghe_samples)} Adyghe-Abkhaz samples:")
        for sample in adyghe_samples:
            print(
                f"  - {sample.get('Surname', 'N/A')} ({sample.get('Субэтнос', 'N/A')})"
            )
    else:
        print(f"ℹ️  No Adyghe-Abkhaz samples found")


if __name__ == "__main__":
    main()
