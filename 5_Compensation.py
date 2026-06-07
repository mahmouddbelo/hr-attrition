import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import *

apply_css()
df_full = load_data()

with st.sidebar:
    kayfa_logo_sidebar()
    st.divider()
    levels = [l for l in ["Entry","Mid","Senior"] if l in df_full["job_level"].unique()]
    sel_level = st.multiselect("Job Level", levels, default=levels)
    roles = sorted(df_full["job_role"].dropna().unique())
    sel_role = st.multiselect("Job Role", roles, default=list(roles))
    st.divider()
    st.caption("Q4 · Pay Fairness  |  Q5 · Retention Timeline")

df = df_full.copy()
if sel_level: df = df[df["job_level"].isin(sel_level)]
if sel_role:  df = df[df["job_role"].isin(sel_role)]

total = len(df); rate = df["attrition"].mean()*100

st.markdown(f"""
<div class="page-header">
    <div class="hdr-week">Q4 · 10 pts · Medium  |  Q5 · 11 pts · Medium</div>
    <h1 class="hdr-title"><em>Pay Fairness</em><br>& Retention Timeline</h1>
    <p class="hdr-sub">Within the same job level, do lower-paid employees leave more? At what tenure stage is attrition highest?</p>
    <div class="hdr-stats">
        <div><div class="hdr-stat-n blue">{rate:.1f}%</div><div class="hdr-stat-l">Current Rate</div></div>
        <div><div class="hdr-stat-n">${df["monthly_income"].mean():,.0f}</div><div class="hdr-stat-l">Avg Monthly Income</div></div>
        <div><div class="hdr-stat-n">{df["years_at_company"].mean():.1f} yrs</div><div class="hdr-stat-l">Avg Tenure</div></div>
    </div>
</div>""", unsafe_allow_html=True)

# ── Q4: Pay Fairness ──────────────────────────────────────────────────────────
qbadge(4, 10, "Pay fairness within job level")
sec("💰","Pay Fairness Within Job Level",
    "Do lower-paid employees leave more often within the same seniority level?")
ins("💡 We compare income distributions for <strong>Stayed</strong> vs <strong>Left</strong> employees within each job level. "
    "If leavers consistently earn less than stayers at the same level, the company has a pay equity problem.")
rec([
    "<strong>Benchmark by level:</strong> run a market salary benchmarking exercise for each job level annually — underpaying even 10% below market at Entry level drives the highest attrition.",
    "<strong>Pay band floors:</strong> establish minimum salary floors per level and review anyone below the 25th percentile for their level — these are your highest flight risks.",
    "<strong>Diminishing returns:</strong> once salaries exceed market median, extra pay has minimal retention impact — invest the surplus in recognition and flexibility instead.",
])

if "job_level" in df.columns and "monthly_income" in df.columns:
    jl_order = ["Entry","Mid","Senior"]
    fig = go.Figure()
    for val, color, name in [(0,SKY,"Stayed"),(1,RED,"Left")]:
        for jl in [j for j in jl_order if j in df["job_level"].unique()]:
            sub = df[(df["attrition"]==val)&(df["job_level"]==jl)]["monthly_income"]
            fig.add_trace(go.Box(
                y=sub, name=f"{name} · {jl}",
                marker_color=color, line_color=color,
                boxmean=True,
                legendgroup=name,
                showlegend=(jl==jl_order[0]),
                hovertemplate=f"<b>{name} · {jl}</b><br>Income: $%{{y:,.0f}}<extra></extra>",
            ))
    fig.update_layout(**CBASE, height=460, boxmode="group",
        title=dict(text="Monthly Income Distribution by Job Level — Stayed vs Left",
                   font=dict(size=14,color=NAVY,family="Sora")),
        yaxis=dict(title="Monthly Income ($)",gridcolor="#f1f5f9",tickprefix="$"),
        xaxis=dict(title=""),
        legend=dict(title="Status",orientation="h",y=-0.12))
    st.plotly_chart(fig, width='stretch')

    # Median comparison table
    pivot_pay = (df.groupby(["job_level","attrition"])["monthly_income"]
                   .median().round(0).reset_index()
                   .pivot(index="job_level",columns="attrition",values="monthly_income")
                   .rename(columns={0:"Stayed ($)",1:"Left ($)"}))
    pivot_pay.index = pd.Categorical(pivot_pay.index, categories=jl_order, ordered=True)
    pivot_pay = pivot_pay.sort_index()
    if "Stayed ($)" in pivot_pay.columns and "Left ($)" in pivot_pay.columns:
        pivot_pay["Gap %"] = ((pivot_pay["Left ($)"]-pivot_pay["Stayed ($)"])/pivot_pay["Stayed ($)"]*100).round(1)
        ins("💡 <strong>Pay gap by level:</strong> " +
            " · ".join([f"<strong>{idx}</strong>: leavers earn {row['Gap %']:+.1f}% vs stayers"
                        for idx, row in pivot_pay.iterrows()]))

# ── Q5: Retention Timeline ────────────────────────────────────────────────────
st.markdown("<br>",unsafe_allow_html=True)
qbadge(5, 11, "At what tenure stage is attrition highest?")
sec("📅","Retention Timeline — When Do People Leave?",
    "Identifying the career stages with the highest exit rates")
ins("💡 Attrition is rarely uniform across tenure. Early-stage exits (0–2 years) are expensive because onboarding investment is lost. Mid-career exits (3–7 years) lose institutional knowledge. Understanding <strong>when</strong> people leave directs retention investment to the right stage.")
rec([
    "<strong>0–2 years (new hires):</strong> implement a structured 90-day integration plan with clear milestones, a dedicated buddy, and a formal 6-month check-in — this is where most preventable attrition happens.",
    "<strong>2–6 years (mid-career):</strong> employees at this stage need visible growth — a promotion or role expansion by year 3 dramatically reduces exit risk.",
    "<strong>Loyalty bonuses:</strong> consider a tenure-based bonus at the 12-month and 24-month marks specifically targeting the highest-risk window.",
])

if "tenure_group" in df.columns:
    agg_ten = att_rate(df,"tenure_group",
                       ["0-1 yr","2-3 yrs","4-6 yrs","7-10 yrs","10+ yrs"])
    peak_stage = agg_ten.iloc[agg_ten["rate"].argmax()]["tenure_group"]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=agg_ten["tenure_group"].astype(str), y=agg_ten["rate"],
        marker=dict(color=[ROYAL if r>rate else SKY for r in agg_ten["rate"]],
                    line=dict(color="#fff",width=1)),
        text=[f"{r}%" for r in agg_ten["rate"]], textposition="outside",
        name="Attrition Rate",
        hovertemplate="<b>%{x}</b><br>Attrition: %{y:.1f}%<br>Headcount: %{customdata:,}<extra></extra>",
        customdata=agg_ten["n"],
    ))
    fig2.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5,
                   annotation_text=f"Company avg {rate:.1f}%",
                   annotation_font=dict(size=10,color="#64748b"))
    fig2.update_layout(**CBASE, height=H,
        title=dict(text="Attrition Rate by Tenure Stage — When Do People Leave?",
                   font=dict(size=14,color=NAVY,family="Sora")),
        yaxis=dict(title="Attrition Rate (%)",gridcolor="#f1f5f9"),
        xaxis=dict(title="Years at Company"),
        showlegend=False)
    st.plotly_chart(fig2, width='stretch')

    ins(f"💡 <strong>Insight (Q5):</strong> Attrition peaks at the <strong>{peak_stage}</strong> tenure stage. "
        f"This is where retention investment has the highest return. "
        f"HR should focus onboarding, growth reviews, and loyalty bonuses specifically at this window.")

footer(total, rate)
