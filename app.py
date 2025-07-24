import base64
import requests
import time
from bs4 import BeautifulSoup
import re
from datetime import datetime
found_maps = []

BASE_URL = "https://metrodreamin.com/view/"
MAX_MISSES = 40
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def extract_user_id(user_input):
    match = re.search(r'/user/([a-zA-Z0-9]+)', user_input)
    return match.group(1) if match else user_input.strip()

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

# Ask the user for input
raw_input = input("Enter a Metrodreamin user ID or profile URL:\n> ")
user_id = extract_user_id(raw_input)

misses = 0
for i in range(1000):
    print(f"looking at ID {i}")
    encoded = encode_id(user_id, i)
    result = check_url(encoded)
    if result:
        print(f"FOUND: {BASE_URL}{encoded}")
        print(f"TITLE: {result}")
        misses = 0
        found_maps.append((i, f"{BASE_URL}{encoded}", result))
    else:
        print("NONE FOUND")
        misses += 1
        if misses >= MAX_MISSES:
            print(f"Gave up after {misses} misses.")
            break
    time.sleep(3)
html_filename = f"found_maps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
with open(html_filename, "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Found Metrodreamin Maps</title>\n")
    f.write("<style>body{font-family:sans-serif;padding:2em;} table{border-collapse:collapse;width:100%;} td,th{border:1px solid #ccc;padding:0.5em;} th{background:#eee;}</style>\n")
    f.write("</head>\n<body>\n")
    f.write("<h1>Found Metrodreamin Maps</h1>\n")
    f.write("<table>\n<tr><th>ID</th><th>Title</th><th>Link</th></tr>\n")
    for idx, url, title in found_maps:
        f.write(f"<tr><td>{idx}</td><td>{title}</td><td><a href='{url}' target='_blank'>{url}</a></td></tr>\n")
    f.write("</table>\n</body>\n</html>")

print(f"\nSaved {len(found_maps)} results to {html_filename}")

