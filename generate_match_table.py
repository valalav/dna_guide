import requests
import json
import math

# Configuration
API_BASE = "https://pystr.valalav.ru/api/profiles"
# FTDNA 37 Marker Order (approximate standard)
MARKER_ORDER = [
    "DYS393", "DYS390", "DYS19", "DYS391", "DYS385", "DYS426", "DYS388", 
    "DYS439", "DYS389i", "DYS392", "DYS389ii", "DYS458", "DYS459", "DYS455", 
    "DYS454", "DYS447", "DYS437", "DYS448", "DYS449", "DYS464", "DYS460", 
    "Y-GATA-H4", "YCAII", "DYS456", "DYS607", "DYS576", "DYS570", "CDY", 
    "DYS442", "DYS438"
]

def fetch_data(kit_number):
    # 1. Get Profile
    print(f"Fetching profile for {kit_number}...")
    p_url = f"{API_BASE}/{kit_number}"
    resp = requests.get(p_url, timeout=30)
    resp.raise_for_status()
    profile = resp.json().get('profile', {})
    markers = profile.get('markers', {})
    
    if not markers:
        raise ValueError("No markers found for this kit")

    # 2. Get Matches
    print(f"Fetching matches...")
    m_url = f"{API_BASE}/find-matches"
    payload = {
        "kitNumber": kit_number,
        "panel": "Y-STR37",
        "maxDist": 10, # Reduced distance for "top 30" relevance
        "limit": 30,   # User requested 30
        "includeSubclades": True,
        "showEmptyHaplogroups": False,
        "markers": markers # sending query markers
    }
    m_resp = requests.post(m_url, json=payload, timeout=30)
    m_resp.raise_for_status()
    matches = m_resp.json().get('matches', [])
    
    return profile, matches

def calculate_diff(q_val, m_val):
    """
    Returns (display_text, color_class)
    Color classes: 'match', 'diff-minor', 'diff-major'
    """
    if q_val == m_val:
        return "-", "match" # Exact match
        
    # Check if both are simple integers
    if q_val.isdigit() and m_val.isdigit():
        q_int = int(q_val)
        m_int = int(m_val)
        diff = m_int - q_int
        
        sign = "+" if diff > 0 else ""
        text = f"{sign}{diff}"
        
        if abs(diff) == 1:
            return text, "diff-minor"
        else:
            return text, "diff-major"
            
    # For multi-copy (e.g. 13-16) or complex values
    return m_val, "diff-major" # Show full value if different

def generate_html_table(profile, matches):
    q_markers = profile.get('markers', {})
    
    # 1. Identify "Variable" markers
    # A marker is interesting if at least one match has a value different from the query
    interesting_markers = set()
    
    # Check all potential markers (from Query)
    # We prioritize the Standard Order for sorting, but scan all query markers
    potential_markers = [m for m in MARKER_ORDER if m in q_markers]
    
    # If a marker is in Query but not in Standard Order, should we show it? 
    # Usually only standard panel matters for STR matching, but let's stick to MARKER_ORDER intersection for now to be safe,
    # OR scan all keys in q_markers. Let's start with MARKER_ORDER intersection to avoid noise like "DYS_EXTRA_999".
    
    for col in potential_markers:
        q_val = str(q_markers.get(col, ""))
        is_variable = False
        
        for m in matches:
            m_prof = m.get('profile', {})
            m_markers = m_prof.get('markers', {})
            m_val = str(m_markers.get(col, ""))
            
            if not m_val: continue # Skip comparison if match misses data
            
            # Simple diff check
            if q_val != m_val:
                is_variable = True
                break
        
        if is_variable:
            interesting_markers.add(col)
            
    # Always include markers if the list ends up empty (edge case: perfect match)
    # But usually there are differences.
    
    # Sort columns by Standard Order
    columns = [m for m in MARKER_ORDER if m in interesting_markers]
    
    # Use standard styles
    style = """
<style>
.str-table { width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 11px; }
.str-table th { background-color: #f8f9fa; padding: 6px 4px; border: 1px solid #dee2e6; text-align: center; }
.str-table td { padding: 4px; border: 1px solid #dee2e6; text-align: center; }
.str-match { color: #adb5bd; } /* Muted gray for match */
.str-diff-minor { color: #c05621; font-weight: bold; background-color: #fffaf0; } /* Orange tint */
.str-diff-major { color: #c53030; font-weight: bold; background-color: #fff5f5; } /* Red tint */
.str-meta { text-align: left !important; white-space: nowrap; max-width: 150px; overflow: hidden; text-overflow: ellipsis; }
.str-kit { font-weight: bold; color: #3182ce; }
.str-gd { font-weight: bold; background-color: #f0fff4; color: #276749; }
</style>
"""

    html = [style, '<div style="overflow-x:auto"><table class="str-table">']
    
    # Header
    html.append('<thead><tr>')
    html.append('<th colspan="4" style="text-align:left">Matches</th>') 
    for col in columns:
        html.append(f'<th>{col.replace("DYS","")}</th>')
    html.append('</tr></thead>')
    
    html.append('<tbody>')
    
    # Query Row
    html.append('<tr style="background-color: #e0f2fe;">')
    html.append(f'<td colspan="3" style="text-align:left;font-weight:bold;padding:4px;border:1px solid #dee2e6;">{profile.get("kitNumber")}</td>')
    html.append('<td class="str-gd">-</td>')
    for col in columns:
        html.append(f'<th>{q_markers.get(col, "")}</th>')
    html.append('</tr>')
    
    # Matches
    for m in matches:
        m_prof = m.get('profile', {})
        m_markers = m_prof.get('markers', {})
        
        html.append('<tr>')
        html.append(f'<td class="str-meta str-kit" title="{m_prof.get("name")}">{m_prof.get("kitNumber")}</td>')
        html.append(f'<td class="str-meta" title="{m_prof.get("name")}">{m_prof.get("name")}</td>')
        html.append(f'<td class="str-meta">{m_prof.get("haplogroup")}</td>')
        html.append(f'<td class="str-gd">{m.get("distance")}</td>')
        
        for col in columns:
            q_val = str(q_markers.get(col, ""))
            m_val = str(m_markers.get(col, ""))
            
            if not m_val:
                html.append('<td class="str-match">-</td>') # Missing treated as match/dash visually for cleaner table
                continue
                
            text, style_class = calculate_diff(q_val, m_val)
            css_class = f"str-{style_class}"
            html.append(f'<td class="{css_class}">{text}</td>')
            
        html.append('</tr>')
        
    html.append('</tbody></table></div>')
    
    return "\n".join(html)

def main():
    target_kit = "55520" # Default or arg
    try:
        profile, matches = fetch_data(target_kit)
        table_html = generate_html_table(profile, matches)
        
        filename = f"matches_{target_kit}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# STR Matches: {target_kit}\n\n")
            f.write(table_html)
            
        print(f"Generated match table: {filename}")
        
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    main()
