import requests
from bs4 import BeautifulSoup
import os
from datetime import date
import csv

# Paieškos parametrai
params = {
    "searchtype": "flexi",
    "tp": "oneway",
    "src": "VNO",
    "dst": "MIL",
    "date": "2025-09-04",
    "ad": "1",
    "ch": "0",
    "in": "0",
    "bags": "0",
    "currency": "eur",
    "submit": "Search"
}

# Užklausos URL
url = "https://www.azair.eu/"

# Siunčiam užklausą
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, params=params, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Randam rezultatus
results = soup.find_all("div", class_="result")

if not results:
    print("❌ Skrydžių nerasta. Galbūt svetainė pasikeitė.")
else:
    # CSV failo kelias
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "flights.csv")
    file_exists = os.path.isfile(output_file)

    # Įrašom duomenis
    with open(output_file, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow(["date", "airline", "time", "price"])

        for result in results[:3]:  # Top 3 pasiūlymai
            airline = result.find("span", class_="company")
            depart = result.find("span", class_="depart-time")
            arrive = result.find("span", class_="arrive-time")
            price = result.find("span", class_="price")

            # Patikrinam ar viskas rasta
            if not (airline and depart and arrive and price):
                continue

            flight_time = f"{depart.get_text(strip=True)} → {arrive.get_text(strip=True)}"
            writer.writerow([
                str(date.today()),
                airline.get_text(strip=True),
                flight_time,
                price.get_text(strip=True)
            ])

    print("✅ CSV sėkmingai atnaujintas.")
