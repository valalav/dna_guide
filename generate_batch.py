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

# --- STR Match Table Helpers ---
def calculate_str_diff(q_val, m_val):
    if q_val == m_val: return "-", "match"
    if q_val.isdigit() and m_val.isdigit():
        diff = int(m_val) - int(q_val)
        return f"+{diff}" if diff > 0 else str(diff), "diff-minor" if abs(diff) == 1 else "diff-major"
    return m_val, "diff-major"

def generate_str_table_html(profile, matches):
    MARKER_ORDER = [
        "DYS393", "DYS390", "DYS19", "DYS391", "DYS385", "DYS426", "DYS388", 
        "DYS439", "DYS389i", "DYS392", "DYS389ii", "DYS458", "DYS459", "DYS455", 
        "DYS454", "DYS447", "DYS437", "DYS448", "DYS449", "DYS464", "DYS460", 
        "Y-GATA-H4", "YCAII", "DYS456", "DYS607", "DYS576", "DYS570", "CDY", 
        "DYS442", "DYS438"
    ]
    q_markers = profile.get('markers', {})
    columns = [m for m in MARKER_ORDER if m in q_markers]
    
    style = """<style>
.str-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 11px; }
.str-table th { background-color: #f1f5f9; padding: 4px; border: 1px solid #e2e8f0; text-align: center; }
.str-table td { padding: 4px; border: 1px solid #e2e8f0; text-align: center; }
.str-match { color: #d1d5db; }
.str-diff-minor { color: #ea580c; font-weight: bold; background-color: #fff7ed; }
.str-diff-major { color: #dc2626; font-weight: bold; background-color: #fef2f2; }
.str-meta { text-align: left !important; white-space: nowrap; max-width: 150px; overflow: hidden; text-overflow: ellipsis; }
.str-kit { font-weight: bold; color: #2563eb; }
.str-gd { font-weight: bold; background-color: #f0fdf4; color: #166534; }
</style>"""
    html = [style, '<div style="overflow-x:auto;"><table class="str-table"><thead><tr>']
    html.append('<th colspan="4" style="text-align:left">Match Info</th>')
    for col in columns: html.append(f'<th>{col.replace("DYS","")}</th>')
    html.append('</tr><tr style="background-color: #dbeafe;">')
    html.append(f'<td class="str-meta str-kit">{profile.get("kitNumber")}</td><td class="str-meta">{profile.get("name")}</td><td class="str-meta">{profile.get("haplogroup")}</td><td class="str-gd">-</td>')
    for col in columns: html.append(f'<th>{q_markers.get(col, "")}</th>')
    html.append('</tr></thead><tbody>')
    
    for m in matches:
        mp = m.get('profile', {})
        mm = mp.get('markers', {})
        html.append('<tr>')
        html.append(f'<td class="str-meta str-kit">{mp.get("kitNumber")}</td><td class="str-meta" title="{mp.get("name")}">{mp.get("name")}</td><td class="str-meta">{mp.get("haplogroup")}</td><td class="str-gd">{m.get("distance")}</td>')
        for col in columns:
            q, val = str(q_markers.get(col, "")), str(mm.get(col, ""))
            if not val: html.append('<td>?</td>')
            else:
                txt, cls = calculate_str_diff(q, val)
                html.append(f'<td class="str-{cls}">{txt}</td>')
        html.append('</tr>')
    html.append('</tbody></table></div>')
    return "".join(html)

def fetch_str_match_table(kit_number):
    try:
        # Pystr API
        API = "https://pystr.valalav.ru/api/profiles"
        p_resp = requests.get(f"{API}/{kit_number}", timeout=10)
        if p_resp.status_code != 200: return None
        profile = p_resp.json().get('profile', {})
        markers = profile.get('markers', {})
        if not markers: return None

        m_resp = requests.post(f"{API}/find-matches", json={
            "kitNumber": kit_number, "panel": "Y-STR37", "maxDist": 10, "limit": 30,
            "includeSubclades": True, "showEmptyHaplogroups": False, "markers": markers
        }, timeout=15)
        if m_resp.status_code != 200: return None
        matches = m_resp.json().get('matches', [])
        return generate_str_table_html(profile, matches)
    except Exception as e:
        print(f"  STR Match Error for {kit_number}: {e}")
        return None
# -----------------------------

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
    
    # Correct list of major haplogroups (NOT including F, K, P etc.)
    MAJOR_HAPLOGROUPS = ['C', 'D', 'E', 'G', 'I', 'J', 'R', 'S', 'T', 'N', 'M', 'Q', 'L', 'O']
    
    for i, branch_id in enumerate(lineage_path):
        branch_tmrca = int(tmrca_index.get(branch_id, 0))
        is_current = (i == total_items - 1)
        # Only mark as major if it's a single letter AND in our major list
        is_major = len(branch_id) == 1 and branch_id.upper() in MAJOR_HAPLOGROUPS
        
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

    # Split into pre-major (horizontal table) and post-major (diagonal) sections
    pre_major_timeline = []
    post_major_timeline = []
    
    tmrca_range = major_tmrca - current_tmrca if major_tmrca > current_tmrca else 1
    
    # Scale helper function (Non-linear: Ancient history compressed, Recent expanded)
    def get_timeline_position(tmrca, major_tmrca, current_tmrca):
        # Constants
        FOCUS_AGE = 5000  # Years ago
        SPLIT_POINT = 65  # % of height for ancient history boundary
        MAX_USABLE_HEIGHT = 80 # Leave bottom 20% empty for the deepest branch explicitly
        
        if tmrca == current_tmrca:
             return 100 # Deepest branch always at very bottom
             
        if major_tmrca <= FOCUS_AGE:
            # If everything is recent, use simple linear scale up to MAX_USABLE_HEIGHT
            if tmrca_range == 0: return 0
            rel_pos = (major_tmrca - tmrca) / tmrca_range
            return int(rel_pos * MAX_USABLE_HEIGHT)
            
        # If we span across the FOCUS_AGE
        if tmrca > FOCUS_AGE:
            # Ancient Section (major -> 5000y) maps to 0 -> SPLIT_POINT
            ancient_range = major_tmrca - FOCUS_AGE
            time_from_major = major_tmrca - tmrca
            return int((time_from_major / ancient_range) * SPLIT_POINT)
        else:
            # Recent Section (5000y -> current) maps to SPLIT_POINT -> MAX_USABLE_HEIGHT
            recent_range = FOCUS_AGE - current_tmrca
            if recent_range == 0: return SPLIT_POINT
            time_from_focus = FOCUS_AGE - tmrca
            rel_recent = time_from_focus / recent_range
            # Map 0..1 to SPLIT..MAX
            return int(SPLIT_POINT + (rel_recent * (MAX_USABLE_HEIGHT - SPLIT_POINT)))

    for item in lineage_timeline_raw:
        if major_index >= 0 and item['index'] >= major_index:
            # Post-major: calculate diagonal position
            if item['tmrca'] > 0:
                position = get_timeline_position(item['tmrca'], major_tmrca, current_tmrca)
            else:
                position = 0
            item['position'] = position
            # Show TMRCA for ALL branches in post-major section (as requested)
            item['show_tmrca'] = item['tmrca'] > 0
            post_major_timeline.append(item)
        else:
            # Pre-major: only include branches WITH TMRCA
            if item['tmrca'] > 0:
                item['position'] = 0
                item['show_tmrca'] = True
                pre_major_timeline.append(item)
    
    # Generate age scale ticks with same non-linear logic
    age_scale_ticks = []
    if major_tmrca > 0:
        # Define ticks
        tick_values = []
        age = major_tmrca
        # Start ticks from rounded major
        start_tick = (major_tmrca // 1000) * 1000
        
        # SMART SCALE: Pre-defined 'nice' values with collision detection
        # This restores visual density while strictly preventing overlaps
        candidates = [
            50000, 45000, 40000, 35000, 30000, 25000, 20000, 
            15000, 12000, 10000, 8000, 6000, 
            5000, 4000, 3000, 2500, 2000, 1500, 1000, 500
        ]
        
        # Filter candidates within range
        tick_values = []
        for c in candidates:
            if c <= major_tmrca and c >= current_tmrca:
                tick_values.append(c)
        
        # Always include the exact Major start point for context
        if start_tick not in tick_values:
            tick_values.append(start_tick)
            
        # Sort descending (top to bottom)
        tick_values = sorted(list(set(tick_values)), reverse=True)
        
        # Collision detection loop
        final_ticks = []
        last_pos_pct = -100 # Initialize far above
        
        for val in tick_values:
            pos_pct = get_timeline_position(val, major_tmrca, current_tmrca)
            
            # Check distance to previous tick (min 6% height difference)
            if abs(pos_pct - last_pos_pct) >= 6:
                final_ticks.append(val)
                last_pos_pct = pos_pct
                
        # Use our collision-checked list
        tick_values = final_ticks
             
        # Sort desc
        tick_values = sorted(list(set(tick_values)), reverse=True)

        last_tick_pos = -100 # Initialize far away
        
        for tick_age in tick_values:
            # Calculate position first
            tick_position = get_timeline_position(tick_age, major_tmrca, current_tmrca)
            
            # Filter ticks too close to current (avoid overlap with bottom distinct label)
            if tick_age - current_tmrca < 200 and tick_age != current_tmrca:
                continue
                
            # Filter ticks too close to EACH OTHER (minimum 5% vertical spacing)
            if abs(tick_position - last_tick_pos) < 5:
                continue

            # Smart labeling: 1.5k instead of 1k for 1500
            if tick_age >= 1000:
                val = tick_age / 1000.0
                if val.is_integer():
                    label = f"{int(val)}k"
                else:
                    label = f"{val}k"
            else:
                label = str(tick_age)

            if tick_age == 5000 and major_tmrca > 8000: label = "5k" # Force clear label at breakpoint
            
            age_scale_ticks.append({
                'age': tick_age,
                'label': label,
                'position': tick_position
            })
            
            last_tick_pos = tick_position
    
    # Combined lineage_timeline for backward compatibility (template uses this)
    lineage_timeline = lineage_timeline_raw

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
        'pre_major_timeline': pre_major_timeline,
        'post_major_timeline': post_major_timeline,
        'age_scale_ticks': age_scale_ticks,
        'history_section': "", # Placeholder or extract from docs if needed
        'y_dna_docs': y_dna_docs,
        'neighbor_context': "", # Simplify for batch
        'records': records,
        'records_count': 1,
        'test_type': row.get('TestType', 'WGS') # Pass TestType
    }

def publish_to_wordpress(local_file, title, slug, tags="", post_date="", publish=True):
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
        # Convert tags from pipe-separated to comma-separated for wp-cli
        tags_param = f'--tags="{tags.replace("|", ",")}"' if tags else ''
        date_param = f'--post_date="{post_date}"' if post_date else ''
        wp_cmd = f'export LANG=en_US.UTF-8 && export LC_ALL=en_US.UTF-8 && TITLE=$(echo "{b64_title}" | base64 -d) && cat /tmp/{os.path.basename(local_file)} | wp post create - --post_title="$TITLE" --post_name="{slug}" --post_status={post_status} --post_type=post {tags_param} {date_param} --path={WP_PATH} --allow-root --porcelain'
        
        print(f"    Creating WordPress post...")
        ssh_cmd = [PLINK_PATH, "-ssh", f"{SERVER_USER}@{SERVER_IP}", "-pw", SERVER_PASS, "-batch", wp_cmd]
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"    WP-CLI failed: {result.stderr}")
            return False
        
        post_id = result.stdout.strip()
        print(f"    Created post ID: {post_id}")
        
        # Step 4: Add tags if provided (using base64 to handle Cyrillic)
        if tags and post_id:
            # Encode tags in base64 for safe transfer
            tags_clean = ','.join([t.strip() for t in tags.split('|') if t.strip()])
            b64_tags = base64.b64encode(tags_clean.encode('utf-8')).decode('ascii')
            tags_cmd = f'export LANG=en_US.UTF-8 && TAGS=$(echo "{b64_tags}" | base64 -d) && IFS="," read -ra TARR <<< "$TAGS" && for t in "${{TARR[@]}}"; do wp post term add {post_id} post_tag "$t" --path={WP_PATH} --allow-root 2>/dev/null; done'
            subprocess.run([PLINK_PATH, "-ssh", f"{SERVER_USER}@{SERVER_IP}", "-pw", SERVER_PASS, "-batch", tags_cmd],
                          capture_output=True, timeout=30)
            print(f"    Added tags: {tags}")
        
        # Step 5: Clear cache
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
    csv_data = None
    
    # Priority 1: Explicit local file
    if args.local:
        if not os.path.exists(BATCH_FILE):
            print(f"Error: {BATCH_FILE} not found.")
            sys.exit(1)
        with open(BATCH_FILE, 'r', encoding='utf-8') as f:
            csv_data = f.read()
            
    # Priority 2: URL with fallback
    else:
        url = args.url if args.url else GOOGLE_SHEETS_URL
        print("Fetching from Google Sheets...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'  # Force UTF-8 encoding
            csv_data = response.text
            print(f"  Received {len(csv_data)} bytes")
            
            # Save backup
            with open("aadna.ru.csv", "w", encoding="utf-8") as f:
                f.write(csv_data)
                
        except Exception as e:
            print(f"  Warning: Network error ({e}).")
            if os.path.exists("aadna.ru.csv"):
                print("  Falling back to local cache: aadna.ru.csv")
                with open("aadna.ru.csv", "r", encoding='utf-8') as f:
                    csv_data = f.read()
            else:
                print("  Error: No local backup found.")
                sys.exit(1)

    print(f"Loading tree...")
    tree = load_tree(TREE_JSON_PATH)

    TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "publication", "templates")
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('batch_post_template.j2')

    reader = csv.DictReader(io.StringIO(csv_data))
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
        
        # New: Fetch STR Match Table
        if kit:
            print(f"  Fetching STR matches for {kit}...")
            context['str_match_table'] = fetch_str_match_table(kit)
        else:
            context['str_match_table'] = None
        
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
                tags = row.get('Tags', '').strip()
                post_date = row.get('Date', '').strip()
                post_id = publish_to_wordpress(output_filename, title, slug, tags=tags, post_date=post_date, publish=not args.draft)
                if post_id:
                    print(f"  Published: https://aadna.ru/{slug}/")
            
        except Exception as e:
            print(f"  Error rendering: {e}")

if __name__ == "__main__":
    main()

