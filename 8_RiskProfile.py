import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import *

apply_css()
df_full = load_data()

with st.sidebar:
    kayfa_logo_sidebar()
    st.divider()
    st.caption("Q9 · Highest-Risk Profile")
    st.markdown("""
    <div style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.3);
                border-radius:8px;padding:10px 12px;margin-top:8px">
        <div style="font-size:0.72rem;font-weight:700;color:#ef4444;
                    text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px">
            ⚠️ At-Risk Profile</div>
        <div style="font-size:0.76rem;color:#cbd5e1;line-height:1.5">
            Age 18-30 · Entry Level<br>
            0 Promotions<br>
            Poor WLB<br>
            Very Low Satisfaction
        </div>
    </div>""", unsafe_allow_html=True)
    st.divider()

df = df_full.copy()
total = len(df); rate = df["attrition"].mean()*100

st.markdown(f"""
<div class="page-header">
    <div class="hdr-week">Q9 · 13 pts · Hard</div>
    <h1 class="hdr-title"><em>Highest-Risk</em><br>Employee Profile</h1>
    <p class="hdr-sub">Combine 3–4 factors to construct the single highest-risk profile. How much higher is their attrition vs the average? How many employees match?</p>
    <div class="hdr-stats">
        <div><div class="hdr-stat-n blue">{rate:.1f}%</div><div class="hdr-stat-l">Company Average</div></div>
    </div>
</div>""", unsafe_allow_html=True)

qbadge(9, 13, "What is the highest-risk employee profile?")
sec("⚠️","Building the Highest-Risk Profile","Combining age, level, promotions, and engagement factors")
ins("💡 We systematically combine factors to find the worst-case attrition profile. "
    "The goal is to (a) quantify how much worse this group is vs average, and "
    "(b) count how many employees match — so leadership knows if it's worth acting on.")

# Build profiles from least to most specific
profiles = []

def profile_rate(mask_conditions):
    mask = pd.Series([True]*len(df))
    for col, val in mask_conditions.items():
        if col in df.columns:
            if isinstance(val, list):
                mask = mask & df[col].isin(val)
            else:
                mask = mask & (df[col] == val)
    sub = df[mask]
    if len(sub) < 30: return None, None, None
    r = sub["attrition"].mean()*100
    return r, len(sub), sub

# Profile tiers
tier_profiles = [
    ("Entry Level only",            {"job_level":["Entry"]}),
    ("Entry + Young (≤30)",         {"job_level":["Entry"],"age_group":["18-25","26-35"]}),
    ("Entry + Young + 0 Promotions",{"job_level":["Entry"],"age_group":["18-25","26-35"],"number_of_promotions":[0]}),
    ("Entry + Young + 0 Promos + Poor WLB",
     {"job_level":["Entry"],"age_group":["18-25","26-35"],"number_of_promotions":[0],"work_life_balance":["Poor","Below Average"]}),
]

profile_results = []
for name, conditions in tier_profiles:
    r, n, _ = profile_rate(conditions)
    if r is not None:
        profile_results.append({
            "Profile": name,
            "Attrition Rate": r,
            "Headcount": n,
            "vs Average": r - rate,
            "Risk Multiplier": r/rate,
        })

if profile_results:
    pr_df = pd.DataFrame(profile_results)

    # Show as bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=pr_df["Profile"], y=pr_df["Attrition Rate"],
        marker=dict(
            color=pr_df["Attrition Rate"],
            colorscale=[[0,ICE],[0.5,ROYAL],[1,RED]],
            line=dict(color="#fff",width=1)
        ),
        text=[f"{r:.1f}%<br>n={n:,}" for r,n in zip(pr_df["Attrition Rate"],pr_df["Headcount"])],
        textposition="outside",
        name="Profile Attrition Rate",
        hovertemplate="<b>%{x}</b><br>Rate: %{y:.1f}%<br>Headcount: %{customdata:,}<extra></extra>",
        customdata=pr_df["Headcount"],
    ))
    fig.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5,
                  annotation_text=f"Company avg {rate:.1f}%",
                  annotation_font=dict(size=10,color="#64748b"))
    fig.update_layout(**CBASE, height=460,
        title=dict(text="Attrition Rate as Risk Factors Are Combined — Building the Worst Profile",
                   font=dict(size=14,color=NAVY,family="Sora")),
        yaxis=dict(title="Attrition Rate (%)",gridcolor="#f1f5f9"),
        xaxis=dict(title="",tickangle=-15),
        showlegend=False)
    st.plotly_chart(fig, width='stretch')

    # Highlight the worst profile
    worst = pr_df.iloc[-1]
    k1,k2,k3,k4 = st.columns(4)
    kpi(k1,"t-red","⚠️","Worst Profile Rate",f"{worst['Attrition Rate']:.1f}%",
        f"{worst['Risk Multiplier']:.1f}× the company average","c-red")
    kpi(k2,"t-navy","👥","Employees at Risk",f"{int(worst['Headcount']):,}",
        f"{worst['Headcount']/total*100:.1f}% of workforce")
    kpi(k3,"t-royal","📈","Above Average",f"+{worst['vs Average']:.1f}%",
        f"vs {rate:.1f}% company average","c-red")
    kpi(k4,"t-amber","🎯","Action Priority","URGENT",
        "This profile needs immediate HR outreach","c-amber")
    st.markdown("<br>",unsafe_allow_html=True)

    ins(f"💡 <strong>Insight (Q9) — Highest-Risk Profile:</strong> "
        f"<strong>{worst['Profile']}</strong> employees have a "
        f"<strong>{worst['Attrition Rate']:.1f}%</strong> attrition rate — "
        f"<strong>{worst['Risk Multiplier']:.1f}×</strong> the company average. "
        f"There are <strong>{int(worst['Headcount']):,}</strong> employees matching this profile "
        f"({worst['Headcount']/total*100:.1f}% of the workforce) — large enough to be worth a targeted retention programme. "
        f"<strong>Recommended action:</strong> assign a dedicated HR contact to schedule stay interviews with all employees in this profile within 30 days.")

    rec([
        f"<strong>Immediate outreach:</strong> the {int(worst['Headcount']):,} employees in the highest-risk profile should each receive a 1-on-1 with their manager or HR within 30 days.",
        "<strong>Targeted incentives:</strong> design a tailored retention package for this profile — clear promotion timeline, recognition, and flexibility are more effective than a blanket pay rise.",
        "<strong>Monitor monthly:</strong> track whether the headcount in this profile shrinks over time as a retention metric for leadership reporting.",
    ])

footer(total, rate)
