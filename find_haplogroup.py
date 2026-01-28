#!/usr/bin/env python3
import json


def find_haplogroup(node, target_id, path=None, parent=None):
    """Recursively search for a haplogroup by ID or SNP."""
    if path is None:
        path = []

    # Check if current node matches
    if node.get("id") == target_id:
        return {"node": node, "path": path + [node.get("id")], "parent": parent}

    # Check in snps field (synonyms)
    snps = node.get("snps", "")
    if snps:
        snp_list = [s.strip() for s in snps.split(",")]
        if target_id in snp_list:
            return {"node": node, "path": path + [node.get("id")], "parent": parent}

    # Search children
    if "children" in node:
        for child in node["children"]:
            result = find_haplogroup(child, target_id, path + [node.get("id")], node)
            if result:
                return result

    return None


def main():
    # Load the tree
    with open("current_tree.json", "r", encoding="utf-8") as f:
        tree = json.load(f)

    # Search for E-BY103341
    target = "BY103341"
    result = find_haplogroup(tree, target)

    if result:
        node = result["node"]
        path = result["path"]

        print("=" * 80)
        print(f"Found: {node.get('id')}")
        print("=" * 80)
        print(f"ID: {node.get('id')}")
        print(f"SNPs: {node.get('snps', 'N/A')}")
        print(f"Formed: {node.get('formed', 'N/A')} ybp (years before present)")
        print(f"TMRCA: {node.get('tmrca', 'N/A')} ybp")
        print(
            f"Formed Range: {node.get('formedlowage', 'N/A')}-{node.get('formedhighage', 'N/A')} ybp"
        )
        print(
            f"TMRCA Range: {node.get('tmrcalowage', 'N/A')}-{node.get('tmrcahighage', 'N/A')} ybp"
        )
        print()
        print("Path from Adam:")
        print(" > ".join(path))
        print()
        print(f"Number of children: {len(node.get('children', []))}")

        if node.get("children"):
            print("\nChildren branches:")
            for child in node["children"]:
                child_tmrca = child.get("tmrca", "N/A")
                child_snps = child.get("snps", "N/A")[:30]
                print(
                    f"  - {child.get('id')} (TMRCA: {child_tmrca} ybp, SNPs: {child_snps}...)"
                )

    else:
        print(f"Haplogroup '{target}' not found in current_tree.json")


if __name__ == "__main__":
    main()
