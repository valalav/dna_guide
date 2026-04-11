import os
import json
import glob
import shutil

BASE_DIR = '10_Haplogroups'
TREE_FILE = 'current_tree.json'

COL1_MARKERS = {
    'G2a2': ['L1259', 'L30', 'L1264', 'PH1780', 'Z3065', 'U1', 'PF3345'],
    'G2a1': ['Z6552', 'Z6553', 'FGC750', 'M406', 'P287'],
    'J2a': ['M410', 'M67', 'L558', 'L24', 'L26', 'PF5008'],
    'J1': ['M267', 'Z1828', 'Z2217', 'L620'],
    'R1a': ['M417', 'Z93', 'Z282', 'M459', 'M198'],
    'R1b': ['M269', 'L23', 'Z2103', 'L584', 'PH491'],
    'E1b': ['M78', 'M35', 'V13']
}

MAJOR_NODES = {
    'R1a': 'R1a',
    'R1b': 'R1b',
    'J1': 'J1',
    'J2': 'J2',
    'I1': 'I1',
    'I2': 'I2',
    'G1': 'G-M285',
    'G2a1': 'G-Z6552',
    'G2a2': 'G-L1259',
    'C': 'C',
    'E': 'E',
    'L': 'L',
    'M': 'M',
    'N': 'N',
    'O': 'O',
    'Q': 'Q',
    'T': 'T',
    'D': 'D',
    'H': 'H'
}

COL2_PRIORITY = {
    'G2a2': ['L1264', 'PH1780', 'L1266'],
    'G2a1': ['FGC750', 'Z6553', 'M406'],
    'J2a': ['M67', 'L558', 'L24', 'PF5000', 'PF4610', 'PF5008'],
    'J1': ['Z1828', 'Z2217'],
    'R1a': ['Z93', 'Z282'],
    'R1b': ['Z2103', 'L584', 'PH491'],
    'E1b': ['V13', 'M78'],
    'I1': ['DF29', 'Z2893'],
    'I2a': ['L621', 'M423', 'CTS10936'],
    'C2': ['M504', 'M217'],
    'Q1a': ['M25']
}

def load_tree():
    with open(TREE_FILE, encoding='utf-8') as f:
        return json.load(f)

def build_paths(node, current_path, mapping):
    node_id = node.get('id', '')
    snps = [s.strip() for s in node.get('snps', '').split(',')]
    path_with_current = current_path + [node_id]
    
    for snp in snps:
        mapping[snp] = path_with_current
    mapping[node_id] = path_with_current
        
    for child in node.get('children', []):
        build_paths(child, path_with_current, mapping)

def determine_col1(path):
    path_set = set()
    for p in path:
        path_set.add(p)
        if '-' in p:
            path_set.add(p.split('-')[1])
            
    for col1, markers in COL1_MARKERS.items():
        if any(m in path_set for m in markers):
            return col1
            
    for col1, major_node in MAJOR_NODES.items():
        if major_node in path_set:
            return col1
            
    return 'Other'

def determine_col2(path, col1):
    if col1 not in COL2_PRIORITY:
        return 'Base'
    path_set = set()
    for p in path:
        path_set.add(p)
        if '-' in p:
            path_set.add(p.split('-')[1])
    for marker in COL2_PRIORITY[col1]:
        if marker in path_set:
            return marker
    return 'Base'

def calculate_level(path):
    major_idx = 0
    for idx, node in enumerate(path):
        if node in MAJOR_NODES.values():
            major_idx = idx
            break
    return max(0, len(path) - 1 - major_idx)

def extract_target_snp(basename):
    # e.g. R_FT230328_анализ -> ft230328 -> FT230328
    b = basename.upper().replace('_ANALYSIS', '').replace('_АНАЛИЗ', '').replace('.MD', '')
    b = b.replace('03_G2A2_', '').replace('03_', '')
    return b.replace('-', '_').split('_')[-1]

def process_files():
    tree = load_tree()
    snp_to_path = {}
    build_paths(tree, [], snp_to_path)
    
    md_files = glob.glob(f'{BASE_DIR}/**/*.md', recursive=True)
    
    NEW_BASE = '10_Haplogroups_Restructured'
    if os.path.exists(NEW_BASE):
        shutil.rmtree(NEW_BASE)
    os.makedirs(NEW_BASE)
        
    success_count = 0
    unmapped_count = 0
    
    for md in md_files:
        basename = os.path.basename(md)
        target_snp = extract_target_snp(basename)
        
        path = snp_to_path.get(target_snp)
        
        # specific fixes for alias mismatch if needed, but let's see how many unmapped we get.
        
        if not path:
            unmapped_dir = os.path.join(NEW_BASE, 'Unmapped')
            os.makedirs(unmapped_dir, exist_ok=True)
            new_path = os.path.join(unmapped_dir, basename)
            shutil.copy2(md, new_path)
            unmapped_count += 1
            continue
            
        col1 = determine_col1(path)
        col2 = determine_col2(path, col1)
        level = calculate_level(path)
        
        prefix = path[-1].split('-')[0] if '-' in path[-1] else col1[0]
        
        new_filename = f"L{level}-{prefix}-{target_snp}.md"
        new_dir = os.path.join(NEW_BASE, col1, col2)
        os.makedirs(new_dir, exist_ok=True)
        
        new_path = os.path.join(new_dir, new_filename)
        
        with open(md, 'r', encoding='utf-8') as f:
            content = f.read()
            
        path_str = ' > '.join([p for p in path if p])
        tag = f"<!-- YFULL_PATH: {path_str} -->\n"
        
        # Don't double inject
        if "<!-- YFULL_PATH:" not in content:
            content = tag + content
            
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        success_count += 1
        
    print(f"Total mapped: {success_count}, Unmapped: {unmapped_count}.")

if __name__ == '__main__':
    process_files()
