import json
import csv
import sys

TREE_JSON = "current_tree.json"
TSV_FILE = "aadna_data.tsv"
TARGET = "R-FT409028"

def load_tree(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_node_path(tree, target_id):
    # Flatten tree to map for easier lookup? No, just traverse
    # Simplified search for ID
    def search(node, path):
        node_id = node.get('id', '')
        curr_path = path + [node_id]
        if node_id == target_id:
            return curr_path
        
        for child in node.get('children', []):
            res = search(child, curr_path)
            if res: return res
        return None

    if isinstance(tree, list):
        for root in tree:
            res = search(root, [])
            if res: return res
    else:
        return search(tree, [])
    return []

def main():
    print(f"Loading tree...")
    tree = load_tree(TREE_JSON)
    print(f"Finding path for {TARGET}...")
    lineage = find_node_path(tree, TARGET)
    
    if not lineage:
        print(f"Target {TARGET} not found in json tree.")
        sys.exit(1)
        
    print(f"Lineage: {' > '.join(lineage)}")
    
    print(f"Loading CSV data...")
    # Read entire CSV into memory string for parsing checks
    with open(TSV_FILE, 'r', encoding='utf-8') as f:
        csv_content = f.read()
        
    # Check each ancestor
    # We want to know: "Is this ID present in ANY of the haplo/hierarchy columns?"
    
    found_ancestors = []
    
    # We iterate reversed (from target up to root)
    for ancestor in reversed(lineage):
        print(f"Checking {ancestor}...", end="", flush=True)
        if ancestor in csv_content:
            print(f" FOUND in text!")
            found_ancestors.append(ancestor)
        else:
            print(f" NOT found.")
            
    if found_ancestors:
        print(f"\nClosest found ancestor in CSV: {found_ancestors[0]}")
    else:
        print("\nNo ancestors found in CSV (unlikely).")

if __name__ == "__main__":
    main()
