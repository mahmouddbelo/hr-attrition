"""
app.py — Entry point for multi-page HR Attrition Dashboard
Week #1 Task: Employee Attrition Intelligence Dashboard
Kayfa AI & Data Analytics Internship Program
"""
import streamlit as st

st.set_page_config(
    page_title="Week #1 Task: Employee Attrition Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

home_page    = st.Page("1_Home.py",         title="Home",              icon="🏠", default=True)
overview     = st.Page("2_Overview.py",      title="Q1 · Headline",     icon="🔍")
engagement   = st.Page("3_Engagement.py",    title="Q2 · Overtime & Engagement", icon="⚖️")
remote       = st.Page("4_Remote.py",        title="Q3 · Remote Work",  icon="🌐")
compensation = st.Page("5_Compensation.py",  title="Q4–5 · Pay & Tenure", icon="💰")
demographics = st.Page("6_Demographics.py",  title="Q7 · Life Stage",   icon="👤")
growth       = st.Page("7_Growth.py",        title="Q8 · Career Growth",icon="🏆")
risk_profile = st.Page("8_RiskProfile.py",   title="Q9 · Risk Profile", icon="⚠️")
what_moves   = st.Page("9_WhatMoves.py",     title="Q10 · What Moves the Needle", icon="📐")

pg = st.navigation({
    "Dashboard": [home_page],
    "Analysis Questions": [overview, engagement, remote, compensation,
                           demographics, growth, risk_profile, what_moves],
})
pg.run()
