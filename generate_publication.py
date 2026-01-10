import json
import csv
import argparse
import requests
import io
import os
import sys
import glob
import re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Configuration
TREE_JSON_PATH = "current_tree.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTp8VNm5yS63RiflBpMY4b8d4RBTPecjU_RrC10EDcgSitcQxRtt1QbeN67g8bYOyqB088GLOTHIG5g/pub?gid=90746110&single=true&output=tsv"
DOCS_DIR = "10_Haplogroups"
MAX_BATCH_SIZE = 50
LOG_FILE = "publication_log.csv"

def load_tree(path):
    """Load the phylogenetic tree from JSON."""
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        sys.exit(1)
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

def find_node_by_synonym(tree, synonym):
    """
    Find a node where the 'snps' field contains the synonym.
    Returns: (node_object, lineage_path_list, set_of_descendant_ids)
    """
    synonym_clean = synonym.strip().upper().replace('J-', '').replace('R-', '').replace('G-', '') # Simplistic prefix removal for search
    
    found_node = None
    lineage = []
    descendants = set()
    
    def traverse(current_node, current_path):
        nonlocal found_node, lineage
        node_id = current_node.get('id', '')
        new_path = current_path + [node_id]
        
        # Check SNPs field
        snps = current_node.get('snps', '').upper()
        # Handle slash-separated synonyms (e.g. "Z2165/CTS1192/PF5413")
        snp_list = []
        for group in snps.split(','):
            for alias in group.split('/'):
                snp_list.append(alias.strip())
        
        # Check if synonym matches ID (case insensitive) or any SNP
        if node_id.upper() == synonym.upper() or synonym_clean in snp_list:
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
            try:
                if 'Ð' in content[:1000]:
                    content = content.encode('latin-1').decode('utf-8')
            except: pass
    else:
        print(f"Downloading from {url}...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        try:
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            response.raise_for_status()
            content = response.text
        except Exception as e:
            print(f"Download failed: {e}. Retrying insecure...")
            try:
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                response = requests.get(url, headers=headers, verify=False)
                response.encoding = 'utf-8'
                response.raise_for_status()
                content = response.text
            except Exception as e2:
                print(f"Download failed: {e2}")
                sys.exit(1)
        if content:
            # OPTIMIZATION: Process content immediately
            try:
                lines = content.splitlines()
                if lines:
                    headers = lines[0].split('\t')
                    MAX_COLS = 23
                    if len(headers) > MAX_COLS: headers = headers[:MAX_COLS]
                    
                    haplo_idx = -1
                    for i, h in enumerate(headers):
                        if 'haplogroup' in h.lower(): 
                            haplo_idx = i
                            break
                    
                    processed_lines = ['\t'.join(headers)]
                    
                    for line in lines[1:]:
                        if not line.strip(): continue
                        cols = line.split('\t')
                        if len(cols) > MAX_COLS: cols = cols[:MAX_COLS]
                        
                        # Filter empty haplogroup
                        if haplo_idx != -1 and haplo_idx < len(cols):
                            if cols[haplo_idx].strip():
                                processed_lines.append('\t'.join(cols))
                        else:
                            # Keep if we can't filter
                            processed_lines.append('\t'.join(cols))
                            
                    content = '\n'.join(processed_lines)
            except Exception as e:
                print(f"Optimization warning: {e}")

            with open(local_file, 'w', encoding='utf-8') as f:
                f.write(content)
    return content

def parse_sheet_data(csv_text, target_id, descendants):
    """Parse TSV data matching target or descendants. Optimized."""
    matches = []
    valid_ids = set()
    for vid in ({target_id} | descendants):
        valid_ids.add(vid)
        if '-' in vid: valid_ids.add(vid.split('-')[-1])
            
    try:
        f = io.StringIO(csv_text)
        reader = csv.reader(f, delimiter='\t')
        try:
            headers = next(reader)
        except StopIteration:
            return []
            
        MAX_COLS = 23
        if len(headers) > MAX_COLS: headers = headers[:MAX_COLS]
            
        haplo_idx = -1
        for i, h in enumerate(headers):
            if 'haplogroup' in h.lower(): haplo_idx = i
            elif 'гг' in h.lower(): pass

        def check_val(val):
            return val and val.strip() in valid_ids

        for row in reader:
            if not row: continue
            
            # LOGIC FIX: Don't skip just because 'Haplogroup' column is empty. 
            # Check if ANY relevant column has data.
            has_data = False
            
            # Check Haplogroup column first
            if haplo_idx != -1 and len(row) > haplo_idx and row[haplo_idx].strip():
                has_data = True
            
            # Also check Gg columns if primary is empty
            if not has_data:
                for i, h in enumerate(headers):
                    if i >= len(row): continue
                    if 'гг' in h.lower() or 'yfull' in h.lower() or 'ftdna' in h.lower():
                        if row[i].strip():
                            has_data = True
                            break
            
            if not has_data: continue

            if len(row) > MAX_COLS: row = row[:MAX_COLS]
            
            record = {}
            for i, val in enumerate(row):
                if i < len(headers): record[headers[i]] = val
            
            is_match = False
            term_val = record.get('Haplogroup', '')
            if check_val(term_val): is_match = True
            
            if not is_match:
                for col_name in ['Гг1', 'Гг2', 'Гг3', 'Гг4', 'Гг5', 'Yfull', 'Yfull_tree', 'FTDNA HG']:
                    val = record.get(col_name)
                    if val and check_val(val):
                        is_match = True
                        break
            if is_match:
                matches.append(record)

    except Exception:
        pass
    return matches
    return matches

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
        # Make hyphens match both hyphens and underscores in filenames
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

    # Shadowing Logic - keep most specific match (highest lineage_index)
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

def log_publication(branch, filename, status):
    """Log publication event to CSV."""
    file_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Branch', 'Filename', 'Date', 'Status'])
        writer.writerow([branch, filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status])

def generate_post_context(branch_name, records, lineage_path, branch_node, related_docs, tree, neighbor_context="", ancestor_note="", canonical_id=None):
    """Prepare context for Jinja2 template."""
    tmrca = branch_node.get('tmrca', 'N/A')
    
    # Use canonical_id if provided, otherwise fallback to branch_node id
    clean_branch_id = canonical_id if canonical_id else branch_node.get('id', '')
    
    # Simple lineage path
    formatted_lineage = " > ".join(lineage_path)
    
    # Build TMRCA index from tree for fast lookup (instead of calling find_node_data in loop)
    def build_tmrca_index(node, idx=None):
        if idx is None:
            idx = {}
        nid = node.get('id', '')
        if nid:
            idx[nid] = node.get('tmrca', 0)
        for child in node.get('children', []):
            build_tmrca_index(child, idx)
        return idx
    
    tmrca_index = {}
    if isinstance(tree, list):
        for root in tree:
            build_tmrca_index(root, tmrca_index)
    else:
        build_tmrca_index(tree, tmrca_index)
    
    # Build lineage with TMRCA for each branch
    lineage_with_tmrca = []
    lineage_timeline_raw = []
    total_items = len(lineage_path)
    major_index = -1
    major_tmrca = 0
    current_tmrca = 0
    
    for i, branch_id in enumerate(lineage_path):
        branch_tmrca = 0
        try:
            branch_tmrca = int(tmrca_index.get(branch_id, 0))
        except:
            pass
        
        is_current = (i == total_items - 1)
        is_major = len(branch_id) == 1 and branch_id.isalpha()
        
        if is_major and major_index == -1:
            major_index = i
            major_tmrca = branch_tmrca
        if is_current:
            current_tmrca = branch_tmrca
        
        tmrca_formatted = f"{branch_tmrca:,}".replace(',', ' ') if branch_tmrca else ''
        if branch_tmrca:
            lineage_with_tmrca.append(f"{branch_id} ({branch_tmrca})")
        else:
            lineage_with_tmrca.append(branch_id)
        
        lineage_timeline_raw.append({
            'id': branch_id,
            'tmrca': branch_tmrca,
            'tmrca_formatted': tmrca_formatted,
            'is_current': is_current,
            'is_major': is_major,
            'index': i
        })
    
    # Calculate positions based on TMRCA from major haplogroup
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
    
    formatted_lineage_tmrca = " > ".join(lineage_with_tmrca)
    
    # Docs preparation
    y_dna_docs = []
    for d in related_docs:
        if "autosomal" in d['filename'].lower() or "mt" in d['filename'].lower():
             continue
        y_dna_docs.append({
            'filename': d['filename'],
            'path': d['path'].replace('\\\\', '/'), # Ensure web safe paths
            'id': d['id']
        })
        
    # History consolidation
    unique_histories = []
    seen_hist = set()
    for rec in records:
        h = rec.get('История', '').strip()
        if h and h not in seen_hist:
            unique_histories.append(h)
            seen_hist.add(h)
    history_section = "\\n\\n".join(unique_histories)

    # Header Logic
    header = {
        'surname': '', 'kit': '', 'subethnos': '', 'location': ''
    }
    if len(records) == 1:
        r = records[0]
        header['surname'] = r.get('Фамилия') or r.get('Name') or ''
        header['kit'] = r.get('Kit Number') or ''
        header['subethnos'] = r.get('Субэтнос') or ''
        header['location'] = r.get('Населенный пункт') or r.get('Lacation') or ''

    # Records cleaning for template
    cleaned_records = []
    if len(records) > 0:
        for rec in records:
            cleaned_records.append({
                'surname': (rec.get('Фамилия') or '').replace('|', '/'),
                'name': (rec.get('Name') or '').replace('|', '/'),
                'kit': (rec.get('Kit Number') or '').replace('|', '/'),
                'subethnos': (rec.get('Субэтнос') or '').replace('|', '/'),
                'location': (rec.get('Населенный пункт') or rec.get('Lacation') or '').replace('|', '/')
            })

    return {
        'ancestor_note': ancestor_note,
        'branch_name': branch_name,
        'branch_id': clean_branch_id,
        'canonical_id': clean_branch_id,
        'header': header,
        'tmrca': tmrca,
        'formatted_lineage': formatted_lineage,
        'formatted_lineage_tmrca': formatted_lineage_tmrca,
        'lineage_timeline': lineage_timeline,
        'history_section': history_section,
        'y_dna_docs': y_dna_docs,
        'neighbor_context': neighbor_context,
        'records': cleaned_records,
        'records_count': len(records)
    }

def process_branch(branch, tree, csv_text, args, env):
    """Process a single branch and generate publication."""
    print(f"Processing branch: {branch}")
    
    # 1. Try finding by ID first
    node, lineage, descendants = find_node_data(tree, branch)
    
    canonical_id = None
    
    # 2. If not found, try synonym lookup
    if not node:
        print(f"Direct match for '{branch}' not found. Checking synonyms...")
        node, lineage, descendants = find_node_by_synonym(tree, branch)
        if node:
            canonical_id = node.get('id', '')
            print(f"Found synonym! Resolved '{branch}' -> Canonical ID '{canonical_id}'")
    else:
        canonical_id = node.get('id', '')
    
    if not node:
        print(f"Error: Branch {branch} not found (neither as ID nor synonym).")
        return False

    # FIX: Collect all aliases (Canonical + Synonyms) to ensure we match records
    # regardless of which name variance is used in the CSV.
    all_aliases = set()
    if node:
        # 1. Add Canonical ID
        cid = node.get('id', '')
        if cid: all_aliases.add(cid)
        
        # 2. Add Synonyms from SNPs field
        snps_str = node.get('snps', '')
        if snps_str:
            for group in snps_str.split(','):
                for alias in group.split('/'):
                    clean_alias = alias.strip()
                    if clean_alias:
                        all_aliases.add(clean_alias)
                        
    # 3. Add the requested branch name itself (just in case)
    all_aliases.add(branch)
    
    # Update descendants set to include all aliases (parse_sheet_data checks {target} | descendants)
    descendants.update(all_aliases)

    matches = parse_sheet_data(csv_text, branch, descendants)
    match_source_branch = branch
    
    neighbor_context = ""
    # Neighbors logic (simplified for brevity, reuse of original logic flow)
    if len(lineage) >= 2:
        parent_id = lineage[-2]
        siblings = find_siblings(tree, parent_id, canonical_id if canonical_id else branch)
        found_neighbors = []
        for sib_id in siblings:
            sib_node, _, sib_descendants = find_node_data(tree, sib_id)
            if not sib_node: continue
            sib_matches = parse_sheet_data(csv_text, sib_id, sib_descendants)
            if sib_matches:
                for m in sib_matches:
                    m['_BranchContext'] = sib_id
                    found_neighbors.append(m)
        if found_neighbors:
             neighbor_context = "\n<p>В смежных ветвях:</p>\n<ul>\n"
             for m in found_neighbors:
                 s_name = m.get('Фамилия') or m.get('Name') or m.get('Kit Number') or ''
                 s_branch = m.get('_BranchContext') or ''
                 neighbor_context += f"<li><strong>{s_branch}</strong>: {s_name}</li>\n"
             neighbor_context += "</ul>\n"
 
    # Fallback
    if not matches:
        print("Searching ancestry for fallback...")
        for ancestor_id in reversed(lineage[:-1]):
            anc_node, _, anc_descendants = find_node_data(tree, ancestor_id)
            anc_matches = parse_sheet_data(csv_text, ancestor_id, anc_descendants)
            if anc_matches:
                matches = anc_matches
                match_source_branch = ancestor_id
                break
    
    clean_lineage = list(dict.fromkeys([l for l in lineage if l])) # Dedup preservation
    related_docs = find_related_docs(branch, clean_lineage)
    
    ancestor_note = ""
    if match_source_branch != branch:
        ancestor_note = f"<div class='note'><strong>Примечание:</strong> Прямых образцов для <strong>{branch}</strong> не найдено. Показаны образцы для ближайшей ветви <strong>{match_source_branch}</strong>.</div>\n"

    context = generate_post_context(
        branch_name=branch, # Keep requested name for display
        records=matches,
        lineage_path=lineage,
        branch_node=node,
        related_docs=related_docs,
        tree=tree,
        neighbor_context=neighbor_context,
        ancestor_note=ancestor_note,
        canonical_id=canonical_id # Pass canonical ID for URL
    )


    try:
        template = env.get_template('post_template.j2')
        output_content = template.render(context)
    except Exception as e:
        print(f"Template rendering failed: {e}")
        return False
    except Exception as e:
        print(f"Template rendering failed: {e}")
        return False

    output_file = f"publication_{branch}.md"
    if args.output and not args.batch_file:
        output_file = args.output
        
    try:
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(output_content)
        print(f"Generated: {output_file}")
        log_publication(branch, output_file, "SUCCESS")
        return True
    except Exception as e:
        print(f"Write failed: {e}")
        log_publication(branch, output_file, f"FAILED: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate publication from DNA data.')
    parser.add_argument('--branch', help='Target haplogroup branch (e.g., R-FT409028)')
    parser.add_argument('--output', help='Output file path (single mode)')
    parser.add_argument('--refresh', action='store_true', help='Force refresh of data')
    parser.add_argument('--batch-file', help='Path to file containing list of branches (one per line)')
    
    args = parser.parse_args()
    
    if not args.branch and not args.batch_file:
        print("Error: Must provide --branch or --batch-file")
        sys.exit(1)

    # Init Template Env
    TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "publication", "templates")
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    
    tree = load_tree(TREE_JSON_PATH)
    csv_text = fetch_sheet_data(SHEET_URL, force_refresh=args.refresh)

    if args.branch:
        process_branch(args.branch, tree, csv_text, args, env)
        
    elif args.batch_file:
        if not os.path.exists(args.batch_file):
            print(f"Batch file not found: {args.batch_file}")
            sys.exit(1)
            
        with open(args.batch_file, 'r', encoding='utf-8') as f:
            branches = [line.strip() for line in f if line.strip()]
            
        print(f"Batch mode: Processing {len(branches)} branches (Max {MAX_BATCH_SIZE})")
        
        count = 0
        for br in branches:
            if count >= MAX_BATCH_SIZE:
                print(f"Batch limit {MAX_BATCH_SIZE} reached. Stopping.")
                break
            success = process_branch(br, tree, csv_text, args, env)
            if success:
                count += 1
                
if __name__ == "__main__":
    main()