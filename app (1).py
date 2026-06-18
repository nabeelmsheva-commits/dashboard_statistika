import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import chi2_contingency

# ═══════════════════════════════════════════════════════════════
# KONFIGURASI HALAMAN
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Financial Intelligence Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
# LUXURY CYBER Y2K CSS THEME
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Bricolage+Grotesque:wght@400;600;800&family=Inter:wght@400;500;600;700&display=swap');

/* ─── GLOBAL LUXURY BACKGROUND ─── */
.stApp {
    background:
        radial-gradient(circle at 15% 15%, rgba(255, 0, 110, 0.18) 0%, transparent 45%),
        radial-gradient(circle at 85% 85%, rgba(131, 56, 236, 0.18) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(58, 134, 255, 0.12) 0%, transparent 60%),
        radial-gradient(ellipse at top, rgba(255, 190, 11, 0.05) 0%, transparent 50%),
        #0A0118;
    background-attachment: fixed;
    font-family: 'Inter', 'Space Grotesk', sans-serif !important;
    color: #E8E4F5;
}

.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image:
        linear-gradient(rgba(255, 0, 110, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(131, 56, 236, 0.03) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
}

.main .block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1500px;
    position: relative;
    z-index: 1;
}

/* ─── SIDEBAR LUXURY GLASS ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,
        rgba(255, 0, 110, 0.08) 0%,
        rgba(131, 56, 236, 0.08) 50%,
        rgba(58, 134, 255, 0.08) 100%) !important;
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    border-right: 1px solid rgba(255, 0, 110, 0.25) !important;
    box-shadow: 4px 0 40px rgba(255, 0, 110, 0.12);
    position: relative;
}

[data-testid="stSidebar"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, #FF006E, #8338EC, #3A86FF);
    box-shadow: 0 0 20px rgba(255, 0, 110, 0.6);
}

[data-testid="stSidebar"] > div {
    padding: 2rem 1.5rem !important;
}

[data-testid="stSidebar"] h2 {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.4rem !important;
    background: linear-gradient(135deg, #FF006E, #8338EC, #3A86FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    margin-bottom: 1rem !important;
}

[data-testid="stSidebar"] * {
    color: #E0D5F5;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label {
    color: #B8A8D8 !important;
}

/* ─── METRIC CARDS - LUXURY GLASS ─── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg,
        rgba(255, 255, 255, 0.06) 0%,
        rgba(255, 255, 255, 0.02) 100%) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 20px !important;
    padding: 22px 26px !important;
    box-shadow:
        0 8px 32px rgba(255, 0, 110, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #FF006E, #8338EC, #3A86FF, #06FFA5);
    border-radius: 20px 20px 0 0;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow:
        0 16px 48px rgba(255, 0, 110, 0.2),
        0 0 50px rgba(131, 56, 236, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 0, 110, 0.4) !important;
}

[data-testid="stMetric"] label {
    color: #FF006E !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-family: 'Space Grotesk', sans-serif !important;
    opacity: 0.95;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 1.85rem !important;
    font-weight: 700 !important;
    font-family: 'Bricolage Grotesque', sans-serif !important;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #FFFFFF 0%, #FFBE0B 50%, #FF006E 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #06FFA5 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}

/* ─── SECTION TITLES - NEON ACCENT ─── */
.section-title {
    color: #FFFFFF !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    font-family: 'Bricolage Grotesque', sans-serif !important;
    letter-spacing: -0.01em;
    padding-left: 18px !important;
    margin: 32px 0 18px 0 !important;
    position: relative;
    display: inline-block;
}

.section-title::before {
    content: "";
    position: absolute;
    left: 0;
    top: 4px;
    width: 4px;
    height: calc(100% - 8px);
    background: linear-gradient(180deg, #FF006E, #8338EC, #3A86FF);
    border-radius: 4px;
    box-shadow: 0 0 14px rgba(255, 0, 110, 0.7);
}

/* ─── TABS - PILL LUXURY STYLE ─── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 50px;
    padding: 8px;
    gap: 6px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #B8A8D8 !important;
    border-radius: 50px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
    padding: 11px 22px !important;
    transition: all 0.3s ease !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FF006E, #8338EC) !important;
    color: white !important;
    box-shadow:
        0 4px 20px rgba(255, 0, 110, 0.4),
        0 0 20px rgba(131, 56, 236, 0.3);
    font-weight: 600 !important;
}

.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
    background: rgba(255, 0, 110, 0.15) !important;
    color: #FF006E !important;
}

/* ─── BUTTONS - LUXURY GRADIENT PILL ─── */
.stButton > button {
    background: linear-gradient(135deg, #FF006E 0%, #8338EC 50%, #3A86FF 100%) !important;
    background-size: 200% 200% !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 13px 34px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em;
    box-shadow:
        0 4px 20px rgba(255, 0, 110, 0.3),
        0 0 30px rgba(131, 56, 236, 0.2);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.02);
    background-position: right center !important;
    box-shadow:
        0 8px 32px rgba(255, 0, 110, 0.5),
        0 0 40px rgba(131, 56, 236, 0.4);
}

/* ─── SELECTBOX - GLASS PILL ─── */
.stSelectbox > div > div,
.stTextInput > div > div {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 0, 110, 0.25) !important;
    border-radius: 14px !important;
    color: #FFFFFF !important;
    padding: 4px 12px !important;
    transition: all 0.3s ease !important;
}

.stSelectbox > div > div:hover,
.stTextInput > div > div:hover {
    border-color: rgba(255, 0, 110, 0.6) !important;
    box-shadow: 0 0 20px rgba(255, 0, 110, 0.25) !important;
}

.stSelectbox label,
.stTextInput label {
    color: #FFBE0B !important;
    font-weight: 500 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ─── DIVIDER - GRADIENT LINE ─── */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        #FF006E,
        #8338EC,
        #3A86FF,
        transparent);
    margin: 36px 0;
    box-shadow: 0 0 10px rgba(255, 0, 110, 0.4);
}

/* ─── PLOTLY CHARTS - LUXURY GLASS FRAME ─── */
.js-plotly-plot .plotly {
    border-radius: 20px !important;
    background: rgba(255, 255, 255, 0.02) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 14px;
    box-shadow: 0 4px 24px rgba(131, 56, 236, 0.12);
}

/* ─── DATAFRAME - GLASS STYLE ─── */
[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    border: 1px solid rgba(255, 0, 110, 0.2) !important;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.02) !important;
}

[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.04) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(131, 56, 236, 0.3) !important;
    border-radius: 20px !important;
}

/* ─── ALERT / INFO BOX - NEON GLASS ─── */
[data-testid="stAlert"] {
    background: rgba(6, 255, 165, 0.05) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(6, 255, 165, 0.3) !important;
    border-radius: 20px !important;
    box-shadow: 0 4px 20px rgba(6, 255, 165, 0.1);
    color: #E8E4F5 !important;
}

[data-testid="stWarning"] {
    background: rgba(255, 190, 11, 0.06) !important;
    border: 1px solid rgba(255, 190, 11, 0.3) !important;
    border-radius: 20px !important;
}

/* ─── SCROLLBAR - NEON ─── */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: rgba(10, 1, 24, 0.5); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #FF006E, #8338EC, #3A86FF);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #3A86FF, #8338EC, #FF006E);
}

/* ─── ANIMATIONS ─── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 20px rgba(255, 0, 110, 0.3); }
    50% { box-shadow: 0 0 40px rgba(131, 56, 236, 0.5); }
}

.element-container, .stPlotlyChart, [data-testid="stMetric"] {
    animation: fadeInUp 0.6s ease-out forwards;
}

/* ─── HERO TITLE - GRADIENT ANIMATED ─── */
.hero-title {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-weight: 800 !important;
    font-size: 3.2rem !important;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin: 0;
    background: linear-gradient(
        135deg,
        #FF006E 0%,
        #FFBE0B 25%,
        #8338EC 50%,
        #3A86FF 75%,
        #06FFA5 100%
    );
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 6s linear infinite;
}

.hero-subtitle {
    color: #B8A8D8;
    font-size: 1.1rem;
    font-weight: 400;
    margin-top: 14px;
    letter-spacing: 0.02em;
}

/* ─── BADGE / TAG ─── */
.badge-tag {
    display: inline-block;
    padding: 5px 14px;
    background: rgba(255, 0, 110, 0.12);
    border: 1px solid rgba(255, 0, 110, 0.3);
    border-radius: 20px;
    font-size: 0.72rem;
    color: #FF006E;
    font-weight: 600;
    margin-right: 8px;
    backdrop-filter: blur(10px);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ─── LUXURY CARD COMPONENT ─── */
.luxury-card {
    padding: 20px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 18px;
    border: 1px solid rgba(131, 56, 236, 0.25);
    backdrop-filter: blur(14px);
    margin-bottom: 14px;
    transition: all 0.3s ease;
}

.luxury-card:hover {
    border-color: rgba(255, 0, 110, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(255, 0, 110, 0.15);
}

.card-label {
    color: #FFBE0B;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-weight: 600;
    margin-bottom: 6px;
}

.card-value {
    color: white;
    font-size: 1.6rem;
    font-weight: 700;
    font-family: 'Bricolage Grotesque', sans-serif;
    letter-spacing: -0.02em;
}

/* ─── HIDE STREAMLIT BRANDING ─── */
#MainMenu, header, footer { visibility: hidden; }

/* ─── SPINNER CUSTOM ─── */
.stSpinner > div {
    border-top-color: #FF006E !important;
}

/* ─── RESPONSIVE ─── */
@media (max-width: 768px) {
    .hero-title { font-size: 2rem !important; }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════════════
# KATEGORI & TEMA WARNA LUXURY
# ═══════════════════════════════════════════════════════════════
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

WARNA_UTAMA = ["#FF006E", "#8338EC", "#3A86FF", "#06FFA5", "#FFBE0B", "#FB5607"]
BG_PLOT = "rgba(10, 1, 24, 0.5)"
PAPER_BG = "rgba(0, 0, 0, 0)"
FONT_COLOR = "#E8E4F5"
GRID_COLOR = "rgba(255, 0, 110, 0.12)"

def style_fig(fig):
    """Terapkan tema luxury cyber ke semua chart Plotly."""
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=BG_PLOT,
        font=dict(color=FONT_COLOR, family="Inter, Space Grotesk, sans-serif", size=12),
        margin=dict(t=40, b=30, l=20, r=20),
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0.03)",
            bordercolor="rgba(255, 0, 110, 0.2)",
            borderwidth=1,
            font=dict(color="#E8E4F5", family="Inter"),
        ),
    )
    fig.update_xaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor="rgba(131, 56, 236, 0.3)",
        tickfont=dict(color="#B8A8D8", family="Inter"),
    )
    fig.update_yaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor="rgba(131, 56, 236, 0.3)",
        tickfont=dict(color="#B8A8D8", family="Inter"),
    )
    return fig

# ═══════════════════════════════════════════════════════════════
# SIDEBAR - FILTER PANEL
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## Panel Filter")
    st.markdown("---")

    gender_options = ["Semua"] + sorted(df["jenis_kelamin"].unique().tolist())
    gender_filter = st.selectbox("Jenis Kelamin", gender_options)

    uang_saku_options = ["Semua"] + ORDER_UANG_SAKU
    uang_saku_filter = st.selectbox("Kategori Uang Saku", uang_saku_options)

    kehabisan_options = ["Semua", "Ya", "Tidak"]
    kehabisan_filter = st.selectbox("Status Kehabisan Uang", kehabisan_options)

    budgeting_options = ["Semua", "Ya", "Tidak"]
    budgeting_filter = st.selectbox("Status Budgeting", budgeting_options)

    st.markdown("---")

    st.markdown(f"""
    <div class="luxury-card">
        <div class="card-label">Total Responden Survei</div>
        <div class="card-value">{len(df)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="luxury-card">
        <div class="card-label">Data Setelah Filter</div>
        <div class="card-value" id="sidebar-filtered">–</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; opacity: 0.7; font-size: 0.75rem; padding: 8px;">
        <span class="badge-tag">Sains Data</span>
        <span class="badge-tag">2026</span>
        <br><br>
        Financial Intelligence Dashboard
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TERAPKAN FILTER
# ═══════════════════════════════════════════════════════════════
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

# Update counter di sidebar dengan JS
st.markdown(f"""
<script>
document.addEventListener("DOMContentLoaded", function() {{
    setTimeout(function() {{
        const el = document.getElementById("sidebar-filtered");
        if (el) el.textContent = "{n}";
    }}, 100);
}});
</script>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HERO HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div style="padding: 40px 0 20px 0; position: relative;">
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
        <span class="badge-tag">Luxury Analytics</span>
        <span class="badge-tag">Financial Intelligence</span>
        <span class="badge-tag">Sains Data</span>
    </div>
    <h1 class="hero-title">
        Financial Intelligence<br>
        Dashboard
    </h1>
    <p class="hero-subtitle">
        Analisis mendalam pola pengeluaran dan perilaku keuangan mahasiswa Sains Data
    </p>
</div>
<hr>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# KPI CARDS
# ═══════════════════════════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)

pct_kehabisan = round(filtered[filtered["kehabisan_uang"] == "Ya"].shape[0] / n * 100, 1) if n else 0
pct_budgeting = round(filtered[filtered["budgeting"] == "Ya"].shape[0] / n * 100, 1) if n else 0
pct_belanja_sering = round(filtered[filtered["frekuensi_belanja_online"] == "3 kali atau lebih"].shape[0] / n * 100, 1) if n else 0
modus_pengeluaran = filtered["total_pengeluaran"].mode()[0] if n else "-"
modus_uang_saku = filtered["uang_saku"].mode()[0] if n else "-"

k1.metric("Responden Aktif", f"{n}")
k2.metric("Kehabisan Uang", f"{pct_kehabisan}%")
k3.metric("Menerapkan Budgeting", f"{pct_budgeting}%")
k4.metric("Belanja ≥ 3x/bulan", f"{pct_belanja_sering}%")
k5.metric("Modus Pengeluaran", modus_pengeluaran.replace("Rp ", "Rp\u00A0"))

st.markdown("")

# ═══════════════════════════════════════════════════════════════
# TAB NAVIGASI
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Demografi & Distribusi",
    "Pola Pengeluaran",
    "Perilaku Keuangan",
    "Analisis Lanjutan",
    "Simulasi Monte Carlo",
])

# ═══════════════════════════════════════════════════════════════
# TAB 1 – DEMOGRAFI & DISTRIBUSI
# ═══════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-title">Distribusi Jenis Kelamin</p>', unsafe_allow_html=True)
        gender_cnt = filtered["jenis_kelamin"].value_counts().reset_index()
        gender_cnt.columns = ["Jenis Kelamin", "Jumlah"]
        fig = px.pie(
            gender_cnt, names="Jenis Kelamin", values="Jumlah",
            color_discrete_sequence=WARNA_UTAMA, hole=0.55,
        )
        fig.update_traces(
            textfont_size=13,
            textinfo="percent+label",
            marker=dict(line=dict(color='#0A0118', width=2))
        )
        fig.update_layout(showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Distribusi Uang Saku Bulanan</p>', unsafe_allow_html=True)
        uang_cnt = filtered["uang_saku"].value_counts().reindex(ORDER_UANG_SAKU, fill_value=0).reset_index()
        uang_cnt.columns = ["Uang Saku", "Jumlah"]
        fig2 = px.bar(
            uang_cnt, x="Uang Saku", y="Jumlah",
            color="Jumlah",
            color_continuous_scale=[
                [0, "#8338EC"],
                [0.5, "#FF006E"],
                [1, "#FFBE0B"]
            ],
            text="Jumlah",
        )
        fig2.update_traces(
            textposition="outside",
            textfont_color=FONT_COLOR,
            marker=dict(line=dict(color='rgba(255,255,255,0.1)', width=1))
        )
        fig2.update_coloraxes(showscale=False)
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Uang Saku Berdasarkan Jenis Kelamin</p>', unsafe_allow_html=True)
    cross = pd.crosstab(filtered["uang_saku"], filtered["jenis_kelamin"]).reindex(ORDER_UANG_SAKU, fill_value=0)
    fig3 = go.Figure()
    for i, col_name in enumerate(cross.columns):
        fig3.add_trace(go.Bar(
            name=col_name, x=cross.index, y=cross[col_name],
            marker_color=WARNA_UTAMA[i],
            text=cross[col_name], textposition="auto",
            marker=dict(line=dict(color='rgba(255,255,255,0.1)', width=1)),
        ))
    fig3.update_layout(barmode="group", xaxis_title="Kategori Uang Saku", yaxis_title="Jumlah Responden")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 2 – POLA PENGELUARAN
# ═══════════════════════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-title">Total Pengeluaran Bulanan</p>', unsafe_allow_html=True)
        tot_cnt = filtered["total_pengeluaran"].value_counts().reindex(ORDER_TOTAL_PENGELUARAN, fill_value=0).reset_index()
        tot_cnt.columns = ["Total Pengeluaran", "Jumlah"]
        fig = px.bar(
            tot_cnt, x="Total Pengeluaran", y="Jumlah",
            color="Total Pengeluaran", color_discrete_sequence=WARNA_UTAMA,
            text="Jumlah",
        )
        fig.update_traces(
            textposition="outside",
            textfont_color=FONT_COLOR,
            showlegend=False,
            marker=dict(line=dict(color='rgba(255,255,255,0.1)', width=1))
        )
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Faktor Pengeluaran Membengkak</p>', unsafe_allow_html=True)
        faktor_cnt = filtered["faktor_membengkak"].value_counts().reset_index()
        faktor_cnt.columns = ["Faktor", "Jumlah"]
        faktor_cnt["Faktor_short"] = faktor_cnt["Faktor"].str.extract(r'^([^(]+)').iloc[:, 0].str.strip()
        fig2 = px.bar(
            faktor_cnt, y="Faktor_short", x="Jumlah",
            orientation="h", color="Jumlah",
            color_continuous_scale=[
                [0, "#3A86FF"],
                [0.5, "#FF006E"],
                [1, "#FFBE0B"]
            ],
            text="Jumlah",
        )
        fig2.update_traces(
            textposition="outside",
            textfont_color=FONT_COLOR,
            marker=dict(line=dict(color='rgba(255,255,255,0.1)', width=1))
        )
        fig2.update_coloraxes(showscale=False)
        fig2.update_layout(yaxis_title="")
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Perbandingan Kategori Pengeluaran</p>', unsafe_allow_html=True)
    col_makan = filtered["pengeluaran_makan"].value_counts()
    col_transport = filtered["pengeluaran_transport"].value_counts()
    col_hiburan = filtered["pengeluaran_hiburan"].value_counts()
    col_kuliah = filtered["pengeluaran_kuliah"].value_counts()

    breakdown_df = pd.DataFrame({
        "Makan": col_makan,
        "Transport": col_transport,
        "Hiburan": col_hiburan,
        "Kuliah": col_kuliah,
    }).fillna(0).reset_index().rename(columns={"index": "Kategori"})
    breakdown_melt = breakdown_df.melt(id_vars="Kategori", var_name="Jenis", value_name="Jumlah")

    fig3 = px.bar(
        breakdown_melt, x="Kategori", y="Jumlah", color="Jenis",
        barmode="group", color_discrete_sequence=WARNA_UTAMA,
        text="Jumlah",
    )
    fig3.update_traces(
        textposition="outside",
        textfont_color=FONT_COLOR,
        marker=dict(line=dict(color='rgba(255,255,255,0.1)', width=1))
    )
    fig3.update_layout(xaxis_title="Rentang Pengeluaran", yaxis_title="Jumlah Mahasiswa")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<p class="section-title">Frekuensi Belanja Online</p>', unsafe_allow_html=True)
    belanja_cnt = filtered["frekuensi_belanja_online"].value_counts().reset_index()
    belanja_cnt.columns = ["Frekuensi", "Jumlah"]
    fig4 = px.pie(
        belanja_cnt, names="Frekuensi", values="Jumlah",
        color_discrete_sequence=WARNA_UTAMA, hole=0.55,
    )
    fig4.update_traces(
        textfont_size=13,
        textinfo="percent+label",
        marker=dict(line=dict(color='#0A0118', width=2))
    )
    style_fig(fig4)
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.plotly_chart(fig4, use_container_width=True)
    with col_b:
        freq_tbl = belanja_cnt.copy()
        freq_tbl["Persentase"] = (freq_tbl["Jumlah"] / n * 100).round(1).astype(str) + "%"
        st.dataframe(freq_tbl, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3 – PERILAKU KEUANGAN
# ═══════════════════════════════════════════════════════════════
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-title">Status Kehabisan Uang</p>', unsafe_allow_html=True)
        kh_cnt = filtered["kehabisan_uang"].value_counts().reset_index()
        kh_cnt.columns = ["Status", "Jumlah"]
        fig = px.pie(kh_cnt, names="Status", values="Jumlah", hole=0.55,
                     color="Status",
                     color_discrete_map={"Ya": "#FF006E", "Tidak": "#06FFA5"})
        fig.update_traces(
            textfont_size=13,
            textinfo="percent+label",
            marker=dict(line=dict(color='#0A0118', width=2))
        )
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Status Penerapan Budgeting</p>', unsafe_allow_html=True)
        bd_cnt = filtered["budgeting"].value_counts().reset_index()
        bd_cnt.columns = ["Status", "Jumlah"]
        fig2 = px.pie(bd_cnt, names="Status", values="Jumlah", hole=0.55,
                      color="Status",
                      color_discrete_map={"Ya": "#8338EC", "Tidak": "#FFBE0B"})
        fig2.update_traces(
            textfont_size=13,
            textinfo="percent+label",
            marker=dict(line=dict(color='#0A0118', width=2))
        )
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Hubungan Budgeting vs Kehabisan Uang</p>', unsafe_allow_html=True)
    cross_bk = pd.crosstab(filtered["budgeting"], filtered["kehabisan_uang"])
    cross_bk_pct = (cross_bk.div(cross_bk.sum(axis=1), axis=0) * 100).round(1)

    fig3 = go.Figure()
    colors_map = {"Ya": "#FF006E", "Tidak": "#06FFA5"}
    for col_name in cross_bk_pct.columns:
        fig3.add_trace(go.Bar(
            name=f"Kehabisan: {col_name}",
            x=cross_bk_pct.index,
            y=cross_bk_pct[col_name],
            marker_color=colors_map.get(col_name, WARNA_UTAMA[0]),
            text=cross_bk_pct[col_name].map(lambda v: f"{v:.1f}%"),
            textposition="inside",
            marker=dict(line=dict(color='rgba(255,255,255,0.1)', width=1)),
        ))
    fig3.update_layout(
        barmode="stack",
        xaxis_title="Status Budgeting",
        yaxis_title="Persentase (%)",
    )
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<p class="section-title">Kehabisan Uang Berdasarkan Uang Saku</p>', unsafe_allow_html=True)
    cross_us = pd.crosstab(
        filtered["uang_saku"], filtered["kehabisan_uang"]
    ).reindex(ORDER_UANG_SAKU, fill_value=0)
    cross_us_pct = (cross_us.div(cross_us.sum(axis=1), axis=0) * 100).round(1)

    fig4 = go.Figure()
    for col_name in cross_us_pct.columns:
        fig4.add_trace(go.Bar(
            name=f"Kehabisan: {col_name}",
            x=cross_us_pct.index,
            y=cross_us_pct[col_name],
            marker_color=colors_map.get(col_name, WARNA_UTAMA[0]),
            text=cross_us_pct[col_name].map(lambda v: f"{v:.1f}%"),
            textposition="inside",
            marker=dict(line=dict(color='rgba(255,255,255,0.1)', width=1)),
        ))
    fig4.update_layout(
        barmode="stack",
        xaxis_title="Kategori Uang Saku",
        yaxis_title="Persentase (%)",
    )
    style_fig(fig4)
    st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 4 – ANALISIS LANJUTAN
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-title">Tabel Frekuensi Detail</p>', unsafe_allow_html=True)
    col_select = st.selectbox("Pilih Variabel:", [
        "uang_saku", "total_pengeluaran", "pengeluaran_makan",
        "pengeluaran_transport", "pengeluaran_hiburan", "pengeluaran_kuliah",
        "kehabisan_uang", "budgeting", "faktor_membengkak", "frekuensi_belanja_online",
        "jenis_kelamin",
    ])

    freq_df = filtered[col_select].value_counts().reset_index()
    freq_df.columns = ["Kategori", "Frekuensi"]
    freq_df["Persentase"] = (freq_df["Frekuensi"] / n * 100).round(2).astype(str) + "%"
    freq_df["Kumulatif"] = freq_df["Frekuensi"].cumsum()
    modus_val = freq_df.iloc[0]["Kategori"]

    col_m, col_t = st.columns([2, 1])
    with col_m:
        fig_f = px.bar(
            freq_df, x="Kategori", y="Frekuensi",
            color="Frekuensi",
            color_continuous_scale=[
                [0, "#3A86FF"],
                [0.5, "#FF006E"],
                [1, "#FFBE0B"]
            ],
            text="Persentase",
        )
        fig_f.update_traces(
            textposition="outside",
            textfont_color=FONT_COLOR,
            marker=dict(line=dict(color='rgba(255,255,255,0.1)', width=1))
        )
        fig_f.update_coloraxes(showscale=False)
        style_fig(fig_f)
        st.plotly_chart(fig_f, use_container_width=True)
    with col_t:
        st.markdown(f"""
        <div class="luxury-card">
            <div class="card-label">Modus (Nilai Terbanyak)</div>
            <div class="card-value" style="font-size: 1.1rem;">{modus_val}</div>
        </div>
        <div class="luxury-card">
            <div class="card-label">Jumlah Observasi</div>
            <div class="card-value">{n}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        st.dataframe(freq_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    st.markdown('<p class="section-title">Heatmap Asosiasi Antar Variabel (Cramér\'s V)</p>', unsafe_allow_html=True)

    cat_cols = [
        "uang_saku", "total_pengeluaran", "pengeluaran_makan",
        "pengeluaran_transport", "pengeluaran_hiburan", "pengeluaran_kuliah",
        "kehabisan_uang", "budgeting", "faktor_membengkak",
        "frekuensi_belanja_online", "jenis_kelamin",
    ]
    cat_labels = [
        "Uang Saku", "Total", "Makan",
        "Transport", "Hiburan", "Kuliah",
        "Kehabisan", "Budget", "Faktor",
        "Belanja", "Gender",
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
            z=np.round(matrix, 2),
            x=cat_labels, y=cat_labels,
            colorscale=[
                [0, "#0A0118"],
                [0.25, "#3A86FF"],
                [0.5, "#8338EC"],
                [0.75, "#FF006E"],
                [1, "#FFBE0B"]
            ],
            zmin=0, zmax=1,
            text=np.round(matrix, 2),
            texttemplate="%{text}",
            textfont={"size": 10, "color": "white"},
        ))
        fig_heat.update_layout(
            height=550,
            xaxis=dict(tickangle=-30),
        )
        style_fig(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True)
        st.caption("Cramér's V: 0 = tidak ada asosiasi, 1 = asosiasi sempurna")
    else:
        st.warning("Data tidak mencukupi. Hapus filter untuk melihat heatmap.")

    st.markdown("---")

    st.markdown('<p class="section-title">Data Mentah (Filtered)</p>', unsafe_allow_html=True)
    with st.expander("Tampilkan Data"):
        st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Unduh CSV (Filtered)",
            data=csv,
            file_name="data_filtered.csv",
            mime="text/csv",
        )

# ═══════════════════════════════════════════════════════════════
# TAB 5 – SIMULASI MONTE CARLO
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<p class="section-title">Simulasi Monte Carlo: Proyeksi Risiko Keuangan</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding: 18px 22px; background: rgba(131,56,236,0.08);
                border-left: 3px solid #8338EC; border-radius: 14px;
                color: #E8E4F5; font-size: 0.95rem; margin-bottom: 20px;
                backdrop-filter: blur(10px);">
        Simulasi ini menjalankan <b>10.000 skenario</b> secara acak untuk memproyeksikan probabilitas kehabisan uang
        dan distribusi sisa uang bulanan berdasarkan distribusi empiris dari data survei yang sedang aktif.
    </div>
    """, unsafe_allow_html=True)

    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        sim_uang_saku = st.selectbox("Skenario Uang Saku", ORDER_UANG_SAKU, index=1)
    with col_sim2:
        sim_budgeting = st.selectbox("Skenario Budgeting", ["Ya", "Tidak"])

    if st.button("Jalankan Simulasi Monte Carlo", type="primary"):
        with st.spinner("Memproses 10.000 iterasi simulasi..."):
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
            kpi1.metric(
                "Probabilitas Kehabisan Uang",
                f"{prob_khabis:.1f}%",
                delta=f"{delta_khabis:+.1f}% vs rata-rata",
                delta_color="inverse" if prob_khabis > overall_khabis else "normal"
            )
            kpi2.metric(
                "Rata-rata Sisa Uang",
                f"Rp {mean_sisa:,.0f}"
            )
            kpi3.metric(
                "Risiko Defisit (Sisa < 0)",
                f"{risk_sisa_negatif:.1f}%"
            )

            st.markdown("---")

            st.markdown('<p class="section-title">Distribusi Sisa Uang Bulanan (10.000 Simulasi)</p>', unsafe_allow_html=True)

            df_sim = pd.DataFrame({"Sisa Uang": sisa_uang})
            fig_sim = px.histogram(
                df_sim, x="Sisa Uang", nbins=50,
                color_discrete_sequence=["#FF006E"],
                marginal="box",
                opacity=0.85
            )
            fig_sim.add_vline(
                x=0,
                line_dash="dash",
                line_color="#FFBE0B",
                line_width=3,
                annotation_text="Titik Impas (Rp 0)",
                annotation_font_color="#FFBE0B",
                annotation_font_size=12,
            )
            fig_sim.add_vrect(
                x0=float("-inf"), x1=0,
                fillcolor="#FF006E", opacity=0.1,
                line_width=0,
                annotation_text="Zona Defisit",
                annotation_position="top left",
                annotation_font_color="#FF006E",
            )

            fig_sim.update_layout(
                xaxis_title="Sisa Uang (Rp)",
                yaxis_title="Frekuensi",
                showlegend=False,
                hovermode="x unified"
            )
            style_fig(fig_sim)
            st.plotly_chart(fig_sim, use_container_width=True)

            st.markdown(f"""
            <div style="padding: 26px; background: rgba(6,255,165,0.05);
                        border: 1px solid rgba(6,255,165,0.3); border-radius: 22px;
                        backdrop-filter: blur(20px); margin-top: 20px;">
                <div style="color: #06FFA5; font-size: 0.8rem;
                            text-transform: uppercase; letter-spacing: 0.15em;
                            font-weight: 700; margin-bottom: 14px;">
                    Interpretasi Simulasi
                </div>
                <div style="color: #E8E4F5; line-height: 1.9;">
                    <div>Berdasarkan profil <b style="color:#FFBE0B">Uang Saku: {sim_uang_saku}</b> dan <b style="color:#FF006E">Budgeting: {sim_budgeting}</b>, simulasi menunjukkan rata-rata sisa uang sebesar <b style="color:#06FFA5">Rp {mean_sisa:,.0f}</b>.</div>
                    <div>Terdapat risiko <b style="color:#FF006E">{risk_sisa_negatif:.1f}%</b> di mana pengeluaran melebihi uang saku (defisit).</div>
                    <div>Rentang sisa uang yang paling mungkin terjadi (90% confidence interval) adalah antara <b style="color:#3A86FF">Rp {p5_sisa:,.0f}</b> hingga <b style="color:#3A86FF">Rp {p95_sisa:,.0f}</b>.</div>
                    <div style="margin-top: 14px; color: #B8A8D8; font-size: 0.9rem; font-style: italic;">
                        Area histogram di sebelah kiri garis kuning (Rp 0) merepresentasikan skenario kehabisan uang sebelum akhir bulan.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; padding: 32px 0;">
        <div style="color: #FFBE0B; font-size: 0.72rem;
                    text-transform: uppercase; letter-spacing: 0.2em;
                    margin-bottom: 10px; font-weight: 600;">
            Luxury Financial Analytics
        </div>
        <div style="background: linear-gradient(135deg, #FF006E, #8338EC, #3A86FF);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    font-family: 'Bricolage Grotesque', sans-serif;
                    font-size: 1.2rem;
                    font-weight: 700;">
            Financial Intelligence Dashboard · Sains Data · 2026
        </div>
        <div style="color: #B8A8D8; font-size: 0.82rem; margin-top: 10px;">
            Dibuat untuk keperluan studi statistika dan analisis data
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
