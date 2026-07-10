

# =====================================================
# IMPORT LIBRARIES
# =====================================================

import streamlit as st
import sqlite3
import pandas as pd
import os


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Country Analysis",
    page_icon="🌍",
    layout="wide"
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🎾 Tennis Analytics")

    st.markdown("---")

    st.subheader("Navigation")

    st.info(
        "Return to the main dashboard."
    )

    st.markdown("---")

    st.markdown("---")

    st.caption("SportRadar Tennis Analytics Dashboard")




# =====================================================
# DATABASE CONNECTION
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(
    BASE_DIR,
    "..",
    "..",
    "database",
    "tennis_analytics.db"
)

db_path = os.path.abspath(db_path)

conn = sqlite3.connect(db_path)


# =====================================================
# PAGE TITLE
# =====================================================

st.title("🌍 Country Analysis")

st.write(
    "Analyze competitors by country using ranking information."
)

st.write("---")


# =====================================================
# COUNTRY SELECTION
# =====================================================

st.header("Select Country")

# Load Countries
country_list = pd.read_sql_query(
    """
    SELECT DISTINCT country
    FROM competitors
    ORDER BY country;
    """,
    conn
)

country_options = ["All Countries"] + country_list["country"].tolist()

selected_country = st.selectbox(
    "Choose a Country",
    country_options
)

st.write("Selected Country:", selected_country)

st.write("---")


# ============================================
# COUNTRY SUMMARY
# ============================================


# SQL Query

if selected_country == "All Countries":

    summary_query = """
    SELECT
        COUNT(*) AS total_competitors,
        ROUND(AVG(cr.rank),0) AS average_rank,
        ROUND(AVG(cr.points),0) AS average_points

    FROM competitors c

    JOIN competitor_rankings cr
        ON c.competitor_id = cr.competitor_id
    """

    summary = pd.read_sql_query(summary_query, conn)

else:

    summary_query = f"""
    SELECT
        COUNT(*) AS total_competitors,
        ROUND(AVG(cr.rank),0) AS average_rank,
        ROUND(AVG(cr.points),0) AS average_points

    FROM competitors c

    JOIN competitor_rankings cr
        ON c.competitor_id = cr.competitor_id

    WHERE c.country = '{selected_country}'
    """

    summary = pd.read_sql_query(summary_query, conn)




# Display Summary

st.write("### Country Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Competitors",
        int(summary["total_competitors"][0])
    )

with col2:
    st.metric(
        "Average Rank",
        int(summary["average_rank"][0])
    )

with col3:
    st.metric(
        "Average Points",
        int(summary["average_points"][0])
    )


st.write("----")


# ==========================================
# COMPETITORS FROM SELECTED COUNTRY
# ==========================================

st.header("Competitors from Selected Country")

if selected_country == "All Countries":

    competitors_query = """
    SELECT
        c.name,
        c.country,
        cr.rank,
        cr.points,
        cr.competitions_played

    FROM competitors c

    JOIN competitor_rankings cr
        ON c.competitor_id = cr.competitor_id

    ORDER BY cr.rank
    """

else:

    competitors_query = f"""
    SELECT
        c.name,
        c.country,
        cr.rank,
        cr.points,
        cr.competitions_played

    FROM competitors c

    JOIN competitor_rankings cr
        ON c.competitor_id = cr.competitor_id

    WHERE c.country = '{selected_country}'

    ORDER BY cr.rank
    """

competitors_df = pd.read_sql_query(
    competitors_query,
    conn
)

st.write("Competitors Found:", len(competitors_df))

st.dataframe(
    competitors_df,
    use_container_width=True
)

st.write("-----")


