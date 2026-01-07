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
            
        # Check for mojibake (Cyrillic displayed as Latin1)
        # 'Ð' is common start byte 0xD0 in UTF-8 displayed as Latin1
        if 'Ð' in content[:1000]:
            print("Detected potential encoding issue (Mojibake). Attempting repair...")
            try:
                # Encode back to bytes using latin-1 (which preserves 1-to-1 byte mapping of mojibake)
                # Then decode using utf-8 to interpretation
                content = content.encode('latin-1').decode('utf-8')
                print("Encoding repair successful.")
            except Exception as e:
                print(f"Encoding repair failed: {e}")
                
    else:
        print(f"Downloading from {url}...")
        try:
            # Try with verification first
            response = requests.get(url)
            # Check encoding if headers are wrong
            response.encoding = 'utf-8'
            response.raise_for_status()
            content = response.text
        except Exception as e:
            print(f"Standard download failed: {e}")
            print("Retrying with SSL verification disabled...")
            try:
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                response = requests.get(url, verify=False)
                response.encoding = 'utf-8'
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
    
    # Normalize valid haplogroups (original, and stripped prefixes)
    # E.g. "R-FT409028" -> "FT409028"
    valid_ids = set()
    for vid in ({target_id} | descendants):
        valid_ids.add(vid)
        if '-' in vid:
            valid_ids.add(vid.split('-')[-1])
            
    # print(f"DEBUG: Valid IDs for matching: {len(valid_ids)}") # Too verbose if big tree
    
    # ... (rest of parsing logic, utilizing valid_ids checks)
    # Re-implementing the matching loop part slightly to use valid_ids
    
    try:
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
            
            # Helper to check match
            def check_val(val):
                if not val: return False
                v = val.strip()
                if v in valid_ids: return True
                # Maybe check if v endswith any valid suffix?
                # Risk of false positives (e.g. '28' matches 'FT28'). strict equality against set is better.
                return False

            # Exact terminal match
            if check_val(terminal):
                is_match = True
            
            # Hierarchy match
            if not is_match:
                for col in h_cols:
                    if check_val(col):
                        is_match = True
                        break
            
            if is_match:
                matches.append(row)
                
    except csv.Error as e:
        # ... (Same fallback logic potentially needed, but standard DictReader is mostly fine now)
        # Implementing the fallback logic again briefly inside this function replacement?
        # The tool requires replacing the whole block if I change the function start.
        # I'll just keep the structure for csv.Error same as before but update matching logic inside fallback too.
        
        print(f"Standard CSV Parsing Error: {e}")
        print("Attempting fallback parsing (line-by-line split)...")
        
        lines = csv_text.splitlines()
        if not lines:
            return []
            
        header = lines[0].split('\t')
        try:
            idx_hap = header.index('Haplogroup')
            idx_gg = [i for i, h in enumerate(header) if h.startswith('Гг')]
        except ValueError:
            return []
            
        for line in lines[1:]:
            parts = line.split('\t')
            if len(parts) != len(header): continue
                
            row_dict = dict(zip(header, parts))
            
            terminal = row_dict.get('Haplogroup', '').strip()
            is_match = False
            if check_val(terminal):
                is_match = True
            
            if not is_match:
                for idx in idx_gg:
                    if idx < len(parts) and check_val(parts[idx]):
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
    # Priority: Фамилия -> Name -> Kit Number -> Unknown
    surname = record.get('Фамилия') or record.get('Name')
    if not surname or surname.strip() == '':
        surname = record.get('Kit Number') or 'Unknown'
        
    subethnos = record.get('Субэтнос', 'Unknown')
    location = record.get('Населенный пункт') or record.get('Lacation') or 'Unknown'
        
    history = record.get('История', '')
    
    # Metadata from JSON
    tmrca = branch_node.get('tmrca', 'Unknown')
    
    formatted_lineage = " >> ".join(lineage_path)
    
    # Docs section
    docs_section = ""
    if related_docs:
        docs_section = "## Справочная информация\n"
        seen_paths = set()
        for term, path in related_docs:
            if path not in seen_paths:
                docs_section += f"- [{os.path.basename(path)}]({path}) (Relates to {term})\n"
                seen_paths.add(path)
    
    template = f"""# {surname}

**Фамилия:** {record.get('Фамилия') or 'Not specified'}
**Имя:** {record.get('Name') or 'Not specified'}
**Kit Number:** {record.get('Kit Number') or 'Unknown'}
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
    
    match_source_branch = branch
    match_source_node = node
    
    if not matches:
        print("No matching records for target. Searching ancestry for closest matches...")
        # Traverse up lineage (reversed, starting from parent)
        # lineage is [Root, ..., Parent, Target]
        # We want to check Parent, then Grandparent...
        
        # We need the full tree access to get descendants for ancestors effectively?
        # Or just checking equality in columns?
        # If we check an ancestor 'A', we should match if row has 'A' in hierarchy or 'A' is haplogroup.
        # But we also want to include descendants of 'A' (which includes our Target).
        # We need a quick way to get descendants of ancestor.
        # Re-traversing tree each time is inefficient but safe for this script size.
        
        # Iterating reversed excluding the last element (Target)
        for ancestor_id in reversed(lineage[:-1]):
            print(f"Checking ancestor {ancestor_id}...")
            # We need to find the node for ancestor to get its descendants
            anc_node, _, anc_descendants = find_node_data(tree, ancestor_id)
            if not anc_node: continue
            
            anc_matches = parse_sheet_data(csv_text, ancestor_id, anc_descendants)
            if anc_matches:
                print(f"Found {len(anc_matches)} matches for ancestor {ancestor_id}")
                matches = anc_matches
                match_source_branch = ancestor_id
                match_source_node = anc_node
                break
                
        if not matches:
             print("No relevant ancestral matches found.")

    # 4. Find Documentation
    print("Searching for related documentation...")
    # Clean empty strings from lineage if any
    clean_lineage = [l for l in lineage if l]
    related_docs = find_related_docs(branch, clean_lineage)
    
    # 5. Generate Content
    full_content = ""
    if matches:
        # Add a note if using ancestor data
        if match_source_branch != branch:
            full_content += f"> [!NOTE]\n> Прямых образцов для **{branch}** не найдено. Показаны образцы для ближайшей ветви **{match_source_branch}**.\n\n"
            
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
