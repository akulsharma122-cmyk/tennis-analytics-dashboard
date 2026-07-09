

"""
===============================================================================
PROJECT: Game Analytics - Unlocking Tennis Data with SportRadar API
MODULE: Competition Data Extraction
AUTHOR: Akul Sharma

PURPOSE:
Extract competition and category data from the SportRadar Tennis API,
transform nested JSON data into a relational format, and prepare it
for loading into the MySQL database.

API ENDPOINT:
Competitions Endpoint

TABLES POPULATED:
1. Categories
2. Competitions

===============================================================================
"""


# =============================================================================
# IMPORT LIBRARIES
# =============================================================================

import requests
import json
import pandas as pd



# =============================================================================
# API CONFIGURATION
# =============================================================================

API_KEY = "dx9aEV5E5n4K5gdWh8wJlowjPAc525bX85wq0KDm"

COMPETITIONS_URL = (
    "https://api.sportradar.com/tennis/trial/v3/en/competitions.json"
)


# =============================================================================
# REQUEST HEADERS
# =============================================================================

headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}


# =============================================================================
# FETCH COMPETITION DATA
# =============================================================================

response = requests.get(
    COMPETITIONS_URL,
    headers=headers
)

print("Status Code:", response.status_code) 


# =============================================================================
# VIEW RESPONSE STRUCTURE
# =============================================================================

data = response.json()

print(data.keys())

# ============================================================
# EXTRACT COMPETITIONS LIST
# ============================================================

competitions = data["competitions"]

print("Total Competitions:", len(competitions))


# ============================================================
# VIEW FIRST COMPETITION RECORD
# ============================================================

print(competitions[0])


# ============================================================
# VIEW ANOTHER COMPETITION RECORD
# ============================================================

print(competitions[10])


# ============================================================
# EXTRACT UNIQUE CATEGORIES
# ============================================================

categories = []

for competition in competitions:
    
    category = competition["category"]
    
    categories.append({
        "category_id": category["id"],
        "category_name": category["name"]
    })

categories_df = pd.DataFrame(categories)

categories_df = categories_df.drop_duplicates()

print("Total Categories:", len(categories_df))

print(categories_df.head())


# ============================================================
# CREATE COMPETITIONS DATAFRAME
# ============================================================

# ==========================================================
# CREATE COMPETITIONS DATAFRAME
# ==========================================================

competition_records = []

for competition in competitions:

    competition_records.append({
        "competition_id": competition.get("id"),
        "competition_name": competition.get("name"),
        "parent_id": competition.get("parent_id"),
        "type": competition.get("type"),
        "gender": competition.get("gender"),
        "category_id": competition.get("category", {}).get("id")
    })

competitions_df = pd.DataFrame(competition_records)

print("Total Competition Records:", len(competitions_df))

print(competitions_df.head())



# ==========================================================
# EXPORT DATA TO CSV
# ==========================================================

categories_df.to_csv(
    "data/categories.csv",
    index=False
)

competitions_df.to_csv(
    "data/competitions.csv",
    index=False
)

print("CSV files exported successfully.")






