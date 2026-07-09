

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
    page_title="Competition Analysis",
    page_icon="🏆",
    layout="wide"
)

# =====================================================
# PAGE TITLE
# =====================================================

st.title("🏆 Competition Analysis")

st.write(
    "Analyze tennis competitions using the SportRadar database."
)

st.write("---")

# =====================================================
# CONNECT TO DATABASE
# =====================================================

conn = sqlite3.connect("database/tennis_analytics.db")

# =====================================================
# LOAD COMPETITION DATA
# =====================================================

competition_query = """
SELECT
    competition_name,
    type,
    gender,
    category_name
FROM competitions
LEFT JOIN categories
ON competitions.category_id = categories.category_id;
"""

competition_df = pd.read_sql_query(
    competition_query,
    conn
)

# =====================================================
# END OF FIRST SECTION
# =====================================================



# =====================================================
# COMPETITION STATISTICS
# =====================================================

st.header("Competition Statistics")

statistics_query = """
SELECT

COUNT(*) AS total_competitions,

SUM(CASE
        WHEN LOWER(type)='singles'
        THEN 1
        ELSE 0
    END) AS singles_competitions,

SUM(CASE
        WHEN LOWER(type)='doubles'
        THEN 1
        ELSE 0
    END) AS doubles_competitions,

COUNT(DISTINCT category_name) AS total_categories

FROM competitions

LEFT JOIN categories
ON competitions.category_id = categories.category_id;
"""

statistics = pd.read_sql_query(
    statistics_query,
    conn
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Competitions",
        int(statistics["total_competitions"][0])
    )

with col2:
    st.metric(
        "Singles",
        int(statistics["singles_competitions"][0])
    )

with col3:
    st.metric(
        "Doubles",
        int(statistics["doubles_competitions"][0])
    )

with col4:
    st.metric(
        "Categories",
        int(statistics["total_categories"][0])
    )

st.write("---")


# =====================================================
# CATEGORY FILTER
# =====================================================

st.header("Select Category")

category_list = pd.read_sql_query(
    """
    SELECT DISTINCT category_name
    FROM categories
    ORDER BY category_name
    """,
    conn
)

category_options = ["All Categories"] + category_list["category_name"].tolist()

selected_category = st.selectbox(
    "Choose a Category",
    category_options
)

st.write("Selected Category:", selected_category)

st.write("---")



# =====================================================
# COMPETITIONS TABLE
# =====================================================

st.header("Competitions")

if selected_category == "All Categories":

    competitions_query = """
    SELECT
        competitions.competition_name,
        competitions.type,
        competitions.gender,
        categories.category_name

    FROM competitions

    LEFT JOIN categories
    ON competitions.category_id = categories.category_id

    ORDER BY competitions.competition_name
    """

else:

    competitions_query = f"""
    SELECT
        competitions.competition_name,
        competitions.type,
        competitions.gender,
        categories.category_name

    FROM competitions

    LEFT JOIN categories
    ON competitions.category_id = categories.category_id

    WHERE categories.category_name = '{selected_category}'

    ORDER BY competitions.competition_name
    """

competitions_df = pd.read_sql_query(
    competitions_query,
    conn
)

st.write(
    "Competitions Found:",
    len(competitions_df)
)

st.dataframe(
    competitions_df,
    use_container_width=True,
    height=450
)

st.write("---")


