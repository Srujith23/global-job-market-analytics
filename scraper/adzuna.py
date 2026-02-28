from dotenv import load_dotenv
import os
import requests

load_dotenv()

APPID = os.getenv('ADZUNA_APP_ID')
APIKEY = os.getenv('ADZUNA_APP_KEY')

def fetch_jobs(country, page, app_id=APPID, api_key=APIKEY, what='data analyst'):
    BASE_URL = "https://api.adzuna.com/v1/api/jobs"
    url = f"{BASE_URL}/{country}/search/{page}"
    params = {
        "app_id": app_id,
        "app_key": api_key,
        "what": what,
        "results_per_page": 50,
        "content-type": "application/json"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
