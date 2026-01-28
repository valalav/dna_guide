#!/usr/bin/env python3
import json


def find_haplogroup_with_details(node, target_id):
    """Recursively search and return node with full details"""
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
            result = find_haplogroup_with_details(child, target_id)
            if result:
                return result

    return None


# Load tree
with open("current_tree.json", "r", encoding="utf-8") as f:
    tree = json.load(f)

# Search for G-FTA78507
target = "G-FTA78507"
node = find_haplogroup_with_details(tree, target)

if node:
    print(f"Node ID: {node.get('id')}")
    print(f"Primary SNP: {target}")
    print(f"All SNPs: {node.get('snps')}")
    print(f"Formed: {node.get('formed')} ybp")
    print(f"TMRCA: {node.get('tmrca')} ybp")

    # Gap (bottleneck)
    formed = int(node.get("formed", 0))
    tmrca = int(node.get("tmrca", 0))
    gap = formed - tmrca
    print(f"Gap (bottleneck): {gap} years")

    # Children details
    if "children" in node and node["children"]:
        print(f"\nChild branches ({len(node['children'])}):")
        for i, child in enumerate(node["children"], 1):
            print(f"  {i}. {child.get('id')}")
            print(f"     - SNPs: {child.get('snps', 'N/A')[:80]}")
            print(f"     - Formed: {child.get('formed')} ybp")
            print(f"     - TMRCA: {child.get('tmrca')} ybp")
            print(f"     - Children: {len(child.get('children', []))} subclades")
