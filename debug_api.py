import requests
import json

API = "https://pystr.valalav.ru/api/profiles"
KIT = "55520"

try:
    print(f"Fetching profile {KIT}...")
    p_resp = requests.get(f"{API}/{KIT}", timeout=10)
    if p_resp.status_code != 200:
        print(f"Profile error: {p_resp.status_code}")
        exit()
        
    markers = p_resp.json().get('profile', {}).get('markers', {})
    if not markers:
        print("No markers in profile.")
        exit()

    print("Fetching matches...")
    resp = requests.post(
        f"{API}/find-matches", 
        json={
            "kitNumber": KIT, 
            "panel": "Y-STR37", 
            "limit": 1,
            "includeSubclades": True,
            "showEmptyHaplogroups": False,
            "markers": markers
        }, 
        timeout=15
    )
    if resp.status_code == 200:
        data = resp.json()
        matches = data.get('matches', [])
        if matches:
            m = matches[0]
            print("\n--- MATCH OBJECT KEYS ---")
            print(list(m.keys()))
            
            # Check for generic 'diffs' key
            if 'diffs' in m:
                print("\n--- FOUND DIFFS ---")
                print(json.dumps(m['diffs'], indent=2))
            else:
                print("\n--- NO DIFFS KEY FOUND ---")
            
            if 'formatted_markers' in m:
                 print("\n--- FOUND FORMATTED MARKERS ---")
                 print(json.dumps(m['formatted_markers'], indent=2))
            
            # Check if markers themselves have diff info? (Usually they are just strings)
        else:
            print("No matches found.")
    else:
        print(f"Error: {resp.status_code} - {resp.text}")
except Exception as e:
    print(f"Exception: {e}")
