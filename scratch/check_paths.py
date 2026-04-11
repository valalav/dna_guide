import json

def find_paths(node, query_ids, path, results):
    node_id = node.get('id', '')
    current_path = path + [node_id]
    
    if node_id in query_ids:
        results[node_id] = current_path
        
    for child in node.get('children', []):
        find_paths(child, query_ids, current_path, results)

tree = json.load(open('current_tree.json', encoding='utf-8'))
results = {}
find_paths(tree, ['G-L1264', 'R-Z282', 'J-M67', 'R-M269'], [], results)

for id, path in results.items():
    print(f"\nPath for {id}:")
    print(path)
