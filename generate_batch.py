import json
import csv
import os
import sys
import re
import io
import requests
from jinja2 import Environment, FileSystemLoader

# Configuration
TREE_JSON_PATH = "current_tree.json"
DOCS_DIR = "10_Haplogroups"
BATCH_FILE = "publications.csv"
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vReAnh5vjuv0DoamQN7ISaTrSZmh4FhhojxZdceKImRfFJ3LBSQaVMuw2f5hT3lvBVod2IXQSDmATAn/pub?gid=0&single=true&output=csv"

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

def publish_to_wordpress(local_file, title, slug, publish=True):
    """Upload file to server and create/update WordPress post."""
    import subprocess
    
    # Configuration
    SERVER_IP = "192.162.246.231"
    SERVER_USER = "root"
    SERVER_PASS = "4S7eBqQa55en"
    WP_PATH = "/var/www/html"
    PSCP_PATH = r"c:\_Data\Soft\Linux\PuTTY\pscp.exe"
    PLINK_PATH = r"c:\_Data\Soft\Linux\PuTTY\plink.exe"
    
    try:
        import base64
        
        # Step 1: Read file content and encode as base64
        print(f"    Uploading {local_file}...")
        with open(local_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Base64 encode the content for safe transfer
        b64_content = base64.b64encode(content.encode('utf-8')).decode('ascii')
        
        # Step 2: Upload via echo + base64 decode on server
        remote_file = f"/tmp/{os.path.basename(local_file)}"
        echo_cmd = f'echo "{b64_content}" | base64 -d > {remote_file}'
        ssh_cmd = [PLINK_PATH, "-ssh", f"{SERVER_USER}@{SERVER_IP}", "-pw", SERVER_PASS, "-batch", echo_cmd]
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"    Upload failed: {result.stderr}")
            return False
        
        # Step 3: Create WordPress post via WP-CLI
        post_status = "publish" if publish else "draft"
        
        # Base64 encode the title to safely pass Cyrillic through SSH
        b64_title = base64.b64encode(title.encode('utf-8')).decode('ascii')
        
        # Use LANG=en_US.UTF-8 and decode title from base64 on server
        wp_cmd = f'export LANG=en_US.UTF-8 && export LC_ALL=en_US.UTF-8 && TITLE=$(echo "{b64_title}" | base64 -d) && cat /tmp/{os.path.basename(local_file)} | wp post create - --post_title="$TITLE" --post_name="{slug}" --post_status={post_status} --post_type=post --path={WP_PATH} --allow-root --porcelain'
        
        print(f"    Creating WordPress post...")
        ssh_cmd = [PLINK_PATH, "-ssh", f"{SERVER_USER}@{SERVER_IP}", "-pw", SERVER_PASS, "-batch", wp_cmd]
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"    WP-CLI failed: {result.stderr}")
            return False
        
        post_id = result.stdout.strip()
        print(f"    Created post ID: {post_id}")
        
        # Step 3: Clear cache
        cache_cmd = f'wp transient delete --all --path={WP_PATH} --allow-root'
        subprocess.run([PLINK_PATH, "-ssh", f"{SERVER_USER}@{SERVER_IP}", "-pw", SERVER_PASS, "-batch", cache_cmd], 
                      capture_output=True, timeout=30)
        
        return post_id
        
    except subprocess.TimeoutExpired:
        print(f"    Timeout during publishing")
        return False
    except Exception as e:
        print(f"    Error: {e}")
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Batch generate and optionally publish posts.')
    parser.add_argument('--publish', action='store_true', help='Publish to WordPress after generation')
    parser.add_argument('--draft', action='store_true', help='Create as draft (not published)')
    parser.add_argument('--url', type=str, help='Google Sheets CSV URL (default: use built-in URL)')
    parser.add_argument('--local', action='store_true', help='Use local publications.csv instead of URL')
    args = parser.parse_args()
    
    # Determine data source
    if args.local:
        if not os.path.exists(BATCH_FILE):
            print(f"Error: {BATCH_FILE} not found.")
            sys.exit(1)
        print(f"Reading from local file: {BATCH_FILE}")
        with open(BATCH_FILE, 'r', encoding='utf-8') as f:
            csv_content = f.read()
    else:
        url = args.url or GOOGLE_SHEETS_URL
        print(f"Fetching from Google Sheets...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'  # Force UTF-8 encoding
            csv_content = response.text
            print(f"  Received {len(csv_content)} bytes")
        except Exception as e:
            print(f"Error fetching URL: {e}")
            sys.exit(1)

    print(f"Loading tree...")
    tree = load_tree(TREE_JSON_PATH)

    TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "publication", "templates")
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('batch_post_template.j2')

    reader = csv.DictReader(io.StringIO(csv_content))
    for row in reader:
        branch = row['Haplogroup'].strip()
        kit = row['Kit'].strip()
        
        # Skip description rows (non-haplogroup values like Russian text)
        if not branch or not re.match(r'^[A-Z]', branch):
            print(f"  Skipping non-data row: {branch[:30]}...")
            continue
            
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
            
            # Auto-publish if requested
            if args.publish or args.draft:
                # Use Title from CSV if available, otherwise generate from haplogroup
                title = row.get('Title', '').strip() or f"Гаплогруппа {branch}"
                post_id = publish_to_wordpress(output_filename, title, slug, publish=not args.draft)
                if post_id:
                    print(f"  Published: https://aadna.ru/{slug}/")
            
        except Exception as e:
            print(f"  Error rendering: {e}")

if __name__ == "__main__":
    main()

