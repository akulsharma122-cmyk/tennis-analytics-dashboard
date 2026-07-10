

# ==========================================
# IMPORT LIBRARIES
# ==========================================

import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Tennis Analytics Dashboard",
    page_icon="🎾",
    layout="wide"
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🎾 Tennis Analytics")

    st.markdown("---")

    st.subheader("Navigation")

    st.info(
        """
        Use the navigation menu on the left
        to explore each section of the project.
        """
    )

    st.markdown("---")

    st.subheader("Project Pages")

    st.write("🏠 Home")

    st.page_link(
         "pages/Competitor_Search.py",
          label="🔍 Competitor Search"
         )

    st.page_link(
         "pages/Competitor_Details.py",
        label="👤 Competitor Details"
               )

    st.page_link(
       "pages/Country_Analysis.py",
        label="🌍 Country Analysis"
           )

    st.page_link(
        "pages/Venue_Analysis.py",
        label="🏟️ Venue Analysis"
         )

    st.page_link(
        "pages/Competition_Analysis.py",
         label="🏆 Competition Analysis"
           )

    st.markdown("---")

    st.caption("SportRadar Tennis Analytics Dashboard")





# ==========================================
# DATABASE CONNECTION
# ==========================================


import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "..", "database", "tennis_analytics.db")
db_path = os.path.abspath(db_path)



conn = sqlite3.connect(db_path)



# ==========================================
# PAGE TITLE
# ==========================================

st.title("🎾 Tennis Analytics Dashboard")

st.write("Welcome to the Tennis Analytics Dashboard.")

st.write("---")



# ==========================================
# SUMMARY STATISTICS
# ==========================================

st.subheader(" Summary Statistics")


total_competitors = pd.read_sql_query("""
SELECT COUNT(*) AS Total_Competitors
FROM competitors;
""", conn)

total_countries = pd.read_sql_query("""
SELECT COUNT(DISTINCT country)
AS Total_Countries
FROM competitors;
""", conn)

highest_points = pd.read_sql_query("""
SELECT MAX(points)
AS Highest_Points
FROM competitor_rankings;
""", conn)

total_competitions = pd.read_sql_query("""
SELECT COUNT(*)
AS Total_Competitions
FROM competitions;
""", conn)


summary_df = pd.DataFrame({

    "Metric": [

        "Total Competitors",
        "Countries Represented",
        "Highest Points",
        "Total Competitions"

    ],

    "Value": [

        total_competitors.iloc[0,0],
        total_countries.iloc[0,0],
        highest_points.iloc[0,0],
        total_competitions.iloc[0,0]

    ]

})

st.table(summary_df)



# ==========================================
# TOP 10 RANKED COMPETITORS
# ==========================================

st.subheader(" Top 10 Ranked Competitors")


top_ranked = pd.read_sql_query("""

SELECT
    c.name,
    c.country,
    r.rank,
    r.points

FROM competitor_rankings r

JOIN competitors c
ON r.competitor_id = c.competitor_id

ORDER BY r.rank ASC

LIMIT 10;

""", conn)


st.dataframe(
    top_ranked,
    use_container_width=True,
    hide_index=True
)



# ==========================================
# COUNTRIES REPRESENTED
# ==========================================

st.subheader("Countries Represented")


countries = pd.read_sql_query("""

SELECT
    country,
    COUNT(*) AS competitors

FROM competitors

GROUP BY country

ORDER BY competitors DESC;

""", conn)


st.dataframe(
    countries,
    use_container_width=True,
    hide_index=True
)



# ==========================================
# TOP 10 HIGHEST POINTS COMPETITORS
# ==========================================


st.subheader(" Top 10 Highest Points Competitors")


highest_points_table = pd.read_sql_query("""

SELECT
    c.name,
    c.country,
    r.points

FROM competitor_rankings r

JOIN competitors c
ON r.competitor_id = c.competitor_id

ORDER BY r.points DESC

LIMIT 10;

""", conn)


st.dataframe(
    highest_points_table,
    use_container_width=True,
    hide_index=True
)






