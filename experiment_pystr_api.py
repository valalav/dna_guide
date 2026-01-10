import requests
import json

URL = "https://pystr.valalav.ru/api/profiles/find-matches"
PAYLOAD = {
    "kitNumber": "55520",
    "panel": "Y-STR37", 
    "maxDist": 25,
    "limit": 5, 
    "includeSubclades": True,
    "showEmptyHaplogroups": False
}

try:
    # Step 1: Get Profile Markers
    profile_url = "https://pystr.valalav.ru/api/profiles/55520"
    print(f"Step 1: Fetching profile from {profile_url}...")
    p_resp = requests.get(profile_url, timeout=30)
    
    if p_resp.status_code == 404:
        # Fallback search if direct ID fails?
        print("Profile not found by ID. Trying search...")
        # (Optional logic omitted for brevity, hoping direct works)
        pass
        
    p_resp.raise_for_status()
    data = p_resp.json()
    profile = data.get('profile', {})
    markers = profile.get('markers', {})
    if not markers:
        print("Error: No markers found in profile.")
        print(f"Response keys: {list(data.keys())}")
        exit(1)

    # Step 2: Find Matches
    print(f"Step 2: Requesting matches from {URL}...")
    # Add markers to payload
    PAYLOAD['markers'] = markers
    
    resp = requests.post(URL, json=PAYLOAD, timeout=30)
    resp.raise_for_status()
    
    data = resp.json()
    print(f"Success! Keys in response: {list(data.keys())}")
    
    if 'matches' in data and len(data['matches']) > 0:
        print(f"Found {len(data['matches'])} matches.")
        first_match = data['matches'][0]
        print("\nStructure of first match object:")
        print(json.dumps(first_match, indent=2))
        
        # Save full debug output
        with open("api_debug.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("\nSaved full response to api_debug.json")
    else:
        print("Response OK but 'matches' list is empty.")
        print(data)
        
except Exception as e:
    print(f"Error calling API: {e}")
    if 'resp' in locals():
        print(f"Server response (Match): {resp.text}")
    if 'p_resp' in locals() and p_resp.status_code >= 400:
        print(f"Server response (Profile): {p_resp.text}")
