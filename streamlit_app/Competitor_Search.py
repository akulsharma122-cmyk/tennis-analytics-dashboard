

# ======================================================
# IMPORT LIBRARIES
# ======================================================

import streamlit as st
import sqlite3
import pandas as pd
import os


# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Competitor Search",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
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
        Click below to return to the Homepage.
        """
    )

    st.markdown("---")

    st.button(
        "🏠 Return to Homepage",
        use_container_width=True,
        disabled=True
    )

    st.markdown("---")

    st.caption("SportRadar Tennis Analytics Dashboard")





# ======================================================
# DATABASE CONNECTION
# ======================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(
    BASE_DIR,
    "..",
    "database",
    "tennis_analytics.db"
)

db_path = os.path.abspath(db_path)

conn = sqlite3.connect(db_path)


# ======================================================
# PAGE TITLE
# ======================================================

st.title("🎾 Competitor Search")

st.write("Search and filter competitors using ranking information.")

st.write("---")





# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.title("🎾 Filters")

# ------------------------------------------
# SEARCH COMPETITOR
# ------------------------------------------

search_name = st.sidebar.text_input(
    "Search Competitor",
    placeholder="Enter competitor name..."
)

# ------------------------------------------
# COUNTRY FILTER
# ------------------------------------------

country_query = """
SELECT DISTINCT country
FROM competitors
ORDER BY country;
"""

country_df = pd.read_sql_query(country_query, conn)

country_options = ["All"] + country_df["country"].tolist()

selected_country = st.sidebar.selectbox(
    "Country",
    country_options
)

# ------------------------------------------
# RANK FILTER
# ------------------------------------------

selected_rank = st.sidebar.slider(
    "Maximum Rank",
    min_value=1,
    max_value=1000,
    value=100
)

# ------------------------------------------
# POINTS FILTER
# ------------------------------------------

selected_points = st.sidebar.slider(
    "Minimum Points",
    min_value=0,
    max_value=11000,
    value=0
)



# ============================================
# FILTERED COMPETITORS
# ============================================

query = """
SELECT
    c.name,
    c.country,
    r.rank,
    r.points,
    r.movement,
    r.competitions_played

FROM competitors c

JOIN competitor_rankings r
ON c.competitor_id = r.competitor_id

WHERE
    c.name LIKE ?
    AND (? = 'All' OR c.country = ?)
    AND r.rank <= ?
    AND r.points >= ?

ORDER BY r.rank ASC
"""

filtered_df = pd.read_sql_query(
    query,
    conn,
    params=(
        "%" + search_name + "%",
        selected_country,
        selected_country,
        selected_rank,
        selected_points
    )
)


# ============================================
# FILTERED RESULTS
# ============================================

st.write("---")

st.subheader("Filtered Competitors")

st.metric(
    label="Competitors Found",
    value=len(filtered_df)
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


