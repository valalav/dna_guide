import json

def find_node(node, snps_to_find, path, results):
    node_id = node.get('id', '')
    snps = [s.strip() for s in node.get('snps', '').split(',')]
    
    current_path = path + [node_id]
    
    for snp in snps:
        if snp in snps_to_find:
            results[snp] = current_path
            
    for child in node.get('children', []):
        find_node(child, snps_to_find, current_path, results)

tree = json.load(open('current_tree.json', encoding='utf-8'))
targets = [
    'M420', 'M198', 'M417', # R1a
    'M343', 'L754', # R1b
    'M267', # J1
    'M172', 'M410', # J2
    'Z6552', 'FGC750', 'P16', # G2a1
    'L1259', 'P15', # G2a2
    'M285', # G1
    'M253', # I1
    'M438', # I2
    'M130', # C
    'M96', # E
    'M20', # L
    'P256', # M
    'M231', # N
    'M175', # O
    'M242', # Q
    'M184', # T
    'M174', # D
    'L901'  # H
]

results = {}
find_node(tree, set(targets), [], results)

for t in targets:
    if t in results:
        print(f"{t}: Depth {len(results[t])} (Path end: {results[t][-3:]})")
    else:
        print(f"{t}: NOT FOUND")
