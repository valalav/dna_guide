import json
import csv
import argparse
import requests
import io
import os
import sys
import glob

# Configuration
TREE_JSON_PATH = "current_tree.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTp8VNm5yS63RiflBpMY4b8d4RBTPecjU_RrC10EDcgSitcQxRtt1QbeN67g8bYOyqB088GLOTHIG5g/pub?gid=90746110&single=true&output=tsv"
DOCS_DIR = "10_Haplogroups"

def load_tree(path):
    """Load the phylogenetic tree from JSON."""
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        sys.exit(1)
    
    # Check if file is empty
    if os.path.getsize(path) == 0:
        print(f"Error: {path} is empty.")
        sys.exit(1)

    print(f"Loading tree structure from {path}...")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)

def find_node_data(tree, target_id):
    """
    Find the node, its full lineage path, and all its descendant IDs.
    Returns: (node_object, lineage_path_list, set_of_descendant_ids)
    """
    target_id_clean = target_id.strip()
    
    # Result holders
    found_node = None
    lineage = []
    descendants = set()
    
    def traverse(current_node, current_path):
        nonlocal found_node, lineage
        
        # Get node ID (some nodes might rely on 'name' if 'id' is missing/generic, but usually 'id' is key)
        node_id = current_node.get('id', '')
        
        # Keep track of path
        new_path = current_path + [node_id]
        
        if node_id == target_id_clean:
            found_node = current_node
            lineage[:] = new_path # Update the outer lineage variable
            # Collect all descendants
            collect_descendants(current_node)
            return True
        
        if 'children' in current_node:
            for child in current_node['children']:
                if traverse(child, new_path):
                    return True
        return False

    def collect_descendants(node):
        """Recursively add all child IDs to the descendants set."""
        if 'children' in node:
            for child in node['children']:
                cid = child.get('id', '')
                if cid:
                    descendants.add(cid)
                collect_descendants(child)

    # Start traversal
    # Handle list of roots or single root
    if isinstance(tree, list):
        for root in tree:
            if traverse(root, []):
                break
    elif isinstance(tree, dict):
        traverse(tree, [])
        
    return found_node, lineage, descendants

def fetch_sheet_data(url):
    """Fetch data from Google Sheets TSV or local file."""
    local_file = "aadna_data.tsv"
    
    content = None
    if os.path.exists(local_file):
        print(f"Using local file: {local_file}")
        with open(local_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        print(f"Downloading from {url}...")
        try:
            # Try with verification first
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
        except Exception as e:
            print(f"Standard download failed: {e}")
            print("Retrying with SSL verification disabled...")
            try:
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                response = requests.get(url, verify=False)
                response.raise_for_status()
                content = response.text
            except Exception as e2:
                print(f"Download failed: {e2}")
                sys.exit(1)
        
        # Save for cache
        if content:
            with open(local_file, 'w', encoding='utf-8') as f:
                f.write(content)

    return content

def parse_sheet_data(csv_text, target_id, descendants):
    """
    Parse TSV data and find rows matching the target branch OR its descendants.
    Robustly handles newlines in fields.
    """
    matches = []
    valid_haplogroups = {target_id} | descendants
    
    # Pre-process lines to handle potential issues
    # Google Sheets TSV sometimes puts newlines in cells without quotes? Or maybe typical CSV issues.
    # We will try standard parsing first, if that fails, maybe we can try to recover.
    # But usually DictReader is fine if the format is correct. 
    # If "new-line character seen in unquoted field" occurs, it means there's a \n inside a column that isn't quoted.
    
    try:
        # csv.reader might be strict. Let's try manual split if csv fails, 
        # or just set strict=False if checking? No, strict param doesn't help with structure.
        # We'll stick to standard first, but with a potential pre-cleaning if needed.
        # Actually, for TSV, we can just split by tab if we assume no tabs in fields. 
        # But fields *can* have tabs if quoted. 
        # Let's try `csv.DictReader` with `quoting=csv.QUOTE_MINIMAL` (default) but maybe `QUOTE_NONE` is better if no quotes used?
        # Google Sheets TSV usually doesn't quote unless needed.
        
        f = io.StringIO(csv_text)
        reader = csv.DictReader(f, delimiter='\t')
        
        for row in reader:
            # Check Terminal Haplogroup
            terminal = (row.get('Haplogroup') or '').strip()
            
            # Check Hierarchy columns
            h_cols = [
                (row.get('Гг1') or ''), (row.get('Гг2') or ''), (row.get('Гг3') or ''),
                (row.get('Гг4') or ''), (row.get('Гг5') or '')
            ]
            
            is_match = False
            
            # Exact terminal match
            if terminal in valid_haplogroups:
                is_match = True
            
            # Hierarchy match
            if not is_match:
                for col in h_cols:
                    if col and col.strip() == target_id:
                        is_match = True
                        break
            
            if is_match:
                matches.append(row)
                
    except csv.Error as e:
        print(f"Standard CSV Parsing Error: {e}")
        print("Attempting fallback parsing (line-by-line split)...")
        # Fallback: simpler split by tab. 
        # Warning: This breaks if fields contain tabs.
        
        lines = csv_text.splitlines()
        if not lines:
            return []
            
        header = lines[0].split('\t')
        # Map headers to indices
        try:
            idx_hap = header.index('Haplogroup')
            # Try to find loose matches for hierarchy columns
            idx_gg = [i for i, h in enumerate(header) if h.startswith('Гг')]
        except ValueError:
            print("Headers missing in fallback mode.")
            return []
            
        for line in lines[1:]:
            parts = line.split('\t')
            if len(parts) != len(header):
                # Length mismatch - skip or try to salvage? 
                # often mismatch is due to newlines. Skipping for now to avoid garbage.
                continue
                
            row_dict = dict(zip(header, parts))
            
            # Re-run match logic
            terminal = row_dict.get('Haplogroup', '').strip()
            is_match = False
            if terminal in valid_haplogroups:
                is_match = True
            
            if not is_match:
                for idx in idx_gg:
                    if idx < len(parts) and parts[idx].strip() == target_id:
                        is_match = True
                        break
            
            if is_match:
                matches.append(row_dict)

    return matches

def find_related_docs(target_id, lineage):
    """Find documentation files related to the branch or its ancestors."""
    related_files = []
    
    # Search terms: specific branch ID, and parent IDs (reversed order for relevance)
    # Filter out empty strings
    search_terms = [t for t in ([target_id] + lineage[::-1]) if t]
    
    # We explicitly look into 10_Haplogroups
    # Walk directory
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                # Check if filename contains any of the search terms
                for term in search_terms:
                    # simplistic check: term in filename
                    # e.g. "G-L1264" in "00_G-L1264_Overview.md"
                    if term in file:
                        path = os.path.join(root, file)
                        related_files.append((term, path))
                        break # Found a match for this file
    
    return related_files

def generate_markdown(record, lineage_path, branch_node, related_docs):
    """Generate markdown content."""
    surname = record.get('Фамилия', 'Unknown')
    subethnos = record.get('Субэтнос', 'Unknown')
    location = record.get('Населенный пункт', 'Unknown')
    if location == 'Unknown': 
        location = record.get('Lacation', 'Unknown') # Handle typo
        
    history = record.get('История', '')
    
    # Metadata from JSON
    tmrca = branch_node.get('tmrca', 'Unknown')
    
    # Format lineage: A -> ... -> Target
    # lineage_path is a list of IDs.
    formatted_lineage = " >> ".join(lineage_path)
    
    # Docs section
    docs_section = ""
    if related_docs:
        docs_section = "## Справочная информация\n"
        seen_paths = set()
        for term, path in related_docs:
            if path not in seen_paths:
                # Relative link logic or just listing it
                # Assuming simple list for now
                docs_section += f"- [{os.path.basename(path)}]({path}) (Relates to {term})\n"
                seen_paths.add(path)
    
    template = f"""# {surname}

**Фамилия:** {surname}
**Субэтнос:** {subethnos}
**Населенный пункт:** {location}

**Гаплогруппа:** {formatted_lineage}
**Возраст ветки (TMRCA):** {tmrca} лет

## История
{history}

{docs_section}

## Внешние ссылки
- [YFull Tree](https://www.yfull.com/tree/{branch_node.get('id', '')}/)
- [Проект AADNA](https://aadna.ru/)
"""
    return template

def main():
    parser = argparse.ArgumentParser(description='Generate publication from DNA data.')
    parser.add_argument('--branch', required=True, help='Target haplogroup branch (e.g., R-FT409028)')
    parser.add_argument('--output', help='Output file path')
    
    args = parser.parse_args()
    branch = args.branch
    
    # 1. Load Tree & Metadata
    tree = load_tree(TREE_JSON_PATH)
    node, lineage, descendants = find_node_data(tree, branch)
    
    if not node:
        print(f"Error: Branch {branch} not found in {TREE_JSON_PATH}")
        sys.exit(1)
        
    print(f"Found branch metadata. TMRCA: {node.get('tmrca', 'N/A')}")
    print(f"Path: {' > '.join(lineage)}")
    print(f"Found {len(descendants)} descendant branches.")
    
    # 2. Fetch Data
    csv_text = fetch_sheet_data(SHEET_URL)
    
    # 3. Filter Data (Hierarchical)
    print("Parsing and filtering CSV data...")
    matches = parse_sheet_data(csv_text, branch, descendants)
    print(f"Found {len(matches)} matching records.")
    
    if not matches:
        print("No matching records found in CSV.")
        # Continue to generation for summary


    # 4. Find Documentation
    print("Searching for related documentation...")
    related_docs = find_related_docs(branch, lineage)
    
    # 5. Generate Content
    full_content = ""
    if matches:
        for record in matches:
            full_content += generate_markdown(record, lineage, node, related_docs)
            full_content += "\n---\n\n"
    else:
        print("No matching records found. Generating summary publication.")
        # Minimal template for branch with no samples
        docs_section = ""
        if related_docs:
            docs_section = "## Справочная информация\n"
            seen_paths = set()
            for term, path in related_docs:
                if path not in seen_paths:
                    docs_section += f"- [{os.path.basename(path)}]({path}) (Relates to {term})\n"
                    seen_paths.add(path)
        
        full_content = f"""# Haplogroup {branch}

**Гаплогруппа:** {" >> ".join(lineage)}
**Возраст ветки (TMRCA):** {node.get('tmrca', 'Unknown')} лет

## Образцы
В текущей базе данных образцов для этой ветки не найдено.

{docs_section}

## Внешние ссылки
- [YFull Tree](https://www.yfull.com/tree/{node.get('id', '')}/)
- [Проект AADNA](https://aadna.ru/)
"""

    output_file = args.output if args.output else f"publication_{branch}.md"
    
    abs_path = os.path.abspath(output_file)
    print(f"Writing to: {abs_path}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_content)
        
    print(f"Successfully generated {output_file}")
    if os.path.exists(output_file):
        print("File verification: Exists.")
    else:
        print("File verification: DOES NOT EXIST.")

if __name__ == "__main__":
    main()
