import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

# Konstantos
URL = "https://www.azair.eu/"

# Užklausa
params = {
    "searchtype": "flexi",
    "from": "VNO",
    "to": "Milan",
    "depdate": "2025-09-04",
    "adults": "1",
    "maxChng": "0",
    "index_submit": "Search"
}
headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(URL, params=params, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Išsaugome HTML debug’ui
with open("azair_page_debug.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

# CSV failas
os.makedirs("data", exist_ok=True)
csv_path = "data/flights.csv"
today = datetime.today().strftime("%Y-%m-%d")

# Ištraukiame duomenis (ši dalis priklauso nuo HTML struktūros)
offers = soup.find_all("tr", class_="result")
if not offers:
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([today, "no data", "no data", "no data"])
else:
    for offer in offers[:3]:  # Tik 3 pigiausi
        time = offer.find("td", class_="departure").text.strip() if offer.find("td", class_="departure") else "?"
        airport = offer.find("td", class_="airport").text.strip() if offer.find("td", class_="airport") else "?"
        price = offer.find("td", class_="price").text.strip() if offer.find("td", class_="price") else "?"
        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([today, time, airport, price])
