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
    roles = sorted(df_full["job_role"].dropna().unique())
    sel_role = st.multiselect("Job Role", roles, default=list(roles))
    wlb_levels = ["Poor","Below Average","Fair","Good","Excellent"]
    sel_wlb = st.multiselect("Work-Life Balance", wlb_levels, default=wlb_levels)
    st.divider()
    st.caption("Q2 · Overtime & Engagement  |  Q6 · Warning Signs")

df = df_full.copy()
if sel_role: df = df[df["job_role"].isin(sel_role)]
if sel_wlb:  df = df[df["work_life_balance"].isin(sel_wlb)]

total = len(df); rate = df["attrition"].mean()*100

st.markdown(f"""
<div class="page-header">
    <div class="hdr-week">Q2 · 6 pts · Easy  |  Q6 · 10 pts · Medium</div>
    <h1 class="hdr-title"><em>Overtime & Engagement</em><br>Warning Signs</h1>
    <p class="hdr-sub">Are overworked employees more likely to leave? Which combination of satisfaction and work-life balance is the strongest early warning sign?</p>
    <div class="hdr-stats">
        <div><div class="hdr-stat-n blue">{rate:.1f}%</div><div class="hdr-stat-l">Current Rate</div></div>
        <div><div class="hdr-stat-n">{total:,}</div><div class="hdr-stat-l">Employees</div></div>
        <div><div class="hdr-stat-n blue">{int(df.get('low_engagement',pd.Series([0])).sum()) if 'low_engagement' in df.columns else 'N/A'}</div>
             <div class="hdr-stat-l">Low Engagement</div></div>
    </div>
</div>""", unsafe_allow_html=True)

# ── Q2: Work-Life Balance as overtime proxy ──────────────────────────────────
qbadge(2, 6, "Overtime & Workload")
sec("⚡","Work-Life Balance & Workload Impact",
    "Work-Life Balance is the primary workload indicator — Poor WLB reflects chronic overwork")
ins("💡 The dataset does not include a direct overtime column. <strong>Work-Life Balance</strong> is the closest proxy — employees rating it 'Poor' are experiencing unsustainable workloads. The chart shows how attrition rises sharply as WLB worsens.")
rec([
    "<strong>Immediate:</strong> any role where >15% of employees rate WLB as 'Poor' needs a headcount or workload review this month.",
    "<strong>Manager training:</strong> equip managers to identify burnout signals — chronic overtime is the #1 controllable driver of 'Poor' WLB ratings.",
    "<strong>Workload caps:</strong> set maximum weekly hours targets per role and measure compliance quarterly.",
])

wlb_order = ["Poor","Below Average","Fair","Good","Excellent"]
agg_wlb = att_rate(df,"work_life_balance", wlb_order)

c1, c2 = st.columns(2)
with c1:
    palette = [ROYAL,"#2563eb",SKY,ICE,FROST]
    n = len(agg_wlb)
    fig = go.Figure(go.Bar(
        x=agg_wlb["work_life_balance"].astype(str),
        y=agg_wlb["rate"],
        marker=dict(color=palette[:n], line=dict(color="#fff",width=1)),
        text=[f"{r}%" for r in agg_wlb["rate"]], textposition="outside",
        name="Attrition Rate",
        hovertemplate="<b>%{x}</b><br>Attrition Rate: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5,
                  annotation_text=f"Avg {rate:.1f}%",
                  annotation_font=dict(size=10,color="#64748b"))
    fig.update_layout(**CBASE, height=H,
        title=dict(text="Attrition Rate by Work-Life Balance Level",
                   font=dict(size=14,color=NAVY,family="Sora")),
        yaxis=dict(title="Attrition Rate (%)",gridcolor="#f1f5f9"),
        xaxis=dict(title="Work-Life Balance"),
        showlegend=False)
    st.plotly_chart(fig, width='stretch')

with c2:
    # WLB distribution — how many employees in each bucket
    wlb_dist = df["work_life_balance"].value_counts()
    wlb_dist = wlb_dist.reindex([w for w in wlb_order if w in wlb_dist.index])
    fig2 = go.Figure(go.Bar(
        x=wlb_dist.index, y=wlb_dist.values,
        marker=dict(color=palette[:len(wlb_dist)], line=dict(color="#fff",width=1)),
        text=wlb_dist.values, textposition="outside",
        name="Headcount",
        hovertemplate="<b>%{x}</b><br>Employees: %{y:,}<extra></extra>",
    ))
    fig2.update_layout(**CBASE, height=H,
        title=dict(text="Employee Count by Work-Life Balance Level",
                   font=dict(size=14,color=NAVY,family="Sora")),
        yaxis=dict(title="Number of Employees",gridcolor="#f1f5f9"),
        xaxis=dict(title="Work-Life Balance"),
        showlegend=False)
    st.plotly_chart(fig2, width='stretch')

# ── Q6: Engagement Warning Signs ─────────────────────────────────────────────
st.markdown("<br>",unsafe_allow_html=True)
qbadge(6, 10, "Engagement Warning Signs")
sec("🚨","Engagement Warning Signs: WLB × Job Satisfaction",
    "Which combination of the two is the strongest predictor of leaving?")
ins("💡 This heatmap combines <strong>Work-Life Balance</strong> and <strong>Job Satisfaction</strong> to find the most dangerous combinations. The darkest red cell = the manager's #1 early warning sign.")
rec([
    "<strong>Watch for the red corner:</strong> any employee with both Poor WLB and Very Low satisfaction has a dramatically higher chance of resigning — these employees need a 1-on-1 within 2 weeks.",
    "<strong>Engagement score:</strong> create a composite engagement metric combining WLB and satisfaction scores — flag anyone below threshold for proactive outreach.",
    "<strong>Quarterly check-in cadence:</strong> teams where >10% fall in the red zone should have bi-weekly manager check-ins, not monthly.",
])

js_order = ["Very Low","Low","Medium","High","Very High"]
if "job_satisfaction" in df.columns and "work_life_balance" in df.columns:
    pivot = (df.groupby(["work_life_balance","job_satisfaction"], observed=True)["attrition"]
               .mean().mul(100).round(1).reset_index()
               .pivot(index="work_life_balance", columns="job_satisfaction", values="attrition")
               .reindex(index=[w for w in wlb_order if w in df["work_life_balance"].unique()])
               .reindex(columns=[j for j in js_order if j in df["job_satisfaction"].unique()]))

    fig3 = px.imshow(pivot, text_auto=".1f",
                     color_continuous_scale=HEAT,
                     title="Attrition Rate (%) — Work-Life Balance × Job Satisfaction",
                     labels=dict(color="Attrition %",
                                 x="Job Satisfaction",
                                 y="Work-Life Balance"))
    fig3.update_layout(**CBASE, height=400,
                       title=dict(font=dict(size=14,color=NAVY,family="Sora")),
                       coloraxis_colorbar=dict(title="Attrition %",ticksuffix="%"))
    st.plotly_chart(fig3, width='stretch')

    # Find the worst combination
    worst_combo = pivot.stack().idxmax()
    worst_rate  = pivot.stack().max()
    ins(f"💡 <strong>Insight (Q6):</strong> The highest-risk combination is "
        f"<strong>WLB = {worst_combo[0]}</strong> + <strong>Satisfaction = {worst_combo[1]}</strong> "
        f"with an attrition rate of <strong>{worst_rate:.1f}%</strong>. "
        f"This is the manager's clearest early warning sign — employees in this cell are "
        f"{worst_rate/rate:.1f}× more likely to leave than the average.")

footer(total, rate)
