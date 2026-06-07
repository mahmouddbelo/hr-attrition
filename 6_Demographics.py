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
    genders = sorted(df_full["gender"].dropna().unique())
    sel_gender = st.multiselect("Gender", genders, default=list(genders))
    roles = sorted(df_full["job_role"].dropna().unique())
    sel_role = st.multiselect("Job Role", roles, default=list(roles))
    st.divider()
    st.caption("Q7 · Life Stage")

df = df_full.copy()
if sel_gender: df = df[df["gender"].isin(sel_gender)]
if sel_role:   df = df[df["job_role"].isin(sel_role)]

total = len(df); rate = df["attrition"].mean()*100

st.markdown(f"""
<div class="page-header">
    <div class="hdr-week">Q7 · 11 pts · Medium</div>
    <h1 class="hdr-title"><em>Life Stage</em><br>& Demographics</h1>
    <p class="hdr-sub">Do age, marital status, and number of dependents change who leaves? Identify the highest-risk life-stage group.</p>
    <div class="hdr-stats">
        <div><div class="hdr-stat-n blue">{rate:.1f}%</div><div class="hdr-stat-l">Current Rate</div></div>
        <div><div class="hdr-stat-n">{total:,}</div><div class="hdr-stat-l">Employees</div></div>
    </div>
</div>""", unsafe_allow_html=True)

qbadge(7, 11, "Which life-stage group is most at risk?")
sec("👤","Life Stage Analysis","Age, gender, and marital status as attrition predictors")
ins("💡 Life stage factors reflect the external circumstances of an employee's life. <strong>Single employees</strong> have fewer financial ties and higher mobility. <strong>Younger employees</strong> are still exploring careers. These factors are not directly controllable — but they tell HR <strong>who to invest in</strong>.")
rec([
    "<strong>18–25 segment:</strong> launch a structured mentorship program — pair every new hire under 26 with a senior buddy for their first 6 months to build organisational ties.",
    "<strong>Single employees:</strong> offer career development tracks, clear promotion timelines, and relocation packages — these build loyalty without requiring personal life changes.",
    "<strong>Run quarterly pulse surveys</strong> segmented by age group and marital status to catch dissatisfaction before it becomes a resignation.",
])

demo_cfg = [
    ("gender",        None,                              "Attrition Rate by Gender"),
    ("marital_status",None,                              "Attrition Rate by Marital Status"),
    ("age_group",     ["18-25","26-35","36-45","46-60"], "Attrition Rate by Age Group"),
]

c1,c2,c3 = st.columns(3)
for widget,(col,order,title) in zip([c1,c2,c3], demo_cfg):
    with widget:
        agg = att_rate(df, col, order)
        fig = go.Figure(go.Bar(
            x=agg[col].astype(str), y=agg["rate"],
            marker=dict(color=[ROYAL if r>rate else ICE for r in agg["rate"]],
                        line=dict(color="#fff",width=1)),
            text=[f"{r}%" for r in agg["rate"]], textposition="outside",
            name="Attrition Rate",
            hovertemplate="<b>%{x}</b><br>Rate: %{y:.1f}%<br>Headcount: %{customdata:,}<extra></extra>",
            customdata=agg["n"],
        ))
        fig.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5,
                      annotation_text=f"Avg {rate:.1f}%",
                      annotation_font=dict(size=10,color="#64748b"))
        _m = {**CBASE,"margin":dict(t=44,b=24,l=12,r=12)}
        fig.update_layout(**_m, height=330, showlegend=False,
            title=dict(text=title, font=dict(size=13,color=NAVY,family="Sora")),
            yaxis=dict(title="Attrition Rate (%)",gridcolor="#f1f5f9",
                       range=[0,agg["rate"].max()*1.25]),
            xaxis=dict(title=""))
        st.plotly_chart(fig, width='stretch')

# Find highest-risk life stage
age_agg = att_rate(df,"age_group",["18-25","26-35","36-45","46-60"])
mar_agg = att_rate(df,"marital_status")
worst_age = age_agg.iloc[0]
worst_mar = mar_agg.iloc[0]

ins(f"💡 <strong>Insight (Q7):</strong> The highest-risk age group is <strong>{worst_age['age_group']}</strong> "
    f"({worst_age['rate']:.1f}% attrition). "
    f"Among marital status groups, <strong>{worst_mar['marital_status']}</strong> employees leave at "
    f"<strong>{worst_mar['rate']:.1f}%</strong>. "
    f"The highest-risk life stage is <strong>young single employees (18–25, Single)</strong> — "
    f"the combination of maximum mobility and minimum organisational ties.")

# Combined: age × marital
st.markdown("<br>",unsafe_allow_html=True)
sec("🔀","Combined: Age × Marital Status","Which life-stage combination has the highest attrition?")

if "marital_status" in df.columns and "age_group" in df.columns:
    import plotly.express as px
    pivot = (df.groupby(["age_group","marital_status"], observed=True)["attrition"]
               .mean().mul(100).round(1).reset_index()
               .pivot(index="age_group", columns="marital_status", values="attrition")
               .reindex(index=["18-25","26-35","36-45","46-60"]))
    fig2 = px.imshow(pivot, text_auto=".1f",
                     color_continuous_scale=HEAT,
                     title="Attrition Rate (%) — Age Group × Marital Status",
                     labels=dict(color="Attrition %",x="Marital Status",y="Age Group"))
    fig2.update_layout(**CBASE, height=380,
                       title=dict(font=dict(size=14,color=NAVY,family="Sora")),
                       coloraxis_colorbar=dict(title="Attrition %",ticksuffix="%"))
    st.plotly_chart(fig2, width='stretch')

footer(total, rate)
