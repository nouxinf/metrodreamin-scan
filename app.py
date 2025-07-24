import base64
import requests
import time
from bs4 import BeautifulSoup

user_id = "BQ14RUqUj5T9qo6l9Mzha98HWaB3"
BASE_URL = "https://metrodreamin.com/view/"
MAX_MISSES = 20
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

def encode_id(usr_id, num):
    combined = f"{usr_id}|{num}"
    encoded_bytes = base64.urlsafe_b64encode(combined.encode())
    return encoded_bytes.decode()

def check_url(encoded_id):
    url = f"{BASE_URL}{encoded_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 404 or "Map not found" in response.text:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        title_element = soup.find('h1', class_='Title-heading')
        if title_element:
            return title_element.text.strip()
        return "Untitled map"
    except requests.RequestException:
        return None

misses = 0
i = 10
for i in range(1000):
    print(f"looking at ID {i}")
    encoded = encode_id(user_id, i)
    result = check_url(encoded)
    if result:
        print(f"FOUND: {BASE_URL}{encoded}")
        print(f"TITLE: {result}")
        misses = 0
    else:
        print("NONE FOUND")
        misses += 1
        if misses >= MAX_MISSES:
            print(f"Gave up after {misses} misses.")
            break
    time.sleep(3)
