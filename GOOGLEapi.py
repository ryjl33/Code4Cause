import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Load API keys from .env
CIVIC_API_KEY = os.environ['CIVIC_API_KEY']
FEC_API_KEY = os.environ['FEC_API_KEY']

# API Endpoints
ZIPPOTAM_URL = "http://api.zippopotam.us/us/"
CIVIC_API_URL = "https://www.googleapis.com/civicinfo/v2/voterinfo"
FEC_SEARCH_URL = "https://api.open.fec.gov/v1/candidates/search/"
FEC_TOTALS_URL = "https://api.open.fec.gov/v1/candidate/{candidate_id}/totals/"

def verify_zip(zip_code):
    res = requests.get(f"{ZIPPOTAM_URL}{zip_code}")
    if res.status_code != 200:
        raise ValueError(f"The ZIP code {zip_code} is not valid or could not be found. Please check and try again.")
    return True

people = ['Tishaura O. Jones', 'Cara Spencer', 'Donna M.C. Baringer', 'Darlene Green', 'Anne Schweitzer', 'Tony Kirchner', 'Dallas Adams', 'Shane Cohn', 'Matt Devoti', 'Alisha Sonnier', 'Cedric Redmon', 'Michael Browning', 'Rebecca McCloud', 'Laura M. Keys', 'Pamela Boyd', 'Karen Collins-Adams', 'Brian H. Marston', 'David L. Jackson, Jr.', 'Allisa (AJ) Foster', 'William (Bill) Monroe', 'Krystal Barnett', 'Zacheriah (Zach) Davis', 'Antionette (Toni) Cousins', 'Tavon Brooks', 'Andre D. Walker', 'Teri Powers', 'Robert Terry Mason II', 'David Addison', 'Holly Talir']

def run_test_case_creve_coeur():
    print("\nTEST CASE: 50 Morwood Ln, Creve Coeur, MO 63141")
    print("\nElection Date: April 8, 2025")

    print("\nMayor (Vote for One):")
    print("  - Tishaura O. Jones")
    print("  - Cara Spencer")
    print("  - Write-In")

    print("\nComptroller (Vote for One):")
    print("  - Donna M.C. Baringer")
    print("  - Darlene Green")
    print("  - Write-In")

    print("\nBoard of Aldermen (by Ward):")
    print("  Ward 1: Anne Schweitzer, Tony Kirchner")
    print("  Ward 3: Dallas Adams, Shane Cohn")
    print("  Ward 5: Matt Devoti")
    print("  Ward 7: Alisha Sonnier, Cedric Redmon")
    print("  Ward 9: Michael Browning")
    print("  Ward 11: Rebecca McCloud, Laura M. Keys")
    print("  Ward 13: Pamela Boyd")

    print("\nBoard of Education (Vote for Three):")
    print("  - Karen Collins-Adams")
    print("  - Brian H. Marston")
    print("  - David L. Jackson, Jr.")
    print("  - Allisa (AJ) Foster")
    print("  - William (Bill) Monroe")
    print("  - Krystal Barnett")
    print("  - Zacheriah (Zach) Davis")
    print("  - Antionette (Toni) Cousins")
    print("  - Tavon Brooks")
    print("  - Andre D. Walker")
    print("  - Teri Powers")
    print("  - Robert Terry Mason II")
    print("  - Write-In (x3)")

    print("\nSt. Louis Community College Trustee – Sub-District 3:")
    print("  - David Addison")
    print("  - Holly Talir")
    print("  - Write-In")

def get_upcoming_election(full_address):
    print(f"\nLooking up: {full_address}")
    params = {"key": CIVIC_API_KEY, "address": full_address}
    res = requests.get(CIVIC_API_URL, params=params)

    if res.status_code == 400:
        error_msg = res.json().get('error', {}).get('message', '')
        if "Election unknown" in error_msg:
            print("There is no upcoming election for this address. Please check back later or verify with your local election office.")
            return
        else:
            print("Something went wrong while fetching election data. Please verify your address or try again later.")
            print(f"Details: {res.json().get('error', {}).get('message', '')}")
            return
    elif res.status_code != 200:
        print("Unable to connect to the Civic API. Please check your internet connection.")
        print(f"Status Code: {res.status_code}, Details: {res.text}")
        return

    data = res.json()
    election = data.get("election")
    if election:
        print(f"\nElection: {election.get('name')}")
        print(f"Date: {election.get('electionDay')}")

    contests = data.get("contests", [])
    for c in contests:
        if "referendumTitle" in c or "ballotTitle" in c:
            print(f"\nBallot Measure: {c.get('referendumTitle') or c.get('ballotTitle')}")
            if "referendumUrl" in c:
                print(f"More info: {c['referendumUrl']}")
        if c.get("type") in ["General", "Primary"] and "candidates" in c:
            print(f"\nOffice: {c.get('office', 'Unknown Office')}")
            print("Candidates:")
            for cand in c.get("candidates", []):
                print(f"  - {cand['name']} ({cand.get('party', 'N/A')})")

def get_names(full_address, test_case=False):
    if test_case:
        return people[:5]

    params = {"key": CIVIC_API_KEY, "address": full_address}
    res = requests.get(CIVIC_API_URL, params=params)

    data = res.json()

    if res.status_code == 400:
        error_msg = res.json().get('error', {}).get('message', '')
        if "Election unknown" in error_msg:
            print("There is no upcoming election for this address. Please check back later or verify with your local election office.")
            return
        else:
            print("Something went wrong while fetching election data. Please verify your address or try again later.")
            print(f"Details: {res.json().get('error', {}).get('message', '')}")
            return []
    elif res.status_code != 200:
        print("Unable to connect to the Civic API. Please check your internet connection.")
        print(f"Status Code: {res.status_code}, Details: {res.text}")
        return []

    contests = data.get("contests", [])
    contestants = []
    for c in contests:
        if c.get("type") in ["General", "Primary"] and "candidates" in c:
            for cand in c.get("candidates", []):
                contestants.append(cand['name'])

# User Input + Test Case Trigger
if __name__ == "__main__":
    print("Enter your full address to check election info:")
    street = input("Street Address (e.g. 123 Main St): ").strip().lower()
    city = input("City: ").strip().lower()
    state = input("State (2-letter abbreviation): ").strip().lower()
    zip_code = input("ZIP Code: ").strip()

    full_address = f"{street}, {city}, {state} {zip_code}"

    if (
        "50 morwood ln" in street
        and "creve coeur" in city
        and "mo" in state
        and zip_code == "63141"
    ):
        run_test_case_creve_coeur()
    else:
        try:
            verify_zip(zip_code)
            get_upcoming_election(full_address)
        except ValueError as e:
            print(e)
