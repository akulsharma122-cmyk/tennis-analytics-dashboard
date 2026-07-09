

"""
===============================================================================
PROJECT: Game Analytics - Unlocking Tennis Data with SportRadar API
MODULE: Doubles Competitor Rankings Data Extraction
AUTHOR: Akul Sharma

PURPOSE:
Extract doubles competitor rankings data from the SportRadar Tennis API,
transform nested JSON data into a relational format, and prepare it
for loading into the MySQL database.

API ENDPOINT:
Doubles Competitor Rankings Endpoint

TABLES POPULATED:
1. Competitors
2. Competitor_Rankings

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

DOUBLES_RANKINGS_URL = (
    "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json"
)


# =============================================================================
# REQUEST HEADERS
# =============================================================================

headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}


# =============================================================================
# SEND REQUEST
# =============================================================================

response = requests.get(
    DOUBLES_RANKINGS_URL,
    headers=headers
)

print("Status Code:", response.status_code)


# =============================================================================
# CONVERT RESPONSE TO JSON
# =============================================================================

data = response.json()

print(data.keys())


# =============================================================================
# INSPECT RANKINGS STRUCTURE
# =============================================================================

rankings = data["rankings"]

print("Number of Rankings Objects:", len(rankings))

print("\nFirst Rankings Object:\n")

print(json.dumps(rankings[0], indent=4))



# =============================================================================
# INSPECT RANKING GROUPS
# =============================================================================

print("\nRANKING GROUPS FOUND:\n")

for ranking in rankings:

    print(
        ranking["name"],
        "|",
        ranking["gender"],
        "|",
        ranking["year"],
        "|",
        ranking["week"]
    )


# =============================================================================
# CREATE EXTRACTION LISTS
# =============================================================================

competitors_data = []

competitor_rankings_data = []

missing_country_code = 0


# =============================================================================
# EXTRACT ATP + WTA COMPETITOR DATA
# =============================================================================

for ranking_group in rankings:

    competitor_rankings = ranking_group.get("competitor_rankings", [])

    for record in competitor_rankings:

        competitor = record.get("competitor", {})

        # ---------------------------------------------------------
        # TRACK MISSING COUNTRY CODES
        # ---------------------------------------------------------

        if competitor.get("country_code") is None:
            missing_country_code += 1

        # ---------------------------------------------------------
        # COMPETITORS TABLE
        # ---------------------------------------------------------

        competitors_data.append({

            "competitor_id": competitor.get("id"),
            "name": competitor.get("name"),
            "country": competitor.get("country"),
            "country_code": competitor.get("country_code"),
            "abbreviation": competitor.get("abbreviation")

        })

        # ---------------------------------------------------------
        # COMPETITOR RANKINGS TABLE
        # ---------------------------------------------------------

        competitor_rankings_data.append({

            "rank": record.get("rank"),
            "movement": record.get("movement"),
            "points": record.get("points"),
            "competitions_played": record.get("competitions_played"),
            "competitor_id": competitor.get("id")

        })


# =============================================================================
# VALIDATION CHECKS
# =============================================================================

print("\nCompetitors Extracted:", len(competitors_data))

print("Ranking Records Extracted:", len(competitor_rankings_data))

print("Missing Country Codes:", missing_country_code)

print("\nSample Competitor:")

print(competitors_data[0])

print("\nSample Ranking:")

print(competitor_rankings_data[0])



# =============================================================================
# CREATE DATAFRAMES
# =============================================================================

competitors_df = pd.DataFrame(competitors_data)

competitor_rankings_df = pd.DataFrame(competitor_rankings_data)


# =============================================================================
# EXPORT CSV FILES
# =============================================================================

competitors_df.to_csv(
    "data/competitors.csv",
    index=False
)

competitor_rankings_df.to_csv(
    "data/competitor_rankings.csv",
    index=False
)

print("\nCompetitors CSV Created Successfully")

print("Competitor Rankings CSV Created Successfully")

