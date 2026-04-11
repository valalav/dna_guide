import os
import json
import glob

# Load YFull tree
def load_tree():
    with open('current_tree.json', encoding='utf-8') as f:
        return json.load(f)

# Build a mapping of SNP to its full path in the tree
def build_snp_paths(node, current_path, mapping):
    node_id = node.get('id', '')
    snps = [s.strip() for s in node.get('snps', '').split(',')]
    
    path_with_current = current_path + [node_id]
    
    # Map all valid SNPs for this node to this path
    for snp in snps:
        mapping[snp] = path_with_current
    mapping[node_id] = path_with_current
        
    for child in node.get('children', []):
        build_snp_paths(child, path_with_current, mapping)

def analyze_structure():
    tree = load_tree()
    snp_to_path = {}
    build_snp_paths(tree, [], snp_to_path)
    
    md_files = glob.glob('10_Haplogroups/**/*.md', recursive=True)
    
    out_of_place = []
    
    for md in md_files:
        basename = os.path.basename(md).replace('_Analysis.md', '').replace('_analysis.md', '').replace('_анализ.md', '').replace('.md', '')
        
        # Heuristics to find target SNP
        target_snp = None
        if '-' in basename:
            target_snp = basename.split('-')[1]
        elif '_' in basename:
            # Maybe like 03_G2a2_FT361088
            parts = basename.split('_')
            target_snp = parts[-1]
        else:
            target_snp = basename
            
        if target_snp in snp_to_path:
            expected_path = snp_to_path[target_snp]
            out_of_place.append({
                'file': md,
                'snp': target_snp,
                'expected_depth': len(expected_path),
                'current_depth': len(md.split(os.sep)) - 1
            })
        else:
            print(f"Could not find SNP {target_snp} in YFull tree for file: {md}")
            
    print(f"\nTotal MD files found: {len(md_files)}")
    print(f"Files mapped to tree: {len(out_of_place)}")
    
    # Just show a few examples
    print("\nSample mapped files:")
    for item in out_of_place[:10]:
        print(f"{item['file']} -> {item['snp']} (Tree Depth: {item['expected_depth']}, Current Depth: {item['current_depth']})")

if __name__ == '__main__':
    analyze_structure()
