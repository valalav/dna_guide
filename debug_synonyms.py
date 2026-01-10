import json
import os

def load_tree(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_node_by_synonym(tree, synonym):
    synonym_clean = synonym.strip().upper().replace('J-', '').replace('R-', '').replace('G-', '')
    print(f"Searching for: '{synonym}' (Clean: '{synonym_clean}')")
    
    found_node = None
    
    def traverse(current_node):
        nonlocal found_node
        node_id = current_node.get('id', '')
        
        # Check SNPs field
        snps = current_node.get('snps', '').upper()
        # Handle slash-separated synonyms (e.g. "Z2165/CTS1192/PF5413")
        snp_list = []
        for group in snps.split(','):
            for alias in group.split('/'):
                snp_list.append(alias.strip())
        
        # Debug print for J-Z387 to see what it has
        if 'Z387' in node_id:
            print(f"DEBUG: Found Z387 node. ID: {node_id}")
            print(f"DEBUG: Z387 SNPs: {snps}")
            if synonym_clean in snp_list:
                print(f"DEBUG: MATCH FOUND in SNP list!")
        
        if node_id.upper() == synonym.upper() or synonym_clean in snp_list:
            found_node = current_node
            return True
        
        if 'children' in current_node:
            for child in current_node['children']:
                if traverse(child):
                    return True
        return False

    if isinstance(tree, list):
        for root in tree:
            if traverse(root):
                break
    elif isinstance(tree, dict):
        traverse(tree)
        
    return found_node

try:
    path = "current_tree.json"
    print(f"Loading {path}...")
    tree = load_tree(path)
    print("Tree loaded.")
    
    target = "CTS1192"
    node = find_node_by_synonym(tree, target)
    
    if node:
        print(f"\nSUCCESS: Found node for '{target}'")
        print(f"Canonical ID: {node.get('id')}")
        print(f"TMRCA: {node.get('tmrca')}")
    else:
        print(f"\nFAILURE: Could not find node for '{target}'")

except Exception as e:
    print(f"Error: {e}")
