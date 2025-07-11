import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

URL = "https://www.azair.eu/"

params = {
    "searchtype": "flexi",
    "srcAirport": "VNO",
    "dstAirport": "MIL",
    "adults": "1",
    "children": "0",
    "infants": "0",
    "minDaysStay": "0",
    "maxDaysStay": "0",
    "departureDate": "2025-09-04",
    "returnDate": "",
    "isOneway": "true",
    "currency": "eur",
    "lang": "en"
}

response = requests.get(URL, params=params, headers={"User-Agent": "Mozilla/5.0"})
html = response.text

# 🔍 Išsaugome HTML debugui
debug_path = "scraper/azair_page_debug.html"
with open(debug_path, "w", encoding="utf-8") as f:
    f.write(html)

soup = BeautifulSoup(html, "html.parser")
offers = soup.select(".result")

data = []
for offer in offers[:3]:  # tik pirmi 3 pasiūlymai
    try:
        time = offer.select_one(".departure .time").text.strip()
        airport = offer.select_one(".departure .airport").text.strip()
        price = offer.select_one(".result-price .price").text.strip()
        data.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": time,
            "airport": airport,
            "price": price
        })
    except:
        continue

# jei nėra pasiūlymų
if not data:
    data = [{
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "no data",
        "airport": "no data",
        "price": "no data"
    }]

df = pd.DataFrame(data)

output_file = "data/flights.csv"
header_needed = not os.path.exists(output_file)

df.to_csv(output_file, mode="a", index=False, header=header_needed)
