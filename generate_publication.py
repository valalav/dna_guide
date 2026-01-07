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

def find_siblings(tree, parent_id, target_id):
    """Find sibling nodes of the target."""
    parent_node, _, _ = find_node_data(tree, parent_id)
    if not parent_node or 'children' not in parent_node:
        return []
    
    siblings = []
    for child in parent_node['children']:
        cid = child.get('id', '')
        if cid and cid != target_id:
            siblings.append(cid)
    return siblings

def fetch_sheet_data(url, force_refresh=False):
    """Fetch data from Google Sheets TSV or local file."""
    local_file = "aadna_data.tsv"
    
    content = None
    if os.path.exists(local_file) and not force_refresh:
        print(f"Using local file: {local_file}")
        with open(local_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for mojibake... (kept from previous iter)
        if 'Ð' in content[:1000]:
             # ... repair logic ...
             try:
                content = content.encode('latin-1').decode('utf-8')
             except: pass
                
    else:
        if force_refresh:
             print("Force refresh requested.")
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

# ... (keep parse_sheet_data, find_related_docs, generate_markdown same or similar)
# We need to update main() to handle siblings

def main():
    parser = argparse.ArgumentParser(description='Generate publication from DNA data.')
    parser.add_argument('--branch', required=True, help='Target haplogroup branch (e.g., R-FT409028)')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--refresh', action='store_true', help='Force refresh of data from Google Sheets')
    
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
    
    # 2. Fetch Data
    csv_text = fetch_sheet_data(SHEET_URL, force_refresh=args.refresh)
    
    # 3. Filter Data (Target)
    print("Parsing and filtering CSV data...")
    matches = parse_sheet_data(csv_text, branch, descendants)
    print(f"Found {len(matches)} matching records for {branch}.")
    
    match_source_branch = branch
    match_source_node = node
    
    # If no matches, fallback to ancestors (User said "I added it", so we expect matches now, 
    # but keep fallback just in case or for context?)
    # User said: "also describe other samples from adjacent branches".
    
    # We will search for siblings regardless of whether matches found?
    # "при описании можешь описывать другие образцы из проекта которые +- в соседних ветках"
    # This implies usually adding them.
    
    neighbor_context = ""
    
    # Find Parent
    if len(lineage) >= 2:
        parent_id = lineage[-2]
        print(f"Checking siblings (children of {parent_id})...")
        siblings = find_siblings(tree, parent_id, branch)
        
        found_neighbors = []
        
        for sib_id in siblings:
            # finding descendants of sibling
            sib_node, _, sib_descendants = find_node_data(tree, sib_id)
            if not sib_node: continue
            
            sib_matches = parse_sheet_data(csv_text, sib_id, sib_descendants)
            if sib_matches:
                print(f"Found {len(sib_matches)} matches for sibling {sib_id}")
                for m in sib_matches:
                    m['_BranchContext'] = sib_id # Mark source
                    found_neighbors.append(m)
        
        if found_neighbors:
             neighbor_context = "\n## Соседние ветви (Context)\n"
             neighbor_context += f"В смежных ветвях (под {parent_id}) найдены следующие образцы:\n\n"
             # Group by branch?
             # Simple listing for now or use generate_markdown short version?
             for m in found_neighbors:
                 # Just a summary line
                 s_name = m.get('Фамилия') or m.get('Name') or m.get('Kit Number')
                 s_branch = m.get('_BranchContext')
                 neighbor_context += f"- **{s_branch}**: {s_name} ({m.get('Субэтнос', '')})\n"

    if not matches:
        print("No matching records for target. Searching ancestry for closest matches (Fallback)...")
        # ... (keep existing fallback logic if still needed, but user expects success)
        # Assuming user added data, we might not hit this. 
        # But if we do, we keep logic.
        for ancestor_id in reversed(lineage[:-1]):
            # ... ancestry fallback code ...
            anc_node, _, anc_descendants = find_node_data(tree, ancestor_id)
            if not anc_node: continue
            anc_matches = parse_sheet_data(csv_text, ancestor_id, anc_descendants)
            if anc_matches:
                 matches = anc_matches
                 match_source_branch = ancestor_id
                 match_source_node = anc_node
                 break

    # 4. Find Documentation
    # ...
    clean_lineage = [l for l in lineage if l]
    related_docs = find_related_docs(branch, clean_lineage)
    
    # 5. Generate Content
    full_content = ""
    # ...
    
    if matches:
        if match_source_branch != branch:
             full_content += f"> [!NOTE]\n> Прямых образцов для **{branch}** не найдено. Показаны образцы для ближайшей ветви **{match_source_branch}**.\n\n"
        
        for record in matches:
            full_content += generate_markdown(record, lineage, node, related_docs)
            full_content += "\n" # Spacing
            
        full_content += f"\n{neighbor_context}\n"
        full_content += "\n---\n\n"
            
    else:
        # Summary mode
        # ...
        full_content = f"""# Haplogroup {branch}
...
{neighbor_context}
...
"""

    output_file = args.output if args.output else f"publication_{branch}.md"
    # ... write ...
    # ...
    # Wait, I need to make sure I don't delete too much code with replace_file_content.
    # The snippet is getting large. I should target specific blocks.


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

import re

# ... existing imports ...

# (Assuming imports are at top, but I can't easily inject import at top with this single replace if I am targeting find_related_docs down below.
# I will use multi_replace to add import at top AND change function.)

def find_related_docs(target_id, lineage):
    """
    Find documentation files related to the branch or its ancestors.
    Uses strict regex matching (word boundaries / separators) to avoid partial matches
    e.g. 'F' matching 'FT9681'.
    """
    related_files = []
    
    # Search terms: specific branch ID, and parent IDs (reversed order for relevance)
    # Filter out empty strings
    search_terms = [t for t in ([target_id] + lineage[::-1]) if t]
    
    # cache regexes
    # We want to match: (start or separator) + term + (end or separator)
    # Separators: _ - . space
    term_regexes = []
    for term in search_terms:
        # Escape term just in case
        safe_term = re.escape(term)
        # Pattern: look for term surrounded by non-alphanumeric or boundaries
        # But commonly in filenames: 00_R_Overview.md -> matches 'R'
        # 03_FT9681.md -> matching 'F'? 'FT' starts with F.
        # We want strict token matching.
        # Let's define separators as [_\-\.]
        # usage: re.search(pattern, filename, re.IGNORECASE)
        pattern = r'(?:^|[\._\-])' + safe_term + r'(?:$|[\._\-])'
        term_regexes.append((term, re.compile(pattern, re.IGNORECASE)))
    
    # We explicitly look into 10_Haplogroups
    # Walk directory
    excluded_docs = ["00_R_Overview.md"]
    
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file in excluded_docs:
                continue
                
            if file.endswith(".md"):
                # Check if filename contains any of the search terms strings strictly
                for term, regex in term_regexes:
                    if regex.search(file):
                        path = os.path.join(root, file)
                        related_files.append((term, path))
                        break # Found a match for this file
    
    return related_files
    
def generate_branch_report(branch_name, records, lineage_path, branch_node, related_docs, neighbor_context="", ancestor_note=""):
    """Generate consolidated markdown content for the branch."""
    
    # Metadata from JSON
    tmrca = branch_node.get('tmrca', 'Unknown')
    formatted_lineage = " > ".join(lineage_path)
    
    # Docs section
    docs_section = "## Справочная информация\n\n"
    
    # 1. Dynamic Haplogroup Refs
    if related_docs:
        docs_section += "### Y-ДНК (Ветки)\n"
        seen_paths = set()
        for term, path in related_docs:
            if path not in seen_paths:
                docs_section += f"- [{os.path.basename(path)}]({path}) (Relates to {term})\n"
                seen_paths.add(path)
        docs_section += "\n"
                
    # 2. Standard Project Refs
    docs_section += "### Аутосомный портрет\n"
    docs_section += "- [01_Autosomal_Guide.md](05_Autosomal\\01_Autosomal_Guide.md) (Справочник по аутосомам)\n\n"
    
    docs_section += "### Митохондриальная ДНК\n"
    docs_section += "- [02_mtDNA_Guide.md](04_Women\\02_mtDNA_Guide.md) (Справочник по mtDNA)\n\n"
    
    docs_section += "### Древняя ДНК\n"
    docs_section += "- [03_Ancient_DNA_Table.md](00_General\\03_Ancient_DNA_Table.md) (Таблица древних образцов)\n"
    
    # History - Consolidate unique histories
    unique_histories = []
    seen_hist = set()
    for rec in records:
        h = rec.get('История', '').strip()
        if h and h not in seen_hist:
            unique_histories.append(h)
            seen_hist.add(h)
    
    history_section = ""
    if unique_histories:
        history_section = "## История\n" + "\n\n".join(unique_histories) + "\n"

    # Samples Table
    samples_section = ""
    if records:
        samples_section = "## Список представителей\n\n"
        samples_section += "| Фамилия | Имя | Kit | Субэтнос | Населенный пункт |\n"
        samples_section += "|---|---|---|---|---|\n"
        
        for rec in records:
            surname = rec.get('Фамилия') or ''
            name = rec.get('Name') or ''
            kit = rec.get('Kit Number') or ''
            subethnos = rec.get('Субэтнос') or ''
            loc = rec.get('Населенный пункт') or rec.get('Lacation') or ''
            
            # Clean pipes for Markdown table safety
            safe_cols = [c.replace('|', '/') for c in [surname, name, kit, subethnos, loc]]
            samples_section += f"| {safe_cols[0]} | {safe_cols[1]} | {safe_cols[2]} | {safe_cols[3]} | {safe_cols[4]} |\n"
    else:
        samples_section = "## Образцы\nВ текущей базе данных образцов для этой ветки не найдено.\n\n"

    # External Links (Move above samples)
    links_section = f"""## Внешние ссылки
- [YFull Tree](https://www.yfull.com/tree/{branch_node.get('id', '')}/)
- [Проект AADNA](https://aadna.ru/)"""

    # User explicitly requests these fields to be present at the top, even if empty/template
    # "Фамилия:", "Kit Number:", "Субэтнос:", "Населенный пункт:"
    
    template = f"""{ancestor_note}# Гаплогруппа {branch_name}

**Фамилия:** 
**Kit Number:** 
**Субэтнос:** 
**Населенный пункт:** 

**Возраст ветки (TMRCA):** {tmrca} лет
**Путь:** {formatted_lineage}

{history_section}

{docs_section}

{neighbor_context}

{links_section}

{samples_section}
"""
    return template
    
    # 1. Dynamic Haplogroup Refs
    if related_docs:
        docs_section += "### Y-ДНК (Ветки)\n"
        seen_paths = set()
        for term, path in related_docs:
            if path not in seen_paths:
                docs_section += f"- [{os.path.basename(path)}]({path}) (Relates to {term})\n"
                seen_paths.add(path)
        docs_section += "\n"
                
    # 2. Standard Project Refs
    docs_section += "### Аутосомный портрет\n"
    docs_section += "- [01_Autosomal_Guide.md](05_Autosomal\\01_Autosomal_Guide.md) (Справочник по аутосомам)\n\n"
    
    docs_section += "### Митохондриальная ДНК\n"
    docs_section += "- [02_mtDNA_Guide.md](04_Women\\02_mtDNA_Guide.md) (Справочник по mtDNA)\n\n"
    
    docs_section += "### Древняя ДНК\n"
    docs_section += "- [03_Ancient_DNA_Table.md](00_General\\03_Ancient_DNA_Table.md) (Таблица древних образцов)\n"
    
    # History - Consolidate unique histories
    unique_histories = []
    seen_hist = set()
    for rec in records:
        h = rec.get('История', '').strip()
        if h and h not in seen_hist:
            unique_histories.append(h)
            seen_hist.add(h)
    
    history_section = ""
    if unique_histories:
        history_section = "## История\n" + "\n\n".join(unique_histories) + "\n"

    # Samples Table
    samples_section = ""
    if records:
        samples_section = "## Список представителей\n\n"
        samples_section += "| Фамилия | Имя | Kit | Субэтнос | Населенный пункт |\n"
        samples_section += "|---|---|---|---|---|\n"
        
        for rec in records:
            surname = rec.get('Фамилия') or ''
            name = rec.get('Name') or ''
            kit = rec.get('Kit Number') or ''
            subethnos = rec.get('Субэтнос') or ''
            loc = rec.get('Населенный пункт') or rec.get('Lacation') or ''
            
            # Clean pipes for Markdown table safety
            safe_cols = [c.replace('|', '/') for c in [surname, name, kit, subethnos, loc]]
            samples_section += f"| {safe_cols[0]} | {safe_cols[1]} | {safe_cols[2]} | {safe_cols[3]} | {safe_cols[4]} |\n"
    else:
        samples_section = "## Образцы\nВ текущей базе данных образцов для этой ветки не найдено.\n\n"


    template = f"""{ancestor_note}# Гаплогруппа {branch_name}

**Возраст ветки (TMRCA):** {tmrca} лет
**Путь:** {formatted_lineage}

{history_section}

{docs_section}

{samples_section}

{neighbor_context}

## Внешние ссылки
- [YFull Tree](https://www.yfull.com/tree/{branch_node.get('id', '')}/)
- [Проект AADNA](https://aadna.ru/)
"""
    return template


def main():
    parser = argparse.ArgumentParser(description='Generate publication from DNA data.')
    parser.add_argument('--branch', required=True, help='Target haplogroup branch (e.g., R-FT409028)')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--refresh', action='store_true', help='Force refresh of data from Google Sheets')
    
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
    
    # 2. Fetch Data
    csv_text = fetch_sheet_data(SHEET_URL, force_refresh=args.refresh)
    
    # 3. Filter Data (Target)
    print("Parsing and filtering CSV data...")
    matches = parse_sheet_data(csv_text, branch, descendants)
    print(f"Found {len(matches)} matching records for {branch}.")
    
    match_source_branch = branch
    match_source_node = node
    
    neighbor_context = ""
    
    # Find Parent and Neighbors (Context)
    if len(lineage) >= 2:
        parent_id = lineage[-2]
        print(f"Checking siblings (children of {parent_id})...")
        siblings = find_siblings(tree, parent_id, branch)
        
        found_neighbors = []
        
        for sib_id in siblings:
            # finding descendants of sibling
            sib_node, _, sib_descendants = find_node_data(tree, sib_id)
            if not sib_node: continue
            
            sib_matches = parse_sheet_data(csv_text, sib_id, sib_descendants)
            if sib_matches:
                print(f"Found {len(sib_matches)} matches for sibling {sib_id}")
                for m in sib_matches:
                    m['_BranchContext'] = sib_id # Mark source
                    found_neighbors.append(m)
        
        if found_neighbors:
             neighbor_context = "\n## Соседние ветви (Context)\n"
             neighbor_context += f"В смежных ветвях (под {parent_id}) найдены следующие образцы:\n\n"
             for m in found_neighbors:
                 # Just a summary line
                 s_name = m.get('Фамилия') or m.get('Name') or m.get('Kit Number') or ''
                 s_branch = m.get('_BranchContext') or ''
                 s_subethnos = m.get('Субэтнос') or ''
                 
                 # Format: - Branch: Name (Subethnos)
                 # Avoid empty parens
                 line = f"- **{s_branch}**: {s_name}"
                 if s_subethnos:
                     line += f" ({s_subethnos})"
                 neighbor_context += line + "\n"

    # Fallback to ancestors if no direct matches
    if not matches:
        print("No matching records for target. Searching ancestry for closest matches (Fallback)...")
        for ancestor_id in reversed(lineage[:-1]):
            print(f"Checking ancestor {ancestor_id}...")
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
    # Remove duplicates while preserving order
    clean_lineage_dedup = []
    seen = set()
    for l in clean_lineage:
        if l not in seen:
            clean_lineage_dedup.append(l)
            seen.add(l)
            
    related_docs = find_related_docs(branch, clean_lineage_dedup)
    
    # 5. Generate Content
    full_content = ""
    ancestor_note = ""
    if matches:
        # Add a note if using ancestor data
        if match_source_branch != branch:
             ancestor_note = f"> [!NOTE]\n> Прямых образцов для **{branch}** не найдено. Показаны образцы для ближайшей ветви **{match_source_branch}**.\n\n"
        
        full_content = generate_branch_report(
            branch_name=branch, 
            records=matches, 
            lineage_path=lineage, 
            branch_node=node,
            related_docs=related_docs,
            neighbor_context=neighbor_context,
            ancestor_note=ancestor_note
        )
            
    else:
        print("No matching records found policy. Generating summary publication.")
        full_content = generate_branch_report(
            branch_name=branch, 
            records=[], 
            lineage_path=lineage, 
            branch_node=node,
            related_docs=related_docs,
            neighbor_context=neighbor_context
        )

    output_file = args.output if args.output else f"publication_{branch}.md"
    write_path = os.path.abspath(output_file)
    print(f"Writing to: {write_path}")
    
    try:
        with open(write_path, "w", encoding='utf-8') as f:
            f.write(full_content)
        print(f"Successfully generated {os.path.basename(output_file)}")
        if os.path.exists(write_path):
            print("File verification: Exists.")
        else:
            print("File verification: FAILED (path not found after write)")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    main()
