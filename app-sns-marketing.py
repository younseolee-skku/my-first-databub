import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import random

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="📊 SNS Marketing Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Epilogue:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Epilogue', sans-serif;
}

.stApp {
    background: #07080f;
    color: #e8eaf0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d0f1a;
    border-right: 1px solid #1e2235;
}
section[data-testid="stSidebar"] * {
    color: #e8eaf0 !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: #12152a !important;
    color: #e8eaf0 !important;
    border: 1px solid #2a2f4a !important;
    border-radius: 8px !important;
    font-family: 'Epilogue', sans-serif !important;
}
.stSelectbox > div > div > div {
    color: #e8eaf0 !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #4f6ef7, #8b5cf6) !important;
    color: white !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.5rem !important;
    letter-spacing: 0.04em !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px #4f6ef755 !important;
}

/* Metric */
div[data-testid="metric-container"] {
    background: #0d0f1a;
    border: 1px solid #1e2235;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 4px 24px #00000044;
}
div[data-testid="metric-container"] label {
    color: #6b7aaa !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-family: 'Epilogue', sans-serif !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e8eaf0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}
div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
}

/* Table */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* Divider */
hr { border-color: #1e2235 !important; }

/* Header */
.main-header {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #4f6ef7, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}
.sub-header {
    color: #4a5278;
    font-size: 0.9rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-family: 'Epilogue', sans-serif;
    margin-bottom: 1.5rem;
}

/* Campaign card */
.campaign-card-good {
    background: linear-gradient(135deg, #0a2a1a, #0d3322);
    border: 1px solid #1a5c38;
    border-left: 4px solid #22c55e;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.campaign-card-bad {
    background: linear-gradient(135deg, #2a0a0a, #331212);
    border: 1px solid #5c1a1a;
    border-left: 4px solid #ef4444;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.campaign-card-neutral {
    background: linear-gradient(135deg, #1a1a0a, #2a2612);
    border: 1px solid #4a4218;
    border-left: 4px solid #f59e0b;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e8eaf0;
}
.card-meta {
    font-size: 0.78rem;
    color: #6b7aaa;
    margin-top: 2px;
}
.roi-badge-good {
    display: inline-block;
    background: #22c55e22;
    color: #4ade80;
    border: 1px solid #22c55e44;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.78rem;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
}
.roi-badge-bad {
    display: inline-block;
    background: #ef444422;
    color: #f87171;
    border: 1px solid #ef444444;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.78rem;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
}
.roi-badge-neutral {
    display: inline-block;
    background: #f59e0b22;
    color: #fbbf24;
    border: 1px solid #f59e0b44;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.78rem;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
}

/* Section label */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #a5b0d8;
    letter-spacing: 0.04em;
    margin-bottom: 0.8rem;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Helpers ─────────────────────────────────────────────────────────────────
PLATFORM_EMOJI = {"Instagram": "📸", "TikTok": "🎵", "YouTube": "▶️"}
PLATFORM_COLOR = {"Instagram": "#e1306c", "TikTok": "#00f2ea", "YouTube": "#ff0000"}

def calc_engagement(followers, likes, shares, comments):
    if followers == 0:
        return 0.0
    return round(((likes + shares + comments) / followers) * 100, 2)

def calc_roi(budget, likes, shares, comments):
    if budget == 0:
        return 0.0
    revenue_proxy = (likes * 0.5) + (shares * 2.0) + (comments * 1.0)
    return round(((revenue_proxy - budget) / budget) * 100, 2)

def roi_status(roi):
    if roi >= 20:
        return "good"
    elif roi >= 0:
        return "neutral"
    else:
        return "bad"

def generate_weekly_data(base_likes, base_shares, base_comments, weeks=8):
    random.seed(42)
    dates = [datetime.today() - timedelta(weeks=weeks - i) for i in range(weeks)]
    data = []
    for i, d in enumerate(dates):
        factor = 0.7 + 0.3 * (i / weeks) + random.uniform(-0.15, 0.15)
        data.append({
            "week": d.strftime("%b %d"),
            "likes": max(0, int(base_likes * factor)),
            "shares": max(0, int(base_shares * factor)),
            "comments": max(0, int(base_comments * factor)),
            "engagement": round((base_likes + base_shares + base_comments) * factor / max(1, base_likes) * 3.5, 2),
        })
    return pd.DataFrame(data)

# ─── Sample Data ─────────────────────────────────────────────────────────────
SAMPLE_CAMPAIGNS = [
    {
        "name": "Summer Glow 2025",
        "platform": "Instagram",
        "budget": 5000,
        "followers": 120000,
        "likes": 18500,
        "shares": 3200,
        "comments": 870,
    },
    {
        "name": "Viral Dance Challenge",
        "platform": "TikTok",
        "budget": 2000,
        "followers": 340000,
        "likes": 95000,
        "shares": 21000,
        "comments": 4300,
    },
    {
        "name": "Brand Story Series",
        "platform": "YouTube",
        "budget": 12000,
        "followers": 55000,
        "likes": 4200,
        "shares": 890,
        "comments": 310,
    },
]

# Compute derived fields
for c in SAMPLE_CAMPAIGNS:
    c["engagement"] = calc_engagement(c["followers"], c["likes"], c["shares"], c["comments"])
    c["roi"] = calc_roi(c["budget"], c["likes"], c["shares"], c["comments"])
    c["status"] = roi_status(c["roi"])

if "campaigns" not in st.session_state:
    st.session_state.campaigns = SAMPLE_CAMPAIGNS.copy()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 New Campaign")
    st.markdown("---")

    c_name     = st.text_input("📌 Campaign Name", placeholder="e.g. Holiday Sale")
    c_platform = st.selectbox("📲 Platform", ["Instagram", "TikTok", "YouTube"])
    c_budget   = st.number_input("💵 Budget (USD)", min_value=0, value=3000, step=100)
    c_followers= st.number_input("👥 Followers", min_value=0, value=50000, step=1000)
    c_likes    = st.number_input("❤️ Likes", min_value=0, value=5000, step=100)
    c_shares   = st.number_input("🔁 Shares", min_value=0, value=800, step=50)
    c_comments = st.number_input("💬 Comments", min_value=0, value=200, step=10)

    # Live preview
    eng = calc_engagement(c_followers, c_likes, c_shares, c_comments)
    roi = calc_roi(c_budget, c_likes, c_shares, c_comments)
    st.markdown("---")
    st.markdown("#### 📊 Live Preview")
    col_a, col_b = st.columns(2)
    col_a.metric("Engagement", f"{eng}%")
    col_b.metric("ROI", f"{roi}%")

    st.markdown("")
    if st.button("➕ Add Campaign", width='stretch'):
        if c_name:
            new_c = {
                "name": c_name,
                "platform": c_platform,
                "budget": c_budget,
                "followers": c_followers,
                "likes": c_likes,
                "shares": c_shares,
                "comments": c_comments,
                "engagement": eng,
                "roi": roi,
                "status": roi_status(roi),
            }
            st.session_state.campaigns.append(new_c)
            st.success(f"✅ **{c_name}** added!")
        else:
            st.error("⚠️ Please enter a campaign name.")

    if st.button("🔄 Reset to Sample Data", width='stretch'):
        st.session_state.campaigns = SAMPLE_CAMPAIGNS.copy()
        st.rerun()

# ─── Main ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">📊 SNS Marketing Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">✦ Real-Time Campaign Intelligence Dashboard ✦</div>', unsafe_allow_html=True)

campaigns = st.session_state.campaigns
df = pd.DataFrame(campaigns)

# ─── KPI Metrics ─────────────────────────────────────────────────────────────
avg_eng    = df["engagement"].mean()
avg_roi    = df["roi"].mean()
total_budget = df["budget"].sum()
total_likes  = df["likes"].sum()
best_camp  = df.loc[df["roi"].idxmax(), "name"]

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📌 Campaigns", len(df), f"+{len(df) - 3} new" if len(df) > 3 else None)
k2.metric("💰 Total Budget", f"${total_budget:,.0f}")
k3.metric("❤️ Total Likes", f"{total_likes:,}", f"+{total_likes - 117700:,}" if total_likes != 117700 else None)
k4.metric("📈 Avg Engagement", f"{avg_eng:.2f}%", f"{avg_eng - 10.5:+.1f}% vs benchmark")
k5.metric("💹 Avg ROI", f"{avg_roi:.1f}%", f"{avg_roi - 50:+.1f}% vs target")

st.markdown("---")

# ─── Campaign Cards + Table ───────────────────────────────────────────────────
col_cards, col_table = st.columns([1, 2])

with col_cards:
    st.markdown('<div class="section-label">🎯 Campaign Status</div>', unsafe_allow_html=True)
    for c in campaigns:
        status = c["status"]
        card_cls = f"campaign-card-{status}"
        badge_cls = f"roi-badge-{status}"
        roi_icon = "✅" if status == "good" else ("⚠️" if status == "neutral" else "❌")
        plat_emoji = PLATFORM_EMOJI.get(c["platform"], "📱")
        st.markdown(f"""
        <div class="{card_cls}">
            <div class="card-title">{plat_emoji} {c['name']}</div>
            <div class="card-meta">{c['platform']} · {c['followers']:,} followers · ${c['budget']:,} budget</div>
            <div style="margin-top:8px; display:flex; gap:8px; flex-wrap:wrap;">
                <span class="{badge_cls}">{roi_icon} ROI {c['roi']:+.1f}%</span>
                <span style="color:#6b7aaa; font-size:0.78rem; margin-top:3px;">
                    📊 {c['engagement']}% eng &nbsp;|&nbsp; ❤️ {c['likes']:,} &nbsp;|&nbsp; 🔁 {c['shares']:,}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_table:
    st.markdown('<div class="section-label">📋 Full Campaign Table</div>', unsafe_allow_html=True)
    table_data = []
    for c in campaigns:
        status_icon = "🟢" if c["status"] == "good" else ("🟡" if c["status"] == "neutral" else "🔴")
        table_data.append({
            "Status": status_icon,
            "Campaign": c["name"],
            "Platform": PLATFORM_EMOJI.get(c["platform"], "") + " " + c["platform"],
            "Budget": f"${c['budget']:,}",
            "Followers": f"{c['followers']:,}",
            "Likes": f"{c['likes']:,}",
            "Shares": f"{c['shares']:,}",
            "Comments": f"{c['comments']:,}",
            "Engagement %": f"{c['engagement']}%",
            "ROI %": f"{c['roi']:+.1f}%",
        })
    st.dataframe(pd.DataFrame(table_data), hide_index=True, width='stretch', height=320)

st.markdown("---")

# ─── Weekly Performance Chart ─────────────────────────────────────────────────
st.markdown('<div class="section-label">📅 Weekly Performance Trends</div>', unsafe_allow_html=True)

# Select campaign to inspect
camp_names = [c["name"] for c in campaigns]
selected = st.selectbox("Select campaign to inspect:", camp_names)
sel_camp = next(c for c in campaigns if c["name"] == selected)

weekly_df = generate_weekly_data(sel_camp["likes"], sel_camp["shares"], sel_camp["comments"])
plat_color = PLATFORM_COLOR.get(sel_camp["platform"], "#4f6ef7")

tab1, tab2 = st.tabs(["📈 Engagement Trend", "📊 Likes / Shares / Comments"])

with tab1:
    fig_eng = go.Figure()
    fig_eng.add_trace(go.Scatter(
        x=weekly_df["week"], y=weekly_df["engagement"],
        mode="lines+markers",
        line=dict(color=plat_color, width=3, shape="spline"),
        marker=dict(size=8, color=plat_color, line=dict(color="#07080f", width=2)),
        fill="tozeroy",
        fillcolor="rgba(225,48,108,0.08)" if sel_camp["platform"] == "Instagram" else (
            "rgba(0,242,234,0.08)" if sel_camp["platform"] == "TikTok" else "rgba(255,0,0,0.08)"
        ),
        name="Engagement %",
        hovertemplate="<b>%{x}</b><br>Engagement: %{y:.2f}%<extra></extra>",
    ))
    fig_eng.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a5b0d8", family="Epilogue"),
        xaxis=dict(showgrid=False, color="#4a5278"),
        yaxis=dict(showgrid=True, gridcolor="#1e2235", color="#4a5278", ticksuffix="%"),
        margin=dict(l=10, r=10, t=20, b=20),
        height=280,
        showlegend=False,
    )
    st.plotly_chart(fig_eng, width='stretch')

with tab2:
    fig_bar = go.Figure()
    colors = ["#4f6ef7", "#a78bfa", "#38bdf8"]
    for col, clr, label in zip(["likes", "shares", "comments"], colors, ["❤️ Likes", "🔁 Shares", "💬 Comments"]):
        fig_bar.add_trace(go.Bar(
            x=weekly_df["week"], y=weekly_df[col],
            name=label,
            marker_color=clr,
            opacity=0.85,
        ))
    fig_bar.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a5b0d8", family="Epilogue"),
        xaxis=dict(showgrid=False, color="#4a5278"),
        yaxis=dict(showgrid=True, gridcolor="#1e2235", color="#4a5278"),
        legend=dict(font=dict(color="#a5b0d8"), bgcolor="rgba(0,0,0,0)", orientation="h", y=1.1),
        margin=dict(l=10, r=10, t=40, b=20),
        height=280,
    )
    st.plotly_chart(fig_bar, width='stretch')

# ─── ROI Comparison ─────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-label">💹 ROI Comparison Across Campaigns</div>', unsafe_allow_html=True)

roi_df = df.sort_values("roi", ascending=True)
roi_colors = [
    "#22c55e" if s == "good" else ("#f59e0b" if s == "neutral" else "#ef4444")
    for s in roi_df["status"]
]

fig_roi = go.Figure(go.Bar(
    x=roi_df["roi"],
    y=roi_df["name"],
    orientation="h",
    marker_color=roi_colors,
    text=[f"{r:+.1f}%" for r in roi_df["roi"]],
    textposition="outside",
    textfont=dict(color="#e8eaf0", size=12),
))
fig_roi.add_vline(x=0, line_color="#4a5278", line_width=1, line_dash="dot")
fig_roi.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#a5b0d8", family="Epilogue"),
    xaxis=dict(showgrid=True, gridcolor="#1e2235", color="#4a5278", ticksuffix="%"),
    yaxis=dict(showgrid=False, color="#e8eaf0"),
    margin=dict(l=10, r=80, t=20, b=20),
    height=max(160, 70 * len(roi_df)),
)
st.plotly_chart(fig_roi, width='stretch')

# ─── Platform Breakdown ───────────────────────────────────────────────────────
st.markdown("---")
col_pie1, col_pie2 = st.columns(2)

with col_pie1:
    st.markdown('<div class="section-label">📲 Budget by Platform</div>', unsafe_allow_html=True)
    plat_budget = df.groupby("platform")["budget"].sum().reset_index()
    fig_p1 = go.Figure(go.Pie(
        labels=plat_budget["platform"],
        values=plat_budget["budget"],
        hole=0.5,
        marker=dict(
            colors=[PLATFORM_COLOR.get(p, "#4f6ef7") for p in plat_budget["platform"]],
            line=dict(color="#07080f", width=3),
        ),
        textinfo="label+percent",
        textfont=dict(color="#e8eaf0", size=11),
    ))
    fig_p1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a5b0d8", family="Epilogue"),
        legend=dict(font=dict(color="#a5b0d8"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=20, b=20),
        height=280,
        annotations=[dict(text="Budget", font=dict(size=13, color="#4f6ef7", family="Syne"), showarrow=False)],
    )
    st.plotly_chart(fig_p1, width='stretch')

with col_pie2:
    st.markdown('<div class="section-label">❤️ Engagement by Platform</div>', unsafe_allow_html=True)
    plat_eng = df.groupby("platform")["likes"].sum().reset_index()
    fig_p2 = go.Figure(go.Pie(
        labels=plat_eng["platform"],
        values=plat_eng["likes"],
        hole=0.5,
        marker=dict(
            colors=[PLATFORM_COLOR.get(p, "#a78bfa") for p in plat_eng["platform"]],
            line=dict(color="#07080f", width=3),
        ),
        textinfo="label+percent",
        textfont=dict(color="#e8eaf0", size=11),
    ))
    fig_p2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a5b0d8", family="Epilogue"),
        legend=dict(font=dict(color="#a5b0d8"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=20, b=20),
        height=280,
        annotations=[dict(text="Likes", font=dict(size=13, color="#38bdf8", family="Syne"), showarrow=False)],
    )
    st.plotly_chart(fig_p2, width='stretch')

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#2a2f4a; font-size:0.78rem; font-family: Epilogue;'>"
    "✦ SNS Marketing Analytics · Built with Streamlit & Plotly ✦"
    "</div>",
    unsafe_allow_html=True,
)
