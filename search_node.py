#!/usr/bin/env python3
import json
import sys


def find_haplogroup(node, target_id):
    """Recursively search for a haplogroup by ID or SNPs"""
    # Check if this node matches
    if node.get("id") == target_id:
        return node

    # Check SNPs
    snps = node.get("snps", "")
    if snps and target_id.replace("G-", "") in snps:
        return node

    # Check children
    if "children" in node and node["children"]:
        for child in node["children"]:
            result = find_haplogroup(child, target_id)
            if result:
                return result

    return None


def get_path_to_node(tree, target_id):
    """Get the full path from root to the target node"""

    def search_with_path(node, target_id, current_path):
        # Check if this node matches
        matches = False
        if node.get("id") == target_id:
            matches = True
        else:
            snps = node.get("snps", "")
            if snps and target_id.replace("G-", "") in snps:
                matches = True

        if matches:
            return current_path + [node.get("id")]

        # Search children
        if "children" in node and node["children"]:
            for child in node["children"]:
                result = search_with_path(
                    child, target_id, current_path + [node.get("id")]
                )
                if result:
                    return result

        return None

    return search_with_path(tree, target_id, [])


# Load tree
with open("current_tree.json", "r", encoding="utf-8") as f:
    tree = json.load(f)

# Search for G-FTA78507
target = "G-FTA78507"
print(f"Searching for {target}...")

node = find_haplogroup(tree, target)

if node:
    print(f"\n✓ Found node: {target}")
    print(f"  ID: {node.get('id')}")
    print(f"  SNPs: {node.get('snps')}")
    print(f"  Formed: {node.get('formed')} ybp")
    print(f"  TMRCA: {node.get('tmrca')} ybp")
    print(f"  Children: {len(node.get('children', []))} subclades")

    # Get path
    path = get_path_to_node(tree, target)
    print(f"\n  Path from root:")
    print(f"    {' → '.join(path)}")
else:
    print(f"\n✗ Node {target} not found in tree")
    print("This haplogroup may be too new or not yet in YFull tree")
