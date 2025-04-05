import requests
from dotenv import load_dotenv
load_dotenv()

import os
CIVIC_API_KEY = os.environ['CIVIC_API_KEY']  # Replace with your real API key
ZIPPOTAM_URL = "http://api.zippopotam.us/us/"
CIVIC_API_URL = "https://www.googleapis.com/civicinfo/v2/voterinfo"

def verify_zip(zip_code):
    res = requests.get(f"{ZIPPOTAM_URL}{zip_code}")
    if res.status_code != 200:
        raise ValueError(f"ZIP code {zip_code} not found.")
    return True

def get_upcoming_election(full_address):
    print(f"\n📍 Looking up: {full_address}")

    params = {
        "key": CIVIC_API_KEY,
        "address": full_address
    }

    res = requests.get(CIVIC_API_URL, params=params)

    if res.status_code == 400:
        error_msg = res.json().get('error', {}).get('message', '')
        if "Election unknown" in error_msg:
            print("🚫 No upcoming election found for this address.")
            return
        else:
            print(f"❌ API error: {res.status_code}")
            print(res.json())
            return
    elif res.status_code != 200:
        print(f"❌ API error: {res.status_code}")
        print(res.json())
        return

    data = res.json()

    # 🗳️ Election Info
    election = data.get("election")
    if election:
        print(f"\n🗳️ Election: {election.get('name')}")
        print(f"📅 Date: {election.get('electionDay')}")
    else:
        print("🚫 No election data found.")

    # 📋 Contests: Candidates and Ballot Measures
    contests = data.get("contests", [])
    if contests:
        print("\n📋 Ballot Items:")
        for c in contests:
            print(f"\n• Office/Measure: {c.get('office', 'Ballot Measure')}")
            if "type" in c:
                print(f"  Type: {c['type']}")
            if "district" in c:
                print(f"  District: {c['district'].get('name')}")
            if "ballotTitle" in c:
                print(f"  🧾 Ballot Title: {c['ballotTitle']}")
            if "ballotSummary" in c:
                print(f"  📄 Summary: {c['ballotSummary']}")
            if "referendumTitle" in c:
                print(f"  🧾 Referendum Title: {c['referendumTitle']}")
            if "referendumSubtitle" in c:
                print(f"  🗂️ Subtitle: {c['referendumSubtitle']}")
            if "referendumUrl" in c:
                print(f"  🔗 More info: {c['referendumUrl']}")
            if "candidates" in c:
                print("  👤 Candidates:")
                for cand in c['candidates']:
                    print(f"    - {cand['name']} ({cand.get('party', 'No party listed')})")
    else:
        print("⚠️ No contests or ballot measures found.")

    # 📍 Polling Place
    polling_locations = data.get("pollingLocations", [])
    if polling_locations:
        print("\n📍 Polling Place:")
        for location in polling_locations:
            addr = location.get("address", {})
            print(f"  - {addr.get('line1', '')}, {addr.get('city', '')}, {addr.get('state', '')} {addr.get('zip', '')}")
            print(f"    Hours: {location.get('pollingHours', 'N/A')}")
    else:
        print("⚠️ No polling place info available.")

    # 🕓 Early Voting
    early_vote_sites = data.get("earlyVoteSites", [])
    if early_vote_sites:
        print("\n🕓 Early Voting Locations:")
        for site in early_vote_sites:
            addr = site.get("address", {})
            print(f"  - {addr.get('line1', '')}, {addr.get('city', '')}, {addr.get('state', '')} {addr.get('zip', '')}")
            print(f"    Hours: {site.get('pollingHours', 'N/A')}")

    # 📦 Drop Boxes
    drop_off_locations = data.get("dropOffLocations", [])
    if drop_off_locations:
        print("\n📦 Drop-off Locations:")
        for site in drop_off_locations:
            addr = site.get("address", {})
            print(f"  - {addr.get('line1', '')}, {addr.get('city', '')}, {addr.get('state', '')} {addr.get('zip', '')}")
            print(f"    Hours: {site.get('pollingHours', 'N/A')}")

    # 🧑‍⚖️ Election Administration
    admin_body = data.get("state", [{}])[0].get("electionAdministrationBody", {})
    if admin_body:
        print("\n🧑‍⚖️ Election Office Contact:")
        print(f"  {admin_body.get('name', 'No name')}")
        addr = admin_body.get("correspondenceAddress", {})
        print(f"  {addr.get('line1', '')}, {addr.get('city', '')}, {addr.get('state', '')} {addr.get('zip', '')}")
        print(f"  Phone: {admin_body.get('electionOfficials', [{}])[0].get('officePhoneNumber', 'N/A')}")
        print(f"  Website: {admin_body.get('electionInfoUrl', 'N/A')}")

# 🧑‍💻 User Input
if __name__ == "__main__":
    print("📬 Enter your full address to check election info:")
    street = input("Street Address (e.g. 123 Main St): ").strip()
    city = input("City: ").strip()
    state = input("State (2-letter abbreviation): ").strip()
    zip_code = input("ZIP Code: ").strip()

    try:
        verify_zip(zip_code)
        full_address = f"{street}, {city}, {state} {zip_code}"
        get_upcoming_election(full_address)
    except ValueError as e:
        print(f"❌ {e}")
