# src/hypermodern_python/wikipedia.py
import requests

API_URL = "https://vi.wikipedia.org/api/rest_v1/page/random/summary"

def random_page():
    with requests.get(API_URL) as response:
        response.raise_for_status()
        return response.json()
