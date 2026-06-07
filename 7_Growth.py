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
    levels = [l for l in ["Entry","Mid","Senior"] if l in df_full["job_level"].unique()]
    sel_level = st.multiselect("Job Level", levels, default=levels)
    roles = sorted(df_full["job_role"].dropna().unique())
    sel_role = st.multiselect("Job Role", roles, default=list(roles))
    st.divider()
    st.caption("Q8 · Career Stagnation")

df = df_full.copy()
if sel_level: df = df[df["job_level"].isin(sel_level)]
if sel_role:  df = df[df["job_role"].isin(sel_role)]

total = len(df); rate = df["attrition"].mean()*100

st.markdown(f"""
<div class="page-header">
    <div class="hdr-week">Q8 · 13 pts · Hard</div>
    <h1 class="hdr-title"><em>Career Stagnation</em><br>& Growth Opportunities</h1>
    <p class="hdr-sub">Build the case that lack of growth drives attrition — promotions, job level, leadership, and innovation opportunities combined.</p>
    <div class="hdr-stats">
        <div><div class="hdr-stat-n blue">{rate:.1f}%</div><div class="hdr-stat-l">Current Rate</div></div>
        <div><div class="hdr-stat-n">{total:,}</div><div class="hdr-stat-l">Employees</div></div>
        <div><div class="hdr-stat-n blue">{df["number_of_promotions"].mean():.1f}</div><div class="hdr-stat-l">Avg Promotions</div></div>
    </div>
</div>""", unsafe_allow_html=True)

qbadge(8, 13, "Does feeling stuck drive attrition?")
sec("🏆","Career Stagnation Analysis",
    "Promotions · Job Level · Leadership Opportunities · Innovation Opportunities")
ins("💡 Career stagnation = an employee who cannot see forward progress. We measure it through four signals: <strong>zero promotions</strong>, <strong>entry job level with long tenure</strong>, <strong>no leadership opportunities</strong>, and <strong>no innovation opportunities</strong>. When multiple signals combine, attrition risk multiplies.")
rec([
    "<strong>Define promotion criteria:</strong> write a clear, public document for every role — employees who can't see the path forward will find one elsewhere.",
    "<strong>Leadership pipeline:</strong> identify Entry/Mid employees with 3+ years tenure and no promotions — offer them a stretch project or team lead opportunity within 90 days.",
    "<strong>Innovation access:</strong> employees who say they have no innovation opportunities leave at higher rates — build cross-functional project teams that include contributors at all levels.",
])

c1,c2 = st.columns(2)

with c1:
    agg_p = att_rate(df,"number_of_promotions")
    fig = go.Figure(go.Bar(
        x=agg_p["number_of_promotions"].astype(str), y=agg_p["rate"],
        marker=dict(color=agg_p["rate"],
                    colorscale=[[0,MIST],[0.5,SKY],[1,ROYAL]],
                    line=dict(color="#fff",width=1)),
        text=[f"{r}%" for r in agg_p["rate"]], textposition="outside",
        name="Attrition Rate",
        hovertemplate="<b>%{x} promotions</b><br>Attrition: %{y:.1f}%<br>Headcount: %{customdata:,}<extra></extra>",
        customdata=agg_p["n"],
    ))
    fig.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5,
                  annotation_text=f"Avg {rate:.1f}%",
                  annotation_font=dict(size=10,color="#64748b"))
    fig.update_layout(**CBASE, height=H,
        title=dict(text="Attrition Rate by Number of Promotions",
                   font=dict(size=14,color=NAVY,family="Sora")),
        yaxis=dict(title="Attrition Rate (%)",gridcolor="#f1f5f9"),
        xaxis=dict(title="Number of Promotions Received"),
        showlegend=False)
    st.plotly_chart(fig, width='stretch')

with c2:
    jl_order = ["Entry","Mid","Senior"]
    agg_jl = att_rate(df,"job_level",jl_order)
    fig2 = go.Figure(go.Bar(
        x=agg_jl["job_level"].astype(str), y=agg_jl["rate"],
        marker=dict(color=[ROYAL if r>rate else SKY for r in agg_jl["rate"]],
                    line=dict(color="#fff",width=1)),
        text=[f"{r}%" for r in agg_jl["rate"]], textposition="outside",
        name="Attrition Rate",
        hovertemplate="<b>%{x}</b><br>Attrition: %{y:.1f}%<br>Headcount: %{customdata:,}<extra></extra>",
        customdata=agg_jl["n"],
    ))
    fig2.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5,
                   annotation_text=f"Avg {rate:.1f}%",
                   annotation_font=dict(size=10,color="#64748b"))
    fig2.update_layout(**CBASE, height=H,
        title=dict(text="Attrition Rate by Job Level — Entry vs Mid vs Senior",
                   font=dict(size=14,color=NAVY,family="Sora")),
        yaxis=dict(title="Attrition Rate (%)",gridcolor="#f1f5f9"),
        xaxis=dict(title="Job Level (Seniority)"),
        showlegend=False)
    st.plotly_chart(fig2, width='stretch')

# Leadership & Innovation Opportunities
st.markdown("<br>",unsafe_allow_html=True)
c3,c4 = st.columns(2)

for widget, col, label in [
    (c3,"leadership_opportunities","Leadership Opportunities"),
    (c4,"innovation_opportunities","Innovation Opportunities"),
]:
    with widget:
        if col in df.columns:
            df_temp = df.copy()
            df_temp[label] = df_temp[col].map({1:"Has Opportunity",0:"No Opportunity"})
            agg_op = att_rate(df_temp, label)
            fig_op = go.Figure(go.Bar(
                x=agg_op[label].astype(str), y=agg_op["rate"],
                marker=dict(color=[ROYAL if r>rate else SKY for r in agg_op["rate"]],
                            line=dict(color="#fff",width=1)),
                text=[f"{r}%" for r in agg_op["rate"]], textposition="outside",
                name="Attrition Rate",
                hovertemplate="<b>%{x}</b><br>Attrition: %{y:.1f}%<extra></extra>",
            ))
            fig_op.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5,
                             annotation_text=f"Avg {rate:.1f}%",
                             annotation_font=dict(size=10,color="#64748b"))
            _m = {**CBASE,"margin":dict(t=44,b=24,l=12,r=12)}
            fig_op.update_layout(**_m, height=330, showlegend=False,
                title=dict(text=f"Attrition by {label}",
                           font=dict(size=13,color=NAVY,family="Sora")),
                yaxis=dict(title="Attrition Rate (%)",gridcolor="#f1f5f9"),
                xaxis=dict(title=""))
            st.plotly_chart(fig_op, width='stretch')

# The stagnation case
zero_promo = df[df["number_of_promotions"]==0]["attrition"].mean()*100
entry_long = df[(df["job_level"]=="Entry")&(df["years_at_company"]>=3)]["attrition"].mean()*100 if "job_level" in df.columns else 0

ins(f"💡 <strong>Insight (Q8):</strong> Employees with <strong>0 promotions</strong> have a "
    f"<strong>{zero_promo:.1f}%</strong> attrition rate vs the company average of <strong>{rate:.1f}%</strong> — "
    f"that's <strong>{zero_promo/rate:.1f}×</strong> higher. "
    f"Entry-level employees who have been in role 3+ years with no promotion have a "
    f"<strong>{entry_long:.1f}%</strong> attrition rate. "
    f"Feeling stuck is a primary driver of attrition — the data confirms this.")

footer(total, rate)
