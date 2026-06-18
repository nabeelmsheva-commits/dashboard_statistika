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
    page_title="Financial Intelligence Report",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
# EDITORIAL THEME · BLOOMBERG × THE ECONOMIST
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,500&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,500;0,8..60,600;0,8..60,700;1,8..60,400&family=Source+Sans+3:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ─── ROOT: EDITORIAL PALETTE ─── */
:root {
    --navy: #0A2540;
    --navy-deep: #061A30;
    --burgundy: #C8102E;
    --burgundy-soft: #8B0A1F;
    --gold-accent: #B8860B;
    --cream: #FAF8F5;
    --cream-warm: #F5F1EA;
    --paper: #FFFFFF;
    --ink: #1A1A1A;
    --ink-soft: #3D3D3D;
    --slate: #64748B;
    --line: #E5E0D8;
    --line-strong: #C9C2B5;
    --rule: #1A1A1A;
}

/* ─── GLOBAL BACKGROUND: WARM PAPER ─── */
.stApp {
    background: var(--cream);
    background-image: 
        radial-gradient(ellipse at top, rgba(184, 134, 11, 0.03) 0%, transparent 50%),
        radial-gradient(ellipse at bottom, rgba(200, 16, 46, 0.02) 0%, transparent 50%);
    background-attachment: fixed;
    font-family: 'Source Sans 3', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--ink);
}

/* Subtle paper texture overlay */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
        repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(26, 26, 26, 0.015) 39px, rgba(26, 26, 26, 0.015) 40px);
    pointer-events: none;
    z-index: 0;
}

.main .block-container {
    padding-top: 3.5rem;
    padding-bottom: 4rem;
    max-width: 1400px;
    position: relative;
    z-index: 1;
}

/* ─── SIDEBAR: CLASSIC EDITORIAL ─── */
[data-testid="stSidebar"] {
    background: var(--paper) !important;
    border-right: 1px solid var(--line) !important;
    box-shadow: 0 0 40px rgba(10, 37, 64, 0.04);
}

[data-testid="stSidebar"] > div {
    padding: 2.5rem 1.75rem !important;
}

[data-testid="stSidebar"] h2 {
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    font-size: 1.6rem !important;
    color: var(--navy) !important;
    letter-spacing: -0.01em;
    margin-bottom: 0.5rem !important;
    padding-bottom: 0.75rem !important;
    border-bottom: 2px solid var(--rule) !important;
}

[data-testid="stSidebar"] * {
    color: var(--ink-soft);
    font-family: 'Source Sans 3', sans-serif !important;
}

[data-testid="stSidebar"] label {
    color: var(--slate) !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    margin-bottom: 6px !important;
    font-family: 'Source Sans 3', sans-serif !important;
}

/* ─── METRIC CARDS: EDITORIAL STATS ─── */
[data-testid="stMetric"] {
    background: var(--paper) !important;
    border: none !important;
    border-top: 3px solid var(--rule) !important;
    border-radius: 0 !important;
    padding: 20px 24px !important;
    box-shadow: 
        0 1px 3px rgba(10, 37, 64, 0.04),
        0 4px 12px rgba(10, 37, 64, 0.03) !important;
    transition: all 0.3s ease;
    position: relative;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 
        0 2px 6px rgba(10, 37, 64, 0.06),
        0 12px 28px rgba(10, 37, 64, 0.06) !important;
    border-top-color: var(--burgundy) !important;
}

[data-testid="stMetric"] label {
    color: var(--slate) !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-family: 'Source Sans 3', sans-serif !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--navy) !important;
    font-size: 2rem !important;
    font-weight: 500 !important;
    font-family: 'Playfair Display', serif !important;
    letter-spacing: -0.02em;
}

[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: var(--burgundy) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ─── SECTION TITLES: EDITORIAL RULE ─── */
.section-title {
    color: var(--ink) !important;
    font-size: 1.4rem !important;
    font-weight: 600 !important;
    font-family: 'Playfair Display', serif !important;
    letter-spacing: -0.01em;
    padding: 0 0 12px 0 !important;
    margin: 48px 0 24px 0 !important;
    position: relative;
    display: block;
    border-bottom: 1px solid var(--line);
}

.section-title::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: -1px;
    width: 60px;
    height: 3px;
    background: var(--burgundy);
}

.section-kicker {
    display: block;
    color: var(--burgundy);
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 6px;
    font-family: 'Source Sans 3', sans-serif;
}

/* ─── TABS: MINIMAL UNDERLINE ─── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-radius: 0;
    padding: 0;
    gap: 0;
    border-bottom: 1px solid var(--line);
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: var(--slate) !important;
    border-radius: 0 !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    padding: 14px 24px !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.02em;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -1px;
}

.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: var(--navy) !important;
    font-weight: 600 !important;
    border-bottom: 2px solid var(--burgundy) !important;
    box-shadow: none !important;
}

.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
    background: transparent !important;
    color: var(--navy) !important;
    border-bottom: 2px solid var(--line-strong) !important;
}

/* ─── BUTTONS: EDITORIAL CTA ─── */
.stButton > button {
    background: var(--navy) !important;
    color: var(--cream) !important;
    border: 1px solid var(--navy) !important;
    border-radius: 2px !important;
    padding: 12px 32px !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    transition: all 0.25s ease !important;
}

.stButton > button:hover {
    background: var(--burgundy) !important;
    border-color: var(--burgundy) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(200, 16, 46, 0.2);
}

/* ─── SELECTBOX: CLASSIC ─── */
.stSelectbox > div > div,
.stTextInput > div > div {
    background: var(--paper) !important;
    border: 1px solid var(--line) !important;
    border-radius: 2px !important;
    color: var(--ink) !important;
    padding: 6px 12px !important;
    transition: all 0.2s ease !important;
}

.stSelectbox > div > div:hover,
.stTextInput > div > div:hover {
    border-color: var(--navy) !important;
}

.stSelectbox label,
.stTextInput label {
    color: var(--slate) !important;
    font-weight: 600 !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

/* ─── DIVIDER: EDITORIAL RULE ─── */
hr {
    border: none;
    height: 1px;
    background: var(--line);
    margin: 56px 0;
    position: relative;
}

hr::before {
    content: "§";
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    background: var(--cream);
    padding: 0 16px;
    color: var(--line-strong);
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
}

/* ─── PLOTLY CHARTS: CLEAN PAPER ─── */
.js-plotly-plot .plotly {
    border-radius: 2px !important;
    background: var(--paper) !important;
    border: 1px solid var(--line);
    padding: 20px;
    box-shadow: 0 1px 3px rgba(10, 37, 64, 0.04);
}

/* ─── DATAFRAME: CLASSIC TABLE ─── */
[data-testid="stDataFrame"] {
    border-radius: 2px !important;
    border: 1px solid var(--line) !important;
    overflow: hidden;
    background: var(--paper) !important;
}

[data-testid="stExpander"] {
    background: var(--paper) !important;
    border: 1px solid var(--line) !important;
    border-radius: 2px !important;
}

/* ─── ALERT / INFO: EDITORIAL NOTE ─── */
[data-testid="stAlert"] {
    background: var(--cream-warm) !important;
    border-left: 3px solid var(--burgundy) !important;
    border-radius: 0 !important;
    color: var(--ink-soft) !important;
    font-family: 'Source Serif 4', serif !important;
    font-style: italic;
}

[data-testid="stWarning"] {
    background: #FFF8E7 !important;
    border-left: 3px solid var(--gold-accent) !important;
    border-radius: 0 !important;
}

[data-testid="stInfo"] {
    background: var(--cream-warm) !important;
    border-left: 3px solid var(--navy) !important;
    border-radius: 0 !important;
}

/* ─── SCROLLBAR: SUBTLE ─── */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--cream); }
::-webkit-scrollbar-thumb {
    background: var(--line-strong);
    border-radius: 0;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--navy);
}

/* ─── ANIMATIONS: SUBTLE FADE ─── */
@keyframes editorialFade {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.element-container, .stPlotlyChart, [data-testid="stMetric"] {
    animation: editorialFade 0.5s ease-out forwards;
}

/* ─── HERO SECTION: NEWSPAPER MASTHEAD ─── */
.masthead {
    text-align: center;
    padding: 20px 0;
    border-top: 3px double var(--rule);
    border-bottom: 3px double var(--rule);
    margin-bottom: 32px;
}

.masthead-date {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--slate);
    font-weight: 500;
    margin-bottom: 8px;
}

.masthead-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    font-weight: 900;
    color: var(--navy);
    letter-spacing: -0.02em;
    line-height: 1;
    margin: 12px 0;
}

.masthead-subtitle {
    font-family: 'Source Serif 4', serif;
    font-style: italic;
    color: var(--ink-soft);
    font-size: 1.05rem;
    font-weight: 400;
    letter-spacing: 0.01em;
}

.masthead-rule {
    display: flex;
    justify-content: center;
    gap: 24px;
    margin-top: 16px;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--slate);
}

.masthead-rule span {
    padding: 0 16px;
    border-right: 1px solid var(--line-strong);
}

.masthead-rule span:last-child {
    border-right: none;
}

/* ─── EDITORIAL CARD: PULL QUOTE STYLE ─── */
.editorial-card {
    padding: 24px 28px;
    background: var(--paper);
    border-top: 3px solid var(--burgundy);
    border-left: 1px solid var(--line);
    border-right: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.editorial-card:hover {
    border-left-width: 3px;
    border-left-color: var(--burgundy);
    box-shadow: 0 4px 16px rgba(10, 37, 64, 0.06);
}

.card-kicker {
    color: var(--burgundy);
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-weight: 600;
    margin-bottom: 8px;
    font-family: 'Source Sans 3', sans-serif;
}

.card-stat {
    color: var(--navy);
    font-size: 1.8rem;
    font-weight: 500;
    font-family: 'Playfair Display', serif;
    letter-spacing: -0.02em;
    line-height: 1.1;
}

.card-caption {
    color: var(--slate);
    font-size: 0.85rem;
    margin-top: 8px;
    font-family: 'Source Serif 4', serif;
    font-style: italic;
}

/* ─── BADGE: NEWSPAPER TAG ─── */
.editorial-tag {
    display: inline-block;
    padding: 3px 10px;
    background: var(--navy);
    color: var(--cream);
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-right: 6px;
    font-family: 'Source Sans 3', sans-serif;
}

/* ─── FOOTER: COLOPHON ─── */
.colophon {
    border-top: 3px double var(--rule);
    padding-top: 32px;
    margin-top: 56px;
    text-align: center;
}

/* ─── HIDE STREAMLIT BRANDING ─── */
#MainMenu, header, footer { visibility: hidden; }

/* ─── RESPONSIVE ─── */
@media (max-width: 768px) {
    .masthead-title { font-size: 2.2rem !important; }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
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
# EDITORIAL PALETTE
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

# Editorial palette: Navy, Burgundy, Gold, Sage, Slate
WARNA_UTAMA = ["#0A2540", "#C8102E", "#B8860B", "#5B7F5B", "#8B7355", "#4A6FA5"]
BG_PLOT = "#FFFFFF"
PAPER_BG = "#FFFFFF"
FONT_COLOR = "#1A1A1A"
GRID_COLOR = "rgba(26, 26, 26, 0.08)"

def style_fig(fig):
    """Terapkan tema editorial ke semua chart Plotly."""
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=BG_PLOT,
        font=dict(color=FONT_COLOR, family="Source Sans 3, sans-serif", size=12),
        margin=dict(t=50, b=40, l=30, r=30),
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0.95)",
            bordercolor="#E5E0D8",
            borderwidth=1,
            font=dict(color="#1A1A1A", family="Source Sans 3", size=11),
        ),
        title_font=dict(family="Playfair Display, serif", size=18, color="#0A2540"),
    )
    fig.update_xaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor="#C9C2B5",
        tickfont=dict(color="#64748B", family="Source Sans 3", size=11),
        linecolor="#E5E0D8",
    )
    fig.update_yaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor="#C9C2B5",
        tickfont=dict(color="#64748B", family="Source Sans 3", size=11),
        linecolor="#E5E0D8",
    )
    return fig

def style_fig_3d(fig):
    """Terapkan tema editorial untuk chart 3D."""
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, family="Source Sans 3, sans-serif", size=12),
        margin=dict(t=50, b=40, l=30, r=30),
        title_font=dict(family="Playfair Display, serif", size=18, color="#0A2540"),
    )
    return fig

# ═══════════════════════════════════════════════════════════════
# SIDEBAR: EDITORIAL INDEX
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## Indeks Laporan")
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
    <div class="editorial-card">
        <div class="card-kicker">Sampel Survei</div>
        <div class="card-stat">{len(df)}</div>
        <div class="card-caption">responden tercatat dalam basis data</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="editorial-card">
        <div class="card-kicker">Sampel Aktif</div>
        <div class="card-stat" id="sidebar-filtered">–</div>
        <div class="card-caption">setelah filter diterapkan</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="padding: 8px 0;">
        <div style="color: #C8102E; font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase; font-weight: 600; margin-bottom: 8px;">
            Colophon
        </div>
        <div style="color: #1A1A1A; font-size: 0.85rem; line-height: 1.7; font-family: 'Source Serif 4', serif;">
            Survei Analisis Statistika<br>
            Program Studi Sains Data<br>
            <em style="color: #64748B;">Edisi Juni 2026</em>
        </div>
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
# MASTHEAD (NEWSPAPER HEADER)
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="masthead">
    <div class="masthead-date">Kamis, 18 Juni 2026 · Edisi Khusus</div>
    <h1 class="masthead-title">The Financial Intelligencer</h1>
    <div class="masthead-subtitle">"Sebuah laporan analitis mengenai perilaku keuangan mahasiswa Sains Data"</div>
    <div class="masthead-rule">
        <span>Vol. MMXXVI</span>
        <span>Laporan Statistik</span>
        <span>Sains Data</span>
        <span>Hal. 1</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="max-width: 720px; margin: 0 auto 40px auto; text-align: center; font-family: 'Source Serif 4', serif; font-size: 1.1rem; line-height: 1.7; color: #3D3D3D;">
    <em>Bagaimana mahasiswa Sains Data mengelola keuangan mereka di tengah tekanan akademik dan gaya hidup modern? 
    Laporan ini menyajikan temuan dari survei komprehensif terhadap pola pengeluaran, perilaku finansial, 
    dan strategi pengelolaan anggaran.</em>
</div>
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
    "Demografi",
    "Pola Pengeluaran",
    "Perilaku Keuangan",
    "Analisis Lanjutan",
    "Simulasi Monte Carlo",
])

# ═══════════════════════════════════════════════════════════════
# TAB 1 – DEMOGRAFI
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<span class="section-kicker">Bagian I</span><p class="section-title">Potret Demografis Responden</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        gender_cnt = filtered["jenis_kelamin"].value_counts().reset_index()
        gender_cnt.columns = ["Jenis Kelamin", "Jumlah"]
        fig = px.pie(
            gender_cnt, names="Jenis Kelamin", values="Jumlah",
            color_discrete_sequence=WARNA_UTAMA, hole=0.5,
        )
        fig.update_traces(
            textfont_size=13,
            textinfo="percent+label",
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        fig.update_layout(showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        uang_cnt = filtered["uang_saku"].value_counts().reindex(ORDER_UANG_SAKU, fill_value=0).reset_index()
        uang_cnt.columns = ["Uang Saku", "Jumlah"]
        fig2 = px.bar(
            uang_cnt, x="Uang Saku", y="Jumlah",
            color="Jumlah",
            color_continuous_scale=[
                [0, "#4A6FA5"],
                [0.5, "#0A2540"],
                [1, "#C8102E"]
            ],
            text="Jumlah",
        )
        fig2.update_traces(
            textposition="outside",
            textfont_color="#1A1A1A",
            marker=dict(line=dict(color='#FFFFFF', width=1))
        )
        fig2.update_coloraxes(showscale=False)
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<span class="section-kicker">Analisis Silang</span><p class="section-title">Uang Saku Berdasarkan Jenis Kelamin</p>', unsafe_allow_html=True)
    cross = pd.crosstab(filtered["uang_saku"], filtered["jenis_kelamin"]).reindex(ORDER_UANG_SAKU, fill_value=0)
    fig3 = go.Figure()
    for i, col_name in enumerate(cross.columns):
        fig3.add_trace(go.Bar(
            name=col_name, x=cross.index, y=cross[col_name],
            marker_color=WARNA_UTAMA[i],
            text=cross[col_name], textposition="auto",
            marker=dict(line=dict(color='#FFFFFF', width=1)),
        ))
    fig3.update_layout(barmode="group", xaxis_title="Kategori Uang Saku", yaxis_title="Jumlah Responden")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 2 – POLA PENGELUARAN + 3D
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<span class="section-kicker">Bagian II</span><p class="section-title">Anatomi Pengeluaran Bulanan</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        tot_cnt = filtered["total_pengeluaran"].value_counts().reindex(ORDER_TOTAL_PENGELUARAN, fill_value=0).reset_index()
        tot_cnt.columns = ["Total Pengeluaran", "Jumlah"]
        fig = px.bar(
            tot_cnt, x="Total Pengeluaran", y="Jumlah",
            color="Total Pengeluaran", color_discrete_sequence=WARNA_UTAMA,
            text="Jumlah",
        )
        fig.update_traces(
            textposition="outside",
            textfont_color="#1A1A1A",
            showlegend=False,
            marker=dict(line=dict(color='#FFFFFF', width=1))
        )
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        faktor_cnt = filtered["faktor_membengkak"].value_counts().reset_index()
        faktor_cnt.columns = ["Faktor", "Jumlah"]
        faktor_cnt["Faktor_short"] = faktor_cnt["Faktor"].str.extract(r'^([^(]+)').iloc[:, 0].str.strip()
        fig2 = px.bar(
            faktor_cnt, y="Faktor_short", x="Jumlah",
            orientation="h", color="Jumlah",
            color_continuous_scale=[
                [0, "#B8860B"],
                [0.5, "#C8102E"],
                [1, "#0A2540"]
            ],
            text="Jumlah",
        )
        fig2.update_traces(
            textposition="outside",
            textfont_color="#1A1A1A",
            marker=dict(line=dict(color='#FFFFFF', width=1))
        )
        fig2.update_coloraxes(showscale=False)
        fig2.update_layout(yaxis_title="")
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    # 3D CHART: Perbandingan Kategori Pengeluaran
    st.markdown('<span class="section-kicker">Visualisasi Tiga Dimensi</span><p class="section-title">Peta Pengeluaran per Kategori</p>', unsafe_allow_html=True)
    
    col_makan = filtered["pengeluaran_makan"].value_counts().reset_index()
    col_makan.columns = ["Range", "Jumlah"]
    col_makan["Kategori"] = "Makan"
    
    col_transport = filtered["pengeluaran_transport"].value_counts().reset_index()
    col_transport.columns = ["Range", "Jumlah"]
    col_transport["Kategori"] = "Transport"
    
    col_hiburan = filtered["pengeluaran_hiburan"].value_counts().reset_index()
    col_hiburan.columns = ["Range", "Jumlah"]
    col_hiburan["Kategori"] = "Hiburan"
    
    col_kuliah = filtered["pengeluaran_kuliah"].value_counts().reset_index()
    col_kuliah.columns = ["Range", "Jumlah"]
    col_kuliah["Kategori"] = "Kuliah"
    
    combined = pd.concat([col_makan, col_transport, col_hiburan, col_kuliah])
    
    fig3d = go.Figure(data=[
        go.Scatter3d(
            x=combined["Kategori"],
            y=combined["Range"],
            z=combined["Jumlah"],
            mode='markers',
            marker=dict(
                size=combined["Jumlah"] / combined["Jumlah"].max() * 14 + 6,
                color=combined["Jumlah"],
                colorscale=[
                    [0, "#FAF8F5"],
                    [0.3, "#4A6FA5"],
                    [0.6, "#0A2540"],
                    [1, "#C8102E"]
                ],
                opacity=0.9,
                colorbar=dict(
                    title='Jumlah',
                    tickfont=dict(color="#1A1A1A"),
                    titlefont=dict(color="#0A2540")
                ),
                line=dict(color='#0A2540', width=1)
            ),
            text=combined.apply(lambda r: f"{r['Kategori']}<br>{r['Range']}<br>{r['Jumlah']} mhs", axis=1),
            hoverinfo='text'
        )
    ])
    
    fig3d.update_layout(
        scene=dict(
            xaxis=dict(
                title='Kategori',
                backgroundcolor="#FAF8F5",
                gridcolor="#E5E0D8",
                titlefont=dict(family="Playfair Display, serif", color="#0A2540")
            ),
            yaxis=dict(
                title='Rentang',
                backgroundcolor="#FAF8F5",
                gridcolor="#E5E0D8",
                titlefont=dict(family="Playfair Display, serif", color="#0A2540")
            ),
            zaxis=dict(
                title='Jumlah Mahasiswa',
                backgroundcolor="#FAF8F5",
                gridcolor="#E5E0D8",
                titlefont=dict(family="Playfair Display, serif", color="#0A2540")
            ),
        ),
        height=600,
        margin=dict(t=40, b=30)
    )
    style_fig_3d(fig3d)
    st.plotly_chart(fig3d, use_container_width=True)
    
    st.markdown('<span class="section-kicker">Perilaku Digital</span><p class="section-title">Frekuensi Belanja Online</p>', unsafe_allow_html=True)
    belanja_cnt = filtered["frekuensi_belanja_online"].value_counts().reset_index()
    belanja_cnt.columns = ["Frekuensi", "Jumlah"]
    fig4 = px.pie(
        belanja_cnt, names="Frekuensi", values="Jumlah",
        color_discrete_sequence=WARNA_UTAMA, hole=0.5,
    )
    fig4.update_traces(
        textfont_size=13,
        textinfo="percent+label",
        marker=dict(line=dict(color='#FFFFFF', width=2))
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
# TAB 3 – PERILAKU + 3D
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<span class="section-kicker">Bagian III</span><p class="section-title">Perilaku dan Kebiasaan Finansial</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        kh_cnt = filtered["kehabisan_uang"].value_counts().reset_index()
        kh_cnt.columns = ["Status", "Jumlah"]
        fig = px.pie(kh_cnt, names="Status", values="Jumlah", hole=0.5,
                     color="Status",
                     color_discrete_map={"Ya": "#C8102E", "Tidak": "#5B7F5B"})
        fig.update_traces(
            textfont_size=13,
            textinfo="percent+label",
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        bd_cnt = filtered["budgeting"].value_counts().reset_index()
        bd_cnt.columns = ["Status", "Jumlah"]
        fig2 = px.pie(bd_cnt, names="Status", values="Jumlah", hole=0.5,
                      color="Status",
                      color_discrete_map={"Ya": "#0A2540", "Tidak": "#B8860B"})
        fig2.update_traces(
            textfont_size=13,
            textinfo="percent+label",
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<span class="section-kicker">Korelasi Perilaku</span><p class="section-title">Budgeting versus Kehabisan Uang</p>', unsafe_allow_html=True)
    cross_bk = pd.crosstab(filtered["budgeting"], filtered["kehabisan_uang"])
    cross_bk_pct = (cross_bk.div(cross_bk.sum(axis=1), axis=0) * 100).round(1)

    fig3 = go.Figure()
    colors_map = {"Ya": "#C8102E", "Tidak": "#5B7F5B"}
    for col_name in cross_bk_pct.columns:
        fig3.add_trace(go.Bar(
            name=f"Kehabisan: {col_name}",
            x=cross_bk_pct.index,
            y=cross_bk_pct[col_name],
            marker_color=colors_map.get(col_name, WARNA_UTAMA[0]),
            text=cross_bk_pct[col_name].map(lambda v: f"{v:.1f}%"),
            textposition="inside",
            marker=dict(line=dict(color='#FFFFFF', width=1)),
        ))
    fig3.update_layout(
        barmode="stack",
        xaxis_title="Status Budgeting",
        yaxis_title="Persentase (%)",
    )
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    # 3D CHART: Kehabisan Uang × Uang Saku × Budgeting
    st.markdown('<span class="section-kicker">Visualisasi Tiga Dimensi</span><p class="section-title">Peta Risiko Kehabisan Uang</p>', unsafe_allow_html=True)
    
    x_data, y_data, z_data, colors = [], [], [], []
    for uang_saku_val in ORDER_UANG_SAKU:
        for budgeting_val in ["Ya", "Tidak"]:
            subset = filtered[
                (filtered["uang_saku"] == uang_saku_val) &
                (filtered["budgeting"] == budgeting_val)
            ]
            if len(subset) > 0:
                pct_kehabisan = (subset["kehabisan_uang"] == "Ya").mean() * 100
                x_data.append(uang_saku_val)
                y_data.append(budgeting_val)
                z_data.append(pct_kehabisan)
                colors.append(pct_kehabisan)
    
    fig3d = go.Figure(data=[
        go.Scatter3d(
            x=x_data, y=y_data, z=z_data,
            mode='markers+text',
            marker=dict(
                size=18,
                color=colors,
                colorscale=[
                    [0, "#5B7F5B"],
                    [0.5, "#B8860B"],
                    [1, "#C8102E"]
                ],
                opacity=0.95,
                colorbar=dict(
                    title='Risiko %',
                    tickfont=dict(color="#1A1A1A"),
                    titlefont=dict(color="#0A2540")
                ),
                line=dict(color='#0A2540', width=1.5)
            ),
            text=[f"{z:.0f}%" for z in z_data],
            textposition="top center",
            textfont=dict(color="#0A2540", size=10, family="JetBrains Mono"),
            hovertemplate="<b>%{x}</b><br>Budgeting: %{y}<br>Risiko: %{z:.1f}%<extra></extra>"
        )
    ])
    
    fig3d.update_layout(
        scene=dict(
            xaxis=dict(
                title='Uang Saku',
                backgroundcolor="#FAF8F5",
                gridcolor="#E5E0D8",
                titlefont=dict(family="Playfair Display, serif", color="#0A2540")
            ),
            yaxis=dict(
                title='Budgeting',
                backgroundcolor="#FAF8F5",
                gridcolor="#E5E0D8",
                titlefont=dict(family="Playfair Display, serif", color="#0A2540")
            ),
            zaxis=dict(
                title='Risiko Kehabisan (%)',
                backgroundcolor="#FAF8F5",
                gridcolor="#E5E0D8",
                titlefont=dict(family="Playfair Display, serif", color="#0A2540")
            ),
        ),
        height=600,
        margin=dict(t=40, b=30)
    )
    style_fig_3d(fig3d)
    st.plotly_chart(fig3d, use_container_width=True)

    st.markdown('<span class="section-kicker">Stratifikasi</span><p class="section-title">Kehabisan Uang Berdasarkan Uang Saku</p>', unsafe_allow_html=True)
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
            marker=dict(line=dict(color='#FFFFFF', width=1)),
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
    st.markdown('<span class="section-kicker">Bagian IV</span><p class="section-title">Analisis Statistik Mendalam</p>', unsafe_allow_html=True)
    
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
                [0, "#4A6FA5"],
                [0.5, "#0A2540"],
                [1, "#C8102E"]
            ],
            text="Persentase",
        )
        fig_f.update_traces(
            textposition="outside",
            textfont_color="#1A1A1A",
            marker=dict(line=dict(color='#FFFFFF', width=1))
        )
        fig_f.update_coloraxes(showscale=False)
        style_fig(fig_f)
        st.plotly_chart(fig_f, use_container_width=True)
    with col_t:
        st.markdown(f"""
        <div class="editorial-card">
            <div class="card-kicker">Modus</div>
            <div class="card-stat" style="font-size: 1.2rem;">{modus_val}</div>
            <div class="card-caption">kategori dengan frekuensi tertinggi</div>
        </div>
        <div class="editorial-card">
            <div class="card-kicker">Observasi</div>
            <div class="card-stat">{n}</div>
            <div class="card-caption">jumlah sampel valid</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        st.dataframe(freq_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    st.markdown('<span class="section-kicker">Asosiasi Statistik</span><p class="section-title">Heatmap Koefisien Cramér\'s V</p>', unsafe_allow_html=True)

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
                [0, "#FAF8F5"],
                [0.3, "#4A6FA5"],
                [0.6, "#0A2540"],
                [1, "#C8102E"]
            ],
            zmin=0, zmax=1,
            text=np.round(matrix, 2),
            texttemplate="%{text}",
            textfont={"size": 10, "color": "#1A1A1A", "family": "JetBrains Mono"},
            colorbar=dict(
                title="Cramér's V",
                tickfont=dict(color="#1A1A1A"),
                titlefont=dict(color="#0A2540", family="Playfair Display")
            )
        ))
        fig_heat.update_layout(
            height=550,
            xaxis=dict(tickangle=-30, tickfont=dict(family="Source Sans 3")),
            yaxis=dict(tickfont=dict(family="Source Sans 3")),
            margin=dict(t=40, b=80)
        )
        style_fig(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True)
        st.caption("**Keterangan:** Cramér's V mengukur kekuatan asosiasi antar variabel kategoris. Nilai 0 menunjukkan tidak ada hubungan, nilai 1 menunjukkan hubungan sempurna.")
    else:
        st.warning("Data tidak mencukupi. Hapus filter untuk melihat heatmap.")

    st.markdown("---")

    st.markdown('<span class="section-kicker">Data Primer</span><p class="section-title">Arsip Data Mentah</p>', unsafe_allow_html=True)
    with st.expander("Tampilkan Data Lengkap"):
        st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Unduh CSV",
            data=csv,
            file_name="arsip_data.csv",
            mime="text/csv",
        )

# ═══════════════════════════════════════════════════════════════
# TAB 5 – SIMULASI MONTE CARLO + 3D
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<span class="section-kicker">Bagian V</span><p class="section-title">Proyeksi Risiko: Simulasi Monte Carlo</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding: 20px 28px; background: var(--cream-warm);
                border-left: 3px solid #C8102E; margin-bottom: 28px;
                font-family: 'Source Serif 4', serif; font-style: italic;
                color: #3D3D3D; line-height: 1.7;">
        Sebuah eksperimen komputasional yang menjalankan <b style="color:#0A2540; font-style:normal;">10.000 skenario acak</b> 
        untuk memproyeksikan probabilitas kehabisan uang dan distribusi sisa uang bulanan, 
        berdasarkan distribusi empiris dari data survei yang sedang aktif.
    </div>
    """, unsafe_allow_html=True)

    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        sim_uang_saku = st.selectbox("Skenario Uang Saku", ORDER_UANG_SAKU, index=1)
    with col_sim2:
        sim_budgeting = st.selectbox("Skenario Budgeting", ["Ya", "Tidak"])

    if st.button("Jalankan Simulasi", type="primary"):
        with st.spinner("Memproses 10.000 iterasi..."):
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
                "Risiko Defisit",
                f"{risk_sisa_negatif:.1f}%"
            )

            st.markdown("---")

            st.markdown('<span class="section-kicker">Distribusi Empiris</span><p class="section-title">Histogram Sisa Uang Bulanan</p>', unsafe_allow_html=True)

            df_sim = pd.DataFrame({"Sisa Uang": sisa_uang})
            fig_sim = px.histogram(
                df_sim, x="Sisa Uang", nbins=50,
                color_discrete_sequence=["#0A2540"],
                marginal="box",
                opacity=0.9
            )
            fig_sim.add_vline(
                x=0,
                line_dash="dash",
                line_color="#C8102E",
                line_width=2,
                annotation_text="Titik Impas (Rp 0)",
                annotation_font_color="#C8102E",
                annotation_font_size=12,
                annotation_font_family="Playfair Display"
            )
            fig_sim.add_vrect(
                x0=float("-inf"), x1=0,
                fillcolor="#C8102E", opacity=0.08,
                line_width=0,
                annotation_text="Zona Defisit",
                annotation_position="top left",
                annotation_font_color="#C8102E",
            )

            fig_sim.update_layout(
                xaxis_title="Sisa Uang (Rp)",
                yaxis_title="Frekuensi",
                showlegend=False,
                hovermode="x unified"
            )
            style_fig(fig_sim)
            st.plotly_chart(fig_sim, use_container_width=True)

            # 3D CHART: Monte Carlo Simulation Results
            st.markdown('<span class="section-kicker">Visualisasi Tiga Dimensi</span><p class="section-title">Kurva Distribusi Kumulatif Simulasi</p>', unsafe_allow_html=True)
            
            n_sample = 2000
            sample_idx = np.random.choice(len(sisa_uang), n_sample, replace=False)
            sisa_uang_sample = sisa_uang[sample_idx]
            
            sorted_sisa = np.sort(sisa_uang_sample)
            cumulative_prob = np.arange(1, n_sample + 1) / n_sample
            
            fig3d = go.Figure(data=[
                go.Scatter3d(
                    x=np.arange(n_sample),
                    y=sorted_sisa,
                    z=cumulative_prob,
                    mode='lines+markers',
                    line=dict(color='#0A2540', width=3),
                    marker=dict(
                        size=3,
                        color=cumulative_prob,
                        colorscale=[
                            [0, "#5B7F5B"],
                            [0.5, "#B8860B"],
                            [1, "#C8102E"]
                        ],
                        opacity=0.8
                    ),
                    hovertemplate=(
                        "<b>Iterasi %{x}</b><br>"
                        "Sisa: Rp %{y:,.0f}<br>"
                        "CDF: %{z:.2f}<extra></extra>"
                    )
                )
            ])
            
            fig3d.update_layout(
                scene=dict(
                    xaxis=dict(
                        title='Iterasi Simulasi',
                        backgroundcolor="#FAF8F5",
                        gridcolor="#E5E0D8",
                        titlefont=dict(family="Playfair Display, serif", color="#0A2540")
                    ),
                    yaxis=dict(
                        title='Sisa Uang (Rp)',
                        backgroundcolor="#FAF8F5",
                        gridcolor="#E5E0D8",
                        titlefont=dict(family="Playfair Display, serif", color="#0A2540")
                    ),
                    zaxis=dict(
                        title='Probabilitas Kumulatif',
                        backgroundcolor="#FAF8F5",
                        gridcolor="#E5E0D8",
                        titlefont=dict(family="Playfair Display, serif", color="#0A2540")
                    ),
                ),
                height=600,
                margin=dict(t=40, b=30)
            )
            style_fig_3d(fig3d)
            st.plotly_chart(fig3d, use_container_width=True)

            st.markdown(f"""
            <div class="editorial-card" style="margin-top: 28px; padding: 32px;">
                <div class="card-kicker">Interpretasi Analitis</div>
                <div style="color: #3D3D3D; line-height: 1.9; font-family: 'Source Serif 4', serif; font-size: 1.02rem; margin-top: 12px;">
                    <p style="margin: 0 0 12px 0;">Berdasarkan profil <b style="color:#0A2540;">Uang Saku: {sim_uang_saku}</b> dengan status <b style="color:#C8102E;">Budgeting: {sim_budgeting}</b>, 
                    simulasi menunjukkan rata-rata sisa uang sebesar <b style="color:#5B7F5B;">Rp {mean_sisa:,.0f}</b>.</p>
                    <p style="margin: 0 0 12px 0;">Terdapat risiko <b style="color:#C8102E;">{risk_sisa_negatif:.1f}%</b> di mana pengeluaran melebihi uang saku (defisit).</p>
                    <p style="margin: 0 0 12px 0;">Rentang sisa uang yang paling mungkin terjadi <em>(90% confidence interval)</em> berada antara 
                    <b style="color:#0A2540;">Rp {p5_sisa:,.0f}</b> hingga <b style="color:#0A2540;">Rp {p95_sisa:,.0f}</b>.</p>
                    <p style="margin: 16px 0 0 0; color: #64748B; font-size: 0.9rem; border-top: 1px solid #E5E0D8; padding-top: 12px;">
                        <em>Area histogram di sebelah kiri garis merah (Rp 0) merepresentasikan skenario defisit sebelum akhir bulan.</em>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# COLOPHON (FOOTER)
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="colophon">
    <div style="color: #C8102E; font-size: 0.7rem; letter-spacing: 0.3em; text-transform: uppercase; font-weight: 600; margin-bottom: 12px;">
        — Akhir Laporan —
    </div>
    <div style="font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; color: #0A2540; letter-spacing: -0.01em;">
        The Financial Intelligencer
    </div>
    <div style="font-family: 'Source Serif 4', serif; font-style: italic; color: #3D3D3D; margin-top: 8px; font-size: 0.95rem;">
        Sebuah publikasi analitis dari Program Studi Sains Data
    </div>
    <div style="color: #64748B; font-size: 0.75rem; margin-top: 16px; letter-spacing: 0.15em; text-transform: uppercase;">
        Edisi MMXXVI · Hak Cipta 2026
    </div>
    <div style="margin-top: 24px; display: flex; justify-content: center; gap: 32px; font-size: 0.72rem; color: #64748B; letter-spacing: 0.1em; text-transform: uppercase;">
        <span>Disusun</span>
        <span>·</span>
        <span>Dianalisis</span>
        <span>·</span>
        <span>Dipublikasikan</span>
    </div>
</div>
""", unsafe_allow_html=True)
