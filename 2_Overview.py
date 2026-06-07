import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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
    st.divider()
    st.caption("Q1 · Headline Attrition")

df = df_full.copy()
if sel_role: df = df[df["job_role"].isin(sel_role)]

total  = len(df); left = int(df["attrition"].sum())
stayed = total - left; rate = left/total*100
base   = df_full["attrition"].mean()*100
diff   = rate - base

st.markdown(f"""
<div class="page-header">
    <div class="hdr-week">Q1 · 6 pts · Easy</div>
    <h1 class="hdr-title"><em>Headline</em> Attrition</h1>
    <p class="hdr-sub">What share of employees left overall, and which job role is losing the most people?</p>
    <div class="hdr-stats">
        <div><div class="hdr-stat-n blue">{rate:.1f}%</div><div class="hdr-stat-l">Attrition Rate</div></div>
        <div><div class="hdr-stat-n">{left:,}</div><div class="hdr-stat-l">Employees Left</div></div>
        <div><div class="hdr-stat-n">{stayed:,}</div><div class="hdr-stat-l">Employees Stayed</div></div>
    </div>
</div>""", unsafe_allow_html=True)

qbadge(1, 6, "What share left & which role is worst?")

k1,k2,k3,k4 = st.columns(4)
kpi(k1,"t-navy","👥","Total Employees",f"{total:,}","In current view")
kpi(k2,"t-red","📉","Attrition Rate",f"{rate:.1f}%",
    f"{'▲' if diff>0 else '▼'} {abs(diff):.1f}% vs overall baseline",
    "c-red" if rate>15 else "c-royal")
kpi(k3,"t-sky","✅","Employees Stayed",f"{stayed:,}",f"{100-rate:.1f}% retention rate")
kpi(k4,"t-green","📊","vs Industry Avg","~15%","Healthy rate for most industries","c-red" if rate>20 else "c-green")
st.markdown("<br>",unsafe_allow_html=True)

sec("🔍","Attrition Overview","Overall split and attrition rate by job role")
ins("💡 <strong>Attrition Rate</strong> = percentage of employees who left. Industry benchmark is 10–15%. "
    "Rates above 20% signal a retention crisis. <strong>Darker blue bars</strong> are above the company average.")
rec([
    "<strong>Benchmark immediately:</strong> a rate above 20% requires a company-wide retention audit this quarter.",
    "<strong>Assign an HR business partner</strong> to the highest-attrition role to run stay interviews within 30 days.",
    "<strong>Track monthly:</strong> a rising trend is an early warning that culture, management, or pay changed.",
])

c1,c2 = st.columns([1,2])
with c1:
    fig = go.Figure(go.Pie(
        labels=["Stayed","Left"], values=[stayed,left], hole=0.58,
        marker=dict(colors=[SKY,RED], line=dict(color="#fff",width=3)),
        textinfo="label+percent",
        textfont=dict(size=13,family="Inter"),
        hovertemplate="%{label}: %{value:,} employees (%{percent})<extra></extra>",
    ))
    fig.update_layout(**CBASE, height=H, showlegend=True,
        legend=dict(orientation="h",y=-0.1,
                    itemclick=False,
                    font=dict(size=12)),
        title=dict(text="Attrition Split — Stayed vs Left",
                   font=dict(size=14,color=NAVY,family="Sora")),
        annotations=[dict(text=f"<b>{rate:.0f}%</b><br><span style='font-size:11px;color:#64748b'>left</span>",
                          x=0.5,y=0.5,font=dict(size=20,color=NAVY,family="Sora"),showarrow=False)])
    st.plotly_chart(fig, width='stretch')

with c2:
    agg = att_rate(df, "job_role")
    worst = agg.iloc[0]["job_role"]
    fig = go.Figure(go.Bar(
        x=agg["job_role"], y=agg["rate"],
        marker=dict(color=[ROYAL if r>rate else SKY for r in agg["rate"]],
                    line=dict(color="#fff",width=1)),
        text=[f"{r}%" for r in agg["rate"]], textposition="outside",
        customdata=agg[["n","left"]],
        hovertemplate="<b>%{x}</b><br>Attrition: %{y:.1f}%<br>Headcount: %{customdata[0]:,}<br>Left: %{customdata[1]:,}<extra></extra>",
        name="Attrition Rate",
    ))
    fig.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5,
                  annotation_text=f"Company avg {rate:.1f}%",
                  annotation_font=dict(size=10,color="#64748b"))
    fig.update_layout(**CBASE, height=H,
        title=dict(text="Attrition Rate by Job Role — Stayed & Left comparison",
                   font=dict(size=14,color=NAVY,family="Sora")),
        yaxis=dict(title="Attrition Rate (%)",gridcolor="#f1f5f9"),
        xaxis=dict(title="Job Role"),
        showlegend=False)
    st.plotly_chart(fig, width='stretch')

ins(f"💡 <strong>Insight:</strong> The overall attrition rate is <strong>{rate:.1f}%</strong> — "
    f"{'above' if rate>15 else 'near'} the 15% industry benchmark. "
    f"<strong>{worst}</strong> is the highest-attrition role and should be prioritised first. "
    f"Dark blue bars indicate roles performing worse than the company average.")

footer(total, rate)
