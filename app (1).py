import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import chi2_contingency

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Analisis Keuangan Mahasiswa ✨",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS (CYBERPUNK / Y2K AESTHETIC)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Outfit:wght@300;400;600;800&display=swap');

/* ─── ANIMATED AURORA BACKGROUND ─── */
.floating-orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(120px);
    z-index: -1;
    opacity: 0.45;
    pointer-events: none;
}
.orb1 {
    width: 600px; height: 600px;
    background: #ff2a6d;
    top: -150px; left: -150px;
    animation: float1 18s infinite alternate ease-in-out;
}
.orb2 {
    width: 700px; height: 700px;
    background: #05d9e8;
    bottom: -200px; right: -200px;
    animation: float2 22s infinite alternate ease-in-out;
}
.orb3 {
    width: 500px; height: 500px;
    background: #d300c5;
    top: 30%; left: 40%;
    animation: float3 25s infinite alternate ease-in-out;
}

@keyframes float1 {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(250px, 200px) scale(1.2); }
}
@keyframes float2 {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(-300px, -200px) scale(1.3); }
}
@keyframes float3 {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(-200px, 250px) scale(0.9); }
}

.stApp {
    background-color: #050510;
    font-family: 'Outfit', sans-serif !important;
    color: #e2e8f0;
}

.main .block-container {
    z-index: 1;
    position: relative;
}

/* ─── GLASSMORPHISM & NEON GLOW CARDS ─── */
[data-testid="metric-container"],
[data-testid="stExpander"],
.js-plotly-plot .plotly {
    background: rgba(15, 23, 42, 0.4) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

[data-testid="metric-container"]::before {
    content: "";
    position: absolute;
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(45deg, #ff2a6d, #05d9e8, #d300c5, #01ff70);
    background-size: 400%;
    z-index: -1;
    filter: blur(10px);
    animation: glowing 15s linear infinite;
    opacity: 0;
    transition: opacity 0.4s ease-in-out;
    border-radius: 26px;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-8px) scale(1.02);
    border-color: transparent !important;
    box-shadow: 0 15px 40px rgba(5, 217, 232, 0.2);
}

[data-testid="metric-container"]:hover::before {
    opacity: 1;
}

@keyframes glowing {
    0% { background-position: 0 0; }
    50% { background-position: 400% 0; }
    100% { background-position: 0 0; }
}

[data-testid="metric-container"] label {
    color: #05d9e8 !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    text-shadow: 0 0 10px rgba(5, 217, 232, 0.5);
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    font-family: 'Orbitron', sans-serif !important;
    text-shadow: 0 0 15px rgba(255, 255, 255, 0.4);
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #01ff70 !important;
    font-weight: 700 !important;
}

/* ─── ANIMATED CYBER TITLE ─── */
.cyber-title {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900 !important;
    background: linear-gradient(90deg, #ff2a6d, #05d9e8, #d300c5, #ff2a6d);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientText 6s ease infinite;
    text-shadow: 0 0 30px rgba(255, 42, 109, 0.4);
    letter-spacing: 3px;
    margin-bottom: 0;
}

@keyframes gradientText {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ─── BADGES ─── */
.cyber-badge {
    display: inline-block;
    padding: 6px 16px;
    background: rgba(5, 217, 232, 0.1);
    border: 1px solid #05d9e8;
    border-radius: 30px;
    color: #05d9e8;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-right: 12px;
    box-shadow: 0 0 15px rgba(5, 217, 232, 0.3);
    animation: pulseBadge 3s infinite;
}
@keyframes pulseBadge {
    0% { box-shadow: 0 0 5px rgba(5, 217, 232, 0.3); }
    50% { box-shadow: 0 0 25px rgba(5, 217, 232, 0.8); }
    100% { box-shadow: 0 0 5px rgba(5, 217, 232, 0.3); }
}

/* ─── SECTION TITLES ─── */
.section-title {
    color: #ffffff;
    font-size: 1.4rem;
    font-weight: 800;
    border-left: 5px solid #ff2a6d;
    padding-left: 16px;
    margin: 32px 0 20px 0;
    letter-spacing: 1px;
    text-shadow: 0 0 10px rgba(255, 42, 109, 0.5);
    font-family: 'Outfit', sans-serif !important;
}

/* ─── SIDEBAR CONTROL PANEL ─── */
[data-testid="stSidebar"] {
    background: rgba(5, 5, 15, 0.95) !important;
    border-right: 2px solid #05d9e8 !important;
    box-shadow: 5px 0 30px rgba(5, 217, 232, 0.2);
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stSidebar"] h2 {
    font-family: 'Orbitron', sans-serif !important;
    color: #05d9e8 !important;
    text-shadow: 0 0 15px rgba(5, 217, 232, 0.6);
    letter-spacing: 2px;
}

/* ─── NEON BUTTONS ─── */
.stButton > button {
    background: linear-gradient(90deg, #d300c5, #05d9e8) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 14px 36px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 0 0 20px rgba(211, 0, 197, 0.5), inset 0 0 15px rgba(5, 217, 232, 0.3);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    position: relative;
    overflow: hidden;
}
.stButton > button:hover {
    box-shadow: 0 0 40px #05d9e8, 0 0 80px #ff2a6d, inset 0 0 25px rgba(255, 255, 255, 0.4);
    transform: scale(1.05) translateY(-2px);
    color: #fff !important;
}

/* ─── SELECTBOXES & INPUTS ─── */
.stSelectbox > div > div, .stTextInput > div > div {
    background: rgba(20, 20, 40, 0.6) !important;
    border: 1px solid rgba(5, 217, 232, 0.3) !important;
    border-radius: 14px !important;
    color: #05d9e8 !important;
    backdrop-filter: blur(5px);
}
.stSelectbox label, .stTextInput label {
    color: #ff2a6d !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.85rem !important;
}

/* ─── HOLOGRAPHIC TABS ─── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(10, 10, 25, 0.6);
    border-radius: 50px;
    padding: 8px;
    gap: 10px;
    border: 1px solid rgba(5, 217, 232, 0.2);
    box-shadow: inset 0 0 30px rgba(0,0,0,0.6);
    backdrop-filter: blur(10px);
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #a0a0a0 !important;
    border-radius: 50px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    padding: 12px 28px !important;
    transition: all 0.3s ease !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #ff2a6d, #d300c5) !important;
    color: white !important;
    box-shadow: 0 0 30px rgba(255, 42, 109, 0.7);
    animation: pulseTab 2.5s infinite;
}
@keyframes pulseTab {
    0% { box-shadow: 0 0 20px rgba(255, 42, 109, 0.5); }
    50% { box-shadow: 0 0 45px rgba(211, 0, 197, 0.9); }
    100% { box-shadow: 0 0 20px rgba(255, 42, 109, 0.5); }
}

/* ─── DIVIDER ─── */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #05d9e8, #ff2a6d, transparent);
    margin: 40px 0;
    box-shadow: 0 0 10px rgba(5, 217, 232, 0.5);
}

/* ─── DATAFRAME ─── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(211, 0, 197, 0.4) !important;
    border-radius: 20px !important;
    box-shadow: 0 0 25px rgba(211, 0, 197, 0.15);
    overflow: hidden;
}

/* ─── ENTRANCE ANIMATIONS ─── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(40px); }
    to { opacity: 1; transform: translateY(0); }
}
.element-container, .stPlotlyChart, [data-testid="stMetric"], .stButton {
    animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

/* Custom Scrollbar */
::-webkit-scrollbar { width: 12px; height: 12px; }
::-webkit-scrollbar-track { background: #050510; }
::-webkit-scrollbar-thumb { 
    background: linear-gradient(#ff2a6d, #05d9e8); 
    border-radius: 10px; 
    border: 2px solid #050510;
}
::-webkit-scrollbar-thumb:hover { 
    background: linear-gradient(#d300c5, #01ff70); 
}

/* Hide Streamlit Default Header/Footer */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Inject Floating Orbs for Aurora Effect
st.markdown("""
<div class="floating-orb orb1"></div>
<div class="floating-orb orb2"></div>
<div class="floating-orb orb3"></div>
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
# ORDER KATEGORIS & WARNA NEON
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

# Synthwave / Cyberpunk Colors
WARNA_UTAMA = ["#ff2a6d", "#05d9e8", "#d300c5", "#01ff70", "#f9f871", "#ff00ff"]
BG_PLOT = "rgba(15, 23, 42, 0.4)"
PAPER_BG = "rgba(0,0,0,0)"
FONT_COLOR = "#e2e8f0"
GRID_COLOR = "rgba(255, 255, 255, 0.05)"

def style_fig(fig):
    """Terapkan tema Cyberpunk Glassmorphism ke semua chart Plotly."""
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=BG_PLOT,
        font=dict(color=FONT_COLOR, family="Outfit, sans-serif", size=12),
        margin=dict(t=40, b=30, l=20, r=20),
        legend=dict(
            bgcolor="rgba(10, 10, 25, 0.8)",
            bordercolor="#05d9e8",
            borderwidth=1,
            font=dict(color="#e2e8f0")
        ),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor="rgba(255,255,255,0.2)", tickfont=dict(color="#a0a0a0"))
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor="rgba(255,255,255,0.2)", tickfont=dict(color="#a0a0a0"))
    return fig

# ─────────────────────────────────────────────
# SIDEBAR – FILTER
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ CONTROL PANEL")
    st.markdown("---")
    
    gender_options = ["Semua"] + sorted(df["jenis_kelamin"].unique().tolist())
    gender_filter = st.selectbox("👤 Jenis Kelamin", gender_options)

    uang_saku_options = ["Semua"] + ORDER_UANG_SAKU
    uang_saku_filter = st.selectbox("💵 Uang Saku", uang_saku_options)

    kehabisan_options = ["Semua", "Ya", "Tidak"]
    kehabisan_filter = st.selectbox("⚠️ Kehabisan Uang", kehabisan_options)

    budgeting_options = ["Semua", "Ya", "Tidak"]
    budgeting_filter = st.selectbox("📒 Budgeting", budgeting_options)

    st.markdown("---")
    st.markdown(f"**Total Responden:** `{len(df)}`")
    st.markdown("**System Status:** 🟢 ONLINE")

# ─────────────────────────────────────────────
# TERAPKAN FILTER
# ─────────────────────────────────────────────
filtered = df.copy()
if gender_filter != "Semua": filtered = filtered[filtered["jenis_kelamin"] == gender_filter]
if uang_saku_filter != "Semua": filtered = filtered[filtered["uang_saku"] == uang_saku_filter]
if kehabisan_filter != "Semua": filtered = filtered[filtered["kehabisan_uang"] == kehabisan_filter]
if budgeting_filter != "Semua": filtered = filtered[filtered["budgeting"] == budgeting_filter]
n = len(filtered)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="padding: 20px 0 10px 0; text-align: center;">
    <h1 class="cyber-title">💰 Dashboard Analisis Keuangan Mahasiswa </h1>
    <div style="margin-top: 15px;">
        <span class="cyber-badge">✨ GEN Z VIBES</span>
        <span class="cyber-badge">🚀 DATA SCIENCE</span>
        <span class="cyber-badge">🔮 MONTE CARLO</span>
    </div>
    <p style="color: #a0a0a0; margin-top: 20px; font-size: 1.1rem; font-weight: 300; letter-spacing: 1px;">
        Analisis Pola Pengeluaran & Perilaku Keuangan Mahasiswa Sains Data
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
pct_kehabisan = round(filtered[filtered["kehabisan_uang"] == "Ya"].shape[0] / n * 100, 1) if n else 0
pct_budgeting = round(filtered[filtered["budgeting"] == "Ya"].shape[0] / n * 100, 1) if n else 0
pct_belanja_sering = round(filtered[filtered["frekuensi_belanja_online"] == "3 kali atau lebih"].shape[0] / n * 100, 1) if n else 0
modus_pengeluaran = filtered["total_pengeluaran"].mode()[0] if n else "-"

k1.metric("👥 RESPONDEN", f"{n}")
k2.metric("⚠️ KEHABISAN", f"{pct_kehabisan}%")
k3.metric("📒 BUDGETING", f"{pct_budgeting}%")
k4.metric("🛒 IMPULSIVE", f"{pct_belanja_sering}%")
k5.metric("💸 DOMINAN", modus_pengeluaran.replace("Rp ", "Rp\u00A0"))
st.markdown("")

# ─────────────────────────────────────────────
# TAB NAVIGASI
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 DEMOGRAFI", "💳 PENGELUARAN", "🔍 PERILAKU", "📈 ANALISIS", "🎲 SIMULASI"
])

# ══════════════════════════════════════════════
# TAB 1 – DEMOGRAFI & DISTRIBUSI
# ══════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-title">Distribusi Gender</p>', unsafe_allow_html=True)
        gender_cnt = filtered["jenis_kelamin"].value_counts().reset_index()
        gender_cnt.columns = ["Jenis Kelamin", "Jumlah"]
        fig = px.pie(gender_cnt, names="Jenis Kelamin", values="Jumlah", color_discrete_sequence=WARNA_UTAMA, hole=0.55)
        fig.update_traces(textfont_size=14, textinfo="percent+label", textfont_color="white")
        fig.update_layout(showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Distribusi Uang Saku</p>', unsafe_allow_html=True)
        uang_cnt = filtered["uang_saku"].value_counts().reindex(ORDER_UANG_SAKU, fill_value=0).reset_index()
        uang_cnt.columns = ["Uang Saku", "Jumlah"]
        fig2 = px.bar(uang_cnt, x="Uang Saku", y="Jumlah", color="Jumlah", color_continuous_scale=[[0, "#2d0b4e"], [0.5, "#d300c5"], [1, "#05d9e8"]], text="Jumlah")
        fig2.update_traces(textposition="outside", textfont_color=FONT_COLOR)
        fig2.update_coloraxes(showscale=False)
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Uang Saku vs Gender</p>', unsafe_allow_html=True)
    cross = pd.crosstab(filtered["uang_saku"], filtered["jenis_kelamin"]).reindex(ORDER_UANG_SAKU, fill_value=0)
    fig3 = go.Figure()
    for i, col_name in enumerate(cross.columns):
        fig3.add_trace(go.Bar(name=col_name, x=cross.index, y=cross[col_name], marker_color=WARNA_UTAMA[i], text=cross[col_name], textposition="auto"))
    fig3.update_layout(barmode="group", xaxis_title="Uang Saku", yaxis_title="Jumlah")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 2 – POLA PENGELUARAN
# ══════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-title">Total Pengeluaran</p>', unsafe_allow_html=True)
        tot_cnt = filtered["total_pengeluaran"].value_counts().reindex(ORDER_TOTAL_PENGELUARAN, fill_value=0).reset_index()
        tot_cnt.columns = ["Total Pengeluaran", "Jumlah"]
        fig = px.bar(tot_cnt, x="Total Pengeluaran", y="Jumlah", color="Total Pengeluaran", color_discrete_sequence=WARNA_UTAMA, text="Jumlah")
        fig.update_traces(textposition="outside", textfont_color=FONT_COLOR, showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Faktor Membengkak</p>', unsafe_allow_html=True)
        faktor_cnt = filtered["faktor_membengkak"].value_counts().reset_index()
        faktor_cnt.columns = ["Faktor", "Jumlah"]
        faktor_cnt["Faktor_short"] = faktor_cnt["Faktor"].str.extract(r'^([^(]+)').iloc[:, 0].str.strip()
        fig2 = px.bar(faktor_cnt, y="Faktor_short", x="Jumlah", orientation="h", color="Jumlah", color_continuous_scale=[[0, "#2d0b4e"], [0.5, "#ff2a6d"], [1, "#f9f871"]], text="Jumlah")
        fig2.update_traces(textposition="outside", textfont_color=FONT_COLOR)
        fig2.update_coloraxes(showscale=False)
        fig2.update_layout(yaxis_title=" ")
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Breakdown Kategori</p>', unsafe_allow_html=True)
    col_makan = filtered["pengeluaran_makan"].value_counts()
    col_transport = filtered["pengeluaran_transport"].value_counts()
    col_hiburan = filtered["pengeluaran_hiburan"].value_counts()
    col_kuliah = filtered["pengeluaran_kuliah"].value_counts()

    breakdown_df = pd.DataFrame({
        "Makan": col_makan, "Transport": col_transport, "Hiburan": col_hiburan, "Kuliah": col_kuliah,
    }).fillna(0).reset_index().rename(columns={"index": "Kategori"})
    breakdown_melt = breakdown_df.melt(id_vars="Kategori", var_name="Jenis", value_name="Jumlah")

    fig3 = px.bar(breakdown_melt, x="Kategori", y="Jumlah", color="Jenis", barmode="group", color_discrete_sequence=WARNA_UTAMA, text="Jumlah")
    fig3.update_traces(textposition="outside", textfont_color=FONT_COLOR)
    fig3.update_layout(xaxis_title="Range Pengeluaran", yaxis_title="Jumlah Mahasiswa")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 – PERILAKU KEUANGAN
# ══════════════════════════════════════════════
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-title">Pernah Kehabisan Uang?</p>', unsafe_allow_html=True)
        kh_cnt = filtered["kehabisan_uang"].value_counts().reset_index()
        kh_cnt.columns = ["Status", "Jumlah"]
        fig = px.pie(kh_cnt, names="Status", values="Jumlah", hole=0.6, color="Status", color_discrete_map={"Ya": "#ff2a6d", "Tidak": "#01ff70"})
        fig.update_traces(textfont_size=14, textinfo="percent+label", textfont_color="white")
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Melakukan Budgeting?</p>', unsafe_allow_html=True)
        bd_cnt = filtered["budgeting"].value_counts().reset_index()
        bd_cnt.columns = ["Status", "Jumlah"]
        fig2 = px.pie(bd_cnt, names="Status", values="Jumlah", hole=0.6, color="Status", color_discrete_map={"Ya": "#05d9e8", "Tidak": "#d300c5"})
        fig2.update_traces(textfont_size=14, textinfo="percent+label", textfont_color="white")
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Budgeting vs Kehabisan Uang</p>', unsafe_allow_html=True)
    cross_bk = pd.crosstab(filtered["budgeting"], filtered["kehabisan_uang"])
    cross_bk_pct = (cross_bk.div(cross_bk.sum(axis=1), axis=0) * 100).round(1)

    fig3 = go.Figure()
    colors_map = {"Ya": "#ff2a6d", "Tidak": "#01ff70"}
    for col_name in cross_bk_pct.columns:
        fig3.add_trace(go.Bar(name=f"Kehabisan: {col_name}", x=cross_bk_pct.index, y=cross_bk_pct[col_name], marker_color=colors_map.get(col_name, WARNA_UTAMA[0]), text=cross_bk_pct[col_name].map(lambda v: f"{v:.1f}%"), textposition="inside"))
    fig3.update_layout(barmode="stack", xaxis_title="Melakukan Budgeting", yaxis_title="Persentase (%)")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 4 – ANALISIS LANJUTAN
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
            colorscale=[[0, "#050510"], [0.3, "#2d0b4e"], [0.6, "#d300c5"], [1, "#05d9e8"]],
            zmin=0, zmax=1,
            text=np.round(matrix, 2), texttemplate="%{text}", textfont={"size": 10, "color": "white"},
        ))
        fig_heat.update_layout(height=550, xaxis=dict(tickangle=-45))
        style_fig(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.markdown("""
        <div style="background: rgba(255, 42, 109, 0.1); border: 1px solid #ff2a6d; border-radius: 16px; padding: 16px; box-shadow: 0 0 20px rgba(255, 42, 109, 0.3);">
            <strong style="color: #ff2a6d; font-family: 'Orbitron', sans-serif;">⚠️ WARNING:</strong> 
            <span style="color: #e2e8f0;">Data terlalu sedikit. Hapus filter untuk melihat heatmap.</span>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 5 – SIMULASI MONTE CARLO
# ══════════════════════════════════════════════
with tab5:
    st.markdown('<p class="section-title">🎲 Simulasi Monte Carlo: Risiko Keuangan</p>', unsafe_allow_html=True)
    st.markdown("Proyeksikan probabilitas kehabisan uang berdasarkan 10.000 iterasi acak (Bootstrap).")
    
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        sim_uang_saku = st.selectbox("💵 Skenario Uang Saku: ", ORDER_UANG_SAKU, index=1)
    with col_sim2:
        sim_budgeting = st.selectbox("📒 Skenario Budgeting: ", ["Ya", "Tidak"])
        
    if st.button("🚀 INITIATE SIMULATION", type="primary"):
        with st.spinner("⚡ Computing 10,000 iterations..."):
            n_sim = 10000
            
            ref_data = filtered[(filtered["uang_saku"] == sim_uang_saku) & (filtered["budgeting"] == sim_budgeting)]
            if len(ref_data) < 5: ref_data = filtered[filtered["uang_saku"] == sim_uang_saku]
            if len(ref_data) < 5: ref_data = filtered 
                
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
            kpi1.metric("📉 PROB. KEHABISAN", f"{prob_khabis:.1f}%", delta=f"{delta_khabis:+.1f}%", delta_color="inverse" if prob_khabis > overall_khabis else "normal")
            kpi2.metric("💰 RATA-RATA SISA", f"Rp {mean_sisa:,.0f}")
            kpi3.metric("⚠️ RISIKO DEFISIT", f"{risk_sisa_negatif:.1f}%")
            
            st.markdown("---")
            
            st.markdown('<p class="section-title">📊 Distribusi Sisa Uang (10k Simulasi)</p>', unsafe_allow_html=True)
            
            df_sim = pd.DataFrame({"Sisa Uang": sisa_uang})
            fig_sim = px.histogram(df_sim, x="Sisa Uang", nbins=50, color_discrete_sequence=["#05d9e8"], marginal="box", opacity=0.8)
            fig_sim.add_vline(x=0, line_dash="dash", line_color="#ff2a6d", annotation_text="TITIK IMPAS", annotation_font_color="#ff2a6d")
            
            fig_sim.update_layout(xaxis_title="Sisa Uang (Rp)", yaxis_title="Frekuensi", showlegend=False, hovermode="x unified")
            style_fig(fig_sim)
            st.plotly_chart(fig_sim, use_container_width=True)
            
            st.markdown(f"""
            <div style="background: rgba(211, 0, 197, 0.05); border: 1px solid rgba(211, 0, 197, 0.5); border-radius: 20px; padding: 24px; margin-top: 20px; box-shadow: 0 0 30px rgba(211, 0, 197, 0.2); backdrop-filter: blur(10px);">
                <h3 style="color: #d300c5; font-family: 'Orbitron', sans-serif; margin-top:0; letter-spacing: 2px; text-shadow: 0 0 10px rgba(211, 0, 197, 0.6);">💡 SYSTEM INSIGHTS</h3>
                <ul style="color: #e2e8f0; line-height: 2; font-size: 1.05rem; margin-bottom: 0;">
                    <li>Profil: <strong style="color:#ff2a6d;">{sim_uang_saku}</strong> & <strong style="color:#05d9e8;">Budgeting: {sim_budgeting}</strong>.</li>
                    <li>Rata-rata sisa uang: <strong style="color:#01ff70;">Rp {mean_sisa:,.0f}</strong>.</li>
                    <li>Risiko defisit (Sisa < 0): <strong style="color:#ff2a6d;">{risk_sisa_negatif:.1f}%</strong>.</li>
                    <li>Confidence Interval (90%): <strong>Rp {p5_sisa:,.0f}</strong> hingga <strong>Rp {p95_sisa:,.0f}</strong>.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#a0a0a0; font-size:0.8rem; margin-top: 32px; font-family: Orbitron, sans-serif; letter-spacing: 3px;'>"
    "SYSTEM ONLINE · CYBER FINANCE DASHBOARD · 2026 ✨"
    "</p>",
    unsafe_allow_html=True,
)
