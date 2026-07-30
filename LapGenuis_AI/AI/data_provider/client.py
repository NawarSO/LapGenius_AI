import requests
import time
from AI.config import LAPTOPS_URL

def fetch_all_laptops():
    page = 1
    url = LAPTOPS_URL
    laptops = []
    
    print('client send laptops requests file 1...')
    while url:
        t = time.time()
        response = requests.get(url)
        print(f"Page {page}: {time.time()-t:.2f}s")
        page += 1
        if response.status_code == 200:
            payload = response.json()
            laptops.extend(payload['data']['data'])
            url = payload['data']['next_page_url']

        else:
            print(f"Error: {response.status_code}")
            break
    
    return laptops