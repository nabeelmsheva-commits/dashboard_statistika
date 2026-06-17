import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import chi2_contingency

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Finance Wrapped 2026 🎵",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS (SPOTIFY WRAPPED THEME)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700&display=swap');

/* ─── GLOBAL THEME ─── */
.stApp {
    background-color: #121212;
    font-family: 'Poppins', sans-serif !important;
    color: #ffffff;
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* ─── SIDEBAR (ALWAYS OPEN) ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a1a 0%, #000000 100%) !important;
    border-right: 2px solid #1DB954 !important;
    z-index: 1000 !important;
    position: relative !important;
}
[data-testid="stSidebar"] > div {
    z-index: 1001 !important;
    position: relative !important;
}
[data-testid="stSidebar"] * {
    color: #ffffff !important;
    font-family: 'Poppins', sans-serif !important;
}
[data-testid="stSidebar"] h2 {
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 900 !important;
    color: #1DB954 !important;
    letter-spacing: -0.02em;
    font-size: 1.5rem !important;
}

/* HIDE HAMBURGER BUTTON */
button[data-testid="baseButton-header"] {
    display: none !important;
}
[data-testid="collapsedControl"] {
    display: none !important;
}
section[data-testid="stSidebar"] > div > div > button {
    display: none !important;
}

/* ─── BIG HERO TITLE (ALBUM COVER STYLE) ─── */
.wrapped-hero {
    text-align: center;
    padding: 40px 20px;
    margin-bottom: 20px;
    background: radial-gradient(circle at center, rgba(29, 185, 84, 0.15) 0%, transparent 70%);
    border-radius: 32px;
    position: relative;
    overflow: hidden;
}
.wrapped-hero::before {
    content: "";
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent, rgba(29, 185, 84, 0.1), transparent);
    animation: rotate 15s linear infinite;
}
@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
.wrapped-title {
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 900 !important;
    font-size: 4.5rem !important;
    background: linear-gradient(135deg, #1DB954 0%, #FFD700 50%, #FF6B6B 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientFlow 4s ease infinite;
    letter-spacing: -0.04em;
    line-height: 1;
    margin: 0;
    position: relative;
    z-index: 1;
}
@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.wrapped-subtitle {
    color: #b3b3b3;
    font-size: 1.15rem;
    font-weight: 400;
    margin-top: 16px;
    position: relative;
    z-index: 1;
}
.wrapped-year {
    display: inline-block;
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 900 !important;
    font-size: 1.8rem;
    color: #1DB954;
    margin-top: 12px;
    position: relative;
    z-index: 1;
}

/* ─── BADGES (PERSONALITY TYPE) ─── */
.personality-badge {
    display: inline-block;
    padding: 14px 28px;
    background: linear-gradient(135deg, #1DB954, #1ed760);
    border-radius: 50px;
    color: #000 !important;
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 900 !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    box-shadow: 0 8px 24px rgba(29, 185, 84, 0.4);
    margin: 16px 8px;
    position: relative;
    z-index: 1;
}

/* ─── BIG STAT CARDS (SPOTIFY STYLE) ─── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%) !important;
    border: 1px solid rgba(29, 185, 84, 0.2) !important;
    border-radius: 24px !important;
    padding: 24px 20px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}
[data-testid="metric-container"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 4px;
    background: linear-gradient(90deg, #1DB954, #FFD700);
    opacity: 1;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-8px) scale(1.02);
    border-color: #1DB954 !important;
    box-shadow: 0 16px 40px rgba(29, 185, 84, 0.3);
}
[data-testid="metric-container"] label {
    color: #b3b3b3 !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-family: 'Montserrat', sans-serif !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 2.5rem !important;
    font-weight: 900 !important;
    font-family: 'Montserrat', sans-serif !important;
    letter-spacing: -0.02em;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #1DB954 !important;
    font-weight: 700 !important;
}

/* ─── SECTION TITLES ─── */
.section-title {
    font-family: 'Montserrat', sans-serif !important;
    color: #ffffff;
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    border-left: 5px solid #1DB954;
    padding-left: 16px;
    margin: 36px 0 20px 0;
    letter-spacing: -0.02em;
}

/* ─── BUTTONS ─── */
.stButton > button {
    background: linear-gradient(135deg, #1DB954, #1ed760) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 500px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    box-shadow: 0 6px 20px rgba(29, 185, 84, 0.4);
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 12px 30px rgba(29, 185, 84, 0.6);
}

/* ─── SELECTBOXES ─── */
.stSelectbox > div > div, .stTextInput > div > div {
    background: #1a1a1a !important;
    border: 2px solid rgba(29, 185, 84, 0.3) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    transition: all 0.3s ease !important;
}
.stSelectbox > div > div:hover, .stTextInput > div > div:hover {
    border-color: #1DB954 !important;
    box-shadow: 0 0 0 4px rgba(29, 185, 84, 0.15) !important;
}
.stSelectbox label, .stTextInput label {
    color: #1DB954 !important;
    font-weight: 700 !important;
    font-family: 'Montserrat', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-size: 0.8rem !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    z-index: 1002 !important;
    position: relative !important;
}

/* ─── TABS (PILL STYLE) ─── */
.stTabs [data-baseweb="tab-list"] {
    background: #1a1a1a;
    border-radius: 500px;
    padding: 6px;
    gap: 6px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #b3b3b3 !important;
    border-radius: 500px !important;
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1DB954, #1ed760) !important;
    color: #000 !important;
    box-shadow: 0 4px 15px rgba(29, 185, 84, 0.4);
}
.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
    background: rgba(29, 185, 84, 0.15) !important;
    color: #ffffff !important;
}

/* ─── DIVIDER ─── */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(29, 185, 84, 0.4), transparent);
    margin: 32px 0;
}

/* ─── PLOTLY CHARTS ─── */
.js-plotly-plot .plotly {
    border-radius: 20px !important;
    background: #1a1a1a !important;
    border: 1px solid rgba(29, 185, 84, 0.1);
    padding: 12px;
}

/* ─── DATAFRAME ─── */
[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    border: 1px solid rgba(29, 185, 84, 0.2) !important;
    overflow: hidden;
}

/* ─── EXPANDER ─── */
[data-testid="stExpander"] {
    background: #1a1a1a !important;
    border: 1px solid rgba(29, 185, 84, 0.2) !important;
    border-radius: 16px !important;
}

/* ─── ALERT / INFO BOX ─── */
[data-testid="stAlert"] {
    background: rgba(29, 185, 84, 0.08) !important;
    border: 1px solid rgba(29, 185, 84, 0.4) !important;
    border-radius: 16px !important;
}

/* ─── CUSTOM SCROLLBAR ─── */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #121212; }
::-webkit-scrollbar-thumb {
    background: #1DB954;
    border-radius: 10px;
    border: 2px solid #121212;
}
::-webkit-scrollbar-thumb:hover { background: #1ed760; }

/* ─── SPOTIFY TOP STATS CARD ─── */
.top-stat-card {
    background: linear-gradient(135deg, #1a1a1a, #0a0a0a);
    border: 1px solid rgba(29, 185, 84, 0.2);
    border-radius: 24px;
    padding: 28px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.top-stat-card:hover {
    transform: translateY(-5px);
    border-color: #1DB954;
    box-shadow: 0 15px 40px rgba(29, 185, 84, 0.2);
}
.top-stat-rank {
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 900 !important;
    font-size: 3rem !important;
    color: #1DB954;
    line-height: 1;
    margin: 0;
}
.top-stat-label {
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 700 !important;
    color: #b3b3b3;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 8px;
}
.top-stat-value {
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 800 !important;
    color: #ffffff;
    font-size: 1.2rem;
    margin-top: 12px;
}

/* ─── ENTRANCE ANIMATIONS ─── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
.element-container, .stPlotlyChart, [data-testid="stMetric"] {
    animation: fadeInUp 0.6s ease-out forwards;
}

/* Hide Streamlit Branding */
#MainMenu, header, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Analisis_Statistika.csv")
    df.columns = [
        "timestamp", "jenis_kelamin", "prodi", "semester",
        "uang_saku", "total_pengeluaran",
        "pengeluaran_makan", "pengeluaran_transport",
        "pengeluaran_hiburan", "pengeluaran_kuliah",
        "kehabisan_uang", "budgeting",
        "faktor_membengkak", "frekuensi_belanja_online"
    ]
    df["timestamp"] = pd.to_datetime(df["timestamp"], dayfirst=True, errors="coerce")
    return df

df = load_data()

# ─────────────────────────────────────────────
# KONSTANTA
# ─────────────────────────────────────────────
ORDER_UANG_SAKU = [
    "< Rp 500.000",
    "Rp 500.000 - Rp 1.000.000",
    "Rp 1.000.001 - Rp 1.500.000",
    "> Rp 1.500.001",
]
ORDER_TOTAL_PENGELUARAN = [
    "< Rp 500.000",
    "Rp 500.000 - Rp 700.000",
    "Rp 700.001 - Rp 1.000.000",
    "> Rp 1.000.001",
]

# Spotify Color Palette
WARNA_UTAMA = ["#1DB954", "#1ed760", "#FFD700", "#FF6B6B", "#4ECDC4", "#FFE66D"]
BG_PLOT = "#1a1a1a"
PAPER_BG = "#121212"
FONT_COLOR = "#ffffff"
GRID_COLOR = "rgba(255, 255, 255, 0.08)"

def style_fig(fig):
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=BG_PLOT,
        font=dict(color=FONT_COLOR, family="Poppins, sans-serif", size=12),
        margin=dict(t=40, b=30, l=20, r=20),
        legend=dict(
            bgcolor="rgba(26, 26, 26, 0.8)",
            bordercolor="rgba(29, 185, 84, 0.3)",
            borderwidth=1,
            font=dict(color="#ffffff")
        ),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor="rgba(255,255,255,0.15)", tickfont=dict(color="#b3b3b3"))
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor="rgba(255,255,255,0.15)", tickfont=dict(color="#b3b3b3"))
    return fig

# ─────────────────────────────────────────────
# SIDEBAR (ALWAYS OPEN)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ YOUR FILTERS")
    st.markdown("---")

    gender_options = ["Semua"] + sorted(df["jenis_kelamin"].unique().tolist())
    gender_filter = st.selectbox("👤 Gender", gender_options)

    uang_saku_options = ["Semua"] + ORDER_UANG_SAKU
    uang_saku_filter = st.selectbox("💵 Uang Saku", uang_saku_options)

    kehabisan_options = ["Semua", "Ya", "Tidak"]
    kehabisan_filter = st.selectbox("⚠️ Kehabisan Uang", kehabisan_options)

    budgeting_options = ["Semua", "Ya", "Tidak"]
    budgeting_filter = st.selectbox("📒 Budgeting", budgeting_options)

    st.markdown("---")
    st.markdown(f"**Total Responden:** `{len(df)}`")
    st.markdown("🎵 **Your Wrapped** · Sains Data 2026")

# ─────────────────────────────────────────────
# TERAPKAN FILTER
# ─────────────────────────────────────────────
filtered = df.copy()
if gender_filter != "Semua":
    filtered = filtered[filtered["jenis_kelamin"] == gender_filter]
if uang_saku_filter != "Semua":
    filtered = filtered[filtered["uang_saku"] == uang_saku_filter]
if kehabisan_filter != "Semua":
    filtered = filtered[filtered["kehabisan_uang"] == kehabisan_filter]
if budgeting_filter != "Semua":
    filtered = filtered[filtered["budgeting"] == budgeting_filter]
n = len(filtered)

# ─────────────────────────────────────────────
# PERSONALITY TYPE LOGIC
# ─────────────────────────────────────────────
def get_personality(df_filtered):
    if len(df_filtered) == 0:
        return "🎭 No Data", "Data belum tersedia untuk analisis personality."

    pct_budgeting = df_filtered[df_filtered["budgeting"] == "Ya"].shape[0] / len(df_filtered) * 100
    pct_kehabisan = df_filtered[df_filtered["kehabisan_uang"] == "Ya"].shape[0] / len(df_filtered) * 100
    pct_impulsive = df_filtered[df_filtered["frekuensi_belanja_online"] == "3 kali atau lebih"].shape[0] / len(df_filtered) * 100

    if pct_budgeting > 60 and pct_kehabisan < 30:
        return "💎 BUDGET MASTER", "Kamu tipe yang disiplin dan terencana! Keekonomian dijamin."
    elif pct_impulsive > 40 and pct_kehabisan > 50:
        return "🔥 IMPULSIVE SPENDER", "YOLO lifestyle! Belanja dulu, pikirkan nanti. Coba atur limit budget ya."
    elif pct_kehabisan > 60:
        return "💸 SURVIVAL MODE", "Banyak yang struggle di akhir bulan. Saatnya review pengeluaran!"
    elif pct_budgeting > 40:
        return "🎯 BALANCED PLANNER", "Cukup seimbang antara rencana dan eksekusi. Keep going!"
    else:
        return "🎭 CASUAL SPENDER", "Santai tapi terkontrol. Nggak terlalu strict, tapi aman."

personality_name, personality_desc = get_personality(filtered)

# ─────────────────────────────────────────────
# HERO SECTION (ALBUM COVER STYLE)
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="wrapped-hero">
    <h1 class="wrapped-title">YOUR FINANCE<br>WRAPPED</h1>
    <p class="wrapped-subtitle">Perjalanan keuanganmu dalam angka, dianalisis khusus untukmu ✨</p>
    <div class="wrapped-year">2026 EDITION</div>
    <div style="margin-top: 24px;">
        <span class="personality-badge">{personality_name}</span>
    </div>
    <p style="color: #b3b3b3; margin-top: 16px; font-size: 0.95rem; position: relative; z-index: 1;">
        {personality_desc}
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CARDS (TOP STATS)
# ─────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
pct_kehabisan = round(filtered[filtered["kehabisan_uang"] == "Ya"].shape[0] / n * 100, 1) if n else 0
pct_budgeting = round(filtered[filtered["budgeting"] == "Ya"].shape[0] / n * 100, 1) if n else 0
pct_belanja_sering = round(filtered[filtered["frekuensi_belanja_online"] == "3 kali atau lebih"].shape[0] / n * 100, 1) if n else 0
modus_pengeluaran = filtered["total_pengeluaran"].mode()[0] if n else "-"

k1.metric("👥 RESPONDEN", f"{n}")
k2.metric("⚠️ STRUGGLE", f"{pct_kehabisan}%")
k3.metric("📒 PLANNER", f"{pct_budgeting}%")
k4.metric("🛒 SHOPAHOLIC", f"{pct_belanja_sering}%")
k5.metric("💸 TOP SPEND", modus_pengeluaran.replace("Rp ", "Rp\u00A0"))

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎵 Demografi", "💳 Pengeluaran", "🎤 Perilaku", "📊 Analisis", "🎲 Simulasi"
])

# ══════════════════════════════════════════════
# TAB 1 – DEMOGRAFI
# ══════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-title">Top Gender</p>', unsafe_allow_html=True)
        gender_cnt = filtered["jenis_kelamin"].value_counts().reset_index()
        gender_cnt.columns = ["Jenis Kelamin", "Jumlah"]
        fig = px.pie(gender_cnt, names="Jenis Kelamin", values="Jumlah",
                     color_discrete_sequence=WARNA_UTAMA, hole=0.55)
        fig.update_traces(textfont_size=14, textinfo="percent+label", textfont_color="white")
        fig.update_layout(showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Uang Saku Vibes</p>', unsafe_allow_html=True)
        uang_cnt = filtered["uang_saku"].value_counts().reindex(ORDER_UANG_SAKU, fill_value=0).reset_index()
        uang_cnt.columns = ["Uang Saku", "Jumlah"]
        fig2 = px.bar(uang_cnt, x="Uang Saku", y="Jumlah",
                      color="Jumlah", color_continuous_scale=[[0, "#0a4a2a"], [0.5, "#1DB954"], [1, "#FFD700"]],
                      text="Jumlah")
        fig2.update_traces(textposition="outside", textfont_color=FONT_COLOR)
        fig2.update_coloraxes(showscale=False)
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Uang Saku vs Gender</p>', unsafe_allow_html=True)
    cross = pd.crosstab(filtered["uang_saku"], filtered["jenis_kelamin"]).reindex(ORDER_UANG_SAKU, fill_value=0)
    fig3 = go.Figure()
    for i, col_name in enumerate(cross.columns):
        fig3.add_trace(go.Bar(name=col_name, x=cross.index, y=cross[col_name],
                              marker_color=WARNA_UTAMA[i], text=cross[col_name], textposition="auto"))
    fig3.update_layout(barmode="group", xaxis_title="Uang Saku", yaxis_title="Jumlah")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 2 – PENGELUARAN
# ══════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-title">Top Pengeluaran</p>', unsafe_allow_html=True)
        tot_cnt = filtered["total_pengeluaran"].value_counts().reindex(ORDER_TOTAL_PENGELUARAN, fill_value=0).reset_index()
        tot_cnt.columns = ["Total Pengeluaran", "Jumlah"]
        fig = px.bar(tot_cnt, x="Total Pengeluaran", y="Jumlah",
                     color="Total Pengeluaran", color_discrete_sequence=WARNA_UTAMA, text="Jumlah")
        fig.update_traces(textposition="outside", textfont_color=FONT_COLOR, showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Top Trigger Boros</p>', unsafe_allow_html=True)
        faktor_cnt = filtered["faktor_membengkak"].value_counts().reset_index()
        faktor_cnt.columns = ["Faktor", "Jumlah"]
        faktor_cnt["Faktor_short"] = faktor_cnt["Faktor"].str.extract(r'^([^(]+)').iloc[:, 0].str.strip()
        fig2 = px.bar(faktor_cnt, y="Faktor_short", x="Jumlah",
                      orientation="h", color="Jumlah",
                      color_continuous_scale=[[0, "#0a4a2a"], [0.5, "#FF6B6B"], [1, "#FFD700"]], text="Jumlah")
        fig2.update_traces(textposition="outside", textfont_color=FONT_COLOR)
        fig2.update_coloraxes(showscale=False)
        fig2.update_layout(yaxis_title=" ")
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Category Breakdown</p>', unsafe_allow_html=True)
    col_makan = filtered["pengeluaran_makan"].value_counts()
    col_transport = filtered["pengeluaran_transport"].value_counts()
    col_hiburan = filtered["pengeluaran_hiburan"].value_counts()
    col_kuliah = filtered["pengeluaran_kuliah"].value_counts()

    breakdown_df = pd.DataFrame({
        "Makan": col_makan, "Transport": col_transport,
        "Hiburan": col_hiburan, "Kuliah": col_kuliah,
    }).fillna(0).reset_index().rename(columns={"index": "Kategori"})
    breakdown_melt = breakdown_df.melt(id_vars="Kategori", var_name="Jenis", value_name="Jumlah")

    fig3 = px.bar(breakdown_melt, x="Kategori", y="Jumlah", color="Jenis",
                  barmode="group", color_discrete_sequence=WARNA_UTAMA, text="Jumlah")
    fig3.update_traces(textposition="outside", textfont_color=FONT_COLOR)
    fig3.update_layout(xaxis_title="Kategori", yaxis_title="Jumlah")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 – PERILAKU
# ══════════════════════════════════════════════
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-title">Kehabisan Uang?</p>', unsafe_allow_html=True)
        kh_cnt = filtered["kehabisan_uang"].value_counts().reset_index()
        kh_cnt.columns = ["Status", "Jumlah"]
        fig = px.pie(kh_cnt, names="Status", values="Jumlah", hole=0.6,
                     color="Status", color_discrete_map={"Ya": "#FF6B6B", "Tidak": "#1DB954"})
        fig.update_traces(textfont_size=14, textinfo="percent+label", textfont_color="white")
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Budgeting Habit</p>', unsafe_allow_html=True)
        bd_cnt = filtered["budgeting"].value_counts().reset_index()
        bd_cnt.columns = ["Status", "Jumlah"]
        fig2 = px.pie(bd_cnt, names="Status", values="Jumlah", hole=0.6,
                      color="Status", color_discrete_map={"Ya": "#1DB954", "Tidak": "#FFD700"})
        fig2.update_traces(textfont_size=14, textinfo="percent+label", textfont_color="white")
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Budgeting vs Kehabisan</p>', unsafe_allow_html=True)
    cross_bk = pd.crosstab(filtered["budgeting"], filtered["kehabisan_uang"])
    cross_bk_pct = (cross_bk.div(cross_bk.sum(axis=1), axis=0) * 100).round(1)

    fig3 = go.Figure()
    colors_map = {"Ya": "#FF6B6B", "Tidak": "#1DB954"}
    for col_name in cross_bk_pct.columns:
        fig3.add_trace(go.Bar(name=f"Kehabisan: {col_name}", x=cross_bk_pct.index, y=cross_bk_pct[col_name],
                              marker_color=colors_map.get(col_name, WARNA_UTAMA[0]),
                              text=cross_bk_pct[col_name].map(lambda v: f"{v:.1f}%"), textposition="inside"))
    fig3.update_layout(barmode="stack", xaxis_title="Budgeting", yaxis_title="Persentase (%)")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 4 – ANALISIS
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-title">🔥 Heatmap Asosiasi (Cramér\'s V)</p>', unsafe_allow_html=True)

    cat_cols = [
        "uang_saku", "total_pengeluaran", "pengeluaran_makan",
        "pengeluaran_transport", "pengeluaran_hiburan", "pengeluaran_kuliah",
        "kehabisan_uang", "budgeting", "faktor_membengkak",
        "frekuensi_belanja_online", "jenis_kelamin",
    ]
    cat_labels = [
        "Uang Saku", "Total", "Makan", "Transport", "Hiburan", "Kuliah",
        "Kehabisan", "Budget", "Faktor", "Belanja", "Gender",
    ]

    def cramers_v(x, y):
        confusion_matrix = pd.crosstab(x, y)
        chi2 = chi2_contingency(confusion_matrix)[0]
        n_obs = confusion_matrix.sum().sum()
        phi2 = chi2 / n_obs
        r, k = confusion_matrix.shape
        phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n_obs - 1))
        rcorr = r - ((r - 1) ** 2) / (n_obs - 1)
        kcorr = k - ((k - 1) ** 2) / (n_obs - 1)
        denom = min((kcorr - 1), (rcorr - 1))
        return np.sqrt(phi2corr / denom) if denom > 0 else 0

    if n >= 5:
        matrix = np.zeros((len(cat_cols), len(cat_cols)))
        for i, c1 in enumerate(cat_cols):
            for j, c2 in enumerate(cat_cols):
                if i == j:
                    matrix[i][j] = 1.0
                elif i < j:
                    try:
                        v = cramers_v(filtered[c1], filtered[c2])
                    except Exception:
                        v = 0.0
                    matrix[i][j] = v
                    matrix[j][i] = v

        fig_heat = go.Figure(data=go.Heatmap(
            z=np.round(matrix, 2), x=cat_labels, y=cat_labels,
            colorscale=[[0, "#121212"], [0.3, "#0a4a2a"], [0.6, "#1DB954"], [1, "#FFD700"]],
            zmin=0, zmax=1,
            text=np.round(matrix, 2), texttemplate="%{text}",
            textfont={"size": 10, "color": "white"},
        ))
        fig_heat.update_layout(height=550, xaxis=dict(tickangle=-45))
        style_fig(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.warning("Data terlalu sedikit. Hapus filter untuk melihat heatmap.")

    st.markdown("---")
    st.markdown('<p class="section-title">📄 Raw Data</p>', unsafe_allow_html=True)
    with st.expander("Lihat Dataset"):
        st.dataframe(filtered.reset_index(drop=True), use_container_width=True)

# ══════════════════════════════════════════════
# TAB 5 – SIMULASI MONTE CARLO
# ══════════════════════════════════════════════
with tab5:
    st.markdown('<p class="section-title">🎲 Your Future Simulation</p>', unsafe_allow_html=True)
    st.markdown("Prediksi masa depan keuanganmu dengan 10.000 skenario!")

    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        sim_uang_saku = st.selectbox("💵 Uang Saku", ORDER_UANG_SAKU, index=1)
    with col_sim2:
        sim_budgeting = st.selectbox("📒 Budgeting", ["Ya", "Tidak"])

    if st.button("🚀 GENERATE YOUR FUTURE", type="primary"):
        with st.spinner("🎵 Generating 10,000 scenarios..."):
            n_sim = 10000

            ref_data = filtered[(filtered["uang_saku"] == sim_uang_saku) & (filtered["budgeting"] == sim_budgeting)]
            if len(ref_data) < 5:
                ref_data = filtered[filtered["uang_saku"] == sim_uang_saku]
            if len(ref_data) < 5:
                ref_data = filtered

            def map_to_numeric(series, jenis):
                res = np.zeros(len(series))
                s_str = series.astype(str)
                if jenis == "uang_saku":
                    res = np.where(s_str.str.contains("< Rp 500.000", na=False), np.random.uniform(100000, 499000, len(series)), res)
                    res = np.where(s_str.str.contains("Rp 500.000 - Rp 1.000.000", na=False), np.random.uniform(500000, 1000000, len(series)), res)
                    res = np.where(s_str.str.contains("Rp 1.000.001 - Rp 1.500.000", na=False), np.random.uniform(1000001, 1500000, len(series)), res)
                    res = np.where(s_str.str.contains("> Rp 1.500.001", na=False), np.random.uniform(1500001, 2500000, len(series)), res)
                elif jenis == "pengeluaran":
                    res = np.where(s_str.str.contains("< Rp 500.000", na=False), np.random.uniform(100000, 499000, len(series)), res)
                    res = np.where(s_str.str.contains("Rp 500.000 - Rp 700.000", na=False), np.random.uniform(500000, 700000, len(series)), res)
                    res = np.where(s_str.str.contains("Rp 700.001 - Rp 1.000.000", na=False), np.random.uniform(700001, 1000000, len(series)), res)
                    res = np.where(s_str.str.contains("> Rp 1.000.001", na=False), np.random.uniform(1000001, 1500000, len(series)), res)
                return res

            sampled_us = np.random.choice(ref_data["uang_saku"].values, size=n_sim)
            sampled_exp = np.random.choice(ref_data["total_pengeluaran"].values, size=n_sim)
            sampled_khabis = np.random.choice(ref_data["kehabisan_uang"].values, size=n_sim)

            vals_us = map_to_numeric(pd.Series(sampled_us), "uang_saku")
            vals_exp = map_to_numeric(pd.Series(sampled_exp), "pengeluaran")
            sisa_uang = vals_us - vals_exp

            prob_khabis = np.mean(sampled_khabis == "Ya") * 100
            mean_sisa = np.mean(sisa_uang)
            risk_sisa_negatif = np.mean(sisa_uang < 0) * 100
            p5_sisa = np.percentile(sisa_uang, 5)
            p95_sisa = np.percentile(sisa_uang, 95)

            overall_khabis = np.mean(filtered["kehabisan_uang"] == "Ya") * 100
            delta_khabis = prob_khabis - overall_khabis

            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("📉 PROB. STRUGGLE", f"{prob_khabis:.1f}%",
                        delta=f"{delta_khabis:+.1f}%",
                        delta_color="inverse" if prob_khabis > overall_khabis else "normal")
            kpi2.metric("💰 AVG. LEFTOVER", f"Rp {mean_sisa:,.0f}")
            kpi3.metric("⚠️ DEFICIT RISK", f"{risk_sisa_negatif:.1f}%")

            st.markdown("---")
            st.markdown('<p class="section-title">📊 Your Money Distribution</p>', unsafe_allow_html=True)

            df_sim = pd.DataFrame({"Sisa Uang": sisa_uang})
            fig_sim = px.histogram(df_sim, x="Sisa Uang", nbins=50,
                                   color_discrete_sequence=["#1DB954"],
                                   marginal="box", opacity=0.9)
            fig_sim.add_vline(x=0, line_dash="dash", line_color="#FF6B6B",
                              annotation_text="BREAK EVEN", annotation_font_color="#FF6B6B")
            fig_sim.update_layout(xaxis_title="Sisa Uang (Rp)", yaxis_title="Frekuensi",
                                  showlegend=False, hovermode="x unified")
            style_fig(fig_sim)
            st.plotly_chart(fig_sim, use_container_width=True)

            st.info(f"""
            🎵 **Your Wrapped Insights:**
            - Profil: **{sim_uang_saku}** + Budgeting: **{sim_budgeting}**
            - Rata-rata sisa: **Rp {mean_sisa:,.0f}**
            - Risiko defisit: **{risk_sisa_negatif:.1f}%**
            - 90% Confidence Interval: **Rp {p5_sisa:,.0f}** - **Rp {p95_sisa:,.0f}**
            """)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#b3b3b3; font-size:0.85rem; margin-top: 32px; "
    "font-family: Montserrat, sans-serif; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase;'>"
    "🎵 Your Finance Wrapped · Sains Data · 2026 🎵"
    "</p>",
    unsafe_allow_html=True,
)
