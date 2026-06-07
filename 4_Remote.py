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
    levels = [l for l in ["Entry","Mid","Senior"] if l in df_full["job_level"].unique()]
    sel_level = st.multiselect("Job Level", levels, default=levels)
    st.divider()
    st.caption("Q3 · Remote Work")

df = df_full.copy()
if sel_role:  df = df[df["job_role"].isin(sel_role)]
if sel_level: df = df[df["job_level"].isin(sel_level)]

total = len(df); rate = df["attrition"].mean()*100

remote_n   = int((df["remote_work"]==1).sum()) if "remote_work" in df.columns else 0
remote_pct = remote_n/total*100

st.markdown(f"""
<div class="page-header">
    <div class="hdr-week">Q3 · 6 pts · Easy</div>
    <h1 class="hdr-title"><em>Remote Work</em><br>Retention Effect</h1>
    <p class="hdr-sub">Does offering remote work appear to keep people? State the size of the effect — and be honest about what can and cannot be concluded.</p>
    <div class="hdr-stats">
        <div><div class="hdr-stat-n blue">{rate:.1f}%</div><div class="hdr-stat-l">Overall Rate</div></div>
        <div><div class="hdr-stat-n">{remote_n:,}</div><div class="hdr-stat-l">Remote Workers</div></div>
        <div><div class="hdr-stat-n blue">{remote_pct:.1f}%</div><div class="hdr-stat-l">% Working Remotely</div></div>
    </div>
</div>""", unsafe_allow_html=True)

qbadge(3, 6, "Does remote work keep people?")
sec("🌐","Remote Work vs Attrition","Comparing attrition rates between remote and on-site employees")
ins("💡 Only <strong>{:.1f}%</strong> of employees work remotely — so conclusions must be made carefully. The chart shows the attrition rate for each group, but the small remote sample limits how generalisable the finding is.".format(remote_pct))
rec([
    "<strong>If remote employees leave less:</strong> expand WFH eligibility to roles where it's operationally feasible — this costs nothing and has a directly measurable impact on retention.",
    "<strong>Honesty caveat:</strong> with only {:.1f}% remote workers, selection bias is possible — remote workers may already be higher performers or more satisfied employees.".format(remote_pct),
    "<strong>Run a pilot:</strong> offer 6-month hybrid trials to 2–3 high-attrition roles, then compare attrition before and after — this generates causal evidence, not just correlation.",
])

if "remote_work" in df.columns:
    df_rw = df.copy()
    df_rw["Work Arrangement"] = df_rw["remote_work"].map({1:"Remote",0:"On-site"})
    agg = att_rate(df_rw,"Work Arrangement")

    r_rate  = float(agg[agg["Work Arrangement"]=="Remote"]["rate"].values[0]) if "Remote" in agg["Work Arrangement"].values else 0
    os_rate = float(agg[agg["Work Arrangement"]=="On-site"]["rate"].values[0]) if "On-site" in agg["Work Arrangement"].values else 0
    diff_r  = r_rate - os_rate

    k1,k2,k3,k4 = st.columns(4)
    kpi(k1,"t-royal","🌐","Remote Attrition",f"{r_rate:.1f}%","Employees working remotely")
    kpi(k2,"t-navy","🏢","On-site Attrition",f"{os_rate:.1f}%","Employees in office")
    kpi(k3,"t-sky","📊","Difference",f"{abs(diff_r):.1f}%",
        f"Remote is {'lower' if diff_r<0 else 'higher'} — {'good sign' if diff_r<0 else 'investigate'}",
        "c-green" if diff_r<0 else "c-red")
    kpi(k4,"t-ice","👥","Remote Share",f"{remote_pct:.1f}%","Of total workforce")
    st.markdown("<br>",unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Bar(
            x=agg["Work Arrangement"], y=agg["rate"],
            marker=dict(color=[ROYAL if r>rate else SKY for r in agg["rate"]],
                        line=dict(color="#fff",width=1)),
            text=[f"{r}%" for r in agg["rate"]], textposition="outside",
            name="Attrition Rate",
            hovertemplate="<b>%{x}</b><br>Attrition Rate: %{y:.1f}%<extra></extra>",
        ))
        fig.add_hline(y=rate, line_dash="dot", line_color="#94a3b8", line_width=1.5,
                      annotation_text=f"Company avg {rate:.1f}%",
                      annotation_font=dict(size=10,color="#64748b"))
        fig.update_layout(**CBASE, height=H,
            title=dict(text="Attrition Rate: Remote vs On-site",
                       font=dict(size=14,color=NAVY,family="Sora")),
            yaxis=dict(title="Attrition Rate (%)",gridcolor="#f1f5f9"),
            xaxis=dict(title="Work Arrangement"),
            showlegend=False)
        st.plotly_chart(fig, width='stretch')

    with c2:
        # Show breakdown by role
        df_rw2 = df.copy()
        df_rw2["Work"] = df_rw2["remote_work"].map({1:"Remote",0:"On-site"})
        agg2 = (df_rw2.groupby(["job_role","Work"], observed=True)["attrition"]
                      .mean().mul(100).round(1).reset_index())
        fig2 = go.Figure()
        for work_type, color, name in [("Remote",ROYAL,"Remote"),("On-site",SKY,"On-site")]:
            sub = agg2[agg2["Work"]==work_type]
            fig2.add_trace(go.Bar(
                x=sub["job_role"], y=sub["attrition"],
                name=name, marker_color=color,
                hovertemplate=f"<b>%{{x}}</b> ({name})<br>Rate: %{{y:.1f}}%<extra></extra>",
            ))
        fig2.update_layout(**CBASE, height=H, barmode="group",
            title=dict(text="Attrition by Role: Remote vs On-site",
                       font=dict(size=14,color=NAVY,family="Sora")),
            yaxis=dict(title="Attrition Rate (%)",gridcolor="#f1f5f9"),
            xaxis=dict(title="Job Role"),
            legend=dict(title="Work Arrangement",orientation="h",y=-0.12))
        st.plotly_chart(fig2, width='stretch')

    ins(f"💡 <strong>Insight (Q3):</strong> Remote employees have a <strong>{r_rate:.1f}%</strong> attrition rate "
        f"vs <strong>{os_rate:.1f}%</strong> for on-site — a difference of <strong>{abs(diff_r):.1f} percentage points</strong>. "
        f"However, only <strong>{remote_pct:.1f}%</strong> of employees work remotely, "
        f"so this finding is directional, not conclusive. A controlled pilot is needed before making policy changes.")

footer(total, rate)
