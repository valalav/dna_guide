#!/usr/bin/env python3
import json


def find_haplogroup(node, target_id, path=None):
    """Recursively search for a haplogroup by ID or SNP."""
    if path is None:
        path = []

    # Check if current node matches
    if node.get("id") == target_id:
        return {"node": node, "path": path + [node.get("id")]}

    # Check in snps field (synonyms)
    snps = node.get("snps", "")
    if snps:
        snp_list = [s.strip() for s in snps.split(",")]
        if target_id in snp_list:
            return {"node": node, "path": path + [node.get("id")]}

    # Search children
    if "children" in node:
        for child in node["children"]:
            result = find_haplogroup(child, target_id, path + [node.get("id")])
            if result:
                return result

    return None


def get_branch_context(tree, node):
    """Get context around a node including parent and children."""
    context = {}

    # Get children
    children = node.get("children", [])
    context["children"] = [
        {"id": c.get("id"), "tmrca": c.get("tmrca"), "snps": c.get("snps", "")[:50]}
        for c in children
    ]

    return context


def main():
    # Load the tree
    with open("current_tree.json", "r", encoding="utf-8") as f:
        tree = json.load(f)

    # Get E-BY103341
    target = "BY103341"
    result = find_haplogroup(tree, target)

    if result:
        node = result["node"]
        path = result["path"]

        print("=" * 80)
        print(f"E-BY103341 ANALYSIS")
        print("=" * 80)

        print(f"\n## 基本信息")
        print(f"**ID:** {node.get('id')}")
        print(f"**SNPs:** {node.get('snps', 'N/A')}")
        print(f"**Formed:** {node.get('formed', 'N/A')} ybp ({2800 - 3400} лет назад)")
        print(f"**TMRCA:** {node.get('tmrca', 'N/A')} ybp ({2400 - 3800} лет назад)")
        print(
            f"**Gap (Formed - TMRCA):** {node.get('formed', 0) - node.get('tmrca', 0)} лет"
        )

        # Calculate approximate calendar years
        current_year = 2025
        formed_year = current_year - node.get("formed", 0)
        tmrca_year = current_year - node.get("tmrca", 0)

        print(f"\n## Chronology")
        print(f"**Formed circa:** {formed_year} BCE")
        print(f"**TMRCA circa:** {tmrca_year} BCE")
        print(f"**Historical Era:** Late Bronze Age / Early Iron Age")

        # Path from Adam
        print(f"\n## Path from Adam")
        print("```")
        print(" > ".join(path))
        print("```")

        # Parent context
        if len(path) > 0:
            parent_id = path[-2] if len(path) >= 2 else "Root"
            print(f"\n**Parent Branch:** {parent_id}")

        # Children
        context = get_branch_context(tree, node)
        if context["children"]:
            print(f"\n## Sub-branches (Дочерние ветки)")
            for child in context["children"]:
                print(
                    f"- **{child['id']}**: TMRCA {child['tmrca']} ybp, SNPs: {child['snps']}"
                )

        print("\n" + "=" * 80)
        print("NOTES FOR AADNA CONTEXT:")
        print("=" * 80)
        print("1. E-V13 is a major European haplogroup")
        print("2. E-Z1057 and its subclades are common in the Balkans")
        print("3. E-BY103341 is a relatively young subclade (~3100 ybp)")
        print("4. Presence in Caucasus would indicate recent integration")
        print("   (likely historical period, not ancient)")


if __name__ == "__main__":
    main()
