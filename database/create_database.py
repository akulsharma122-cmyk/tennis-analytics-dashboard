

import sqlite3


conn = sqlite3.connect("database/tennis_analytics.db")

# Create Cursor
cursor = conn.cursor()

# Enable Foreign Keys
cursor.execute("PRAGMA foreign_keys = ON;")

# ==========================================================
# CREATE CATEGORIES TABLE
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (

    category_id TEXT PRIMARY KEY,
    category_name TEXT NOT NULL

);
""")





# ==========================================================
# CREATE COMPETITIONS TABLE
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS competitions (

    competition_id TEXT PRIMARY KEY,
    competition_name TEXT NOT NULL,
    parent_id TEXT,
    type TEXT NOT NULL,
    gender TEXT NOT NULL,
    category_id TEXT,

    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)

);
""")






# ==========================================================
# CREATE COMPLEXES TABLE
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS complexes (

    complex_id TEXT PRIMARY KEY,
    complex_name TEXT NOT NULL

);
""")



# ==========================================================
# CREATE VENUES TABLE
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS venues (

    venue_id TEXT PRIMARY KEY,
    venue_name TEXT NOT NULL,
    city_name TEXT NOT NULL,
    country_name TEXT NOT NULL,
    country_code TEXT NOT NULL,
    timezone TEXT NOT NULL,
    complex_id TEXT,

    FOREIGN KEY (complex_id)
        REFERENCES complexes(complex_id)

);
""")




# ==========================================================
# CREATE COMPETITORS TABLE
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS competitors (

    competitor_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    country_code TEXT NOT NULL,
    abbreviation TEXT NOT NULL

);
""")


# ==========================================================
# CREATE COMPETITOR RANKINGS TABLE
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS competitor_rankings (

    rank_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rank INTEGER NOT NULL,
    movement INTEGER NOT NULL,
    points INTEGER NOT NULL,
    competitions_played INTEGER NOT NULL,
    competitor_id TEXT,

    FOREIGN KEY (competitor_id)
        REFERENCES competitors(competitor_id)

);
""")



conn.commit()
conn.close()

print("Database and Tables Created Successfully!")


