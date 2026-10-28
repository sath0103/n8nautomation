import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=10)
print("HTTP Status Code:", response.status_code)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Find headline elements using the selector we inspected
items = soup.select('h2[data-testid="card-headline"]')

print("Headlines found:", len(items))

for item in items[:5]:
    print(item.get_text(strip=True))