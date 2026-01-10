import json
import csv
import sys
import requests
import io

# Configuration
TREE_JSON_PATH = r"c:\_Data\obsidian\01_ЛЧ Проекты\00_DNA\Публикации\claude_2025_12_29\dna_guide\current_tree.json"
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTp8VNm5yS63RiflBpMY4b8d4RBTPecjU_RrC10EDcgSitcQxRtt1QbeN67g8bYOyqB088GLOTHIG5g/pub?gid=90746110&single=true&output=csv"
REPORT_PATH = r"c:\_Data\obsidian\01_ЛЧ Проекты\00_DNA\Публикации\claude_2025_12_29\dna_guide\hierarchy_validation_report.md"

DEEP_LABS = ["YFull", "Nebo", "Dante Labs", "Big Y", "YSEQ-WGS"] 
SURFACE_LABS = ["Genotek", "23andMe", "Ancestry", "MyHeritage", "Living DNA"]

def load_tree(json_path):
    print("Loading tree JSON...")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {json_path}")
        sys.exit(1)
        
    node_map = {} 
    parent_map = {} 
    snp_map = {} 
    
    def traverse(node, parent_id=None):
        node_id = node.get('id')
        if parent_id:
            parent_map[node_id] = parent_id
        
        node_map[node_id] = node
        
        snps = node.get('snps', '')
        if snps:
            for snp in snps.split(', '):
                clean_snp = snp.strip()
                for variant in clean_snp.split('/'):
                    v = variant.strip()
                    if v:
                        snp_map[v] = node_id
        
        children = node.get('children', [])
        for child in children:
            traverse(child, node_id)

    if isinstance(data, list):
        for root in data:
            traverse(root)
    else:
        traverse(data)
        
    print(f"Tree loaded. {len(node_map)} nodes, {len(snp_map)} SNP mappings.")
    return node_map, parent_map, snp_map

def get_ancestors(node_id, parent_map):
    ancestors = []
    curr = node_id
    while curr in parent_map:
        curr = parent_map[curr]
        ancestors.append(curr)
    return set(ancestors)

def find_node_id(hg_input, node_map, snp_map):
    if not hg_input:
        return None
    hg_input = hg_input.strip()
    
    if hg_input in node_map:
        return hg_input
    
    if hg_input in snp_map:
        return snp_map[hg_input]
    
    if '-' in hg_input:
        snp = hg_input.split('-')[-1].strip()
        if snp in snp_map:
            return snp_map[snp]
            
    return None

def validate_csv(csv_url, node_map, parent_map, snp_map):
    print("Fetching CSV...")
    response = requests.get(csv_url)
    response.encoding = 'utf-8'
    f = io.StringIO(response.text)
    reader = csv.DictReader(f)
    
    report_lines = ["# Validation Report\n"]
    
    for i, row in enumerate(reader):
        row_num = i + 2 
        
        kit_num = row.get('Kit Number', '')
        name = row.get('Name', '')
        if len(kit_num) < 3 and not kit_num.isdigit() and not kit_num.startswith('gt') and not kit_num.startswith('YF'): 
             # Heuristic for technical rows: Short kit numbers like C2, E often
             if "C2" in kit_num or "E" == kit_num: # Adjust based on data
                 continue
        if '>' in name: 
             continue
             
        gg_cols = [row.get(f'Гг{n}', '').strip() for n in range(1, 6)]
        haplogroup = row.get('Haplogroup', '').strip()
        
        resolved_nodes = []
        path_error = False
        
        for idx, val in enumerate(gg_cols):
            if not val:
                resolved_nodes.append(None)
                continue
            
            node_id = find_node_id(val, node_map, snp_map)
            resolved_nodes.append(node_id)
            
            if idx > 0 and resolved_nodes[idx-1] and node_id:
                parent_node = resolved_nodes[idx-1]
                ancestors = get_ancestors(node_id, parent_map)
                if parent_node not in ancestors and parent_node != node_id:
                    report_lines.append(f"- **Row {row_num} ({kit_num})**: Hierarchy break. `{val}` (Col {idx+1}) is NOT a descendant of `{gg_cols[idx-1]}`.")
                    path_error = True
        
        if haplogroup and not path_error:
            term_node = find_node_id(haplogroup, node_map, snp_map)
            
            last_gg_idx = -1
            for k in range(4, -1, -1):
                if resolved_nodes[k]:
                    last_gg_idx = k
                    break
            
            if last_gg_idx >= 0 and term_node:
                last_gg_node = resolved_nodes[last_gg_idx]
                if term_node != last_gg_node:
                    term_ancestors = get_ancestors(term_node, parent_map)
                    if last_gg_node not in term_ancestors:
                         report_lines.append(f"- **Row {row_num} ({kit_num})**: Terminal Haplogroup `{haplogroup}` is inconsistent with hierarchy end `{gg_cols[last_gg_idx]}`.")

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.writelines([l + '\n' for l in report_lines])
    
    print(f"Report generated at {REPORT_PATH}")

if __name__ == "__main__":
    node_map, parent_map, snp_map = load_tree(TREE_JSON_PATH)
    try:
        validate_csv(CSV_URL, node_map, parent_map, snp_map)
    except Exception as e:
        print(f"Error: {e}")
