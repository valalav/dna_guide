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
    
    # Filter markers to only those present in the Query or Standard List
    # We use MARKER_ORDER as the base column definition
    columns = [m for m in MARKER_ORDER if m in q_markers]
    
    # CSS Styles (Inline for portability)
    style = """
<style>
.str-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 11px; }
.str-table th { background-color: #f1f5f9; padding: 4px; border: 1px solid #e2e8f0; text-align: center; }
.str-table td { padding: 4px; border: 1px solid #e2e8f0; text-align: center; }
.str-match { color: #d1d5db; } /* Light gray for dash */
.str-diff-minor { color: #ea580c; font-weight: bold; background-color: #fff7ed; } /* Orange */
.str-diff-major { color: #dc2626; font-weight: bold; background-color: #fef2f2; } /* Red */
.str-meta { text-align: left !important; white-space: nowrap; max-width: 150px; overflow: hidden; text-overflow: ellipsis; }
.str-kit { font-weight: bold; color: #2563eb; }
.str-gd { font-weight: bold; background-color: #f0fdf4; color: #166534; }
</style>
"""

    html = [style, '<table class="str-table">']
    
    # Header 1: Marker Names
    html.append('<thead><tr>')
    html.append('<th colspan="4" style="text-align:left">Match Info</th>') # Kit, Name, HG, GD
    for col in columns:
        html.append(f'<th>{col.replace("DYS","")}</th>') # Shorten names for compactness
    html.append('</tr>')
    
    # Header 2: Query Values (Reference)
    html.append('<tr style="background-color: #dbeafe;">') # Light blue for Query
    html.append(f'<td class="str-meta str-kit">{profile.get("kitNumber")}</td>')
    html.append(f'<td class="str-meta">{profile.get("name")}</td>')
    html.append(f'<td class="str-meta">{profile.get("haplogroup")}</td>')
    html.append('<td class="str-gd">-</td>')
    for col in columns:
        html.append(f'<th>{q_markers.get(col, "")}</th>')
    html.append('</tr></thead>')
    
    html.append('<tbody>')
    
    for m in matches:
        m_prof = m.get('profile', {})
        m_markers = m_prof.get('markers', {})
        
        html.append('<tr>')
        # Meta columns
        html.append(f'<td class="str-meta str-kit">{m_prof.get("kitNumber")}</td>')
        html.append(f'<td class="str-meta" title="{m_prof.get("name")}">{m_prof.get("name")}</td>')
        html.append(f'<td class="str-meta">{m_prof.get("haplogroup")}</td>')
        html.append(f'<td class="str-gd">{m.get("distance")}</td>')
        
        # Marker columns
        for col in columns:
            q_val = str(q_markers.get(col, ""))
            m_val = str(m_markers.get(col, ""))
            
            # Logic: If query has value but match missing -> ?
            if not m_val:
                html.append('<td>?</td>')
                continue
                
            text, style_class = calculate_diff(q_val, m_val)
            css_class = f"str-{style_class}"
            
            html.append(f'<td class="{css_class}">{text}</td>')
            
        html.append('</tr>')
        
    html.append('</tbody></table>')
    
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
