import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import apply_css, load_data, kayfa_logo_sidebar, footer, att_rate, NAVY, SKY, RED, ICE, ROYAL, CBASE, H

apply_css()

df_full = load_data()
total     = len(df_full)
left      = int(df_full["attrition"].sum())
rate      = left / total * 100
avg_inc   = df_full["monthly_income"].mean()
avg_ten   = df_full["years_at_company"].mean()

# ── SIDEBAR ──
with st.sidebar:
    kayfa_logo_sidebar()
    st.markdown("### Navigation")
    st.caption("Use the menu above to explore each analysis question.")
    st.divider()
    st.caption("Week 1 · Data Analytics Track")
    st.caption("Kayfa Internship Program")

# ── HEADER ──
st.markdown(f"""
<div class="page-header">
    <div class="hdr-week">📊 Kayfa Internship · Week 1 · Data Analytics Track</div>
    <h1 class="hdr-title">Week #1 Task:<br><em>Employee Attrition</em><br>Intelligence Dashboard</h1>
    <p class="hdr-sub">
        An end-to-end analytics project on a synthetic HR dataset with 74,498 employee records.
        Explore who leaves, why, and what HR can do about it — through 10 analysis questions.
    </p>
    <div class="hdr-stats">
        <div>
            <div class="hdr-stat-n">{total:,}</div>
            <div class="hdr-stat-l">Total Employees</div>
        </div>
        <div>
            <div class="hdr-stat-n blue">{rate:.1f}%</div>
            <div class="hdr-stat-l">Overall Attrition Rate</div>
        </div>
        <div>
            <div class="hdr-stat-n">{left:,}</div>
            <div class="hdr-stat-l">Employees Who Left</div>
        </div>
        <div>
            <div class="hdr-stat-n blue">${avg_inc:,.0f}</div>
            <div class="hdr-stat-l">Avg Monthly Income</div>
        </div>
        <div>
            <div class="hdr-stat-n">{avg_ten:.1f} yrs</div>
            <div class="hdr-stat-l">Avg Tenure</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KAYFA LOGO CARD ──
import os, base64 as _b64
_logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logo.png")
if os.path.exists(_logo_path):
    with open(_logo_path, "rb") as _f:
        _b64_str = _b64.b64encode(_f.read()).decode()
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0a1628,#1d4ed8);
                border-radius:16px;padding:28px 36px;margin-bottom:28px;
                display:flex;align-items:center;gap:28px;
                box-shadow:0 8px 32px rgba(10,22,40,0.25)">
        <img src="data:image/png;base64,{_b64_str}"
             style="width:90px;height:90px;object-fit:contain;flex-shrink:0;" />
        <div>
            <div style="font-family:Sora,sans-serif;font-size:1.6rem;font-weight:800;
                        color:#ffffff;letter-spacing:0.02em;line-height:1.1">Kayfa · كيف</div>
            <div style="font-size:0.8rem;color:#93c5fd;font-weight:500;
                        letter-spacing:0.1em;text-transform:uppercase;margin-top:6px">
                AI & Data Analytics Internship Program</div>
            <div style="font-size:0.75rem;color:#60a5fa;margin-top:4px">
                Week 1 · Data Analytics Track</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0a1628,#1d4ed8);
                border-radius:16px;padding:28px 36px;margin-bottom:28px;
                display:flex;align-items:center;gap:28px;
                box-shadow:0 8px 32px rgba(10,22,40,0.25)">
        <div style="font-family:Sora,sans-serif;font-size:3rem;font-weight:800;
                    color:#ffffff;letter-spacing:0.04em;line-height:1">كيف</div>
        <div>
            <div style="font-family:Sora,sans-serif;font-size:1.6rem;font-weight:700;
                        color:#60a5fa;letter-spacing:0.06em">Kayfa</div>
            <div style="font-size:0.78rem;color:#93c5fd;font-weight:500;
                        letter-spacing:0.1em;text-transform:uppercase;margin-top:2px">
                AI & Data Analytics Internship Program</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── WHAT THIS DASHBOARD ANSWERS ──
st.markdown("""
<div class="sec-hdr">
    <div class="sec-ico">📋</div>
    <div>
        <p class="sec-ttl">10 Analysis Questions</p>
        <p class="sec-dsc">Navigate using the sidebar — each page answers one or more questions</p>
    </div>
</div>
""", unsafe_allow_html=True)

q_data = [
    ("Q1","🔍 Headline","What share of employees left, and which role is losing the most?","Easy · 6 pts","2_Overview"),
    ("Q2","⚖️ Overtime & Engagement","Are overworked employees more likely to leave?","Easy · 6 pts","3_Engagement"),
    ("Q3","🌐 Remote Work","Does remote work keep employees? What is the size of the effect?","Easy · 6 pts","4_Remote"),
    ("Q4","💰 Pay Fairness","Within the same job level, do lower-paid employees leave more?","Medium · 10 pts","5_Compensation"),
    ("Q5","📅 Retention Timeline","At what tenure stage is attrition highest?","Medium · 11 pts","5_Compensation"),
    ("Q6","⚖️ Engagement Warning","Which Satisfaction + WLB combination is the strongest warning sign?","Medium · 10 pts","3_Engagement"),
    ("Q7","👤 Life Stage","Do age, marital status, and dependents predict who leaves?","Medium · 11 pts","6_Demographics"),
    ("Q8","🏆 Career Stagnation","Does feeling stuck drive attrition?","Hard · 13 pts","7_Growth"),
    ("Q9","⚠️ Highest-Risk Profile","What is the single highest-risk employee profile?","Hard · 13 pts","8_RiskProfile"),
    ("Q10","📐 What Moves the Needle","If HR could fix one thing, what should it be?","Hard · 14 pts","9_WhatMoves"),
]

cols = st.columns(2)
for i, (qn, title, desc, pts, _) in enumerate(q_data):
    color = "#22c55e" if "Easy" in pts else ("#f59e0b" if "Medium" in pts else "#ef4444")
    with cols[i % 2]:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:12px;padding:16px 20px;
                    margin-bottom:12px;border-left:4px solid {color};
                    box-shadow:0 2px 10px rgba(10,22,40,0.06)">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                <span style="font-family:Sora,sans-serif;font-weight:700;
                             font-size:0.85rem;color:#0a1628">{title}</span>
                <span style="font-size:0.65rem;font-weight:700;color:{color};
                             background:{color}18;padding:2px 8px;border-radius:10px">{pts}</span>
            </div>
            <div style="font-size:0.8rem;color:#64748b;line-height:1.5">{desc}</div>
        </div>""", unsafe_allow_html=True)

# ── DATASET INFO ──
st.markdown("""
<div class="sec-hdr" style="margin-top:32px">
    <div class="sec-ico">📦</div>
    <div>
        <p class="sec-ttl">Dataset Overview</p>
        <p class="sec-dsc">Synthetic Employee Attrition Dataset — Kaggle</p>
    </div>
</div>
""", unsafe_allow_html=True)

d1, d2, d3, d4 = st.columns(4)
for col_w, cls, ico, lbl, val, dlt in [
    (d1,"t-navy","👥","Total Records","74,498","train.csv + test.csv combined"),
    (d2,"t-royal","📊","Features","22 columns","Demographics, job, workplace factors"),
    (d3,"t-red","📉","Attrition Rate",f"{rate:.1f}%","Employees who left the company"),
    (d4,"t-sky","🏢","Job Roles","5 departments","Finance, Healthcare, Technology, Education, Media"),
]:
    with col_w:
        st.markdown(f"""
        <div class="kpi-card {cls}">
            <span class="kpi-ico">{ico}</span>
            <div class="kpi-lbl">{lbl}</div>
            <div class="kpi-val c-royal">{val}</div>
            <div class="kpi-dlt">{dlt}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
footer(total, rate)