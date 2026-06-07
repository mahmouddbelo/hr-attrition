"""
utils.py — shared helpers, styles, and data loader for all pages
"""
import streamlit as st
import pandas as pd
import numpy as np

# ── COLOURS ───────────────────────────────────────────────────────────────────
NAVY  = "#0a1628"
ROYAL = "#1d4ed8"
SKY   = "#3b82f6"
ICE   = "#60a5fa"
FROST = "#93c5fd"
MIST  = "#dbeafe"
RED   = "#ef4444"
GREEN = "#22c55e"
AMBER = "#f59e0b"
TMPL  = "plotly_white"
H     = 400
CBASE = dict(
    template=TMPL,
    font=dict(family="Inter, sans-serif", size=12, color="#334155"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=52, b=28, l=16, r=16),
)
HEAT = [[0, MIST],[0.25, ICE],[0.55, ROYAL],[0.82, "#7c1c1c"],[1, RED]]

# ── SHARED CSS ────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main .block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1440px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#050e1c 0%,#0a1628 35%,#0f2044 70%,#1a3a6b 100%) !important;
    border-right: 1px solid rgba(29,78,216,0.35);
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 {
    color:#ffffff !important; font-family:'Sora',sans-serif !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    color:#93c5fd !important; font-size:0.71rem !important;
    font-weight:700 !important; letter-spacing:0.1em !important;
    text-transform:uppercase !important;
}
[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div,
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background:rgba(29,78,216,0.2) !important;
    border:1px solid rgba(96,165,250,0.3) !important; border-radius:8px !important;
}
[data-testid="stSidebar"] hr { border-color:rgba(59,130,246,0.25) !important; }
[data-testid="stSidebar"] .stCaption * { color:#475569 !important; font-size:0.7rem !important; }

/* ── KAYFA LOGO BLOCK ── */
.kayfa-logo {
    background: linear-gradient(135deg,#0a1628,#1d4ed8);
    border-radius:12px; padding:14px 18px; margin-bottom:16px;
    text-align:center; border:1px solid rgba(96,165,250,0.25);
}
.kayfa-logo-text {
    font-family:'Sora',sans-serif; font-size:1.5rem; font-weight:800;
    color:#ffffff; letter-spacing:0.05em; line-height:1;
}
.kayfa-logo-sub {
    font-size:0.62rem; color:#60a5fa; font-weight:600;
    letter-spacing:0.18em; text-transform:uppercase; margin-top:4px;
}

/* ── PAGE HEADER ── */
.page-header {
    background: linear-gradient(125deg,#050e1c 0%,#0a1628 25%,#0f2044 55%,#1d4ed8 100%);
    border-radius:18px; padding:36px 48px 32px; margin-bottom:26px;
    position:relative; overflow:hidden;
    box-shadow:0 14px 48px rgba(5,14,28,0.5),0 3px 10px rgba(29,78,216,0.2);
}
.page-header::before {
    content:""; position:absolute; top:-80px; right:-80px;
    width:340px; height:340px; border-radius:50%;
    background:radial-gradient(circle,rgba(37,99,235,0.38) 0%,transparent 68%);
    pointer-events:none;
}
.hdr-week {
    font-size:0.68rem; font-weight:700; letter-spacing:0.18em;
    text-transform:uppercase; color:#60a5fa; margin-bottom:8px;
}
.hdr-title {
    font-family:'Sora',sans-serif; font-size:2.6rem; font-weight:800;
    color:#ffffff; line-height:1.08; margin:0 0 10px; letter-spacing:-0.02em;
}
.hdr-title em { color:#60a5fa; font-style:normal; }
.hdr-sub {
    font-size:0.95rem; color:#7aa3d4; margin:0; max-width:620px; line-height:1.6;
}
.hdr-stats {
    display:flex; gap:32px; flex-wrap:wrap;
    margin-top:26px; padding-top:22px;
    border-top:1px solid rgba(59,130,246,0.2);
}
.hdr-stat-n {
    font-family:'Sora',sans-serif; font-size:1.6rem; font-weight:700;
    color:#fff; line-height:1;
}
.hdr-stat-n.blue { color:#60a5fa; }
.hdr-stat-l {
    font-size:0.65rem; color:#5c87b2; font-weight:600;
    letter-spacing:0.08em; text-transform:uppercase; margin-top:4px;
}

/* ── KPI CARDS ── */
.kpi-card {
    background:#ffffff; border-radius:14px; padding:22px 26px 20px;
    box-shadow:0 3px 18px rgba(10,22,40,0.07);
    border-top:5px solid #3b82f6; position:relative; overflow:hidden;
}
.kpi-card::before {
    content:""; position:absolute; right:-18px; top:-18px;
    width:80px; height:80px; border-radius:50%;
    background:rgba(59,130,246,0.05);
}
.kpi-card.t-navy  { border-top-color:#0a1628; }
.kpi-card.t-royal { border-top-color:#1d4ed8; }
.kpi-card.t-sky   { border-top-color:#3b82f6; }
.kpi-card.t-ice   { border-top-color:#60a5fa; }
.kpi-card.t-red   { border-top-color:#ef4444; }
.kpi-card.t-green { border-top-color:#22c55e; }
.kpi-card.t-amber { border-top-color:#f59e0b; }
.kpi-ico  { font-size:1.4rem; margin-bottom:8px; display:block; }
.kpi-lbl  { font-size:0.66rem; font-weight:700; color:#94a3b8; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:5px; }
.kpi-val  { font-family:'Sora',sans-serif; font-size:2.1rem; font-weight:800; color:#0a1628; line-height:1.1; margin-bottom:5px; }
.kpi-val.c-royal { color:#1d4ed8; }
.kpi-val.c-red   { color:#dc2626; }
.kpi-val.c-green { color:#16a34a; }
.kpi-val.c-amber { color:#d97706; }
.kpi-dlt  { font-size:0.74rem; color:#94a3b8; }
.kpi-dlt.up { color:#dc2626; }
.kpi-dlt.dn { color:#16a34a; }

/* ── SECTION HEADER ── */
.sec-hdr {
    display:flex; align-items:flex-start; gap:14px;
    margin:36px 0 16px; padding:14px 18px;
    background:linear-gradient(135deg,#0a1628,#0f2044);
    border-bottom:2px solid #3b82f6; border-radius:12px;
    box-shadow:0 4px 14px rgba(10,22,40,0.16);
}
.sec-ico {
    background:linear-gradient(135deg,#0f2044,#1d4ed8);
    border-radius:10px; width:40px; height:40px; flex-shrink:0;
    display:flex; align-items:center; justify-content:center;
    font-size:1rem; box-shadow:0 4px 12px rgba(29,78,216,0.3);
}
.sec-ttl {
    font-family:'Sora',sans-serif !important; font-size:1.25rem !important;
    font-weight:700 !important; color:#ffffff !important; margin:0 0 2px;
}
.sec-dsc { font-size:0.78rem !important; color:#93c5fd !important; margin:0; }

/* ── INSIGHT & REC BOXES ── */
.insight {
    background:linear-gradient(135deg,#f0f7ff,#e8f2ff);
    border:1px solid #bfdbfe; border-left:4px solid #2563eb;
    border-radius:0 10px 10px 0;
    padding:12px 16px; font-size:0.83rem; color:#1e3a5f;
    line-height:1.65; margin-bottom:16px;
}
.insight strong { color:#1d4ed8; }
.hr-rec {
    background:linear-gradient(135deg,#0a1628,#0f2044);
    border:1px solid rgba(59,130,246,0.3); border-left:4px solid #60a5fa;
    border-radius:0 10px 10px 0;
    padding:13px 16px; font-size:0.83rem; color:#e2eaf8;
    line-height:1.65; margin-bottom:18px;
}
.hr-rec-title {
    font-family:'Sora',sans-serif; font-size:0.68rem; font-weight:700;
    color:#60a5fa; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:7px;
}
.hr-rec ul { margin:0; padding-left:18px; }
.hr-rec li { margin-bottom:5px; color:#cbd5e1; }
.hr-rec strong { color:#93c5fd; }

/* ── Q-BADGE (question number) ── */
.q-badge {
    display:inline-flex; align-items:center; gap:8px;
    background:linear-gradient(135deg,#1d4ed8,#3b82f6);
    border-radius:20px; padding:4px 14px 4px 10px;
    font-size:0.72rem; font-weight:700; color:#ffffff;
    letter-spacing:0.08em; margin-bottom:12px;
}

/* ── TABS ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background:#f0f4fc; border-radius:10px; padding:4px; gap:3px;
    border:1px solid #dbeafe;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius:8px; padding:8px 20px; font-weight:600; font-size:0.82rem;
    color:#64748b !important; background:transparent; border:none;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background:linear-gradient(135deg,#0f2044,#1d4ed8) !important;
    color:white !important; box-shadow:0 2px 8px rgba(29,78,216,0.3);
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    border:1px solid #dbeafe !important; border-radius:12px !important;
    background:#ffffff; box-shadow:0 2px 8px rgba(10,22,40,0.04); overflow:hidden;
}
[data-testid="stExpander"] summary { font-weight:600; color:#1d4ed8; }

/* ── FOOTER ── */
.page-footer {
    background:linear-gradient(135deg,#050e1c,#0a1628,#0f2044);
    border-radius:14px; padding:20px 32px; margin-top:40px;
    display:flex; justify-content:space-between; align-items:center;
    flex-wrap:wrap; gap:10px; border:1px solid rgba(29,78,216,0.18);
}
.ft-brand { font-family:'Sora',sans-serif; font-weight:700; font-size:0.85rem; color:#60a5fa; }
.ft-txt   { font-size:0.7rem; color:#334a6b; margin-top:2px; }
</style>
"""

# ── HELPERS ───────────────────────────────────────────────────────────────────
def apply_css():
    st.markdown(CSS, unsafe_allow_html=True)

def kayfa_logo_sidebar():
    import os, base64
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <div class="kayfa-logo">
            <img src="data:image/png;base64,{b64}"
                 style="width:72px;height:72px;object-fit:contain;display:block;margin:0 auto 8px;" />
            <div class="kayfa-logo-sub">AI & Data Analytics</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="kayfa-logo">
            <div class="kayfa-logo-text">كيف · Kayfa</div>
            <div class="kayfa-logo-sub">AI & Data Analytics</div>
        </div>""", unsafe_allow_html=True)

def sec(icon, title, desc=""):
    d = f'<p class="sec-dsc">{desc}</p>' if desc else ""
    st.markdown(
        f'<div class="sec-hdr"><div class="sec-ico">{icon}</div>'
        f'<div><p class="sec-ttl">{title}</p>{d}</div></div>',
        unsafe_allow_html=True)

def ins(text):
    st.markdown(f'<div class="insight">{text}</div>', unsafe_allow_html=True)

def rec(items: list):
    bullets = "".join(f"<li>{i}</li>" for i in items)
    st.markdown(f"""
    <div class="hr-rec">
        <div class="hr-rec-title">🎯 HR Recommendation</div>
        <ul>{bullets}</ul>
    </div>""", unsafe_allow_html=True)

def qbadge(n, pts, label):
    st.markdown(
        f'<div class="q-badge">Q{n} · {pts} pts · {label}</div>',
        unsafe_allow_html=True)

def footer(total, rate):
    st.markdown(f"""
    <div class="page-footer">
        <div>
            <div class="ft-brand">كيف · Kayfa — HR Attrition Intelligence</div>
            <div class="ft-txt">Week 1 · Data Analytics Track · Internship Program</div>
        </div>
        <div style="text-align:center">
            <div class="ft-txt" style="color:#60a5fa;font-weight:600">{total:,} employees · {rate:.1f}% attrition rate</div>
            <div class="ft-txt">Built with Streamlit · Plotly · Pandas · SciPy</div>
        </div>
        <div style="text-align:right">
            <div class="ft-brand" style="font-size:0.74rem">v5 · Kayfa Internship</div>
            <div class="ft-txt">Data Analytics Track</div>
        </div>
    </div>""", unsafe_allow_html=True)

def att_rate(data, col, order=None):
    agg = (data.groupby(col, observed=True)["attrition"]
               .agg(["mean","count","sum"])
               .rename(columns={"mean":"rate","count":"n","sum":"left"})
               .reset_index()
               .assign(rate=lambda x: (x["rate"]*100).round(1)))
    if order:
        agg[col] = pd.Categorical(agg[col], categories=order, ordered=True)
        agg = agg.sort_values(col)
    else:
        agg = agg.sort_values("rate", ascending=False)
    return agg

def kpi(col_widget, cls, icon, label, value, delta, delta_cls=""):
    with col_widget:
        st.markdown(f"""
        <div class="kpi-card {cls}">
            <span class="kpi-ico">{icon}</span>
            <div class="kpi-lbl">{label}</div>
            <div class="kpi-val {delta_cls}">{value}</div>
            <div class="kpi-dlt">{delta}</div>
        </div>""", unsafe_allow_html=True)

# ── DATA LOADER ───────────────────────────────────────────────────────────────
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
            st.error("Place hr_attrition_clean.csv (or train.csv + test.csv) in the project folder.")
            st.stop()

        def to_snake(c):
            return c.strip().lower().replace(" ","_").replace("-","_").replace("/","_").replace("'","")
        df.columns = [to_snake(c) for c in df.columns]

        def normalize_text(s):
            return (s.astype(str)
                     .str.replace('\u2019',"'",regex=False)
                     .str.replace('\u2018',"'",regex=False).str.strip())
        for col in df.select_dtypes(include="object").columns:
            df[col] = normalize_text(df[col])

        if "_source" in df.columns: df = df.drop(columns=["_source"])
        if "employee_id" in df.columns:
            df = df.drop_duplicates(subset=["employee_id"], keep="first")

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
            if col in df.columns:
                df[col] = df[col].map({"Yes":1,"No":0}).fillna(0).astype(int)

    # Always ensure derived columns exist
    if "age_group" not in df.columns and "age" in df.columns:
        lbl = ["18-25","26-35","36-45","46-60"]
        df["age_group"] = pd.Categorical(
            pd.cut(df["age"], bins=[17,25,35,45,60], labels=lbl),
            categories=lbl, ordered=True)
    if "income_annual" not in df.columns and "monthly_income" in df.columns:
        df["income_annual"] = df["monthly_income"] * 12
    if "low_engagement" not in df.columns:
        if "work_life_balance_num" in df.columns and "job_satisfaction_num" in df.columns:
            df["low_engagement"] = (
                (df["work_life_balance_num"]<=2) & (df["job_satisfaction_num"]<=2)
            ).astype(int)
    # Tenure buckets for Q5
    if "tenure_group" not in df.columns and "years_at_company" in df.columns:
        lbl2 = ["0-1 yr","2-3 yrs","4-6 yrs","7-10 yrs","10+ yrs"]
        df["tenure_group"] = pd.Categorical(
            pd.cut(df["years_at_company"], bins=[-1,1,3,6,10,100], labels=lbl2),
            categories=lbl2, ordered=True)
    return df