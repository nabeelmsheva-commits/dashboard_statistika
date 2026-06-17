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
    page_title="Cyber Dashboard Keuangan 💾",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS (CYBER THEME + ALWAYS OPEN SIDEBAR)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

/* ─── GLOBAL CYBER THEME ─── */
.stApp {
    background: linear-gradient(135deg, #0a0e27 0%, #1a0a2e 50%, #0a0e27 100%);
    background-attachment: fixed;
    font-family: 'Rajdhani', sans-serif !important;
    color: #00ffff;
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    z-index: 1;
    position: relative;
}

/* ─── SIDEBAR (ALWAYS OPEN - NO COLLAPSE) ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f1e 0%, #1a0a2e 100%) !important;
    border-right: 3px solid #00ffff !important;
    box-shadow: 5px 0 30px rgba(0, 255, 255, 0.3);
    z-index: 1000 !important;
    position: relative !important;
}
[data-testid="stSidebar"] > div {
    z-index: 1001 !important;
    position: relative !important;
}
[data-testid="stSidebar"] * {
    color: #00ffff !important;
    font-family: 'Rajdhani', sans-serif !important;
}
[data-testid="stSidebar"] h2 {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900 !important;
    color: #00ffff !important;
    text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* HIDE SIDEBAR COLLAPSE BUTTON */
button[data-testid="baseButton-header"], 
[data-testid="collapsedControl"],
section[data-testid="stSidebar"] > div > div > button {
    display: none !important;
}

/* ─── CYBER METRIC CARDS ─── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0f0f1e 0%, #1a0a2e 100%) !important;
    border: 2px solid #00ffff !important;
    border-radius: 16px !important;
    padding: 20px !important;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.3), inset 0 0 20px rgba(0, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
[data-testid="metric-container"]::before {
    content: "";
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, #00ffff, transparent);
    animation: cyberScan 3s linear infinite;
}
@keyframes cyberScan {
    0% { left: -100%; }
    100% { left: 100%; }
}
[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 30px rgba(0, 255, 255, 0.5), inset 0 0 30px rgba(0, 255, 255, 0.2);
    border-color: #ff00ff !important;
}
[data-testid="metric-container"] label {
    color: #ff00ff !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-family: 'Orbitron', sans-serif !important;
    text-shadow: 0 0 5px #ff00ff;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 2.2rem !important;
    font-weight: 900 !important;
    font-family: 'Orbitron', sans-serif !important;
    text-shadow: 0 0 15px #00ffff, 0 0 25px #00ffff;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #00ff00 !important;
    font-weight: 700 !important;
    text-shadow: 0 0 5px #00ff00;
}

/* ─── CYBER HEADER & TITLES ─── */
.cyber-title {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900 !important;
    background: linear-gradient(90deg, #00ffff, #ff00ff, #00ffff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientFlow 4s linear infinite;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
}
@keyframes gradientFlow {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}
.cyber-subtitle {
    color: #00ffff;
    font-size: 1.1rem;
    font-weight: 500;
    margin-top: 10px;
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}
.section-title {
    color: #00ffff;
    font-size: 1.3rem;
    font-weight: 700;
    border-left: 5px solid #ff00ff;
    padding-left: 16px;
    margin: 32px 0 18px 0;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-family: 'Orbitron', sans-serif !important;
    text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
}

/* ─── CYBER BUTTONS ─── */
.stButton > button {
    background: linear-gradient(135deg, #ff00ff, #00ffff) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0.8rem 2rem !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    box-shadow: 0 0 20px rgba(255, 0, 255, 0.5);
    transition: all 0.3s ease !important;
    clip-path: polygon(10px 0, 100% 0, calc(100% - 10px) 100%, 0 100%);
}
.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 40px rgba(0, 255, 255, 0.8);
}

/* ─── CYBER SELECTBOXES ─── */
.stSelectbox > div > div, .stTextInput > div > div {
    background: rgba(15, 15, 30, 0.8) !important;
    border: 2px solid #00ffff !important;
    border-radius: 0 !important;
    color: #00ffff !important;
    transition: all 0.3s ease !important;
    clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 10px, 100% 100%, 10px 100%, 0 calc(100% - 10px));
}
.stSelectbox > div > div:hover, .stTextInput > div > div:hover {
    border-color: #ff00ff !important;
    box-shadow: 0 0 20px rgba(255, 0, 255, 0.5) !important;
}
.stSelectbox label, .stTextInput label {
    color: #ff00ff !important;
    font-weight: 700 !important;
    font-family: 'Orbitron', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 0.85rem !important;
    text-shadow: 0 0 5px #ff00ff;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    z-index: 1002 !important;
    position: relative !important;
}

/* ─── CYBER TABS ─── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15, 15, 30, 0.8);
    border-radius: 0;
    padding: 6px;
    gap: 6px;
    border: 2px solid #00ffff;
    clip-path: polygon(15px 0, 100% 0, calc(100% - 15px) 100%, 0 100%);
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #00ffff !important;
    border-radius: 0 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    clip-path: polygon(8px 0, 100% 0, calc(100% - 8px) 100%, 0 100%);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #ff00ff, #00ffff) !important;
    color: #000 !important;
    box-shadow: 0 0 20px rgba(255, 0, 255, 0.6);
}
.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
    background: rgba(0, 255, 255, 0.2) !important;
    color: #ffffff !important;
}

/* ─── CYBER DIVIDER ─── */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00ffff, #ff00ff, transparent);
    margin: 32px 0;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

/* ─── CYBER CHARTS & CONTAINERS ─── */
.js-plotly-plot .plotly {
    border-radius: 0 !important;
    background: rgba(15, 15, 30, 0.6) !important;
    border: 2px solid #00ffff;
    padding: 10px;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
}
[data-testid="stDataFrame"] {
    border-radius: 0 !important;
    border: 2px solid #00ffff !important;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}
[data-testid="stExpander"] {
    background: rgba(15, 15, 30, 0.8) !important;
    border: 2px solid #ff00ff !important;
    border-radius: 0 !important;
    clip-path: polygon(10px 0, 100% 0, calc(100% - 10px) 100%, 0 100%);
}
[data-testid="stAlert"] {
    background: rgba(0, 255, 255, 0.1) !important;
    border: 2px solid #00ffff !important;
    border-radius: 0 !important;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

/* ─── CYBER SCROLLBAR ─── */
::-webkit-scrollbar { width: 12px; height: 12px; }
::-webkit-scrollbar-track { background: #0a0e27; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00ffff, #ff00ff);
    border-radius: 0;
    border: 2px solid #0a0e27;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #ff00ff, #00ffff);
}

/* ─── ANIMATIONS ─── */
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

WARNA_UTAMA = ["#00ffff", "#ff00ff", "#00ff00", "#ffff00", "#ff0000", "#0080ff"]
BG_PLOT = "rgba(15, 15, 30, 0.6)"
PAPER_BG = "rgba(0,0,0,0)"
FONT_COLOR = "#00ffff"
GRID_COLOR = "rgba(0, 255, 255, 0.15)"

def style_fig(fig):
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=BG_PLOT,
        font=dict(color=FONT_COLOR, family="Rajdhani, sans-serif", size=12),
        margin=dict(t=40, b=30, l=20, r=20),
        legend=dict(
            bgcolor="rgba(15, 15, 30, 0.8)",
            bordercolor="#00ffff",
            borderwidth=2,
            font=dict(color="#00ffff")
        ),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor="rgba(0,255,255,0.3)", tickfont=dict(color="#00ffff"))
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor="rgba(0,255,255,0.3)", tickfont=dict(color="#00ffff"))
    return fig

# ─────────────────────────────────────────────
# SIDEBAR (ALWAYS OPEN)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ CYBER FILTERS")
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
    st.markdown("💾 **CYBER DASHBOARD** · 2026")

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
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="padding: 20px 0 10px 0;">
    <h1 class="cyber-title">💰 CYBER KEUANGAN DASHBOARD</h1>
    <p class="cyber-subtitle">
        Analisis pola pengeluaran & perilaku keuangan mahasiswa Sains Data [SYSTEM ONLINE]
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
k4.metric("🛒 SHOPAHOLIC", f"{pct_belanja_sering}%")
k5.metric("💸 TOP SPEND", modus_pengeluaran.replace("Rp ", "Rp\u00A0"))
st.markdown("")

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 DEMOGRAFI", "💳 PENGELUARAN", "🔍 PERILAKU", "📈 ANALISIS", "🎲 SIMULASI"
])

# ══════════════════════════════════════════════
# TAB 1 – DEMOGRAFI
# ══════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-title">Distribusi Gender</p>', unsafe_allow_html=True)
        gender_cnt = filtered["jenis_kelamin"].value_counts().reset_index()
        gender_cnt.columns = ["Jenis Kelamin", "Jumlah"]
        fig = px.pie(gender_cnt, names="Jenis Kelamin", values="Jumlah", color_discrete_sequence=WARNA_UTAMA, hole=0.55)
        fig.update_traces(textfont_size=13, textinfo="percent+label")
        fig.update_layout(showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Uang Saku Bulanan</p>', unsafe_allow_html=True)
        uang_cnt = filtered["uang_saku"].value_counts().reindex(ORDER_UANG_SAKU, fill_value=0).reset_index()
        uang_cnt.columns = ["Uang Saku", "Jumlah"]
        fig2 = px.bar(uang_cnt, x="Uang Saku", y="Jumlah", color="Jumlah", 
                      color_continuous_scale=[[0, "#0080ff"], [0.5, "#00ffff"], [1, "#ff00ff"]], text="Jumlah")
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
# TAB 2 – PENGELUARAN
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
        fig2 = px.bar(faktor_cnt, y="Faktor_short", x="Jumlah", orientation="h", color="Jumlah", 
                      color_continuous_scale=[[0, "#0080ff"], [0.5, "#ff00ff"], [1, "#ffff00"]], text="Jumlah")
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

    st.markdown('<p class="section-title">Belanja Online</p>', unsafe_allow_html=True)
    belanja_cnt = filtered["frekuensi_belanja_online"].value_counts().reset_index()
    belanja_cnt.columns = ["Frekuensi", "Jumlah"]
    fig4 = px.pie(belanja_cnt, names="Frekuensi", values="Jumlah", color_discrete_sequence=WARNA_UTAMA, hole=0.55)
    fig4.update_traces(textfont_size=13, textinfo="percent+label")
    style_fig(fig4)
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.plotly_chart(fig4, use_container_width=True)
    with col_b:
        st.markdown(" ")
        st.markdown(" ")
        freq_tbl = belanja_cnt.copy()
        freq_tbl["Persentase"] = (freq_tbl["Jumlah"] / n * 100).round(1).astype(str) + "%"
        st.dataframe(freq_tbl, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════
# TAB 3 – PERILAKU
# ══════════════════════════════════════════════
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-title">Kehabisan Uang?</p>', unsafe_allow_html=True)
        kh_cnt = filtered["kehabisan_uang"].value_counts().reset_index()
        kh_cnt.columns = ["Status", "Jumlah"]
        fig = px.pie(kh_cnt, names="Status", values="Jumlah", hole=0.55, color="Status", color_discrete_map={"Ya": "#ff0000", "Tidak": "#00ff00"})
        fig.update_traces(textfont_size=13, textinfo="percent+label")
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Budgeting Habit</p>', unsafe_allow_html=True)
        bd_cnt = filtered["budgeting"].value_counts().reset_index()
        bd_cnt.columns = ["Status", "Jumlah"]
        fig2 = px.pie(bd_cnt, names="Status", values="Jumlah", hole=0.55, color="Status", color_discrete_map={"Ya": "#00ffff", "Tidak": "#ffff00"})
        fig2.update_traces(textfont_size=13, textinfo="percent+label")
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Budgeting vs Kehabisan</p>', unsafe_allow_html=True)
    cross_bk = pd.crosstab(filtered["budgeting"], filtered["kehabisan_uang"])
    cross_bk_pct = (cross_bk.div(cross_bk.sum(axis=1), axis=0) * 100).round(1)

    fig3 = go.Figure()
    colors_map = {"Ya": "#ff0000", "Tidak": "#00ff00"}
    for col_name in cross_bk_pct.columns:
        fig3.add_trace(go.Bar(name=f"Kehabisan: {col_name}", x=cross_bk_pct.index, y=cross_bk_pct[col_name], marker_color=colors_map.get(col_name, WARNA_UTAMA[0]), text=cross_bk_pct[col_name].map(lambda v: f"{v:.1f}%"), textposition="inside"))
    fig3.update_layout(barmode="stack", xaxis_title="Budgeting", yaxis_title="Persentase (%)")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<p class="section-title">Kehabisan per Uang Saku</p>', unsafe_allow_html=True)
    cross_us = pd.crosstab(filtered["uang_saku"], filtered["kehabisan_uang"]).reindex(ORDER_UANG_SAKU, fill_value=0)
    cross_us_pct = (cross_us.div(cross_us.sum(axis=1), axis=0) * 100).round(1)

    fig4 = go.Figure()
    for col_name in cross_us_pct.columns:
        fig4.add_trace(go.Bar(name=f"Kehabisan: {col_name}", x=cross_us_pct.index, y=cross_us_pct[col_name], marker_color=colors_map.get(col_name, WARNA_UTAMA[0]), text=cross_us_pct[col_name].map(lambda v: f"{v:.1f}%"), textposition="inside"))
    fig4.update_layout(barmode="stack", xaxis_title="Uang Saku", yaxis_title="Persentase (%)")
    style_fig(fig4)
    st.plotly_chart(fig4, use_container_width=True)

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
            colorscale=[[0, "#0a0e27"], [0.3, "#0080ff"], [0.6, "#00ffff"], [1, "#ff00ff"]],
            zmin=0, zmax=1,
            text=np.round(matrix, 2), texttemplate="%{text}", textfont={"size": 10, "color": "white"},
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
# TAB 5 – SIMULASI
# ══════════════════════════════════════════════
with tab5:
    st.markdown('<p class="section-title">🎲 Monte Carlo Simulation</p>', unsafe_allow_html=True)
    st.markdown("Prediksi masa depan keuanganmu dengan 10.000 skenario!")

    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        sim_uang_saku = st.selectbox("💵 Uang Saku", ORDER_UANG_SAKU, index=1)
    with col_sim2:
        sim_budgeting = st.selectbox("📒 Budgeting", ["Ya", "Tidak"])

    if st.button("🚀 GENERATE FUTURE", type="primary"):
        with st.spinner("⚡ Processing 10,000 scenarios..."):
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
            st.markdown('<p class="section-title">📊 Money Distribution</p>', unsafe_allow_html=True)

            df_sim = pd.DataFrame({"Sisa Uang": sisa_uang})
            fig_sim = px.histogram(df_sim, x="Sisa Uang", nbins=50,
                                   color_discrete_sequence=["#00ffff"],
                                   marginal="box", opacity=0.9)
            fig_sim.add_vline(x=0, line_dash="dash", line_color="#ff0000",
                              annotation_text="BREAK EVEN", annotation_font_color="#ff0000")
            fig_sim.update_layout(xaxis_title="Sisa Uang (Rp)", yaxis_title="Frekuensi",
                                  showlegend=False, hovermode="x unified")
            style_fig(fig_sim)
            st.plotly_chart(fig_sim, use_container_width=True)

            st.info(f"""
            💾 **SYSTEM OUTPUT:**
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
    "<p style='text-align:center; color:#00ffff; font-size:0.85rem; margin-top: 32px; "
    "font-family: Orbitron, sans-serif; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase;'>"
    "💾 CYBER KEUANGAN DASHBOARD · SAINS DATA · 2026 💾"
    "</p>",
    unsafe_allow_html=True,
)
