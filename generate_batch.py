import json
import csv
import os
import sys
import re
from jinja2 import Environment, FileSystemLoader

# Configuration
TREE_JSON_PATH = "current_tree.json"
DOCS_DIR = "10_Haplogroups"
BATCH_FILE = "publications.csv"

def load_tree(path):
    """Load the phylogenetic tree from JSON."""
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        sys.exit(1)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)

def find_node_data(tree, target_id):
    """Find the node, lineage, and descendants."""
    target_id_clean = target_id.strip()
    found_node = None
    lineage = []
    descendants = set()
    
    def traverse(current_node, current_path):
        nonlocal found_node, lineage
        node_id = current_node.get('id', '')
        new_path = current_path + [node_id]
        
        if node_id == target_id_clean:
            found_node = current_node
            lineage[:] = new_path
            collect_descendants(current_node)
            return True
        
        if 'children' in current_node:
            for child in current_node['children']:
                if traverse(child, new_path):
                    return True
        return False

    def collect_descendants(node):
        if 'children' in node:
            for child in node['children']:
                cid = child.get('id', '')
                if cid:
                    descendants.add(cid)
                collect_descendants(child)

    if isinstance(tree, list):
        for root in tree:
            if traverse(root, []):
                break
    elif isinstance(tree, dict):
        traverse(tree, [])
        
    return found_node, lineage, descendants

def find_related_docs(target_id, lineage):
    """Find related markdown documentation."""
    all_md_files = []
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                all_md_files.append(os.path.join(root, file))
    
    raw_matches = []
    for item in lineage:
        if not item: continue
        esc_item = re.escape(item).replace(r'\-', '[-_]')
        pattern = re.compile(fr'(^|[\\/\\\\_\\-\\s\\.])({esc_item})($|[\\/\\\\_\\-\\s\\.])', re.IGNORECASE)
        for file_path in all_md_files:
            filename = os.path.basename(file_path)
            if pattern.search(filename):
                raw_matches.append({
                    'id': item,
                    'path': file_path,
                    'filename': filename,
                    'lineage_index': lineage.index(item)
                })

    final_docs = []
    seen_paths = set()
    matches_by_path = {}
    for m in raw_matches:
        path = m['path']
        if path not in matches_by_path or m['lineage_index'] > matches_by_path[path]['lineage_index']:
            matches_by_path[path] = m
    unique_matches = list(matches_by_path.values())
    
    for m in unique_matches:
        is_redundant = False
        if "overview" in m['filename'].lower():
            for other in unique_matches:
                if other['path'] == m['path']: continue
                if other['lineage_index'] > m['lineage_index']:
                    is_redundant = True
                    break
        if len(m['id']) == 1 and m['id'].isalpha():
             for other in unique_matches:
                if other['path'] == m['path']: continue
                if other['lineage_index'] > m['lineage_index']:
                    is_redundant = True
                    break
        if not is_redundant and m['path'] not in seen_paths:
            final_docs.append(m)
            seen_paths.add(m['path'])
            
    final_docs.sort(key=lambda x: x['lineage_index'])
    return final_docs

def generate_post_context(row, lineage_path, branch_node, related_docs, tree):
    """Prepare context for Jinja2 template using row data."""
    branch_name = row['Haplogroup']
    tmrca = branch_node.get('tmrca', 'N/A')
    formatted_lineage = " > ".join(lineage_path)
    
    # TMRCA Indexing
    def build_tmrca_index(node, idx=None):
        if idx is None: idx = {}
        nid = node.get('id', '')
        if nid: idx[nid] = node.get('tmrca', 0)
        for child in node.get('children', []):
            build_tmrca_index(child, idx)
        return idx
    
    tmrca_index = {}
    if isinstance(tree, list):
        for root in tree: build_tmrca_index(root, tmrca_index)
    else: build_tmrca_index(tree, tmrca_index)
    
    lineage_timeline_raw = []
    major_index = -1
    major_tmrca = 0
    current_tmrca = 0
    total_items = len(lineage_path)
    
    for i, branch_id in enumerate(lineage_path):
        branch_tmrca = int(tmrca_index.get(branch_id, 0))
        is_current = (i == total_items - 1)
        is_major = len(branch_id) == 1 and branch_id.isalpha()
        
        if is_major and major_index == -1:
            major_index = i
            major_tmrca = branch_tmrca
        if is_current:
            current_tmrca = branch_tmrca
            
        lineage_timeline_raw.append({
            'id': branch_id,
            'tmrca': branch_tmrca,
            'tmrca_formatted': f"{branch_tmrca:,}".replace(',', ' ') if branch_tmrca else '',
            'is_current': is_current,
            'is_major': is_major,
            'index': i
        })

    lineage_timeline = []
    tmrca_range = major_tmrca - current_tmrca if major_tmrca > current_tmrca else 1
    for item in lineage_timeline_raw:
        position = 0
        if item['index'] >= major_index and major_index >= 0:
            if tmrca_range > 0 and item['tmrca'] > 0:
                time_from_major = major_tmrca - item['tmrca']
                position = int((time_from_major / tmrca_range) * 100)
                position = max(0, min(100, position))
        item['position'] = position
        lineage_timeline.append(item)

    y_dna_docs = []
    for d in related_docs:
        if "autosomal" in d['filename'].lower() or "mt" in d['filename'].lower(): continue
        y_dna_docs.append({
            'filename': d['filename'],
            'path': d['path'].replace('\\', '/'),
            'id': d['id']
        })

    # Header from CSV Row
    header = {
        'surname': row.get('Surname', ''),
        'kit': row.get('Kit', ''),
        'subethnos': row.get('Subethnos', ''),
        'location': row.get('Location', '')
    }

    # Record list for table (Single record as per batch logic, or we could add neighbor find logic here if requested)
    # For now, we list THE person themselves to ensure they appear in the table.
    records = [{
        'surname': row.get('Surname', ''),
        'name': '', # CSV doesn't have Name separate from Surname usually, or assumes Surname is enough
        'kit': row.get('Kit', ''),
        'subethnos': row.get('Subethnos', ''),
        'location': row.get('Location', '')
    }]

    return {
        'ancestor_note': "", # No ancestor fallback note needed as we force the branch
        'branch_name': branch_name,
        'branch_id': branch_node.get('id', ''),
        'header': header,
        'tmrca': tmrca,
        'formatted_lineage': formatted_lineage,
        'lineage_timeline': lineage_timeline,
        'history_section': "", # Placeholder or extract from docs if needed
        'y_dna_docs': y_dna_docs,
        'neighbor_context': "", # Simplify for batch
        'records': records,
        'records_count': 1,
        'test_type': row.get('TestType', 'WGS') # Pass TestType
    }

def main():
    if not os.path.exists(BATCH_FILE):
        print(f"Error: {BATCH_FILE} not found.")
        sys.exit(1)

    print(f"Loading tree...")
    tree = load_tree(TREE_JSON_PATH)

    TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "publication", "templates")
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('batch_post_template.j2')

    with open(BATCH_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            branch = row['Haplogroup'].strip()
            kit = row['Kit'].strip()
            print(f"Processing Kit {kit} ({branch})...")
            
            node, lineage, _ = find_node_data(tree, branch)
            if not node:
                print(f"  Warning: Branch {branch} not found in tree. Skipping.")
                continue

            clean_lineage = list(dict.fromkeys([l for l in lineage if l]))
            related_docs = find_related_docs(branch, clean_lineage)

            context = generate_post_context(row, lineage, node, related_docs, tree)
            
            try:
                output_content = template.render(context)
                slug = row.get('Slug') or f"publication_{branch}_{kit}"
                output_filename = f"{slug}.md"
                
                with open(output_filename, 'w', encoding='utf-8') as out_f:
                    out_f.write(output_content)
                print(f"  Generated: {output_filename}")
                
            except Exception as e:
                print(f"  Error rendering: {e}")

if __name__ == "__main__":
    main()
