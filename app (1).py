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
    page_title="Gen Z Finance Tracker 💸",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS (NEO-BRUTALISM THEME)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Space+Grotesk:wght@400;500;700&display=swap');

/* ─── GLOBAL THEME ─── */
.stApp {
    background-color: #FDF6E3;
    font-family: 'Space Grotesk', sans-serif !important;
    color: #1A1A1A;
}

/* ─── SIDEBAR (ALWAYS OPEN & BRUTALIST) ─── */
[data-testid="stSidebar"] {
    background-color: #FFE66D !important;
    border-right: 4px solid #000 !important;
    z-index: 1000 !important;
    position: relative !important;
}
[data-testid="stSidebar"] > div {
    z-index: 1001 !important;
    position: relative !important;
}
[data-testid="stSidebar"] h2 {
    font-family: 'Archivo Black', sans-serif !important;
    color: #000 !important;
    text-transform: uppercase;
    letter-spacing: -1px;
}
[data-testid="stSidebar"] * {
    color: #000 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stSidebar"] hr {
    border: none;
    height: 3px;
    background: #000;
    margin: 20px 0;
}

/* Hide Hamburger Toggle */
button[data-testid="baseButton-header"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] > div > div > button { display: none !important; }

/* ─── BRUTALIST METRIC CARDS ─── */
[data-testid="metric-container"] {
    background-color: #ffffff !important;
    border: 3px solid #000 !important;
    border-radius: 16px !important;
    box-shadow: 6px 6px 0px #000 !important;
    padding: 20px !important;
    transition: all 0.1s ease-in-out;
}
[data-testid="metric-container"]:hover {
    transform: translate(3px, 3px);
    box-shadow: 2px 2px 0px #000 !important;
}
[data-testid="metric-container"] label {
    font-family: 'Archivo Black', sans-serif !important;
    color: #000 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #FF6B6B !important;
    font-family: 'Archivo Black', sans-serif !important;
    font-size: 2.2rem !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #2EC4B6 !important;
    font-weight: bold !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ─── SECTION TITLES ─── */
.brutal-title {
    font-family: 'Archivo Black', sans-serif !important;
    font-size: 1.4rem !important;
    background: #4ECDC4;
    display: inline-block;
    padding: 6px 16px;
    border: 3px solid #000;
    border-radius: 10px;
    box-shadow: 4px 4px 0px #000;
    margin: 28px 0 18px 0;
    text-transform: uppercase;
    letter-spacing: -0.5px;
    color: #000 !important;
}
.brutal-title-pink { background: #FF6B6B; color: #fff !important; }
.brutal-title-purple { background: #CDB4DB; }
.brutal-title-yellow { background: #FFE66D; }

/* ─── BUTTONS ─── */
.stButton > button {
    background-color: #FF6B6B !important;
    color: #fff !important;
    border: 3px solid #000 !important;
    border-radius: 12px !important;
    font-family: 'Archivo Black', sans-serif !important;
    font-size: 1rem !important;
    box-shadow: 5px 5px 0px #000 !important;
    transition: all 0.1s ease-in-out;
    padding: 0.8rem 1.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.stButton > button:hover {
    transform: translate(3px, 3px);
    box-shadow: 1px 1px 0px #000 !important;
    color: #fff !important;
}

/* ─── SELECTBOXES & INPUTS ─── */
.stSelectbox > div > div, .stTextInput > div > div {
    background-color: #fff !important;
    border: 2px solid #000 !important;
    border-radius: 10px !important;
    color: #000 !important;
    font-weight: 500 !important;
}
.stSelectbox label, .stTextInput label {
    font-family: 'Archivo Black', sans-serif !important;
    color: #000 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    z-index: 1002 !important;
    position: relative !important;
}

/* ─── TABS ─── */
.stTabs [data-baseweb="tab-list"] {
    background-color: #fff !important;
    border: 3px solid #000 !important;
    border-radius: 16px !important;
    box-shadow: 5px 5px 0px #000;
    padding: 8px !important;
    gap: 8px !important;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #000 !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
}
.stTabs [aria-selected="true"] {
    background-color: #4ECDC4 !important;
    border: 2px solid #000 !important;
    color: #000 !important;
}

/* ─── DIVIDER ─── */
hr {
    border: none;
    height: 4px;
    background: #000;
    margin: 32px 0;
    border-radius: 2px;
}

/* ─── DATAFRAME & PLOTLY CHARTS ─── */
[data-testid="stDataFrame"] {
    border: 3px solid #000 !important;
    border-radius: 12px !important;
    box-shadow: 5px 5px 0px #000 !important;
    overflow: hidden;
}
.js-plotly-plot .plotly {
    border-radius: 16px !important;
    background: #ffffff !important;
    border: 3px solid #000 !important;
    box-shadow: 6px 6px 0px #000 !important;
    padding: 16px !important;
}

/* ─── EXPANDER & INFO BOXES ─── */
[data-testid="stExpander"] {
    background-color: #fff !important;
    border: 3px solid #000 !important;
    border-radius: 12px !important;
    box-shadow: 5px 5px 0px #000 !important;
}
[data-testid="stExpander"] summary span {
    font-family: 'Archivo Black', sans-serif !important;
    color: #000 !important;
}
[data-testid="stAlert"] {
    background-color: #CDB4DB !important;
    border: 3px solid #000 !important;
    border-radius: 12px !important;
    box-shadow: 5px 5px 0px #000 !important;
    color: #000 !important;
}
[data-testid="stAlert"] * { 
    color: #000 !important; 
    font-weight: 500 !important; 
}

/* ─── CUSTOM SCROLLBAR ─── */
::-webkit-scrollbar { width: 14px; }
::-webkit-scrollbar-track { background: #FDF6E3; border-left: 2px solid #000; }
::-webkit-scrollbar-thumb { background: #FF6B6B; border: 2px solid #000; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #4ECDC4; }

/* Hide Streamlit Branding */
#MainMenu, header, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD DATA (BERSIH DARI BUG SPASI)
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
# KONSTANTA & WARNA NEO-BRUTALISM
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

# Palet Warna Brutalism
WARNA_UTAMA = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#CDB4DB", "#FF9F1C", "#2EC4B6"]
BG_PLOT = "#FDF6E3"
PAPER_BG = "#FDF6E3"
FONT_COLOR = "#1A1A1A"
GRID_COLOR = "#E0E0E0"

def style_fig(fig):
    """Terapkan tema Neo-Brutalism ke chart Plotly."""
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor="#FFFFFF",
        font=dict(color=FONT_COLOR, family="Space Grotesk, sans-serif", size=13, weight=500),
        margin=dict(t=40, b=30, l=20, r=20),
        legend=dict(
            bgcolor="#FFFFFF",
            bordercolor="#000000",
            borderwidth=2,
            font=dict(family="Space Grotesk, sans-serif", size=12, color="#000")
        ),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor="#000", linewidth=2, tickfont=dict(family="Space Grotesk", color="#000"))
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor="#000", linewidth=2, tickfont=dict(family="Space Grotesk", color="#000"))
    # Tambahkan outline hitam pada bar chart
    fig.update_traces(marker_line_color='black', marker_line_width=2)
    return fig

# ─────────────────────────────────────────────
# SIDEBAR – FILTER (SELALU TERBUKA)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Filter Data")
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
    st.markdown("**Sumber Data:** Survei Statistika")

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
# HEADER (BRUTALIST HERO CARD)
# ─────────────────────────────────────────────
st.markdown("""
<div style="background: #FFE66D; border: 4px solid #000; border-radius: 24px; padding: 32px; box-shadow: 10px 10px 0px #000; text-align: center; margin-bottom: 32px;">
    <h1 style="font-family: 'Archivo Black', sans-serif; font-size: 3.5rem; margin: 0; color: #000; text-transform: uppercase; letter-spacing: -2px; line-height: 1;">
        💸 GEN Z FINANCE <br><span style="color: #FF6B6B; -webkit-text-stroke: 2px #000;">TRACKER</span>
    </h1>
    <p style="font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; font-weight: 700; color: #000; margin-top: 16px;">
        Analisis pola pengeluaran mahasiswa Sains Data tanpa basa-basi. ✨
    </p>
    <div style="margin-top: 24px; display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;">
        <span style="background: #FF6B6B; color: #fff; padding: 8px 20px; border: 2px solid #000; border-radius: 50px; font-weight: bold; font-family: 'Space Grotesk'; box-shadow: 4px 4px 0px #000; text-transform: uppercase;">✨ No Cap Data</span>
        <span style="background: #4ECDC4; color: #000; padding: 8px 20px; border: 2px solid #000; border-radius: 50px; font-weight: bold; font-family: 'Space Grotesk'; box-shadow: 4px 4px 0px #000; text-transform: uppercase;">💅 Budgeting Slay</span>
        <span style="background: #CDB4DB; color: #000; padding: 8px 20px; border: 2px solid #000; border-radius: 50px; font-weight: bold; font-family: 'Space Grotesk'; box-shadow: 4px 4px 0px #000; text-transform: uppercase;">🔥 Monte Carlo FR FR</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
pct_kehabisan = round(filtered[filtered["kehabisan_uang"] == "Ya"].shape[0] / n * 100, 1) if n else 0
pct_budgeting = round(filtered[filtered["budgeting"] == "Ya"].shape[0] / n * 100, 1) if n else 0
pct_belanja_sering = round(filtered[filtered["frekuensi_belanja_online"] == "3 kali atau lebih"].shape[0] / n * 100, 1) if n else 0
modus_pengeluaran = filtered["total_pengeluaran"].mode()[0] if n else "-"

k1.metric("👥 RESPONDEN", f"{n}")
k2.metric("⚠️ STRUGGLE", f"{pct_kehabisan}%")
k3.metric("📒 PLANNER", f"{pct_budgeting}%")
k4.metric("🛒 IMPULSIVE", f"{pct_belanja_sering}%")
k5.metric("💸 DOMINAN", modus_pengeluaran.replace("Rp ", "Rp\u00A0"))

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
        st.markdown('<p class="brutal-title">Distribusi Gender</p>', unsafe_allow_html=True)
        gender_cnt = filtered["jenis_kelamin"].value_counts().reset_index()
        gender_cnt.columns = ["Jenis Kelamin", "Jumlah"]
        fig = px.pie(gender_cnt, names="Jenis Kelamin", values="Jumlah",
                     color_discrete_sequence=WARNA_UTAMA, hole=0.45)
        fig.update_traces(textfont_size=14, textinfo="percent+label", textfont_color="#000", textfont_family="Archivo Black")
        fig.update_layout(showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="brutal-title brutal-title-yellow">Uang Saku Bulanan</p>', unsafe_allow_html=True)
        uang_cnt = filtered["uang_saku"].value_counts().reindex(ORDER_UANG_SAKU, fill_value=0).reset_index()
        uang_cnt.columns = ["Uang Saku", "Jumlah"]
        fig2 = px.bar(uang_cnt, x="Uang Saku", y="Jumlah",
                      color="Jumlah", color_continuous_scale=[[0, "#FFE66D"], [0.5, "#FF9F1C"], [1, "#FF6B6B"]],
                      text="Jumlah")
        fig2.update_traces(textposition="outside", textfont_color="#000", textfont_family="Archivo Black")
        fig2.update_coloraxes(showscale=False)
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="brutal-title brutal-title-pink">Uang Saku vs Gender</p>', unsafe_allow_html=True)
    cross = pd.crosstab(filtered["uang_saku"], filtered["jenis_kelamin"]).reindex(ORDER_UANG_SAKU, fill_value=0)
    fig3 = go.Figure()
    for i, col_name in enumerate(cross.columns):
        fig3.add_trace(go.Bar(name=col_name, x=cross.index, y=cross[col_name],
                              marker_color=WARNA_UTAMA[i], text=cross[col_name], textposition="auto",
                              marker_line_color='black', marker_line_width=2))
    fig3.update_layout(barmode="group", xaxis_title="Uang Saku", yaxis_title="Jumlah")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 2 – POLA PENGELUARAN
# ══════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="brutal-title">Total Pengeluaran</p>', unsafe_allow_html=True)
        tot_cnt = filtered["total_pengeluaran"].value_counts().reindex(ORDER_TOTAL_PENGELUARAN, fill_value=0).reset_index()
        tot_cnt.columns = ["Total Pengeluaran", "Jumlah"]
        fig = px.bar(tot_cnt, x="Total Pengeluaran", y="Jumlah",
                     color="Total Pengeluaran", color_discrete_sequence=WARNA_UTAMA, text="Jumlah")
        fig.update_traces(textposition="outside", textfont_color="#000", textfont_family="Archivo Black", showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="brutal-title brutal-title-pink">Trigger Boros</p>', unsafe_allow_html=True)
        faktor_cnt = filtered["faktor_membengkak"].value_counts().reset_index()
        faktor_cnt.columns = ["Faktor", "Jumlah"]
        faktor_cnt["Faktor_short"] = faktor_cnt["Faktor"].str.extract(r'^([^(]+)').iloc[:, 0].str.strip()
        fig2 = px.bar(faktor_cnt, y="Faktor_short", x="Jumlah",
                      orientation="h", color="Jumlah",
                      color_continuous_scale=[[0, "#FFE66D"], [0.5, "#FF6B6B"], [1, "#CDB4DB"]], text="Jumlah")
        fig2.update_traces(textposition="outside", textfont_color="#000", textfont_family="Archivo Black")
        fig2.update_coloraxes(showscale=False)
        fig2.update_layout(yaxis_title=" ")
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="brutal-title brutal-title-purple">Breakdown Kategori</p>', unsafe_allow_html=True)
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
    fig3.update_traces(textposition="outside", textfont_color="#000", textfont_family="Archivo Black")
    fig3.update_layout(xaxis_title="Kategori", yaxis_title="Jumlah")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 – PERILAKU KEUANGAN
# ══════════════════════════════════════════════
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="brutal-title brutal-title-pink">Pernah Kehabisan?</p>', unsafe_allow_html=True)
        kh_cnt = filtered["kehabisan_uang"].value_counts().reset_index()
        kh_cnt.columns = ["Status", "Jumlah"]
        fig = px.pie(kh_cnt, names="Status", values="Jumlah", hole=0.5,
                     color="Status", color_discrete_map={"Ya": "#FF6B6B", "Tidak": "#4ECDC4"})
        fig.update_traces(textfont_size=16, textinfo="percent+label", textfont_color="#000", textfont_family="Archivo Black")
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="brutal-title">Budgeting Habit</p>', unsafe_allow_html=True)
        bd_cnt = filtered["budgeting"].value_counts().reset_index()
        bd_cnt.columns = ["Status", "Jumlah"]
        fig2 = px.pie(bd_cnt, names="Status", values="Jumlah", hole=0.5,
                      color="Status", color_discrete_map={"Ya": "#2EC4B6", "Tidak": "#FFE66D"})
        fig2.update_traces(textfont_size=16, textinfo="percent+label", textfont_color="#000", textfont_family="Archivo Black")
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="brutal-title brutal-title-purple">Budgeting vs Kehabisan</p>', unsafe_allow_html=True)
    cross_bk = pd.crosstab(filtered["budgeting"], filtered["kehabisan_uang"])
    cross_bk_pct = (cross_bk.div(cross_bk.sum(axis=1), axis=0) * 100).round(1)

    fig3 = go.Figure()
    colors_map = {"Ya": "#FF6B6B", "Tidak": "#4ECDC4"}
    for col_name in cross_bk_pct.columns:
        fig3.add_trace(go.Bar(name=f"Kehabisan: {col_name}", x=cross_bk_pct.index, y=cross_bk_pct[col_name],
                              marker_color=colors_map.get(col_name, WARNA_UTAMA[0]),
                              text=cross_bk_pct[col_name].map(lambda v: f"{v:.1f}%"), textposition="inside",
                              marker_line_color='black', marker_line_width=2))
    fig3.update_layout(barmode="stack", xaxis_title="Budgeting", yaxis_title="Persentase (%)")
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 4 – ANALISIS LANJUTAN
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<p class="brutal-title">🔥 Heatmap Asosiasi (Cramér\'s V)</p>', unsafe_allow_html=True)

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
            colorscale=[[0, "#FDF6E3"], [0.3, "#FFE66D"], [0.6, "#FF9F1C"], [1, "#FF6B6B"]],
            zmin=0, zmax=1,
            text=np.round(matrix, 2), texttemplate="%{text}",
            textfont={"size": 12, "color": "#000", "family": "Archivo Black"},
        ))
        fig_heat.update_layout(height=550, xaxis=dict(tickangle=-45))
        style_fig(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.warning("Data terlalu sedikit. Hapus filter untuk melihat heatmap.")

    st.markdown("---")
    st.markdown('<p class="brutal-title brutal-title-yellow">📄 Raw Data</p>', unsafe_allow_html=True)
    with st.expander("Lihat Dataset Lengkap"):
        st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download CSV",
            data=csv,
            file_name="data_filtered.csv",
            mime="text/csv",
        )

# ══════════════════════════════════════════════
# TAB 5 – SIMULASI MONTE CARLO
# ══════════════════════════════════════════════
with tab5:
    st.markdown('<p class="brutal-title brutal-title-purple">🎲 Simulasi Monte Carlo</p>', unsafe_allow_html=True)
    st.markdown("Coba prediksi masa depan keuanganmu dengan 10.000 skenario acak! ✨")
    
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        sim_uang_saku = st.selectbox("💵 Skenario Uang Saku", ORDER_UANG_SAKU, index=1)
    with col_sim2:
        sim_budgeting = st.selectbox("📒 Skenario Budgeting", ["Ya", "Tidak"])
        
    if st.button("🚀 Generate Future", type="primary"):
        with st.spinner("⏳ Loading masa depan..."):
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
            kpi1.metric("📉 PROB. STRUGGLE", f"{prob_khabis:.1f}%",
                        delta=f"{delta_khabis:+.1f}%",
                        delta_color="inverse" if prob_khabis > overall_khabis else "normal")
            kpi2.metric("💰 AVG. LEFTOVER", f"Rp {mean_sisa:,.0f}")
            kpi3.metric("⚠️ DEFICIT RISK", f"{risk_sisa_negatif:.1f}%")
            
            st.markdown("---")
            
            st.markdown('<p class="brutal-title brutal-title-pink">📊 Distribusi Sisa Uang</p>', unsafe_allow_html=True)
            
            df_sim = pd.DataFrame({"Sisa Uang": sisa_uang})
            fig_sim = px.histogram(df_sim, x="Sisa Uang", nbins=50,
                                   color_discrete_sequence=["#4ECDC4"],
                                   marginal="box", opacity=0.95)
            fig_sim.add_vline(x=0, line_dash="solid", line_color="#FF6B6B", line_width=4,
                              annotation_text="BREAK EVEN", annotation_font_color="#FF6B6B",
                              annotation_font_family="Archivo Black")
            
            fig_sim.update_layout(xaxis_title="Sisa Uang (Rp)", yaxis_title="Frekuensi",
                                  showlegend=False, hovermode="x unified")
            style_fig(fig_sim)
            st.plotly_chart(fig_sim, use_container_width=True)
            
            st.info(f"""
            💡 **Insight Simulasi:**
            - Profil: **Uang Saku: {sim_uang_saku}** & **Budgeting: {sim_budgeting}**
            - Rata-rata sisa: **Rp {mean_sisa:,.0f}**
            - Risiko defisit (Sisa < 0): **{risk_sisa_negatif:.1f}%**
            - 90% Confidence Interval: **Rp {p5_sisa:,.0f}** hingga **Rp {p95_sisa:,.0f}**
            """)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#000; font-size:1rem; margin-top: 32px; "
    "font-family: Archivo Black, sans-serif; text-transform: uppercase; letter-spacing: 1px;'>"
    "✨ Gen Z Finance Tracker · Sains Data · 2026 ✨"
    "</p>",
    unsafe_allow_html=True,
)
