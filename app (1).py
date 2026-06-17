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
    page_title="Aesthetic Finance Hub 💜",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS - AESTHETIC VIBES THEME
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');

/* ─── GLOBAL AESTHETIC THEME ─── */
.stApp {
    background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%);
    background-attachment: fixed;
    font-family: 'Poppins', sans-serif !important;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* ─── SIDEBAR AESTHETIC ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%) !important;
    backdrop-filter: blur(20px);
    border-right: 2px solid rgba(139, 92, 246, 0.3) !important;
    padding: 2rem 1rem !important;
}

[data-testid="stSidebar"] h2 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #8B5CF6, #EC4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 1.8rem !important;
    margin-bottom: 1.5rem !important;
}

/* HIDE SIDEBAR COLLAPSE BUTTON */
button[data-testid="baseButton-header"], 
[data-testid="collapsedControl"],
section[data-testid="stSidebar"] > div > div > button {
    display: none !important;
}

/* ─── AESTHETIC METRIC CARDS ─── */
[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px);
    border: 2px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 20px !important;
    padding: 1.5rem !important;
    box-shadow: 0 8px 32px rgba(139, 92, 246, 0.2);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

[data-testid="metric-container"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #8B5CF6, #EC4899, #06B6D4);
}

[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(139, 92, 246, 0.4);
    border-color: rgba(236, 72, 153, 0.5) !important;
}

[data-testid="metric-container"] label {
    color: #C4B5FD !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: 'Poppins', sans-serif !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 2rem !important;
    font-weight: 900 !important;
    font-family: 'Poppins', sans-serif !important;
    background: linear-gradient(135deg, #8B5CF6, #EC4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #10B981 !important;
    font-weight: 700 !important;
}

/* ─── AESTHETIC HEADER & TITLES ─── */
.aesthetic-title {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 900 !important;
    font-size: 2.5rem !important;
    background: linear-gradient(135deg, #8B5CF6, #EC4899, #06B6D4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    text-align: center;
}

.aesthetic-subtitle {
    color: #C4B5FD;
    font-size: 1.1rem;
    font-weight: 400;
    text-align: center;
    margin-bottom: 2rem;
}

.section-title {
    color: #FFFFFF;
    font-size: 1.2rem;
    font-weight: 700;
    padding-left: 20px;
    margin: 2rem 0 1rem 0;
    position: relative;
    font-family: 'Poppins', sans-serif !important;
}

.section-title::before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, #8B5CF6, #EC4899);
    border-radius: 2px;
}

/* ─── AESTHETIC BUTTONS ─── */
.stButton > button {
    background: linear-gradient(135deg, #8B5CF6, #EC4899) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.8rem 2.5rem !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.05em;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(236, 72, 153, 0.6);
}

/* ─── AESTHETIC SELECTBOXES ─── */
.stSelectbox > div > div, .stTextInput > div > div {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px);
    border: 2px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 12px !important;
    color: #C4B5FD !important;
    padding: 0.5rem !important;
    transition: all 0.3s ease !important;
}

.stSelectbox > div > div:hover, .stTextInput > div > div:hover {
    border-color: rgba(236, 72, 153, 0.6) !important;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.3) !important;
}

.stSelectbox label, .stTextInput label {
    color: #C4B5FD !important;
    font-weight: 600 !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 0.85rem !important;
}

/* ─── AESTHETIC TABS ─── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 0.5rem;
    gap: 0.5rem;
    border: 2px solid rgba(139, 92, 246, 0.2);
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #C4B5FD !important;
    border-radius: 12px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.8rem 1.5rem !important;
    transition: all 0.3s ease !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #8B5CF6, #EC4899) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
}

.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
    background: rgba(139, 92, 246, 0.2) !important;
    color: white !important;
}

/* ─── AESTHETIC DIVIDER ─── */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #8B5CF6, #EC4899, transparent);
    margin: 2rem 0;
    border-radius: 1px;
}

/* ─── AESTHETIC CHARTS & CONTAINERS ─── */
.js-plotly-plot .plotly {
    border-radius: 16px !important;
    background: rgba(255, 255, 255, 0.03) !important;
    backdrop-filter: blur(10px);
    border: 2px solid rgba(139, 92, 246, 0.2);
    padding: 1rem;
}

[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    border: 2px solid rgba(139, 92, 246, 0.3) !important;
    overflow: hidden;
}

[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px);
    border: 2px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 16px !important;
}

[data-testid="stAlert"] {
    background: rgba(139, 92, 246, 0.1) !important;
    backdrop-filter: blur(10px);
    border: 2px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 16px !important;
}

/* ─── AESTHETIC SCROLLBAR ─── */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.5); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #8B5CF6, #EC4899);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #EC4899, #8B5CF6);
}

/* ─── ANIMATIONS ─── */
@keyframes fadeInUp {
    from { 
        opacity: 0; 
        transform: translateY(20px); 
    }
    to { 
        opacity: 1; 
        transform: translateY(0); 
    }
}

.element-container, .stPlotlyChart, [data-testid="stMetric"] {
    animation: fadeInUp 0.6s ease-out forwards;
}

/* Hide Streamlit Branding */
#MainMenu, header, footer { visibility: hidden; }

/* ─── RESPONSIVE ADJUSTMENTS ─── */
@media (max-width: 768px) {
    .aesthetic-title {
        font-size: 1.8rem !important;
    }
    
    [data-testid="metric-container"] {
        padding: 1rem !important;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
}
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

WARNA_UTAMA = ["#8B5CF6", "#EC4899", "#06B6D4", "#10B981", "#F59E0B", "#EF4444"]
BG_PLOT = "rgba(255, 255, 255, 0.03)"
PAPER_BG = "rgba(0,0,0,0)"
FONT_COLOR = "#E0E7FF"
GRID_COLOR = "rgba(139, 92, 246, 0.15)"

def style_fig(fig):
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=BG_PLOT,
        font=dict(color=FONT_COLOR, family="Poppins, sans-serif", size=12),
        margin=dict(t=40, b=30, l=20, r=20),
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0.05)",
            bordercolor="rgba(139, 92, 246, 0.3)",
            borderwidth=2,
            font=dict(color="#E0E7FF")
        ),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor="rgba(139, 92, 246, 0.3)", tickfont=dict(color="#C4B5FD"))
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor="rgba(139, 92, 246, 0.3)", tickfont=dict(color="#C4B5FD"))
    return fig

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✨ Filter Aesthetic")
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
    st.markdown("💜 **Aesthetic Finance Hub** · 2026")

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
<div style="padding: 2rem 0 1rem 0;">
    <h1 class="aesthetic-title">💰 Aesthetic Finance Hub</h1>
    <p class="aesthetic-subtitle">
        Analisis pola pengeluaran & perilaku keuangan mahasiswa Sains Data ✨
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
k5.metric("💸 TOP SPEND", modus_pengeluaran.replace("Rp ", "Rp "))
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
        fig = px.pie(gender_cnt, names="Jenis Kelamin", values="Jumlah", 
                     color_discrete_sequence=WARNA_UTAMA, hole=0.55)
        fig.update_traces(textfont_size=13, textinfo="percent+label")
        fig.update_layout(showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Uang Saku Bulanan</p>', unsafe_allow_html=True)
        uang_cnt = filtered["uang_saku"].value_counts().reindex(ORDER_UANG_SAKU, fill_value=0).reset_index()
        uang_cnt.columns = ["Uang Saku", "Jumlah"]
        fig2 = px.bar(uang_cnt, x="Uang Saku", y="Jumlah", color="Jumlah", 
                      color_continuous_scale=[[0, "#8B5CF6"], [0.5, "#EC4899"], [1, "#06B6D4"]], 
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
        st.markdown('<p class="section-title">Total Pengeluaran</p>', unsafe_allow_html=True)
        tot_cnt = filtered["total_pengeluaran"].value_counts().reindex(ORDER_TOTAL_PENGELUARAN, fill_value=0).reset_index()
        tot_cnt.columns = ["Total Pengeluaran", "Jumlah"]
        fig = px.bar(tot_cnt, x="Total Pengeluaran", y="Jumlah", color="Total Pengeluaran", 
                     color_discrete_sequence=WARNA_UTAMA, text="Jumlah")
        fig.update_traces(textposition="outside", textfont_color=FONT_COLOR, showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Faktor Membengkak</p>', unsafe_allow_html=True)
        faktor_cnt = filtered["faktor_membengkak"].value_counts().reset_index()
        faktor_cnt.columns = ["Faktor", "Jumlah"]
        faktor_cnt["Faktor_short"] = faktor_cnt["Faktor"].str.extract(r'^([^(]+)').iloc[:, 0].str.strip()
        fig2 = px.bar(faktor_cnt, y="Faktor_short", x="Jumlah", orientation="h", color="Jumlah", 
                      color_continuous_scale=[[0, "#EC4899"], [0.5, "#8B5CF6"], [1, "#F59E0B"]], 
                      text="Jumlah")
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

    fig3 = px.bar(breakdown_melt, x="Kategori", y="Jumlah", color="Jenis", barmode="group", 
                  color_discrete_sequence=WARNA_UTAMA, text="Jumlah")
    fig3.update_traces(textposition="outside", textfont_color=FONT_COLOR)
    fig3.update_layout(xaxis_title="Range Pengeluaran", yaxis_title="Jumlah Mahasiswa")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<p class="section-title">Belanja Online</p>', unsafe_allow_html=True)
    belanja_cnt = filtered["frekuensi_belanja_online"].value_counts().reset_index()
    belanja_cnt.columns = ["Frekuensi", "Jumlah"]
    fig4 = px.pie(belanja_cnt, names="Frekuensi", values="Jumlah", 
                  color_discrete_sequence=WARNA_UTAMA, hole=0.55)
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
        fig = px.pie(kh_cnt, names="Status", values="Jumlah", hole=0.55, color="Status", 
                     color_discrete_map={"Ya": "#EF4444", "Tidak": "#10B981"})
        fig.update_traces(textfont_size=13, textinfo="percent+label")
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Budgeting Habit</p>', unsafe_allow_html=True)
        bd_cnt = filtered["budgeting"].value_counts().reset_index()
        bd_cnt.columns = ["Status", "Jumlah"]
        fig2 = px.pie(bd_cnt, names="Status", values="Jumlah", hole=0.55, color="Status", 
                      color_discrete_map={"Ya": "#8B5CF6", "Tidak": "#F59E0B"})
        fig2.update_traces(textfont_size=13, textinfo="percent+label")
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Budgeting vs Kehabisan</p>', unsafe_allow_html=True)
    cross_bk = pd.crosstab(filtered["budgeting"], filtered["kehabisan_uang"])
    cross_bk_pct = (cross_bk.div(cross_bk.sum(axis=1), axis=0) * 100).round(1)

    fig3 = go.Figure()
    colors_map = {"Ya": "#EF4444", "Tidak": "#10B981"}
    for col_name in cross_bk_pct.columns:
        fig3.add_trace(go.Bar(name=f"Kehabisan: {col_name}", x=cross_bk_pct.index, y=cross_bk_pct[col_name], 
                              marker_color=colors_map.get(col_name, WARNA_UTAMA[0]), 
                              text=cross_bk_pct[col_name].map(lambda v: f"{v:.1f}%"), textposition="inside"))
    fig3.update_layout(barmode="stack", xaxis_title="Budgeting", yaxis_title="Persentase (%)")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<p class="section-title">Kehabisan per Uang Saku</p>', unsafe_allow_html=True)
    cross_us = pd.crosstab(filtered["uang_saku"], filtered["kehabisan_uang"]).reindex(ORDER_UANG_SAKU, fill_value=0)
    cross_us_pct = (cross_us.div(cross_us.sum(axis=1), axis=0) * 100).round(1)

    fig4 = go.Figure()
    for col_name in cross_us_pct.columns:
        fig4.add_trace(go.Bar(name=f"Kehabisan: {col_name}", x=cross_us_pct.index, y=cross_us_pct[col_name], 
                              marker_color=colors_map.get(col_name, WARNA_UTAMA[0]), 
                              text=cross_us_pct[col_name].map(lambda v: f"{v:.1f}%"), textposition="inside"))
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
            colorscale=[[0, "#1E1B4B"], [0.3, "#8B5CF6"], [0.6, "#EC4899"], [1, "#06B6D4"]],
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
    st.markdown("Prediksi masa depan keuanganmu dengan 10.000 skenario! ✨")

    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        sim_uang_saku = st.selectbox("💵 Uang Saku", ORDER_UANG_SAKU, index=1)
    with col_sim2:
        sim_budgeting = st.selectbox("📒 Budgeting", ["Ya", "Tidak"])

    if st.button("🚀 GENERATE FUTURE", type="primary"):
        with st.spinner("✨ Processing 10,000 scenarios..."):
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
                                   color_discrete_sequence=["#8B5CF6"],
                                   marginal="box", opacity=0.8)
            fig_sim.add_vline(x=0, line_dash="dash", line_color="#EF4444",
                              annotation_text="BREAK EVEN", annotation_font_color="#EF4444")
            fig_sim.update_layout(xaxis_title="Sisa Uang (Rp)", yaxis_title="Frekuensi",
                                  showlegend=False, hovermode="x unified")
            style_fig(fig_sim)
            st.plotly_chart(fig_sim, use_container_width=True)

            st.info(f"""
            ✨ **SYSTEM OUTPUT:**
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
    "<p style='text-align:center; color:#C4B5FD; font-size:0.9rem; margin-top: 2rem; "
    "font-family: Poppins, sans-serif; font-weight: 600; letter-spacing: 0.05em;'>"
    "💜 Aesthetic Finance Hub · Sains Data · 2026 💜"
    "</p>",
    unsafe_allow_html=True,
)
