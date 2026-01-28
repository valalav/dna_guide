#!/usr/bin/env python3
import json
import sys


def find_node_recursive(node, target_id, path=None):
    if path is None:
        path = []

    # Check if this node matches
    if node.get("id") == target_id:
        return node, path

    # Check snps field for synonym matches
    if "snps" in node and node["snps"]:
        snps_list = [s.strip() for s in node["snps"].split(",")]
        for snp in snps_list:
            if (
                snp == target_id
                or f"{node['id']}-{snp}" == target_id
                or snp.replace(f"{node['id']}-", "")
                == target_id.replace(f"{node['id']}-", "")
            ):
                return node, path

    # Recursively search children
    if "children" in node and node["children"]:
        current_path = path + [node.get("id", "unknown")]
        for child in node["children"]:
            result = find_node_recursive(child, target_id, current_path)
            if result:
                return result

    return None, None


# Load the tree
with open("current_tree.json", "r") as f:
    tree = json.load(f)

# Search for R-Y210364
target = "R-Y210364"
result, path = find_node_recursive(tree, target)

if result:
    print(f"✅ Found node: {result.get('id')}")
    print(f"Path: {' -> '.join(path)}")
    print(f"Formed: {result.get('formed', 'N/A')} ybp")
    print(f"TMRCA: {result.get('tmrca', 'N/A')} ybp")
    print(f"SNPs: {result.get('snps', 'N/A')}")
    print(f"Children: {len(result.get('children', []))}")

    # List children names
    if result.get("children"):
        print("\nChildren branches:")
        for child in result["children"]:
            print(f"  - {child.get('id')} (TMRCA: {child.get('tmrca', 'N/A')})")
else:
    print(f"❌ Node '{target}' not found in current_tree.json")
