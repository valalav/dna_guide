
import re
from generate_match_table import generate_html_table

def parse_and_reconstruct(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract the HTML table block
    # Find the STR Matches section first
    str_section_start = content.find("<!-- STR Matches")
    if str_section_start == -1:
        print("STR Matches section not found")
        return None, None, content
        
    str_section = content[str_section_start:]
    table_match = re.search(r'<table.*?>(.*?)</table>', str_section, re.DOTALL)
    if not table_match:
        print("No STR table found")
        return None, None, content
        
    table_html = table_match.group(1)
    
    # Extract HEADERS from thead
    thead_match = re.search(r'<thead>(.*?)</thead>', table_html, re.DOTALL)
    if not thead_match:
        print("No thead found")
        return None, None, content
        
    thead_html = thead_match.group(1)
    headers = re.findall(r'<th.*?>(.*?)</th>', thead_html)
    
    marker_names = []
    for h in headers:
        h = re.sub(r'<.*?>', '', h).strip() # Clean tags
        if h in ["Matches", "Match Info", "Kit", "Haplogroup", "GD", "Name", "-"]: continue
        if not h: continue
        
        if h.isdigit():
            marker_names.append(f"DYS{h}")
        else:
            marker_names.append(h)
    
    print(f"Detected markers: {marker_names}")
    
    # Extract ROWS from tbody
    tbody_match = re.search(r'<tbody>(.*?)</tbody>', table_html, re.DOTALL)
    if not tbody_match:
        # Fallback if no tbody tag?
        # But looking at snippet, it might not have explicit tbody if malformed?
        # Let's assume tbody exists based on typical output.
        print("No tbody found")
        # Try finding rows generally after head
        search_area = table_html
    else:
        search_area = tbody_match.group(1)
        
    rows = re.findall(r'<tr.*?>(.*?)</tr>', search_area, re.DOTALL)
    
    # We assume Row 0 is header1, Row 1 is header2 (Query Reference)
    # Wait, existing table has:
    # Header 1: Cols
    # Row 2 (Query): 55520 | Name | HG | - | Val1 | Val2 ...
    
    # Let's look for the row with 55520 as first data cell
    query_row_idx = -1
    for i, r in enumerate(rows):
        if "55520" in r and "str-gd" in r:
           query_row_idx = i
           break
           
    if query_row_idx == -1:
        print("Could not find query row")
        return None, None, content

    # Parse Query Row to get Profile Markers
    q_cells = re.findall(r'<td.*?>(.*?)</td>|<th>(.*?)</th>', rows[query_row_idx])
    # flatten tuples
    q_values = [c[0] or c[1] for c in q_cells]
    
    # Query row structure: Kit, Name, HG, GD, M1, M2...
    # We assume first 4 are meta
    q_meta = q_values[:4]
    q_marker_vals = q_values[4:]
    
    profile = {
        "kitNumber": q_meta[0],
        "name": q_meta[1],
        "haplogroup": q_meta[2],
        "markers": {}
    }
    
    for i, m_name in enumerate(marker_names):
        if i < len(q_marker_vals):
            profile["markers"][m_name] = q_marker_vals[i]
            
    # Parse Matches
    matches = []
    for i in range(query_row_idx + 1, len(rows)):
        r = rows[i]
        # skip if standard header
        if "<th" in r and "Matches" in r: continue
        
        cells = re.findall(r'<td.*?>(.*?)</td>', r)
        if not cells: continue
        
        # Meta: Kit, Name, HG, GD
        m_kit = cells[0]
        # Clean up kit name (remove HTML tags if any)
        m_kit = re.sub(r'<.*?>', '', m_kit).strip()
        m_name = re.sub(r'<.*?>', '', cells[1]).strip()
        m_hg = re.sub(r'<.*?>', '', cells[2]).strip()
        m_dist = re.sub(r'<.*?>', '', cells[3]).strip()
        
        m_marker_vals = cells[4:]
        
        m_markers = {}
        # Pre-fill with query values because the table logic usually put "-" for matches
        # BUT wait. The table shows "-". Does that mean "Same as Query" or "Missing"?
        # Usually "-" means match (Same as Query).
        # We need to reconstruction actual values to run the NEW logic.
        # If cell is "-", value = query_value.
        # If cell is "13" or "+1", value is derived?
        # Standard "diff" logic in generate_match_table: 
        #   Exact match -> "-", "match"
        #   Diff -> "+1", "13", etc.
        
        for idx, val in enumerate(m_marker_vals):
            if idx >= len(marker_names): break
            m_key = marker_names[idx]
            q_val = profile["markers"].get(m_key, "")
            
            clean_val = re.sub(r'<.*?>', '', val).strip()
            
            if clean_val == "-" or clean_val == "":
                m_markers[m_key] = q_val
            elif clean_val.startswith("+") or clean_val.startswith("-"):
                # Relative diff? The existing script logic produced "+1" for integers.
                # If we see "+1", we need to calculate strict value?
                # Actually, for the NEW logic to work, we just need to know if it's SAME or DIFFERENT.
                # If existing table says "+1", it is DIFFERENT.
                # So we can just store the literal "+1" as the value, ensuring it differs from query value ("12").
                m_markers[m_key] = clean_val
            else:
                # Raw value "13"
                m_markers[m_key] = clean_val
                
        matches.append({
            "profile": {
                "kitNumber": m_kit,
                "name": m_name,
                "haplogroup": m_hg,
                "markers": m_markers
            },
            "distance": m_dist
        })
        
    return profile, matches, content

def main():
    profile, matches, raw_content = parse_and_reconstruct("test_match_55520_v2.md")
    if not profile: return
    
    print(f"Reconstructed profile {profile['kitNumber']} with {len(profile['markers'])} markers.")
    print(f"Reconstructed {len(matches)} matches.")
    
    new_html = generate_html_table(profile, matches)
    
    # Verify DYS393
    if "<th>393</th>" not in new_html:
        print("[SUCCESS] DYS393 column is hidden.")
    
    # Save v3
    # Replace the old table in content
    # Regex replace is tricky due to varying content, but we extracted table_html earlier via search
    # Let's just create a new file with just the table for now, OR try to splice it.
    
    start_marker = '<!-- STR Matches'
    end_marker = '<!-- Митохондриальная'
    
    # Find block
    p1 = raw_content.find(start_marker)
    p2 = raw_content.find(end_marker)
    
    if p1 != -1 and p2 != -1:
        prefix = raw_content[:p1]
        suffix = raw_content[p2:]
        
        # Keep the spoiler wrapper
        new_content = prefix + f"""<!-- STR Matches (для всех типов тестов) -->
<details class="dna-spoiler" open>
<summary>🔗 STR Совпадения (Variable Markers Only)</summary>
<div class="dna-spoiler-content">

{new_html}

<p>&nbsp;</p>

[github_md path="00_General/00_strmf.md"]
</div>
</details>

""" + suffix
        
        with open("test_match_55520_v3.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Written to test_match_55520_v3.md")
        
if __name__ == "__main__":
    main()
