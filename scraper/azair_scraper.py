import requests, pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

# ---------- Failo kelias ----------
CSV_PATH = Path("data/flights.csv")
CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

# ---------- Azair užklausa ----------
params = {
    "searchtype": "flexi",
    "origin": "Vilnius",
    "destination": "Milan",
    "adults": "1",
    "children": "0",
    "infants": "0",
    "minDaysStay": "0",
    "maxDaysStay": "0",
    "oneway": "1",
    "departure": "2025-09-04",
    "currency": "eur",
    "submit": "Search"
}
url = "https://www.azair.eu/azair/"
headers = {"User-Agent": "Mozilla/5.0"}
print("🔍 Sending request to Azair…")
html = requests.get(url, params=params, headers=headers, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

# ---------- Rezultatų parinkimas ----------
rows = soup.select(".resultTable tr[class^='resultRow']")
offers = []
for row in rows:
    try:
        price_txt = row.select_one(".resultPrice").get_text(strip=True)
        price = int(price_txt.replace("€", "").replace("\xa0", ""))
        airline = row.select_one(".res_airline").get_text(strip=True)
        times = row.select_all(".res_time")
    except Exception:
        continue
    if len(times) >= 2:
        offers.append({
            "date_checked": datetime.utcnow().strftime("%Y-%m-%d"),
            "departure_date": "2025-09-04",
            "from_city": "Vilnius",
            "to_city": "Milan",
            "price_eur": price,
            "airline": airline,
            "departure_time": times[0].text.strip(),
            "arrival_time": times[1].text.strip()
        })

print(f"✅ Found {len(offers)} offers.")
if not offers:
    exit()

# ---------- 3 pigiausi + CSV ----------
offers = sorted(offers, key=lambda x: x["price_eur"])[:3]
df = pd.DataFrame(offers)
df.to_csv(CSV_PATH, mode="a", header=not CSV_PATH.exists(), index=False)
print("💾 CSV updated.")
