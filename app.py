"""
HR Attrition Analytics Dashboard — v4
Professional blue-spectrum design
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import pointbiserialr

st.set_page_config(
    page_title="HR Attrition Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# BLUE DESIGN SYSTEM
# Navy   #0a1628 · Royal  #1d4ed8 · Sky    #3b82f6 · Ice   #60a5fa
# Frost  #93c5fd · Mist   #dbeafe · White  #ffffff · Slate #f0f4fc
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Sora:wght@600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #eef2fb;
}
.main .block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
    max-width: 1440px;
}

/* ══ SIDEBAR ══════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050e1c 0%, #0a1628 30%, #0f2044 65%, #1a3a6b 100%) !important;
    border-right: 1px solid rgba(29,78,216,0.4);
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ffffff !important; font-family: 'Sora', sans-serif !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    color: #93c5fd !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div,
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: rgba(29,78,216,0.2) !important;
    border: 1px solid rgba(96,165,250,0.3) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(59,130,246,0.25) !important; }
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] .stCaption * { color: #475569 !important; font-size: 0.72rem !important; }

/* ══ PAGE HEADER ═══════════════════════════════════════════════════ */
.page-header {
    background: linear-gradient(125deg, #050e1c 0%, #0a1628 25%, #0f2044 55%, #1d4ed8 100%);
    border-radius: 20px;
    padding: 44px 52px 40px;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 16px 56px rgba(5,14,28,0.55), 0 4px 12px rgba(29,78,216,0.25);
}
.page-header::before {
    content: "";
    position: absolute; top: -90px; right: -90px;
    width: 380px; height: 380px; border-radius: 50%;
    background: radial-gradient(circle, rgba(37,99,235,0.4) 0%, transparent 68%);
    pointer-events: none;
}
.page-header::after {
    content: "";
    position: absolute; bottom: -70px; left: 28%;
    width: 280px; height: 280px; border-radius: 50%;
    background: radial-gradient(circle, rgba(96,165,250,0.18) 0%, transparent 68%);
    pointer-events: none;
}
.hdr-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(59,130,246,0.22);
    border: 1px solid rgba(96,165,250,0.45);
    border-radius: 22px;
    padding: 5px 16px;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.15em;
    text-transform: uppercase; color: #93c5fd;
    margin-bottom: 16px;
}
.hdr-title {
    font-family: 'Sora', sans-serif;
    font-size: 3.4rem; font-weight: 800;
    color: #ffffff; line-height: 1.05;
    margin: 0 0 12px; letter-spacing: -0.025em;
}
.hdr-title em { color: #60a5fa; font-style: normal; }
.hdr-sub {
    font-size: 1.0rem; font-weight: 400;
    color: #7aa3d4; margin: 0; max-width: 640px; line-height: 1.65;
}
.hdr-stats {
    display: flex; gap: 36px; flex-wrap: wrap;
    margin-top: 30px; padding-top: 26px;
    border-top: 1px solid rgba(59,130,246,0.22);
}
.hdr-stat { min-width: 80px; }
.hdr-stat-n {
    font-family: 'Sora', sans-serif;
    font-size: 1.75rem; font-weight: 700; color: #fff; line-height: 1;
}
.hdr-stat-n.blue { color: #60a5fa; }
.hdr-stat-l {
    font-size: 0.68rem; color: #5c87b2; font-weight: 600;
    letter-spacing: 0.08em; text-transform: uppercase; margin-top: 5px;
}

/* ══ KPI CARDS ═════════════════════════════════════════════════════ */
.kpi-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 24px 28px 22px;
    box-shadow: 0 4px 24px rgba(10,22,40,0.07), 0 1px 4px rgba(10,22,40,0.04);
    border-top: 5px solid #3b82f6;
    position: relative; overflow: hidden;
}
.kpi-card::before {
    content: ""; position: absolute;
    right: -20px; top: -20px;
    width: 88px; height: 88px; border-radius: 50%;
    background: rgba(59,130,246,0.05);
}
.kpi-card.t-navy  { border-top-color: #0a1628; }
.kpi-card.t-royal { border-top-color: #1d4ed8; }
.kpi-card.t-sky   { border-top-color: #3b82f6; }
.kpi-card.t-ice   { border-top-color: #60a5fa; }
.kpi-card.t-red   { border-top-color: #ef4444; }
.kpi-card.t-green { border-top-color: #22c55e; }
.kpi-ico   { font-size: 1.5rem; margin-bottom: 10px; display: block; line-height: 1; }
.kpi-lbl   { font-size: 0.67rem; font-weight: 700; color: #94a3b8; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 6px; }
.kpi-val   { font-family: 'Sora', sans-serif; font-size: 2.2rem; font-weight: 800; color: #0a1628; line-height: 1.1; margin-bottom: 6px; }
.kpi-val.c-royal  { color: #1d4ed8; }
.kpi-val.c-red    { color: #dc2626; }
.kpi-val.c-green  { color: #16a34a; }
.kpi-dlt   { font-size: 0.76rem; color: #94a3b8; }
.kpi-dlt.up   { color: #dc2626; }
.kpi-dlt.dn   { color: #16a34a; }

/* ══ SECTION HEADERS ═══════════════════════════════════════════════ */
.sec-hdr {
    display: flex; align-items: flex-start; gap: 14px;
    margin: 40px 0 18px; padding: 16px 20px 16px;
    border-bottom: 2px solid #3b82f6;
    background: linear-gradient(135deg, #0a1628, #0f2044);
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(10,22,40,0.18);
}
.sec-ico {
    background: linear-gradient(135deg, #0f2044, #1d4ed8);
    border-radius: 12px; width: 42px; height: 42px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.05rem;
    box-shadow: 0 4px 14px rgba(29,78,216,0.35);
}
.sec-ttl {
    font-family: 'Sora', sans-serif !important;
    font-size: 1.3rem !important; font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: -0.015em; margin: 0 0 3px;
}
.sec-dsc { font-size: 0.8rem !important; color: #93c5fd !important; margin: 0; }

/* ══ INSIGHT BOX ═══════════════════════════════════════════════════ */
.insight {
    background: linear-gradient(135deg, #f0f7ff, #e8f2ff);
    border: 1px solid #bfdbfe; border-left: 4px solid #2563eb;
    border-radius: 0 12px 12px 0;
    padding: 13px 18px; font-size: 0.84rem;
    color: #1e3a5f; line-height: 1.65; margin-bottom: 18px;
}
.insight strong { color: #1d4ed8; }

/* ══ HR RECOMMENDATION BOX ══════════════════════════════════════════ */
.hr-rec {
    background: linear-gradient(135deg, #0a1628, #0f2044);
    border: 1px solid rgba(59,130,246,0.35);
    border-left: 4px solid #60a5fa;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px; font-size: 0.84rem;
    color: #e2eaf8; line-height: 1.65; margin-bottom: 20px;
}
.hr-rec-title {
    font-family: 'Sora', sans-serif;
    font-size: 0.7rem; font-weight: 700;
    color: #60a5fa; letter-spacing: 0.12em;
    text-transform: uppercase; margin-bottom: 8px;
}
.hr-rec ul { margin: 0; padding-left: 18px; }
.hr-rec li { margin-bottom: 5px; color: #cbd5e1; }
.hr-rec strong { color: #93c5fd; }

/* ══ TABS ═══════════════════════════════════════════════════════════ */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #f0f4fc; border-radius: 12px; padding: 5px; gap: 4px;
    border: 1px solid #dbeafe;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 9px; padding: 9px 22px;
    font-weight: 600; font-size: 0.83rem;
    color: #64748b !important; background: transparent; border: none;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, #0f2044, #1d4ed8) !important;
    color: white !important;
    box-shadow: 0 3px 10px rgba(29,78,216,0.35);
}

/* ══ EXPANDER ═══════════════════════════════════════════════════════ */
[data-testid="stExpander"] {
    border: 1px solid #dbeafe !important;
    border-radius: 14px !important;
    background: #ffffff;
    box-shadow: 0 2px 10px rgba(10,22,40,0.05);
    overflow: hidden;
}
[data-testid="stExpander"] summary { font-weight: 600; color: #1d4ed8; }

/* ══ DOWNLOAD BUTTON ════════════════════════════════════════════════ */
.stDownloadButton > button {
    background: linear-gradient(135deg, #0f2044, #1d4ed8) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-weight: 600 !important;
    font-size: 0.82rem !important;
}

/* ══ FOOTER ═════════════════════════════════════════════════════════ */
.page-footer {
    background: linear-gradient(135deg, #050e1c, #0a1628, #0f2044);
    border-radius: 16px; padding: 22px 36px;
    margin-top: 44px;
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 12px;
    border: 1px solid rgba(29,78,216,0.2);
}
.ft-brand { font-family: 'Sora', sans-serif; font-weight: 700; font-size: 0.88rem; color: #60a5fa; }
.ft-txt   { font-size: 0.72rem; color: #334a6b; margin-top: 3px; }
</style>
""", unsafe_allow_html=True)


# ── DATA LOADING ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("hr_attrition_clean.csv")
    except FileNotFoundError:
        try:
            train = pd.read_csv("train.csv")
            test  = pd.read_csv("test.csv")
            df    = pd.concat([train, test], ignore_index=True)
        except FileNotFoundError:
            st.error("Place hr_attrition_clean.csv (or train.csv + test.csv) in the app folder.")
            st.stop()

        def to_snake(c):
            return c.strip().lower().replace(" ","_").replace("-","_").replace("/","_").replace("'","")
        df.columns = [to_snake(c) for c in df.columns]

        def normalize_text(s):
            return s.astype(str).str.replace('\u2019',"'",regex=False).str.replace('\u2018',"'",regex=False).str.strip()
        for col in df.select_dtypes(include="object").columns:
            df[col] = normalize_text(df[col])

        if "_source"     in df.columns: df = df.drop(columns=["_source"])
        if "employee_id" in df.columns: df = df.drop_duplicates(subset=["employee_id"], keep="first")

        df["attrition"] = df["attrition"].map({"Stayed":0,"Left":1})
        df = df.dropna(subset=["attrition"])
        df["attrition"] = df["attrition"].astype(int)

        ordinal_maps = {
            "work_life_balance"   : {"Poor":1,"Below Average":2,"Fair":3,"Good":4,"Excellent":5},
            "job_satisfaction"    : {"Very Low":1,"Low":2,"Medium":3,"High":4,"Very High":5},
            "performance_rating"  : {"Low":1,"Below Average":2,"Average":3,"High":4},
            "education_level"     : {"High School":1,"Associate's Degree":2,"Bachelor's Degree":3,"Master's Degree":4,"PhD":5},
            "job_level"           : {"Entry":1,"Mid":2,"Senior":3},
            "company_size"        : {"Small":1,"Medium":2,"Large":3},
            "company_reputation"  : {"Very Poor":1,"Poor":2,"Fair":3,"Good":4,"Excellent":5},
            "employee_recognition": {"Very Low":1,"Low":2,"Medium":3,"High":4,"Very High":5},
        }
        for col, mapping in ordinal_maps.items():
            if col in df.columns: df[f"{col}_num"] = df[col].map(mapping)
        for col in ["remote_work","leadership_opportunities","innovation_opportunities"]:
            if col in df.columns: df[col] = df[col].map({"Yes":1,"No":0}).fillna(0).astype(int)

    if "age_group" not in df.columns and "age" in df.columns:
        lbl = ["18-25","26-35","36-45","46-60"]
        df["age_group"] = pd.Categorical(pd.cut(df["age"], bins=[17,25,35,45,60], labels=lbl), categories=lbl, ordered=True)
    if "income_annual" not in df.columns and "monthly_income" in df.columns:
        df["income_annual"] = df["monthly_income"] * 12
    if "low_engagement" not in df.columns:
        if "work_life_balance_num" in df.columns and "job_satisfaction_num" in df.columns:
            df["low_engagement"] = ((df["work_life_balance_num"]<=2)&(df["job_satisfaction_num"]<=2)).astype(int)
    return df

df_full = load_data()


# ── HELPERS ───────────────────────────────────────────────────────────────────
def att_rate(data, col, order=None):
    agg = (data.groupby(col, observed=True)["attrition"]
               .agg(["mean","count","sum"])
               .rename(columns={"mean":"rate","count":"n","sum":"left"})
               .reset_index()
               .assign(rate=lambda x:(x["rate"]*100).round(1)))
    if order:
        agg[col] = pd.Categorical(agg[col], categories=order, ordered=True)
        agg = agg.sort_values(col)
    else:
        agg = agg.sort_values("rate", ascending=False)
    return agg

def sec(icon, title, desc=""):
    d = f'<p class="sec-dsc">{desc}</p>' if desc else ""
    st.markdown(f'<div class="sec-hdr"><div class="sec-ico">{icon}</div><div><p class="sec-ttl">{title}</p>{d}</div></div>', unsafe_allow_html=True)

def ins(text):
    st.markdown(f'<div class="insight">{text}</div>', unsafe_allow_html=True)

def rec(items: list):
    """Render a dark HR Recommendation card with bullet points."""
    bullets = "".join(f"<li>{i}</li>" for i in items)
    st.markdown(f"""
    <div class="hr-rec">
        <div class="hr-rec-title">🎯 HR Recommendation</div>
        <ul>{bullets}</ul>
    </div>""", unsafe_allow_html=True)

# Chart palette — blue spectrum
NAVY  = "#0a1628"; ROYAL = "#1d4ed8"; SKY = "#3b82f6"; ICE = "#60a5fa"; FROST = "#93c5fd"
RED   = "#ef4444"; GREEN = "#22c55e"
TMPL  = "plotly_white"
H     = 400
CBASE = dict(template=TMPL, font=dict(family="Inter", size=12, color="#334155"),
             paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
             margin=dict(t=52, b=28, l=16, r=16))
HEAT  = [[0,"#dbeafe"],[0.25,ICE],[0.55,ROYAL],[0.82,"#7c1c1c"],[1,RED]]


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔧 Dashboard Filters")
    st.divider()

    genders = sorted(df_full["gender"].dropna().unique())
    sel_gender = st.multiselect("Gender", genders, default=list(genders))

    roles = sorted(df_full["job_role"].dropna().unique())
    sel_role = st.multiselect("Job Role", roles, default=list(roles))

    levels = [l for l in ["Entry","Mid","Senior"] if l in df_full["job_level"].unique()]
    sel_level = st.multiselect("Job Level", levels, default=levels)

    age_min, age_max = int(df_full["age"].min()), int(df_full["age"].max())
    sel_age = st.slider("Age Range", age_min, age_max, (age_min, age_max))

    inc_min = int(df_full["monthly_income"].min())
    inc_max = int(df_full["monthly_income"].max())
    sel_inc = st.slider("Monthly Income ($)", inc_min, inc_max, (inc_min, inc_max), step=100)

    remote_opts = {"All employees": None, "Remote only": 1, "On-site only": 0}
    sel_remote = st.selectbox("Work Arrangement", list(remote_opts.keys()))

    wlb_levels = ["Poor","Below Average","Fair","Good","Excellent"]
    sel_wlb = st.multiselect("Work-Life Balance", wlb_levels, default=wlb_levels)

    st.divider()
    st.caption("HR Attrition Analytics · v4")


# ── APPLY FILTERS ─────────────────────────────────────────────────────────────
df = df_full.copy()
if sel_gender : df = df[df["gender"].isin(sel_gender)]
if sel_role   : df = df[df["job_role"].isin(sel_role)]
if sel_level  : df = df[df["job_level"].isin(sel_level)]
df = df[(df["age"] >= sel_age[0]) & (df["age"] <= sel_age[1])]
df = df[(df["monthly_income"] >= sel_inc[0]) & (df["monthly_income"] <= sel_inc[1])]
if remote_opts[sel_remote] is not None:
    df = df[df["remote_work"] == remote_opts[sel_remote]]
if sel_wlb: df = df[df["work_life_balance"].isin(sel_wlb)]

if len(df) == 0:
    st.warning("No employees match the current filters — adjust the sidebar.")
    st.stop()

total     = len(df)
left      = int(df["attrition"].sum())
stayed    = total - left
rate      = left / total * 100
avg_inc   = df["monthly_income"].mean()
avg_ten   = df["years_at_company"].mean()
base_rate = df_full["attrition"].mean() * 100
low_eng   = int(df["low_engagement"].sum()) if "low_engagement" in df.columns else 0
low_pct   = low_eng / total * 100 if total else 0


# ══════════════════════════════════════════════════════════════════════════════
# HEADER BANNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="page-header">
    <div class="hdr-badge">📊 Workforce Analytics Platform</div>
    <h1 class="hdr-title">HR <em>Attrition</em><br>Dashboard</h1>
    <p class="hdr-sub">
        Explore retention patterns across roles, demographics, and workplace factors.
        All charts update live with the sidebar filters.
    </p>
    <div class="hdr-stats">
        <div class="hdr-stat">
            <div class="hdr-stat-n">{total:,}</div>
            <div class="hdr-stat-l">Employees in view</div>
        </div>
        <div class="hdr-stat">
            <div class="hdr-stat-n blue">{rate:.1f}%</div>
            <div class="hdr-stat-l">Attrition rate</div>
        </div>
        <div class="hdr-stat">
            <div class="hdr-stat-n">{left:,}</div>
            <div class="hdr-stat-l">Employees left</div>
        </div>
        <div class="hdr-stat">
            <div class="hdr-stat-n blue">${avg_inc:,.0f}</div>
            <div class="hdr-stat-l">Avg monthly income</div>
        </div>
        <div class="hdr-stat">
            <div class="hdr-stat-n">{avg_ten:.1f} yrs</div>
            <div class="hdr-stat-l">Avg tenure</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
k1, k2, k3, k4 = st.columns(4)
diff = rate - base_rate
arrow = "▲" if diff > 0 else "▼"

with k1:
    st.markdown(f"""<div class="kpi-card t-navy">
        <span class="kpi-ico">👥</span>
        <div class="kpi-lbl">Total Employees</div>
        <div class="kpi-val c-royal">{total:,}</div>
        <div class="kpi-dlt">Matching current filters</div>
    </div>""", unsafe_allow_html=True)
with k2:
    cls = "up" if diff > 0 else "dn"
    st.markdown(f"""<div class="kpi-card t-red">
        <span class="kpi-ico">📉</span>
        <div class="kpi-lbl">Attrition Rate</div>
        <div class="kpi-val c-red">{rate:.1f}%</div>
        <div class="kpi-dlt {cls}">{arrow} {abs(diff):.1f}% vs overall baseline</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="kpi-card t-sky">
        <span class="kpi-ico">💵</span>
        <div class="kpi-lbl">Avg Monthly Income</div>
        <div class="kpi-val">${avg_inc:,.0f}</div>
        <div class="kpi-dlt">Across filtered group</div>
    </div>""", unsafe_allow_html=True)
with k4:
    risk_cls = "c-red" if low_pct > 10 else "c-royal"
    st.markdown(f"""<div class="kpi-card t-ice">
        <span class="kpi-ico">⚠️</span>
        <div class="kpi-lbl">Low Engagement</div>
        <div class="kpi-val {risk_cls}">{low_pct:.1f}%</div>
        <div class="kpi-dlt">{low_eng:,} at-risk employees</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
sec("🔍", "Attrition Overview", "Overall split and attrition rate by job role")
ins("💡 <strong>Attrition Rate</strong> = the percentage of employees who left. A rate above 15% is considered high in most industries. Darker blue bars in the role chart indicate roles with above-average attrition — those departments need the most attention.")
rec([
    "<strong>Benchmark immediately:</strong> if your overall rate exceeds 20%, launch a company-wide retention audit before the next quarter.",
    "<strong>Focus on the highest-attrition role first</strong> — assign an HR business partner to that department to run stay interviews within 30 days.",
    "<strong>Track this KPI monthly</strong> — a rising attrition rate is an early warning signal that something changed in culture, management, or compensation.",
])

c1, c2 = st.columns([1, 2])
with c1:
    fig = go.Figure(go.Pie(
        labels=["Stayed","Left"], values=[stayed, left], hole=0.58,
        marker=dict(colors=[SKY, RED], line=dict(color="#fff", width=3)),
        textinfo="label+percent", textfont=dict(size=13, family="Inter", color="white"),
        hovertemplate="%{label}: %{value:,} (%{percent})<extra></extra>",
    ))
    fig.update_layout(**CBASE, height=H, showlegend=False,
        title=dict(text="Attrition Split", font=dict(size=15, color=NAVY, family="Sora")),
        annotations=[dict(text=f"<b>{rate:.0f}%</b><br><span style='font-size:11px;color:#64748b'>attrition</span>",
                          x=0.5, y=0.5, font=dict(size=21, color=NAVY, family="Sora"), showarrow=False)])
    st.plotly_chart(fig, width='stretch')

with c2:
    agg = att_rate(df, "job_role")
    fig = go.Figure(go.Bar(
        x=agg["job_role"], y=agg["rate"],
        marker=dict(color=[ROYAL if r > rate else SKY for r in agg["rate"]],
                    line=dict(color="#fff", width=1)),
        text=[f"{r}%" for r in agg["rate"]], textposition="outside",
        textfont=dict(size=12, family="Inter", color=NAVY),
        hovertemplate="<b>%{x}</b><br>Attrition: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5,
                  annotation_text=f"Avg {rate:.1f}%", annotation_font=dict(size=10, color="#64748b"))
    fig.update_layout(**CBASE, height=H,
        title=dict(text="Attrition Rate by Job Role", font=dict(size=15, color=NAVY, family="Sora")),
        yaxis=dict(title="Attrition Rate (%)", gridcolor="#f1f5f9"),
        xaxis=dict(title=""))
    st.plotly_chart(fig, width='stretch')


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — DEMOGRAPHICS
# ══════════════════════════════════════════════════════════════════════════════
sec("👤", "Demographics", "Attrition rates by gender, marital status, and age group")
ins("💡 <strong>Darker blue = above average attrition rate.</strong> The dotted line marks the current filtered average. Rates are used (not raw counts) so groups of different sizes are fairly compared.")
rec([
    "<strong>18–25 age group:</strong> launch a structured onboarding mentorship program — pair every new hire under 26 with a senior buddy for their first 6 months.",
    "<strong>Single employees</strong> tend to leave more (less financial ties, higher mobility) — offer them career development tracks and relocation packages to build loyalty.",
    "<strong>Run quarterly pulse surveys</strong> segmented by age group and marital status to catch dissatisfaction early before it becomes a resignation.",
])

c1, c2, c3 = st.columns(3)
demo_cfg = [
    (c1, "gender",        None,                              "By Gender"),
    (c2, "marital_status",None,                              "By Marital Status"),
    (c3, "age_group",     ["18-25","26-35","36-45","46-60"], "By Age Group"),
]
for widget, col, order, title in demo_cfg:
    with widget:
        agg = att_rate(df, col, order)
        fig = go.Figure(go.Bar(
            x=agg[col].astype(str), y=agg["rate"],
            marker=dict(color=[ROYAL if r > rate else ICE for r in agg["rate"]],
                        line=dict(color="#fff", width=1)),
            text=[f"{r}%" for r in agg["rate"]], textposition="outside",
            textfont=dict(size=11, family="Inter"),
            hovertemplate="<b>%{x}</b><br>Rate: %{y:.1f}%<extra></extra>",
        ))
        fig.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5)
        _m3 = {**CBASE, "margin": dict(t=44, b=24, l=12, r=12)}
        fig.update_layout(**_m3, height=330, showlegend=False,
            title=dict(text=title, font=dict(size=13, color=NAVY, family="Sora")),
            yaxis=dict(title="Rate (%)", gridcolor="#f1f5f9", range=[0, agg["rate"].max()*1.25]),
            xaxis=dict(title=""))
        st.plotly_chart(fig, width='stretch')


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — WORK-LIFE BALANCE & SATISFACTION
# ══════════════════════════════════════════════════════════════════════════════
sec("⚖️", "Work-Life Balance & Job Satisfaction", "5-level ordinal scales — the real dataset has more categories than the data dictionary stated")
ins("💡 Both scales have <strong>5 levels</strong> in the actual Kaggle data. Moving right (better conditions) should show a clear drop in attrition — if it does, these are genuine controllable levers for HR.")
rec([
    "<strong>Work-Life Balance:</strong> introduce flexible working hours or hybrid schedules for roles with 'Poor' WLB — this is the single highest-impact, lowest-cost retention lever available.",
    "<strong>Job Satisfaction:</strong> conduct monthly 1-on-1 check-ins between managers and direct reports — employees rarely leave jobs they enjoy; they leave managers.",
    "<strong>Set a WLB threshold:</strong> any team where >20% of employees rate WLB as Poor or Below Average should trigger an automatic HR review of workload and headcount.",
])

c1, c2 = st.columns(2)

for widget, col, order, title in [
    (c1, "work_life_balance", ["Poor","Below Average","Fair","Good","Excellent"], "Attrition by Work-Life Balance"),
    (c2, "job_satisfaction",  ["Very Low","Low","Medium","High","Very High"],     "Attrition by Job Satisfaction"),
]:
    with widget:
        agg = att_rate(df, col, order)
        n   = len(agg)
        # Build blue gradient darkest → lightest left to right (worst → best condition)
        palette = [ROYAL, "#2563eb", SKY, ICE, FROST]
        bar_col = palette[:n][::-1]  # reverse: best condition gets lightest
        bar_col = palette[:n]        # worst gets darkest
        fig = go.Figure(go.Bar(
            x=agg[col].astype(str), y=agg["rate"],
            marker=dict(color=bar_col, line=dict(color="#fff", width=1)),
            text=[f"{r}%" for r in agg["rate"]], textposition="outside",
            textfont=dict(size=12, family="Inter"),
        ))
        fig.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5,
                      annotation_text=f"Avg {rate:.1f}%", annotation_font=dict(size=10, color="#64748b"))
        fig.update_layout(**CBASE, height=H,
            title=dict(text=title, font=dict(size=14, color=NAVY, family="Sora")),
            yaxis=dict(title="Attrition Rate (%)", gridcolor="#f1f5f9"),
            xaxis=dict(title=""))
        st.plotly_chart(fig, width='stretch')


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — COMPENSATION & TENURE
# ══════════════════════════════════════════════════════════════════════════════
sec("💰", "Compensation & Tenure", "Distribution comparison: employees who stayed vs left")
ins("💡 <strong>Violin plots</strong> reveal the full shape of the distribution — not just median. Wider = more employees at that value. The median gap % is shown in the chart subtitle.")
rec([
    "<strong>Compensation gap:</strong> if employees who left earned less at median, benchmark salaries against market data by role — even a 5–10% raise can prevent a costly resignation and rehire.",
    "<strong>New-hire attrition:</strong> if leavers have shorter tenure, your onboarding experience needs work — implement a 90-day structured integration plan with clear milestones and feedback loops.",
    "<strong>Retention bonuses:</strong> for employees in their first 2 years (highest-risk period), consider a tenure-based loyalty bonus at the 12-month and 24-month marks.",
])

c1, c2 = st.columns(2)
for widget, col, ytitle, title in [
    (c1, "monthly_income",  "Monthly Income ($)", "Monthly Income"),
    (c2, "years_at_company","Years at Company",   "Tenure at Company"),
]:
    with widget:
        fig = go.Figure()
        for val, color, name in [(0, SKY, "Stayed"), (1, RED, "Left")]:
            sub = df[df["attrition"]==val][col]
            fig.add_trace(go.Violin(
                y=sub, name=name, box_visible=True, meanline_visible=True,
                line_color=color, fillcolor=color, opacity=0.55, points=False,
            ))
        ms = df[df.attrition==0][col].median()
        ml = df[df.attrition==1][col].median()
        d  = (ml-ms)/ms*100
        fig.update_layout(**CBASE, height=H, violinmode="group",
            title=dict(text=f"{title}  ·  <sup>Median gap: {'▲' if d>0 else '▼'}{abs(d):.1f}%</sup>",
                       font=dict(size=14, color=NAVY, family="Sora")),
            yaxis=dict(title=ytitle, gridcolor="#f1f5f9"),
            legend=dict(orientation="h", y=-0.12, font=dict(size=12)))
        st.plotly_chart(fig, width='stretch')


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — PROMOTIONS, RECOGNITION & REMOTE WORK
# ══════════════════════════════════════════════════════════════════════════════
sec("🏆", "Promotions, Recognition & Remote Work", "Three controllable HR levers — things the company can actually change")
ins("💡 These three factors are entirely within HR's control. Employees with <strong>zero promotions</strong> exit at the highest rate. <strong>Low recognition</strong> amplifies dissatisfaction. <strong>Remote flexibility</strong> can reduce commute-related attrition.")
rec([
    "<strong>Promotion pathways:</strong> define a written promotion criteria document for every role — employees who can't see a clear path forward will find one elsewhere.",
    "<strong>Recognition program:</strong> implement a peer-to-peer recognition platform (low cost, high impact) — even a monthly 'shout-out' culture measurably reduces attrition in low-recognition groups.",
    "<strong>Remote work policy:</strong> if remote employees show lower attrition, expand WFH eligibility for roles where it is operationally feasible — this costs nothing and improves retention.",
])

c1, c2, c3 = st.columns(3)

with c1:
    agg = att_rate(df, "number_of_promotions")
    fig = go.Figure(go.Bar(
        x=agg["number_of_promotions"].astype(str), y=agg["rate"],
        marker=dict(color=agg["rate"], colorscale=[[0,"#dbeafe"],[0.5,SKY],[1,ROYAL]],
                    line=dict(color="#fff", width=1)),
        text=[f"{r}%" for r in agg["rate"]], textposition="outside",
        textfont=dict(size=11, family="Inter"),
    ))
    fig.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5)
    fig.update_layout(**CBASE, height=350,
        title=dict(text="By Promotions Received", font=dict(size=13, color=NAVY, family="Sora")),
        yaxis=dict(title="Rate (%)", gridcolor="#f1f5f9"),
        xaxis=dict(title="# Promotions"))
    st.plotly_chart(fig, width='stretch')

with c2:
    rec_order = ["Very Low","Low","Medium","High","Very High"]
    agg = att_rate(df, "employee_recognition", rec_order)
    fig = go.Figure(go.Bar(
        x=agg["employee_recognition"].astype(str), y=agg["rate"],
        marker=dict(color=agg["rate"], colorscale=[[0,"#dbeafe"],[0.5,SKY],[1,ROYAL]],
                    line=dict(color="#fff", width=1)),
        text=[f"{r}%" for r in agg["rate"]], textposition="outside",
        textfont=dict(size=11, family="Inter"),
    ))
    fig.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5)
    fig.update_layout(**CBASE, height=350,
        title=dict(text="By Employee Recognition", font=dict(size=13, color=NAVY, family="Sora")),
        yaxis=dict(title="Rate (%)", gridcolor="#f1f5f9"),
        xaxis=dict(title="Recognition Level"))
    st.plotly_chart(fig, width='stretch')

with c3:
    df_rw = df.copy()
    df_rw["Work"] = df_rw["remote_work"].map({1:"Remote", 0:"On-site"})
    agg = att_rate(df_rw, "Work")
    fig = go.Figure(go.Bar(
        x=agg["Work"].astype(str), y=agg["rate"],
        marker=dict(color=[ROYAL if r > rate else SKY for r in agg["rate"]],
                    line=dict(color="#fff", width=1)),
        text=[f"{r}%" for r in agg["rate"]], textposition="outside",
        textfont=dict(size=13, family="Inter"),
    ))
    fig.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5)
    fig.update_layout(**CBASE, height=350,
        title=dict(text="Remote vs On-site", font=dict(size=13, color=NAVY, family="Sora")),
        yaxis=dict(title="Rate (%)", gridcolor="#f1f5f9"),
        xaxis=dict(title="Work Arrangement"))
    st.plotly_chart(fig, width='stretch')


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — HEATMAPS
# ══════════════════════════════════════════════════════════════════════════════
sec("🗺️", "Cross-Variable Heatmaps", "How combinations of role + workplace condition drive attrition")
ins("💡 Each cell shows the attrition rate (%) for that role & condition pair. <strong>Deep blue = low risk · Deep red = high risk.</strong> Look for unexpected hot spots.")
rec([
    "<strong>Red cell = immediate action:</strong> any role-condition combination with attrition above 35% should have a dedicated retention plan — identify the 5–10 employees in that cell and schedule stay interviews this month.",
    "<strong>Cross-department learning:</strong> find a role that stays green (low attrition) even with poor WLB — investigate what that team does differently and replicate it company-wide.",
    "<strong>Use the heatmap in leadership meetings</strong> to show executives exactly which business units are hemorrhaging talent and why — it makes the business case for HR investment concrete.",
])

tab1, tab2 = st.tabs(["📊  Role × Job Satisfaction", "📊  Role × Work-Life Balance"])

with tab1:
    js_order = ["Very Low","Low","Medium","High","Very High"]
    pivot = (df.groupby(["job_role","job_satisfaction"], observed=True)["attrition"]
               .mean().mul(100).round(1).reset_index()
               .pivot(index="job_role", columns="job_satisfaction", values="attrition")
               .reindex(columns=[c for c in js_order if c in df["job_satisfaction"].unique()]))
    fig = px.imshow(pivot, text_auto=".1f", color_continuous_scale=HEAT,
                    title="Attrition Rate (%) — Job Role × Job Satisfaction",
                    labels=dict(color="Rate %"))
    fig.update_layout(**CBASE, height=395,
                      title=dict(font=dict(size=14, color=NAVY, family="Sora")),
                      coloraxis_colorbar=dict(title="Rate %", ticksuffix="%"))
    st.plotly_chart(fig, width='stretch')

with tab2:
    wlb_order = ["Poor","Below Average","Fair","Good","Excellent"]
    pivot = (df.groupby(["job_role","work_life_balance"], observed=True)["attrition"]
               .mean().mul(100).round(1).reset_index()
               .pivot(index="job_role", columns="work_life_balance", values="attrition")
               .reindex(columns=[c for c in wlb_order if c in df["work_life_balance"].unique()]))
    fig = px.imshow(pivot, text_auto=".1f", color_continuous_scale=HEAT,
                    title="Attrition Rate (%) — Job Role × Work-Life Balance",
                    labels=dict(color="Rate %"))
    fig.update_layout(**CBASE, height=395,
                      title=dict(font=dict(size=14, color=NAVY, family="Sora")),
                      coloraxis_colorbar=dict(title="Rate %", ticksuffix="%"))
    st.plotly_chart(fig, width='stretch')


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — CORRELATION
# ══════════════════════════════════════════════════════════════════════════════
sec("📐", "Feature Correlation with Attrition", "Point-biserial correlation — the statistically correct method for a binary target variable")
ins("💡 <strong>Blue bars (left)</strong> = higher values associated with staying. <strong>Red bars (right)</strong> = higher values associated with leaving. Longer bar = stronger relationship with attrition.")
rec([
    "<strong>Prioritize the top 3 red features</strong> — these are the variables most strongly linked to employees leaving; build your retention strategy around improving them.",
    "<strong>Monthly income correlation:</strong> if income is a top positive predictor of staying, a salary review cycle tied to market benchmarks will have a directly measurable impact on retention.",
    "<strong>Don't act on weak correlations</strong> (bars near zero) — focus HR budget and energy only on features with correlations above ±0.05, which have practical significance at this dataset size.",
])

num_cols = [c for c in df.select_dtypes(include=np.number).columns
            if c not in ["attrition","employee_id","income_annual","low_engagement","is_early_career"]]
corr_results = []
for col in num_cols:
    try:
        r, p = pointbiserialr(df["attrition"], df[col])
        corr_results.append({"feature": col, "r": round(r,4), "p": round(p,5)})
    except: pass

corr_df = pd.DataFrame(corr_results).sort_values("r")
fig = go.Figure(go.Bar(
    x=corr_df["r"], y=corr_df["feature"], orientation="h",
    marker=dict(color=[ROYAL if v < 0 else RED for v in corr_df["r"]],
                line=dict(color="#fff", width=0.5)),
    text=[f"{v:+.3f}" for v in corr_df["r"]], textposition="outside",
    textfont=dict(size=11, family="Inter", color=NAVY),
    hovertemplate="<b>%{y}</b><br>r = %{x:+.4f}<extra></extra>",
))
fig.add_vline(x=0, line_width=1.5, line_color=NAVY)
_m7 = {**CBASE, "margin": dict(l=210, r=90, t=52, b=28)}
fig.update_layout(**_m7, height=520,
    title=dict(text="Point-Biserial Correlation with Attrition",
               font=dict(size=14, color=NAVY, family="Sora")),
    xaxis=dict(title="Correlation Coefficient", gridcolor="#f1f5f9"),
    yaxis=dict(title=""))
st.plotly_chart(fig, width='stretch')


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — HR RECOMMENDATIONS SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
sec("🎯", "HR Recommendations Summary", "Prioritized action plan based on the data analysis above")

rec_cols = st.columns(3)
recs = [
    ("🚨 Immediate (0–30 days)", ROYAL, [
        "Run stay interviews in the highest-attrition role",
        "Identify all employees with 0 promotions > 2 years",
        "Schedule 1-on-1s with 'Poor' WLB employees",
    ]),
    ("📅 Short-term (1–3 months)", SKY, [
        "Launch peer recognition program company-wide",
        "Benchmark salaries vs market by job role",
        "Define written promotion criteria for every role",
    ]),
    ("🗓️ Long-term (3–12 months)", ICE, [
        "Implement flexible / hybrid work policy",
        "Build structured 90-day onboarding program",
        "Set up monthly attrition KPI dashboard review",
    ]),
]
for col_widget, (title, color, items) in zip(rec_cols, recs):
    with col_widget:
        bullets = "".join(f"<li style='margin-bottom:6px;color:#cbd5e1'>{i}</li>" for i in items)
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0a1628,#0f2044);
                    border-top:4px solid {color};border-radius:14px;
                    padding:20px 22px;box-shadow:0 4px 20px rgba(10,22,40,0.18);
                    height:100%">
            <div style="font-family:Sora,sans-serif;font-size:0.8rem;font-weight:700;
                        color:{color};letter-spacing:0.06em;margin-bottom:12px">{title}</div>
            <ul style="margin:0;padding-left:18px">{bullets}</ul>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 9 — DATA EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
sec("📋", "Data Explorer", "Browse and download the filtered dataset")

with st.expander("🔎 Open Data Table"):
    show_cols = [c for c in ["age","gender","job_role","job_level","monthly_income",
                              "years_at_company","work_life_balance","job_satisfaction",
                              "number_of_promotions","employee_recognition","attrition"]
                 if c in df.columns]
    disp = df[show_cols].rename(columns={"attrition":"Left (1=Yes)"}).reset_index(drop=True)
    st.dataframe(disp, width='stretch', height=300)

    dl1, dl2 = st.columns([3,1])
    with dl1:
        st.caption(f"Showing {len(df):,} rows · {len(show_cols)} columns")
    with dl2:
        st.download_button("⬇️ Download CSV",
                           disp.to_csv(index=False).encode(),
                           "filtered_employees.csv", "text/csv",
                           width='stretch')


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="page-footer">
    <div>
        <div class="ft-brand">👥 HR Attrition Analytics</div>
        <div class="ft-txt">Workforce Retention Intelligence Platform</div>
    </div>
    <div style="text-align:center">
        <div class="ft-txt" style="color:#60a5fa;font-weight:600">{total:,} employees · {rate:.1f}% attrition rate</div>
        <div class="ft-txt">Built with Streamlit · Plotly · Pandas · SciPy</div>
    </div>
    <div style="text-align:right">
        <div class="ft-brand" style="font-size:0.76rem">v4 · Educational Use</div>
        <div class="ft-txt">Data Analytics Track</div>
    </div>
</div>
""", unsafe_allow_html=True)