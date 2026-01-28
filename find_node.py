#!/usr/bin/env python3
import json
import sys


def find_haplogroup(node, target_id):
    """Recursively find a haplogroup by id in the tree."""
    if node.get("id") == target_id:
        return node

    if "children" in node:
        for child in node["children"]:
            result = find_haplogroup(child, target_id)
            if result:
                return result

    return None


def get_path_from_root(tree, target_id, path=None):
    """Get the path from root to the target node."""
    if path is None:
        path = []

    if tree.get("id") == target_id:
        return path + [target_id]

    if "children" in tree:
        for child in tree["children"]:
            result = get_path_from_root(child, target_id, path + [tree.get("id")])
            if result:
                return result

    return None


# Load the tree
with open("current_tree.json", "r") as f:
    tree = json.load(f)

# Find G-Y152745
target = "G-Y152745"
node = find_haplogroup(tree, target)

if node:
    print(f"Found: {target}")
    print(f"Formed: {node.get('formed', 'N/A')} ybp")
    print(f"TMRCA: {node.get('tmrca', 'N/A')} ybp")
    print(f"SNPs: {node.get('snps', 'N/A')}")

    # Get path from root
    path = get_path_from_root(tree, target)
    print(f"\nPath from root: {' > '.join(filter(None, path))}")

    # Check for children
    children = node.get("children", [])
    print(f"\nNumber of children: {len(children)}")
    if children:
        print("Children:")
        for child in children[:10]:  # Show first 10 children
            print(f"  - {child.get('id')}")
else:
    print(f"Not found: {target}")
