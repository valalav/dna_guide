#!/usr/bin/env python3
import json


def find_node_path(node, target_id, path=None):
    """Recursively find a node and build its path from root."""
    if path is None:
        path = []

    node_name = node.get("id") or node.get("name", "Unknown")
    current_path = path + [node_name]

    if node.get("id") == target_id or node.get("name") == target_id:
        return node, current_path

    if "children" in node:
        for child in node["children"]:
            result = find_node_path(child, target_id, current_path)
            if result:
                return result

    return None


def main():
    target = "R-BY103576"

    with open("current_tree.json", "r", encoding="utf-8") as f:
        tree = json.load(f)

    result = find_node_path(tree, target)

    if result:
        node, path = result

        print(f"=== Node: {target} ===\n")
        print(f"Path from root: {' > '.join(path)}\n")

        print(f"ID: {node.get('id')}")
        print(f"Name: {node.get('name')}")
        print(f"SNPs: {node.get('snps', 'N/A')}")
        print(f"Formed: {node.get('formed', 'N/A')} years ago")
        print(f"TMRCA: {node.get('tmrca', 'N/A')} years ago")

        if "children" in node and node["children"]:
            print(f"\nChildren ({len(node['children'])}):")
            for i, child in enumerate(node["children"], 1):
                child_id = child.get("id", child.get("name", "Unknown"))
                child_snps = child.get("snps", "N/A")
                child_tmrca = child.get("tmrca", "N/A")
                print(
                    f"  {i}. {child_id} (TMRCA: {child_tmrca} ya, SNPs: {child_snps})"
                )
        else:
            print("\nNo children found (terminal node)")

    else:
        print(f"Node {target} not found in tree")


if __name__ == "__main__":
    main()
