import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from pathlib import Path

CSV_PATH = Path("data/flights.csv")
CSV_PATH.parent.mkdir(exist_ok=True)

# Konfigūracija
params = {
    "searchtype": "flexi",
    "origin": "vilnius",
    "destination": "milan",
    "adults": "1",
    "children": "0",
    "infants": "0",
    "minDaysStay": "0",
    "maxDaysStay": "0",
    "departure": "2025-09-04",
    "return": "",
    "oneway": "1",
    "currency": "eur",
    "submit": "Search"
}

print("🔍 Siunčiam užklausą...")
response = requests.get("https://www.azair.eu/azair/", params=params)
soup = BeautifulSoup(response.text, "html.parser")
rows = soup.select(".resultTable tr[class^='resultRow']")

offers = []
for row in rows:
    try:
        price = row.select_one(".resultPrice").get_text(strip=True).replace("€", "").strip()
        from_time = row.select_one(".from").get_text(strip=True)
        to_time = row.select_one(".to").get_text(strip=True)
        duration = row.select_one(".duration").get_text(strip=True)
        airline = row.select_one(".res_airline").get_text(strip=True)

        offers.append(dict(
            date_checked=datetime.utcnow().strftime("%Y-%m-%d"),
            departure_date="2025-09-04",
            from_city="Vilnius",
            to_city="Milan",
            price_eur=int(price),
            airline=airline,
            departure_time=from_time,
            arrival_time=to_time,
            duration=duration
        ))
    except Exception as e:
        continue

print(f"✅ Rasta {len(offers)} pasiūlymų.")

if not offers:
    print("⚠️ Nepavyko rasti pasiūlymų.")
    exit()

# 3 pigiausi
offers = sorted(offers, key=lambda x: x["price_eur"])[:3]
df = pd.DataFrame(offers)
df.to_csv(CSV_PATH, mode="a", index=False, header=not CSV_PATH.exists())
print("💾 CSV atnaujintas.")
