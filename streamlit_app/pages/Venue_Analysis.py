

# =====================================================
# IMPORT LIBRARIES
# =====================================================

import streamlit as st
import pandas as pd
import sqlite3

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Venue Analysis",
    page_icon="🏟️",
    layout="wide"
)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("🏟️ Venue Analysis")

st.write(
    "Analyze tennis venues and complexes from the SportRadar database."
)

st.write("---")

# =====================================================
# CONNECT TO DATABASE
# =====================================================

conn = sqlite3.connect("database/tennis_analytics.db")

# =====================================================
# LOAD VENUE DATA
# =====================================================

venue_query = """
SELECT
    venue_name,
    city_name,
    country_name,
    timezone,
    complex_name
FROM venues
LEFT JOIN complexes
ON venues.complex_id = complexes.complex_id;
"""

venues_df = pd.read_sql_query(venue_query, conn)

# =====================================================
# END OF FIRST SECTION
# =====================================================


# =====================================================
# VENUE STATISTICS
# =====================================================

st.header("Venue Statistics")

summary_query = """
SELECT
    COUNT(*) AS total_venues,
    COUNT(DISTINCT country_name) AS total_countries,
    COUNT(DISTINCT complex_id) AS total_complexes
FROM venues;
"""

summary = pd.read_sql_query(summary_query, conn)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Venues",
        int(summary["total_venues"][0])
    )

with col2:
    st.metric(
        "Total Countries",
        int(summary["total_countries"][0])
    )

with col3:
    st.metric(
        "Total Complexes",
        int(summary["total_complexes"][0])
    )

st.write("---")


# =====================================================
# SELECT COUNTRY
# =====================================================

st.header("Select Country")

country_query = """
SELECT DISTINCT country_name
FROM venues
ORDER BY country_name;
"""

country_list = pd.read_sql_query(
    country_query,
    conn
)

country_options = ["All Countries"] + country_list["country_name"].tolist()

selected_country = st.selectbox(
    "Choose a Country",
    country_options
)

st.write("Selected Country:", selected_country)

st.write("---")



# =====================================================
# VENUES TABLE
# =====================================================

st.header("Venues from Selected Country")

# SQL Query
if selected_country == "All Countries":

    venue_query = """
    SELECT
        venue_name,
        city_name,
        country_name,
        timezone,
        complex_name
    FROM venues
    LEFT JOIN complexes
        ON venues.complex_id = complexes.complex_id
    ORDER BY country_name, venue_name;
    """

else:

    venue_query = f"""
    SELECT
        venue_name,
        city_name,
        country_name,
        timezone,
        complex_name
    FROM venues
    LEFT JOIN complexes
        ON venues.complex_id = complexes.complex_id
    WHERE country_name = '{selected_country}'
    ORDER BY venue_name;
    """

venue_table = pd.read_sql_query(
    venue_query,
    conn
)

st.write(
    "Venues Found:",
    len(venue_table)
)

st.dataframe(
    venue_table,
    use_container_width=True,
    hide_index=True
)

st.write("---")


