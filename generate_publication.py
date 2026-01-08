import json
import csv
import argparse
import requests
import io
import os
import sys
import glob
import re

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

def parse_sheet_data(csv_text, target_id, descendants):
    """
    Parse TSV data and find rows matching the target branch OR its descendants.
    Robustly handles newlines in fields.
    OPTIMIZATION: Reads only first 23 columns, filters empty haplogroups.
    """
    matches = []
    
    # Normalize valid haplogroups (original, and stripped prefixes)
    # E.g. "R-FT409028" -> "FT409028"
    valid_ids = set()
    for vid in ({target_id} | descendants):
        valid_ids.add(vid)
        if '-' in vid:
            valid_ids.add(vid.split('-')[-1])
            
    try:
        f = io.StringIO(csv_text)
        # Using strict reader first
        reader = csv.reader(f, delimiter='\t')
        
        try:
            headers = next(reader)
        except StopIteration:
            return []
            
        # 1. OPTIMIZATION: SLICE COLUMNS (First 23)
        MAX_COLS = 23
        if len(headers) > MAX_COLS:
            headers = headers[:MAX_COLS]
            
        # Identify relevant columns
        haplo_idx = -1
        gg_indices = []
        for i, h in enumerate(headers):
            h_low = h.lower()
            if 'haplogroup' in h_low:
                haplo_idx = i
            elif 'гг' in h_low:
                gg_indices.append(i)

        # Helper to check match
        def check_val(val):
            if not val: return False
            v = val.strip()
            if v in valid_ids: return True
            return False

        for row in reader:
            if not row: continue
            
            # 2. OPTIMIZATION: FILTER EMPTY HAPLOGROUP
            if haplo_idx != -1:
                if len(row) > haplo_idx:
                    if not row[haplo_idx].strip():
                        continue 
                else:
                    continue

            # Slice row data
            if len(row) > MAX_COLS:
                row = row[:MAX_COLS]
            
            # Convert to dict
            record = {}
            for i, val in enumerate(row):
                 if i < len(headers):
                     record[headers[i]] = val
            
            # Check Match
            is_match = False
            
            # Check Terminal
            term_val = record.get('Haplogroup', '')
            if check_val(term_val):
                is_match = True
            
            # Check Hierarchy
            if not is_match:
                for col_name in ['Гг1', 'Гг2', 'Гг3', 'Гг4', 'Гг5']:
                    val = record.get(col_name)
                    if val and check_val(val):
                        is_match = True
                        break
            
            if is_match:
                matches.append(record)

    except (csv.Error, Exception) as e:
        # Fallback for "new-line character seen in unquoted field" etc.
        # print(f"CSV Parsing Error ({e}). Switching to manual fallback parsing.")
        
        lines = csv_text.splitlines()
        if not lines: return []
        
        # Manual Header Parsing
        headers = lines[0].split('\t')
        MAX_COLS = 23
        if len(headers) > MAX_COLS:
            headers = headers[:MAX_COLS]
            
        haplo_idx = -1
        gg_indices = []
        for i, h in enumerate(headers):
            h_low = h.lower()
            if 'haplogroup' in h_low:
                haplo_idx = i
            elif 'гг' in h_low:
                gg_indices.append(i)
                
        def check_val(val):
            if not val: return False
            v = val.strip()
            if v in valid_ids: return True
            return False

        for line in lines[1:]:
            if not line: continue
            row = line.split('\t')
            
            # Filter Empty Haplogroup
            if haplo_idx != -1:
                if len(row) > haplo_idx:
                    if not row[haplo_idx].strip():
                        continue
                else:
                    continue
            
            # Slice
            if len(row) > MAX_COLS:
                row = row[:MAX_COLS]
                
            # Dict
            record = {}
            for i, val in enumerate(row):
                if i < len(headers):
                    record[headers[i]] = val
            
            # Match Logic
            is_match = False
            term_val = record.get('Haplogroup', '')
            if check_val(term_val):
                is_match = True
            
            if not is_match:
                for col_name in ['Гг1', 'Гг2', 'Гг3', 'Гг4', 'Гг5']:
                    val = record.get(col_name)
                    if val and check_val(val):
                        is_match = True
                        break
            
            if is_match:
                matches.append(record)
        
    return matches

def find_related_docs(target_id, lineage):
    """
    Find documentation files related to the branch or its ancestors.
    Uses strict regex matching.
    Implements SHADOWING: If a specific deep branch doc exists (e.g. R1b), 
    suppress generic top-level docs (e.g. R Overview).
    """
    docs = []
    all_md_files = []
    
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                all_md_files.append(os.path.join(root, file))
    
    raw_matches = []
    
    # 1. Collect all raw matches
    for item in lineage:
        if not item: continue
        # Normalize item for regex (escape + word boundaries)
        esc_item = re.escape(item)
        
        # Pattern: exact match of the haplogroup ID in the filename
        # e.g. "R1b" in "01_R1b.md" or "R1b_L23..."
        # But we must avoid "R" matching "R1b" (handled by boundaries usually, or specific checks)
        # To be safe for "R", we ensure it's distinct.
        
        pattern = re.compile(fr'(^|[\/\\_\-\s\.])({esc_item})($|[\/\\_\-\s\.])', re.IGNORECASE)
        
        for file_path in all_md_files:
            filename = os.path.basename(file_path)
            if pattern.search(filename):
                raw_matches.append({
                    'id': item,
                    'path': file_path,
                    'filename': filename,
                    'lineage_index': lineage.index(item)
                })

    # 2. Filter / Shadowing Selection
    # Logic: Group matches by ID.
    # If we have matches for 'R1b' (or deeper), and also for 'R', we want to DROP 'R'.
    
    # Identify which lineage depths are covered.
    covered_indices = {m['lineage_index'] for m in raw_matches}
    
    final_docs = []
    seen_paths = set()
    
    # Sort matches by lineage index (deepest first? No, we iterate all)
    # Actually, we want to KEEP the most specific ones.
    
    # Define "Top Level" IDs that are prone to being redundant
    # (Single letters usually: R, G, J, I, E, N, Q, C...)
    # Logic: If we have a match at index X, and there is a match at index Y (where Y < X),
    # AND index Y corresponds to a "Basic/Overview" level, we might drop Y.
    
    # User Rule: "Separate R1a and R1b. For R1b - remove R. For R1a - remove R."
    
    matches_by_path = {m['path']: m for m in raw_matches}
    unique_matches = list(matches_by_path.values())
    
    # Check if we have specific docs
    max_depth_found = -1
    if covered_indices:
        max_depth_found = max(covered_indices)
        
    # Heuristic: If we have documentation for a node at index X, 
    # suppress documentation for nodes at index < X-1 (Grandparents) or even Parents if they are "Overview".
    # User specifically hates "R Overview" when "R1b" is there. Lineage: R -> R1 -> R1b. 
    # indices: R=0, R1=1, R1b=2 (roughly).
    
    for m in unique_matches:
        is_redundant = False
        
        # Shadowing Rule 1: 'Overview' suppression
        # If the filename contains "Overview" (e.g. 00_R_Overview.md), 
        # AND we have any OTHER doc that is NOT this one and is "deeper" or specific.
        if "overview" in m['filename'].lower():
            # Check if we have more specific docs (not overview, deeper index)
            # or just ANY other specific doc for a sub-branch.
            for other in unique_matches:
                if other['path'] == m['path']: continue
                if other['lineage_index'] > m['lineage_index']:
                    is_redundant = True
                    break
                    
        # Shadowing Rule 2: Single Letter Roots (e.g. "R") suppression
        # If this doc matches a single-letter ID (e.g. "R"), and we have deeper docs.
        if len(m['id']) == 1 and m['id'].isalpha():
             for other in unique_matches:
                if other['path'] == m['path']: continue
                if other['lineage_index'] > m['lineage_index']:
                    is_redundant = True
                    break

        if not is_redundant:
            if m['path'] not in seen_paths:
                final_docs.append(m)
                seen_paths.add(m['path'])

    # Sort final docs by lineage usage (or alphabet? Lineage is better context)
    final_docs.sort(key=lambda x: x['lineage_index'])
    
    return final_docs

def generate_branch_report(branch_name, records, lineage_path, branch_node, related_docs, neighbor_context="", ancestor_note=""):
    """
    Generate consolidated markdown content for the branch.
    Includes Metadata, History, Documentation, External Links, Neighbor Context, and Sample List.
    """
    tmrca = branch_node.get('tmrca', 'N/A')
    
    # Formatting lineage: > A > B > C
    formatted_lineage = " > ".join(lineage_path)
    
    # Documentation Section
    docs_section = "## Справочная информация\n\n![Справочная информация](00_General/00_inf.md)\n\n"
    
    # Categorize docs
    y_dna_docs = []
    other_docs = []
    
    for d in related_docs:
        link = f"- [{d['filename']}]({d['path']}) (Relates to {d['id']})"
        # Simplistic categorization
        if "autosomal" in d['filename'].lower():
             pass # Handled by static text?
        elif "mt" in d['filename'].lower():
             pass 
        else:
             y_dna_docs.append(link)
             
    if y_dna_docs:
        docs_section += "### Y-ДНК (Ветки)\n" + "\n".join(y_dna_docs) + "\n\n"
        
    docs_section += "### Аутосомный портрет\n"
    docs_section += "- [01_Autosomal_Guide.md](05_Autosomal\\01_Autosomal_Guide.md) (Справочник по аутосомам)\n\n"

    docs_section += "### Митохондриальная ДНК\n"
    docs_section += "- [02_mtDNA_Guide.md](04_Women\\02_mtDNA_Guide.md) (Справочник по mtDNA)\n\n"
    
    # Ancient DNA REMOVED per user request

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

    # Conditional Logic for Header and Samples Table
    h_surname = ""
    h_kit = ""
    h_subethnos = ""
    h_location = ""
    samples_section = ""
    
    if len(records) == 1:
        # Single Record: Fill header, suppress table
        r = records[0]
        h_surname = r.get('Фамилия') or r.get('Name') or ''
        h_kit = r.get('Kit Number') or ''
        h_subethnos = r.get('Субэтнос') or ''
        h_location = r.get('Населенный пункт') or r.get('Lacation') or ''
        # samples_section remains empty
        
    elif len(records) > 1:
        # Multiple Records: Empty header, show table
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
        # No records
        samples_section = "## Образцы\nВ текущей базе данных образцов для этой ветки не найдено.\n\n"

    # External Links (Move above samples)
    links_section = f"""## Внешние ссылки
- [YFull Tree](https://www.yfull.com/tree/{branch_node.get('id', '')}/)
- [Проект AADNA](https://aadna.ru/)"""

    # User explicit request: NO double empty lines. Only single empty line between sections.
    
    template = f"""{ancestor_note}# Гаплогруппа {branch_name}

**Фамилия:** {h_surname}
**Kit Number:** {h_kit}
**Субэтнос:** {h_subethnos}
**Населенный пункт:** {h_location}

## Краткое резюме
<!-- Вставьте сюда краткое описание ветки и её значимости -->

![Общая инфо по WGS](00_General/00_wgs.md)

**Возраст ветки (TMRCA):** {tmrca} лет
**Путь:** {formatted_lineage}

[Как читать YFull — экскурсия по интерфейсу](https://github.com/valalav/dna_guide/blob/main/02_Practical/01_YFull_Guide.md)

{history_section}
{docs_section}
{neighbor_context}
{links_section}

{samples_section}"""
    
    # Post-processing to ensure exactly one empty line max
    # Replace 3 or more newlines with 2 newlines
    template = re.sub(r'\n{3,}', '\n\n', template)
    
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
    clean_lineage = [l for l in lineage if l]
    # Remove duplicates
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
