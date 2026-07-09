

import sqlite3
import pandas as pd


# Connect to SQLite Database
conn = sqlite3.connect("database/tennis_analytics.db")

# Create Cursor
cursor = conn.cursor()


cursor.execute("PRAGMA foreign_keys = ON;")



# =====================================================
# CLEAR EXISTING DATA
# =====================================================

cursor.execute("DELETE FROM competitor_rankings")
cursor.execute("DELETE FROM competitors")
cursor.execute("DELETE FROM venues")
cursor.execute("DELETE FROM complexes")
cursor.execute("DELETE FROM competitions")
cursor.execute("DELETE FROM categories")

conn.commit()


# =====================================================
# LOAD CATEGORIES DATA
# =====================================================

categories_df = pd.read_csv("data/categories.csv")


categories_df.to_sql(
    "categories",
    conn,
    if_exists="append",
    index=False
)

print("Categories Loaded Successfully!")


# =====================================================
# LOAD COMPETITIONS DATA
# =====================================================

competitions_df = pd.read_csv("data/competitions.csv")

competitions_df.to_sql(
    "competitions",
    conn,
    if_exists="append",
    index=False
)

print("Competitions Loaded Successfully!")


# ============================================
# LOAD COMPLEXES DATA
# ============================================

complexes_df = pd.read_csv("data/complexes.csv")

complexes_df.to_sql(
    "complexes",
    conn,
    if_exists="append",
    index=False
)

print("Complexes Loaded Successfully!")


# ============================================
# LOAD VENUES DATA
# ============================================

venues_df = pd.read_csv("data/venues.csv")

venues_df.to_sql(
    "venues",
    conn,
    if_exists="append",
    index=False
)

print("Venues Loaded Successfully!")



# ==========================================
# LOAD COMPETITIONS DATA
# ==========================================

competitions_df = pd.read_csv("data/competitions.csv")

# Check for missing values in the gender column
print("Missing Gender Values:", competitions_df["gender"].isnull().sum())

print("\nRows with NULL Gender:")
print(competitions_df[competitions_df["gender"].isnull()])

print("\nRows with Empty Gender:")
print(competitions_df[competitions_df["gender"] == ""])

competitions_df.to_sql(
    "competitions",
    conn,
    if_exists="append",
    index=False
)

print("Competitions Loaded Successfully!")


# ============================================
# LOAD COMPETITOR RANKINGS DATA
# ============================================

competitor_rankings_df = pd.read_csv("data/competitor_rankings.csv")

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



