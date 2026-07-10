

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
    page_title="Competitor Details",
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
        Return to the main dashboard.
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





# =====================================================
# DATABASE CONNECTION
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(
    BASE_DIR,
    "..",
    "database",
    "tennis_analytics.db"
)

db_path = os.path.abspath(db_path)

conn = sqlite3.connect(db_path)


# =====================================================
# PAGE TITLE
# =====================================================

st.title("🎾 Competitor Details")

st.write(
    "View detailed information about an individual competitor."
)

st.write("---") 


# =====================================================
# SELECT COMPETITOR
# =====================================================

st.subheader("Select Competitor")

# Get all competitors
competitor_list = pd.read_sql_query(
    """
    SELECT name
    FROM competitors
    ORDER BY name;
    """,
    conn
)

# Convert dataframe to Python list
competitor_options = competitor_list["name"].tolist()

# Dropdown menu
selected_competitor = st.selectbox(
    "Choose a Competitor",
    competitor_options
)

st.write("Selected Competitor:", selected_competitor)

st.write("---")


# =====================================================
# COMPETITOR DETAILS
# =====================================================

competitor_details = pd.read_sql_query(
    """
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

    WHERE c.name = ?

    LIMIT 1;
    """,
    conn,
    params=(selected_competitor,)
)

st.subheader("Competitor Information")

st.dataframe(
    competitor_details,
    use_container_width=True,
    hide_index=True
)


