

import requests

API_KEY = "dx9aEV5E5n4K5gdWh8wJlowjPAc525bX85wq0KDm"

url = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json"

headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

response = requests.get(url, headers=headers)


print("Status Code:", response.status_code)

if response.status_code != 200:
    print(response.text)


data = response.json()

print(data.keys())


print("Total Complexes:", len(data["complexes"]))

print(data["complexes"][0])


complexes_list = []
venues_list = []


print(type(complexes_list))
print(type(venues_list))


for complex_item in data["complexes"]:

    complexes_list.append({
        "complex_id": complex_item["id"],
        "complex_name": complex_item["name"]
    })


print("Extracted Complexes:", len(complexes_list))


# ==========================================
# CHECK FOR COMPLEXES WITH NO VENUES
# ==========================================

missing_venues = 0

for complex_item in data["complexes"]:

    if "venues" not in complex_item:
        missing_venues += 1

print("Complexes Missing Venues:", missing_venues)


# ==========================================
# EXTRACT VENUES
# ==========================================

for complex_item in data["complexes"]:

    if "venues" in complex_item:

        for venue in complex_item["venues"]:

            venues_list.append({
                "venue_id": venue["id"],
                "venue_name": venue["name"],
                "city_name": venue["city_name"],
                "country_name": venue["country_name"],
                "country_code": venue["country_code"],
                "timezone": venue["timezone"],
                "complex_id": complex_item["id"]
            })

print("Extracted Venues:", len(venues_list))


print(complexes_list[0])

print(venues_list[0])


import pandas as pd

# Create DataFrames
complexes_df = pd.DataFrame(complexes_list)
venues_df = pd.DataFrame(venues_list)

# Save CSV files
complexes_df.to_csv("data/complexes.csv", index=False)
venues_df.to_csv("data/venues.csv", index=False)

print("Complexes CSV Created Successfully")
print("Venues CSV Created Successfully")

