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
    page_title="Luxe Financial Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
# LUXURY THEME · EMERALD & IVORY
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;0,9..144,800;0,9..144,900&family=Inter:wght@300;400;500;600;700&display=swap');

/* ─── ROOT VARIABLES ─── */
:root {
    --emerald-deep: #0F766E;
    --emerald: #10B981;
    --emerald-soft: #6EE7B7;
    --gold: #D4AF37;
    --gold-soft: #E8D5A0;
    --ivory: #FAFAF7;
    --ivory-warm: #F5F3EC;
    --surface: #FFFFFF;
    --ink: #1C1917;
    --ink-soft: #44403C;
    --muted: #78716C;
    --line: rgba(15, 118, 110, 0.08);
    --line-strong: rgba(15, 118, 110, 0.2);
}

/* ─── GLOBAL BACKGROUND ─── */
.stApp {
    background: 
        radial-gradient(ellipse at top left, rgba(110, 231, 183, 0.08) 0%, transparent 50%),
        radial-gradient(ellipse at bottom right, rgba(212, 175, 55, 0.04) 0%, transparent 50%),
        linear-gradient(180deg, #FAFAF7 0%, #F5F3EC 100%);
    background-attachment: fixed;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--ink);
}

.main .block-container {
    padding-top: 3rem;
    padding-bottom: 4rem;
    max-width: 1400px;
}

/* ─── LUXURY SIDEBAR ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F5F3EC 100%) !important;
    border-right: 1px solid var(--line) !important;
}

[data-testid="stSidebar"] > div {
    padding: 2.5rem 1.75rem !important;
}

[data-testid="stSidebar"] h2 {
    font-family: 'Fraunces', serif !important;
    font-weight: 600 !important;
    font-size: 1.5rem !important;
    color: var(--emerald-deep) !important;
    letter-spacing: -0.02em;
    margin-bottom: 1.5rem !important;
    font-variation-settings: "opsz" 144;
}

[data-testid="stSidebar"] * {
    color: var(--ink-soft);
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] label {
    color: var(--muted) !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    margin-bottom: 6px !important;
}

/* ─── METRIC CARDS · LUXURY ─── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--line) !important;
    border-radius: 16px !important;
    padding: 22px 26px !important;
    box-shadow:
        0 1px 2px rgba(28, 25, 23, 0.04),
        0 4px 16px rgba(15, 118, 110, 0.04) !important;
    transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
    position: relative;
    overflow: hidden;
}

[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--emerald-deep), var(--emerald), var(--gold));
    opacity: 0.8;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow:
        0 4px 8px rgba(28, 25, 23, 0.06),
        0 20px 40px rgba(15, 118, 110, 0.08) !important;
    border-color: var(--line-strong) !important;
}

[data-testid="stMetric"] label {
    color: var(--muted) !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--ink) !important;
    font-size: 1.85rem !important;
    font-weight: 600 !important;
    font-family: 'Fraunces', serif !important;
    letter-spacing: -0.02em;
    font-variation-settings: "opsz" 144;
}

[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: var(--emerald-deep) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    font-family: 'Inter', sans-serif !important;
}

/* ─── SECTION TITLES · ELEGANT ─── */
.section-title {
    color: var(--ink) !important;
    font-size: 1.3rem !important;
    font-weight: 500 !important;
    font-family: 'Fraunces', serif !important;
    letter-spacing: -0.01em;
    padding-left: 20px !important;
    margin: 40px 0 20px 0 !important;
    position: relative;
    display: inline-block;
    font-variation-settings: "opsz" 144;
}

.section-title::before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 3px;
    height: 70%;
    background: linear-gradient(180deg, var(--emerald-deep), var(--gold));
    border-radius: 4px;
}

/* ─── TABS · MINIMAL LUXURY ─── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface);
    border-radius: 14px;
    padding: 6px;
    gap: 4px;
    border: 1px solid var(--line);
    box-shadow: 0 1px 2px rgba(28, 25, 23, 0.03);
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: var(--muted) !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 11px 22px !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.01em;
}

.stTabs [aria-selected="true"] {
    background: var(--emerald-deep) !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25);
}

.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
    background: rgba(15, 118, 110, 0.06) !important;
    color: var(--emerald-deep) !important;
}

/* ─── BUTTONS · REFINED ─── */
.stButton > button {
    background: var(--emerald-deep) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 13px 34px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em;
    box-shadow: 
        0 1px 2px rgba(28, 25, 23, 0.1),
        0 4px 12px rgba(15, 118, 110, 0.2);
    transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1) !important;
}

.stButton > button:hover {
    transform: translateY(-1px);
    background: #0D6560 !important;
    box-shadow: 
        0 2px 4px rgba(28, 25, 23, 0.12),
        0 12px 28px rgba(15, 118, 110, 0.3);
}

/* ─── SELECTBOX · REFINED ─── */
.stSelectbox > div > div,
.stTextInput > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
    color: var(--ink) !important;
    padding: 6px 14px !important;
    transition: all 0.3s ease !important;
}

.stSelectbox > div > div:hover,
.stTextInput > div > div:hover {
    border-color: var(--line-strong) !important;
    box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.06) !important;
}

.stSelectbox label,
.stTextInput label {
    color: var(--muted) !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

/* ─── DIVIDER · ELEGANT ─── */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        var(--line-strong),
        var(--gold-soft),
        var(--line-strong),
        transparent);
    margin: 48px 0;
}

/* ─── PLOTLY CHARTS · MINIMAL ─── */
.js-plotly-plot .plotly {
    border-radius: 16px !important;
    background: var(--surface) !important;
    border: 1px solid var(--line);
    padding: 16px;
    box-shadow: 
        0 1px 2px rgba(28, 25, 23, 0.03),
        0 4px 16px rgba(15, 118, 110, 0.04);
}

/* ─── DATAFRAME · REFINED ─── */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    border: 1px solid var(--line) !important;
    overflow: hidden;
    background: var(--surface) !important;
}

[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--line) !important;
    border-radius: 16px !important;
}

/* ─── ALERT / INFO · LUXURY ─── */
[data-testid="stAlert"] {
    background: rgba(15, 118, 110, 0.04) !important;
    border: 1px solid rgba(15, 118, 110, 0.15) !important;
    border-radius: 14px !important;
    color: var(--ink-soft) !important;
}

[data-testid="stWarning"] {
    background: rgba(212, 175, 55, 0.06) !important;
    border: 1px solid rgba(212, 175, 55, 0.2) !important;
    border-radius: 14px !important;
}

/* ─── SCROLLBAR · SUBTLE ─── */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--ivory-warm); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--emerald-soft), var(--emerald-deep));
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--emerald-deep);
}

/* ─── ANIMATIONS ─── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

.element-container, .stPlotlyChart, [data-testid="stMetric"] {
    animation: fadeInUp 0.5s ease-out forwards;
}

/* ─── HERO SECTION · APPLE/STRIPE STYLE ─── */
.hero-kicker {
    color: var(--emerald-deep);
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 16px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.hero-kicker::before {
    content: "";
    width: 24px;
    height: 1px;
    background: var(--gold);
    display: inline-block;
}

.hero-title {
    font-family: 'Fraunces', serif !important;
    font-weight: 400 !important;
    font-size: 3.8rem !important;
    letter-spacing: -0.035em;
    line-height: 1.05;
    margin: 0 0 20px 0;
    color: var(--ink);
    font-variation-settings: "opsz" 144;
}

.hero-title em {
    font-style: italic;
    background: linear-gradient(135deg, var(--emerald-deep) 0%, var(--gold) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 500;
}

.hero-subtitle {
    color: var(--ink-soft);
    font-size: 1.1rem;
    font-weight: 400;
    line-height: 1.6;
    max-width: 640px;
    letter-spacing: 0.005em;
}

/* ─── BADGE · LUXURY ─── */
.badge-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 100px;
    font-size: 0.72rem;
    color: var(--emerald-deep);
    font-weight: 600;
    margin-right: 8px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    box-shadow: 0 1px 2px rgba(28, 25, 23, 0.03);
}

/* ─── LUXURY CARD COMPONENT ─── */
.luxury-card {
    padding: 22px;
    background: var(--surface);
    border-radius: 14px;
    border: 1px solid var(--line);
    margin-bottom: 14px;
    transition: all 0.3s ease;
    box-shadow: 0 1px 2px rgba(28, 25, 23, 0.03);
}

.luxury-card:hover {
    border-color: var(--line-strong);
    transform: translateY(-2px);
    box-shadow: 
        0 4px 8px rgba(28, 25, 23, 0.04),
        0 12px 24px rgba(15, 118, 110, 0.06);
}

.card-label {
    color: var(--muted);
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-weight: 600;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.card-label::before {
    content: "";
    width: 16px;
    height: 1px;
    background: var(--gold);
}

.card-value {
    color: var(--ink);
    font-size: 1.6rem;
    font-weight: 500;
    font-family: 'Fraunces', serif;
    letter-spacing: -0.02em;
    font-variation-settings: "opsz" 144;
}

/* ─── HIDE STREAMLIT BRANDING ─── */
#MainMenu, header, footer { visibility: hidden; }

/* ─── SPINNER CUSTOM ─── */
.stSpinner > div {
    border-top-color: var(--emerald-deep) !important;
}

/* ─── RESPONSIVE ─── */
@media (max-width: 768px) {
    .hero-title { font-size: 2.4rem !important; }
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
# KATEGORI & PALET WARNA LUXURY
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

# Palette: Emerald + Gold luxury
WARNA_UTAMA = ["#0F766E", "#D4AF37", "#10B981", "#6EE7B7", "#B45309", "#134E4A"]
BG_PLOT = "#FFFFFF"
PAPER_BG = "#FFFFFF"
FONT_COLOR = "#44403C"
GRID_COLOR = "rgba(15, 118, 110, 0.08)"

def style_fig(fig):
    """Terapkan tema luxury ke semua chart Plotly."""
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=BG_PLOT,
        font=dict(color=FONT_COLOR, family="Inter, sans-serif", size=12),
        margin=dict(t=50, b=35, l=20, r=20),
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="rgba(15, 118, 110, 0.1)",
            borderwidth=1,
            font=dict(color="#44403C", family="Inter"),
        ),
        title_font=dict(family="Fraunces, serif", size=16, color="#1C1917"),
    )
    fig.update_xaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor="rgba(15, 118, 110, 0.15)",
        tickfont=dict(color="#78716C", family="Inter", size=11),
    )
    fig.update_yaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor="rgba(15, 118, 110, 0.15)",
        tickfont=dict(color="#78716C", family="Inter", size=11),
    )
    return fig

# ═══════════════════════════════════════════════════════════════
# SIDEBAR · FILTER
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
        <div class="card-label">Total Responden</div>
        <div class="card-value">{len(df)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="luxury-card">
        <div class="card-label">Data Aktif</div>
        <div class="card-value" id="sidebar-filtered">–</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align: left; padding: 12px 0;">
        <div style="color: #78716C; font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 8px;">
            Sumber Data
        </div>
        <div style="color: #1C1917; font-size: 0.88rem; line-height: 1.6;">
            Survei Analisis Statistika<br>
            <span style="color: #D4AF37; font-weight: 600;">Sains Data · 2026</span>
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
# HERO HEADER · APPLE/STRIPE STYLE
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div style="padding: 40px 0 32px 0;">
    <div class="hero-kicker">Financial Intelligence Report</div>
    <h1 class="hero-title">
        Dashboard Analisis<br>
        Keuangan <em>Mahasiswa</em>
    </h1>
    <p class="hero-subtitle">
        Studi mendalam mengenai pola pengeluaran, perilaku finansial, dan manajemen anggaran mahasiswa Sains Data. 
        Sebuah pendekatan analitis terhadap literasi keuangan generasi muda.
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
    "Demografi",
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
            color_discrete_sequence=WARNA_UTAMA, hole=0.6,
        )
        fig.update_traces(
            textfont_size=13,
            textinfo="percent+label",
            marker=dict(line=dict(color='#FFFFFF', width=3))
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
                [0, "#6EE7B7"],
                [0.5, "#10B981"],
                [1, "#0F766E"]
            ],
            text="Jumlah",
        )
        fig2.update_traces(
            textposition="outside",
            textfont_color="#1C1917",
            marker=dict(line=dict(color='#FFFFFF', width=1))
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
            marker=dict(line=dict(color='#FFFFFF', width=1)),
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
            textfont_color="#1C1917",
            showlegend=False,
            marker=dict(line=dict(color='#FFFFFF', width=1))
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
                [0, "#D4AF37"],
                [0.5, "#0F766E"],
                [1, "#134E4A"]
            ],
            text="Jumlah",
        )
        fig2.update_traces(
            textposition="outside",
            textfont_color="#1C1917",
            marker=dict(line=dict(color='#FFFFFF', width=1))
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
        textfont_color="#1C1917",
        marker=dict(line=dict(color='#FFFFFF', width=1))
    )
    fig3.update_layout(xaxis_title="Rentang Pengeluaran", yaxis_title="Jumlah Mahasiswa")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<p class="section-title">Frekuensi Belanja Online</p>', unsafe_allow_html=True)
    belanja_cnt = filtered["frekuensi_belanja_online"].value_counts().reset_index()
    belanja_cnt.columns = ["Frekuensi", "Jumlah"]
    fig4 = px.pie(
        belanja_cnt, names="Frekuensi", values="Jumlah",
        color_discrete_sequence=WARNA_UTAMA, hole=0.6,
    )
    fig4.update_traces(
        textfont_size=13,
        textinfo="percent+label",
        marker=dict(line=dict(color='#FFFFFF', width=3))
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
        fig = px.pie(kh_cnt, names="Status", values="Jumlah", hole=0.6,
                     color="Status",
                     color_discrete_map={"Ya": "#0F766E", "Tidak": "#D4AF37"})
        fig.update_traces(
            textfont_size=13,
            textinfo="percent+label",
            marker=dict(line=dict(color='#FFFFFF', width=3))
        )
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Status Penerapan Budgeting</p>', unsafe_allow_html=True)
        bd_cnt = filtered["budgeting"].value_counts().reset_index()
        bd_cnt.columns = ["Status", "Jumlah"]
        fig2 = px.pie(bd_cnt, names="Status", values="Jumlah", hole=0.6,
                      color="Status",
                      color_discrete_map={"Ya": "#10B981", "Tidak": "#B45309"})
        fig2.update_traces(
            textfont_size=13,
            textinfo="percent+label",
            marker=dict(line=dict(color='#FFFFFF', width=3))
        )
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Hubungan Budgeting vs Kehabisan Uang</p>', unsafe_allow_html=True)
    cross_bk = pd.crosstab(filtered["budgeting"], filtered["kehabisan_uang"])
    cross_bk_pct = (cross_bk.div(cross_bk.sum(axis=1), axis=0) * 100).round(1)

    fig3 = go.Figure()
    colors_map = {"Ya": "#0F766E", "Tidak": "#D4AF37"}
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
                [0, "#6EE7B7"],
                [0.5, "#0F766E"],
                [1, "#134E4A"]
            ],
            text="Persentase",
        )
        fig_f.update_traces(
            textposition="outside",
            textfont_color="#1C1917",
            marker=dict(line=dict(color='#FFFFFF', width=1))
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
                [0, "#F5F3EC"],
                [0.25, "#6EE7B7"],
                [0.5, "#10B981"],
                [0.75, "#0F766E"],
                [1, "#134E4A"]
            ],
            zmin=0, zmax=1,
            text=np.round(matrix, 2),
            texttemplate="%{text}",
            textfont={"size": 10, "color": "#1C1917"},
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
    st.markdown('<p class="section-title">Simulasi Monte Carlo · Proyeksi Risiko Keuangan</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding: 20px 24px; background: linear-gradient(135deg, rgba(15,118,110,0.04) 0%, rgba(212,175,55,0.03) 100%);
                border-left: 3px solid #0F766E; border-radius: 14px;
                color: #44403C; font-size: 0.95rem; margin-bottom: 24px;
                border: 1px solid rgba(15,118,110,0.08);">
        Simulasi Monte Carlo menjalankan <b style="color:#0F766E;">10.000 skenario acak</b> untuk memproyeksikan probabilitas kehabisan uang 
        dan distribusi sisa uang bulanan, berdasarkan distribusi empiris dari data survei yang sedang aktif.
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
                color_discrete_sequence=["#0F766E"],
                marginal="box",
                opacity=0.9
            )
            fig_sim.add_vline(
                x=0,
                line_dash="dash",
                line_color="#D4AF37",
                line_width=3,
                annotation_text="Titik Impas (Rp 0)",
                annotation_font_color="#D4AF37",
                annotation_font_size=12,
            )
            fig_sim.add_vrect(
                x0=float("-inf"), x1=0,
                fillcolor="#B45309", opacity=0.08,
                line_width=0,
                annotation_text="Zona Defisit",
                annotation_position="top left",
                annotation_font_color="#B45309",
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
            <div style="padding: 28px; background: var(--surface);
                        border: 1px solid rgba(15,118,110,0.1); border-radius: 16px;
                        margin-top: 24px; box-shadow: 0 4px 16px rgba(15,118,110,0.06);">
                <div style="color: #0F766E; font-size: 0.72rem;
                            text-transform: uppercase; letter-spacing: 0.18em;
                            font-weight: 600; margin-bottom: 14px;
                            display: flex; align-items: center; gap: 10px;">
                    <span style="width: 20px; height: 1px; background: #D4AF37;"></span>
                    Interpretasi Simulasi
                </div>
                <div style="color: #44403C; line-height: 1.9; font-size: 0.95rem;">
                    <div>Berdasarkan profil <b style="color:#D4AF37; font-weight:600;">Uang Saku: {sim_uang_saku}</b> dan <b style="color:#0F766E; font-weight:600;">Budgeting: {sim_budgeting}</b>, simulasi menunjukkan rata-rata sisa uang sebesar <b style="color:#0F766E;">Rp {mean_sisa:,.0f}</b>.</div>
                    <div style="margin-top:8px;">Terdapat risiko <b style="color:#B45309;">{risk_sisa_negatif:.1f}%</b> di mana pengeluaran melebihi uang saku (defisit).</div>
                    <div style="margin-top:8px;">Rentang sisa uang yang paling mungkin terjadi (90% confidence interval) adalah antara <b style="color:#0F766E;">Rp {p5_sisa:,.0f}</b> hingga <b style="color:#0F766E;">Rp {p95_sisa:,.0f}</b>.</div>
                    <div style="margin-top: 16px; color: #78716C; font-size: 0.85rem; font-style: italic; padding-top: 12px; border-top: 1px solid rgba(15,118,110,0.08);">
                        Area histogram di sebelah kiri garis emas (Rp 0) merepresentasikan skenario kehabisan uang sebelum akhir bulan.
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
    <div style="text-align:center; padding: 40px 0 20px 0;">
        <div style="display: flex; justify-content: center; align-items: center; gap: 12px; margin-bottom: 16px;">
            <span style="width: 40px; height: 1px; background: #D4AF37;"></span>
            <span style="color: #0F766E; font-size: 0.7rem; letter-spacing: 0.25em; text-transform: uppercase; font-weight: 600;">
                Financial Intelligence
            </span>
            <span style="width: 40px; height: 1px; background: #D4AF37;"></span>
        </div>
        <div style="font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 500; color: #1C1917; letter-spacing: -0.02em; font-variation-settings: 'opsz' 144;">
            Dashboard Analisis Keuangan Mahasiswa
        </div>
        <div style="color: #78716C; font-size: 0.82rem; margin-top: 10px; font-weight: 400;">
            Sains Data · 2026
        </div>
        <div style="color: #B8B4AC; font-size: 0.72rem; margin-top: 16px; letter-spacing: 0.1em;">
            DIBUAT DENGAN KETELITIAN ANALITIS
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
