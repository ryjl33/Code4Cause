import requests

API_KEY = 'uDnojcUfucxrzpEhZwckQJBO8zMXOeaBV4S5ueks'
BASE_URL = 'https://api.open.fec.gov/v1/election-dates/'

def get_election_dates(year):
    params = {
        'year': year,
        'api_key': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

election_dates = get_election_dates(2024)
print(election_dates)
