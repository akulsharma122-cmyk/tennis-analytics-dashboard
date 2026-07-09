

import sqlite3
import pandas as pd


# Connect to SQLite Database
conn = sqlite3.connect("database/tennis_analytics.db")

# Create Cursor
cursor = conn.cursor()


cursor.execute("PRAGMA foreign_keys = ON;")


# ==========================================
# LOAD COMPETITOR RANKINGS DATA
# ==========================================

competitor_rankings_df = pd.read_csv("data/competitor_rankings.csv")

# Check for missing values
print("Missing values per column:")
print(competitor_rankings_df.isnull().sum())

# Show rows containing NULL values
print("\nRows with NULL values:")
print(competitor_rankings_df[competitor_rankings_df.isnull().any(axis=1)])

# Check for empty strings in object columns
for column in competitor_rankings_df.select_dtypes(include="object").columns:
    empty_rows = competitor_rankings_df[competitor_rankings_df[column] == ""]
    print(f"\nRows with Empty {column}:")
    print(empty_rows)

# Display unique values for each text column
for column in competitor_rankings_df.select_dtypes(include="object").columns:
    print(f"\nUnique values in {column}:")
    print(competitor_rankings_df[column].unique())

# Load data into SQLite
competitor_rankings_df.to_sql(
    "competitor_rankings",
    conn,
    if_exists="append",
    index=False
)

print("Competitor Rankings Loaded Successfully!")


# ============================================
# SAVE CHANGES AND CLOSE DATABASE
# ============================================

conn.commit()
conn.close()

print("All Data Loaded Successfully!")

