import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

# 🔗 Paieškos URL (one way, Vilnius -> Milan, 2025-09-04)
url = (
    "https://www.azair.eu/?searchtype=flexi&tp=oneway&src=VNO&dst=MIL&"
    "date=2025-09-04&ad=1&ch=0&in=0&bags=0&currency=eur&submit=Search"
)

# 💬 Užklausos HEADERS (kad atrodytų kaip naršyklė)
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

# 🔄 Siunčiame GET užklausą
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# 💾 Saugom visą HTML debug'ui (laikinai)
with open("azair_page_debug.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

# 🔍 Ieškom visų pasiūlymų
results = soup.select("div.result")
data = []

for result in results[:3]:  # paimkim tik 3 pigiausius (pirmi sąraše)
    try:
        time = result.select_one("div.time").text.strip()
        airport = result.select_one("div.airport").text.strip()
        price = result.select_one("div.price").text.strip()

        data.append({
            "date": datetime.today().strftime("%Y-%m-%d"),
            "time": time,
            "airport": airport,
            "price": price,
        })
    except Exception as e:
        continue

# 📁 CSV failas
csv_file = "data/flights.csv"

# 🔘 Sukuriam failą su header jei dar neegzistuoja
file_exists = os.path.isfile(csv_file)
with open(csv_file, mode="a", newline="", encoding="utf-8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=["date", "time", "airport", "price"])

    if not file_exists:
        writer.writeheader()

    for row in data:
        writer.writerow(row)

# Jei nerasta nei vieno rezultato – sukuriam tuščią eilutę kad matytum dieną
if not data:
    with open(csv_file, mode="a", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=["date", "time", "airport", "price"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "date": datetime.today().strftime("%Y-%m-%d"),
            "time": "no data",
            "airport": "no data",
            "price": "no data"
        })
