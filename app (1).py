import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="💸 MoneyTracker Gen Z",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS - GEN Z STYLE
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* Background dengan gradient */
.stApp { 
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    background-attachment: fixed;
}

/* Glassmorphism cards */
[data-testid="metric-container"] {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
    transition: all 0.3s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.25);
    border-color: rgba(99, 102, 241, 0.6);
}

[data-testid="metric-container"] label {
    color: #a5b4fc !important;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e0e7ff !important;
    font-size: 2rem;
    font-weight: 800;
}

/* Header section dengan glow effect */
.section-title {
    color: #e0e7ff;
    font-size: 1.2rem;
    font-weight: 700;
    border-left: 4px solid #818cf8;
    padding-left: 12px;
    margin: 24px 0 16px 0;
    text-shadow: 0 0 20px rgba(129, 140, 248, 0.5);
}

/* Sidebar modern */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    border-right: 1px solid rgba(99, 102, 241, 0.3);
}

[data-testid="stSidebar"] * { 
    color: #e2e8f0; 
}

/* Button styling */
.stButton>button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
}

/* Plotly chart styling */
.js-plotly-plot .plotly { 
    border-radius: 16px; 
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

/* Tab styling modern */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(30, 41, 59, 0.6);
    border-radius: 12px;
    padding: 6px;
    gap: 6px;
    border: 1px solid rgba(99, 102, 241, 0.2);
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #94a3b8;
    border-radius: 10px;
    font-weight: 600;
    padding: 8px 16px;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

/* Info boxes dengan gradient */
.stAlert {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
    border: 1px solid rgba(99, 102, 241, 0.4);
    border-radius: 12px;
    color: #e0e7ff;
}

/* Progress bar modern */
.stProgress > div > div {
    background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    border-radius: 10px;
}

/* Divider dengan glow */
hr { 
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.2);
}

/* Badge styling */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    margin: 2px;
}

.badge-high {
    background: linear-gradient(135deg, #f43f5e, #fb7185);
    color: white;
}

.badge-medium {
    background: linear-gradient(135deg, #f59e0b, #fbbf24);
    color: white;
}

.badge-low {
    background: linear-gradient(135deg, #10b981, #34d399);
    color: white;
}

/* Animation */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
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
# ORDER KATEGORIS
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

# Gen Z Color Palette - Vibrant & Modern
WARNA_PRIMER = "#6366f1"
WARNA_SEKUNDER = "#8b5cf6"
WARNA_AKSEN = "#06b6d4"
WARNA_PANAS = "#f43f5e"
WARNA_SUCESS = "#10b981"
WARNA_PERINGATAN = "#f59e0b"

WARNA_UTAMA = [WARNA_PRIMER, WARNA_AKSEN, WARNA_PERINGATAN, WARNA_SUCESS, WARNA_PANAS, WARNA_SEKUNDER]

BG_PLOT = "#1e293b"
PAPER_BG = "rgba(15, 23, 42, 0.8)"
FONT_COLOR = "#e2e8f0"
GRID_COLOR = "#334155"

def style_fig(fig):
    """Modern dark theme untuk semua chart Plotly."""
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=BG_PLOT,
        font=dict(color=FONT_COLOR, family="Inter, sans-serif", size=11),
        margin=dict(t=50, b=40, l=30, r=20),
        legend=dict(
            bgcolor="rgba(30, 41, 59, 0.8)",
            bordercolor=GRID_COLOR,
            borderwidth=1,
            font=dict(size=10),
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="rgba(30, 41, 59, 0.95)",
            font_size=11,
            font_family="Inter, sans-serif",
        ),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, showline=True, linewidth=1, linecolor=GRID_COLOR)
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, showline=True, linewidth=1, linecolor=GRID_COLOR)
    return fig

# ─────────────────────────────────────────────
# SIDEBAR – FILTER
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='color: #e0e7ff; margin: 0; font-size: 1.8rem;'>🎛️ Control Panel</h2>
        <p style='color: #94a3b8; margin: 8px 0 0 0; font-size: 0.9rem;'>Filter Data Keuangan</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    gender_options = ["Semua"] + sorted(df["jenis_kelamin"].unique().tolist())
    gender_filter = st.selectbox("👤 Gender", gender_options)

    uang_saku_options = ["Semua"] + ORDER_UANG_SAKU
    uang_saku_filter = st.selectbox("💵 Uang Saku/Bulan", uang_saku_options)

    kehabisan_options = ["Semua", "Ya", "Tidak"]
    kehabisan_filter = st.selectbox("⚠️ Pernah Kehabisan Uang?", kehabisan_options)

    budgeting_options = ["Semua", "Ya", "Tidak"]
    budgeting_filter = st.selectbox("📒 Pakai Budgeting?", budgeting_options)

    st.markdown("---")
    
    # Stats sidebar dengan style modern
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2)); 
                padding: 16px; border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.3);'>
        <div style='text-align: center;'>
            <div style='font-size: 2rem; font-weight: 800; color: #e0e7ff;'>{len(df)}</div>
            <div style='font-size: 0.85rem; color: #a5b4fc; margin-top: 4px;'>Total Responden</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 12px;'>📊 Data Real-time</div>", unsafe_allow_html=True)

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
# HEADER DENGAN HERO SECTION
# ─────────────────────────────────────────────
st.markdown("""
<div style='padding: 30px 0 20px 0; text-align: center;'>
    <h1 style='background: linear-gradient(135deg, #e0e7ff 0%, #a5b4fc 50%, #818cf8 100%); 
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               font-size: 3rem; font-weight: 900; margin: 0; letter-spacing: -1px;'>
        💸 MoneyTracker Gen Z
    </h1>
    <p style='color: #94a3b8; margin: 12px 0 0 0; font-size: 1.1rem; font-weight: 400;'>
        Analisis Pola Keuangan & Gaya Hidup Mahasiswa Modern
    </p>
    <div style='display: flex; justify-content: center; gap: 12px; margin-top: 16px;'>
        <span class='badge badge-high'>📈 Real-time</span>
        <span class='badge badge-medium'>🎯 Data-Driven</span>
        <span class='badge badge-low'>🔒 Private</span>
    </div>
</div>
<hr style='margin: 24px 0;'>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CARDS - MODERN DESIGN
# ─────────────────────────────────────────────
pct_kehabisan = round(filtered[filtered["kehabisan_uang"] == "Ya"].shape[0] / n * 100, 1) if n else 0
pct_budgeting = round(filtered[filtered["budgeting"] == "Ya"].shape[0] / n * 100, 1) if n else 0
pct_belanja_sering = round(filtered[filtered["frekuensi_belanja_online"] == "3 kali atau lebih"].shape[0] / n * 100, 1) if n else 0
modus_pengeluaran = filtered["total_pengeluaran"].mode()[0] if n else "-"

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.1)); 
                padding: 24px; border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.3);
                text-align: center; box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);'>
        <div style='font-size: 2.5rem; margin-bottom: 8px;'>👥</div>
        <div style='font-size: 2rem; font-weight: 800; color: #e0e7ff;'>{n}</div>
        <div style='color: #a5b4fc; font-size: 0.9rem; font-weight: 600; margin-top: 4px;'>Responden Aktif</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    delta_color = "inverse" if pct_kehabisan > 50 else "normal"
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(244, 63, 94, 0.2), rgba(251, 113, 133, 0.1)); 
                padding: 24px; border-radius: 16px; border: 1px solid rgba(244, 63, 94, 0.3);
                text-align: center; box-shadow: 0 8px 32px rgba(244, 63, 94, 0.15);'>
        <div style='font-size: 2.5rem; margin-bottom: 8px;'>⚠️</div>
        <div style='font-size: 2rem; font-weight: 800; color: #e0e7ff;'>{pct_kehabisan}%</div>
        <div style='color: #fca5a5; font-size: 0.9rem; font-weight: 600; margin-top: 4px;'>Kehabisan Uang</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(52, 211, 153, 0.1)); 
                padding: 24px; border-radius: 16px; border: 1px solid rgba(16, 185, 129, 0.3);
                text-align: center; box-shadow: 0 8px 32px rgba(16, 185, 129, 0.15);'>
        <div style='font-size: 2.5rem; margin-bottom: 8px;'>📒</div>
        <div style='font-size: 2rem; font-weight: 800; color: #e0e7ff;'>{pct_budgeting}%</div>
        <div style='color: #6ee7b7; font-size: 0.9rem; font-weight: 600; margin-top: 4px;'>Pakai Budgeting</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(34, 211, 238, 0.1)); 
                padding: 24px; border-radius: 16px; border: 1px solid rgba(6, 182, 212, 0.3);
                text-align: center; box-shadow: 0 8px 32px rgba(6, 182, 212, 0.15);'>
        <div style='font-size: 2.5rem; margin-bottom: 8px;'>🛒</div>
        <div style='font-size: 2rem; font-weight: 800; color: #e0e7ff;'>{pct_belanja_sering}%</div>
        <div style='color: #67e8f9; font-size: 0.9rem; font-weight: 600; margin-top: 4px;'>Shopaholic</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB NAVIGASI
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Demografi & Distribusi",
    "💳 Pola Pengeluaran",
    "🔍 Perilaku Keuangan",
    "📈 Analisis Lanjutan",
    "🎲 Simulasi Monte Carlo",
])

# ══════════════════════════════════════════════
# TAB 1 – DEMOGRAFI & DISTRIBUSI
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<p class="section-title">👥 Distribusi Demografi</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div style="background: rgba(30, 41, 59, 0.6); padding: 20px; border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.2);">', unsafe_allow_html=True)
        st.markdown('<p style="color: #e0e7ff; font-weight: 700; margin-bottom: 12px;">🚹🚺 Gender Distribution</p>')
        gender_cnt = filtered["jenis_kelamin"].value_counts().reset_index()
        gender_cnt.columns = ["Gender", "Jumlah"]
        fig = px.pie(
            gender_cnt, names="Gender", values="Jumlah",
            color_discrete_sequence=WARNA_UTAMA, hole=0.5,
        )
        fig.update_traces(textfont_size=14, textinfo="percent+label", pull=[0.05, 0.05])
        fig.update_layout(showlegend=False, height=350)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="background: rgba(30, 41, 59, 0.6); padding: 20px; border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.2);">', unsafe_allow_html=True)
        st.markdown('<p style="color: #e0e7ff; font-weight: 700; margin-bottom: 12px;">💵 Uang Saku Bulanan</p>')
        uang_cnt = filtered["uang_saku"].value_counts().reindex(ORDER_UANG_SAKU, fill_value=0).reset_index()
        uang_cnt.columns = ["Range", "Jumlah"]
        fig2 = px.bar(
            uang_cnt, x="Range", y="Jumlah",
            color="Jumlah", color_continuous_scale="Viridis",
            text="Jumlah",
        )
        fig2.update_traces(textposition="outside", textfont_color=FONT_COLOR, 
                          marker=dict(line=dict(color=WARNA_PRIMER, width=2)))
        fig2.update_coloraxes(showscale=False)
        fig2.update_layout(height=350)
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Uang Saku vs Jenis Kelamin - Grouped Bar
    st.markdown('<p class="section-title">💰 Uang Saku Berdasarkan Gender</p>', unsafe_allow_html=True)
    cross = pd.crosstab(filtered["uang_saku"], filtered["jenis_kelamin"]).reindex(ORDER_UANG_SAKU, fill_value=0)
    fig3 = go.Figure()
    for i, col_name in enumerate(cross.columns):
        fig3.add_trace(go.Bar(
            name=col_name, x=cross.index, y=cross[col_name],
            marker_color=WARNA_UTAMA[i],
            text=cross[col_name], textposition="auto",
            hovertemplate=f"{col_name}<br>Jumlah: %{{y}}<extra></extra>",
        ))
    fig3.update_layout(
        barmode="group", 
        xaxis_title="Range Uang Saku", 
        yaxis_title="Jumlah Mahasiswa",
        height=450,
    )
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 2 – POLA PENGELUARAN
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-title">💸 Pola & Tren Pengeluaran</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div style="background: rgba(30, 41, 59, 0.6); padding: 20px; border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.2);">', unsafe_allow_html=True)
        st.markdown('<p style="color: #e0e7ff; font-weight: 700; margin-bottom: 12px;">📊 Total Pengeluaran</p>')
        tot_cnt = filtered["total_pengeluaran"].value_counts().reindex(ORDER_TOTAL_PENGELUARAN, fill_value=0).reset_index()
        tot_cnt.columns = ["Range", "Jumlah"]
        fig = px.bar(
            tot_cnt, x="Range", y="Jumlah",
            color="Jumlah", color_discrete_sequence=[WARNA_PRIMER, WARNA_SEKUNDER, WARNA_AKSEN, WARNA_PANAS],
            text="Jumlah",
        )
        fig.update_traces(textposition="outside", textfont_color=FONT_COLOR, showlegend=False)
        fig.update_layout(height=350)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="background: rgba(30, 41, 59, 0.6); padding: 20px; border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.2);">', unsafe_allow_html=True)
        st.markdown('<p style="color: #e0e7ff; font-weight: 700; margin-bottom: 12px;">🔥 Faktor Pembengkakan</p>')
        faktor_cnt = filtered["faktor_membengkak"].value_counts().reset_index()
        faktor_cnt.columns = ["Faktor", "Jumlah"]
        faktor_cnt["Faktor_short"] = faktor_cnt["Faktor"].str.extract(r'^([^(]+)').iloc[:, 0].str.strip()
        fig2 = px.bar(
            faktor_cnt, y="Faktor_short", x="Jumlah",
            orientation="h", color="Jumlah",
            color_continuous_scale="Viridis", text="Jumlah",
        )
        fig2.update_traces(textposition="outside", textfont_color=FONT_COLOR)
        fig2.update_coloraxes(showscale=False)
        fig2.update_layout(yaxis_title="", height=350)
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Breakdown kategori pengeluaran
    st.markdown('<p class="section-title">📦 Breakdown Kategori Pengeluaran</p>', unsafe_allow_html=True)
    col_makan = filtered["pengeluaran_makan"].value_counts()
    col_transport = filtered["pengeluaran_transport"].value_counts()
    col_hiburan = filtered["pengeluaran_hiburan"].value_counts()
    col_kuliah = filtered["pengeluaran_kuliah"].value_counts()

    breakdown_df = pd.DataFrame({
        "Makan 🍔": col_makan,
        "Transport 🚗": col_transport,
        "Hiburan 🎬": col_hiburan,
        "Kuliah 📚": col_kuliah,
    }).fillna(0).reset_index().rename(columns={"index": "Kategori"})
    
    breakdown_melt = breakdown_df.melt(id_vars="Kategori", var_name="Jenis", value_name="Jumlah")

    fig3 = px.bar(
        breakdown_melt, x="Kategori", y="Jumlah", color="Jenis",
        barmode="group", color_discrete_sequence=WARNA_UTAMA,
        text="Jumlah",
    )
    fig3.update_traces(textposition="outside", textfont_color=FONT_COLOR)
    fig3.update_layout(xaxis_title="Range Pengeluaran", yaxis_title="Jumlah Mahasiswa", height=450)
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    # Frekuensi belanja online
    st.markdown('<p class="section-title">🛍️ Frekuensi Belanja Online</p>', unsafe_allow_html=True)
    belanja_cnt = filtered["frekuensi_belanja_online"].value_counts().reset_index()
    belanja_cnt.columns = ["Frekuensi", "Jumlah"]
    fig4 = px.pie(
        belanja_cnt, names="Frekuensi", values="Jumlah",
        color_discrete_sequence=WARNA_UTAMA, hole=0.5,
    )
    fig4.update_traces(textfont_size=13, textinfo="percent+label", pull=[0.05, 0.05, 0.05])
    style_fig(fig4)
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.plotly_chart(fig4, use_container_width=True)
    with col_b:
        st.markdown("<div style='padding: 20px;'></div>", unsafe_allow_html=True)
        freq_tbl = belanja_cnt.copy()
        freq_tbl["Persentase"] = (freq_tbl["Jumlah"] / n * 100).round(1).astype(str) + "%"
        
        # Tampilkan dengan st.dataframe yang lebih modern
        st.markdown("""
        <div style='background: rgba(30, 41, 59, 0.6); padding: 16px; border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.2);'>
            <p style='color: #e0e7ff; font-weight: 700; margin-bottom: 12px;'>📊 Detail Statistik</p>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(freq_tbl, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════
# TAB 3 – PERILAKU KEUANGAN
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-title">💳 Perilaku & Kebiasaan Keuangan</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div style="background: rgba(30, 41, 59, 0.6); padding: 20px; border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.2);">', unsafe_allow_html=True)
        st.markdown('<p style="color: #e0e7ff; font-weight: 700; margin-bottom: 12px;'>⚠️ Pernah Kehabisan Uang?</p>')
        kh_cnt = filtered["kehabisan_uang"].value_counts().reset_index()
        kh_cnt.columns = ["Status", "Jumlah"]
        fig = px.pie(kh_cnt, names="Status", values="Jumlah", hole=0.5,
                     color="Status",
                     color_discrete_map={"Ya": WARNA_PANAS, "Tidak": WARNA_SUCESS})
        fig.update_traces(textfont_size=14, textinfo="percent+label", pull=[0.05, 0.05])
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="background: rgba(30, 41, 59, 0.6); padding: 20px; border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.2);">', unsafe_allow_html=True)
        st.markdown('<p style="color: #e0e7ff; font-weight: 700; margin-bottom: 12px;'>📒 Melakukan Budgeting?</p>')
        bd_cnt = filtered["budgeting"].value_counts().reset_index()
        bd_cnt.columns = ["Status", "Jumlah"]
        fig2 = px.pie(bd_cnt, names="Status", values="Jumlah", hole=0.5,
                      color="Status",
                      color_discrete_map={"Ya": WARNA_PRIMER, "Tidak": WARNA_PERINGATAN})
        fig2.update_traces(textfont_size=14, textinfo="percent+label", pull=[0.05, 0.05])
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Hubungan Budgeting vs Kehabisan Uang
    st.markdown('<p class="section-title">📊 Korelasi: Budgeting vs Kehabisan Uang</p>', unsafe_allow_html=True)
    cross_bk = pd.crosstab(filtered["budgeting"], filtered["kehabisan_uang"])
    cross_bk_pct = (cross_bk.div(cross_bk.sum(axis=1), axis=0) * 100).round(1)

    fig3 = go.Figure()
    colors_map = {"Ya": WARNA_PANAS, "Tidak": WARNA_SUCESS}
    for col_name in cross_bk_pct.columns:
        fig3.add_trace(go.Bar(
            name=f"Kehabisan: {col_name}",
            x=cross_bk_pct.index,
            y=cross_bk_pct[col_name],
            marker_color=colors_map.get(col_name, WARNA_UTAMA[0]),
            text=cross_bk_pct[col_name].map(lambda v: f"{v:.1f}%"),
            textposition="inside",
            hovertemplate=f"%{{x}}<br>Persentase: %{{y:.1f}}%<extra></extra>",
        ))
    fig3.update_layout(
        barmode="stack",
        xaxis_title="Melakukan Budgeting",
        yaxis_title="Persentase (%)",
        height=450,
    )
    style_fig(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    # Kehabisan uang per uang saku
    st.markdown('<p class="section-title">💰 Risiko Kehabisan Uang per Range Uang Saku</p>', unsafe_allow_html=True)
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
            hovertemplate=f"%{{x}}<br>Persentase: %{{y:.1f}}%<extra></extra>",
        ))
    fig4.update_layout(
        barmode="stack",
        xaxis_title="Range Uang Saku",
        yaxis_title="Persentase (%)",
        height=450,
    )
    style_fig(fig4)
    st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 4 – ANALISIS LANJUTAN
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-title">📋 Tabel Frekuensi Lengkap</p>', unsafe_allow_html=True)
    
    col_select = st.selectbox("🔍 Pilih Variabel:", [
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
            color="Frekuensi", color_continuous_scale="Viridis",
            text="Persentase",
        )
        fig_f.update_traces(textposition="outside", textfont_color=FONT_COLOR)
        fig_f.update_coloraxes(showscale=False)
        style_fig(fig_f)
        st.plotly_chart(fig_f, use_container_width=True)
    
    with col_t:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.1)); 
                    padding: 20px; border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.3);
                    margin-bottom: 16px;'>
            <div style='color: #a5b4fc; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;'>Modus</div>
            <div style='color: #e0e7ff; font-size: 1.2rem; font-weight: 700; margin-top: 4px;'>{modus_val}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background: rgba(30, 41, 59, 0.6); padding: 16px; border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.2);'>
            <div style='color: #94a3b8; font-size: 0.85rem;'>Total Responden</div>
            <div style='color: #e0e7ff; font-size: 1.5rem; font-weight: 700; margin-top: 4px;'>{n}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(freq_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Heatmap Korelasi
    st.markdown('<p class="section-title">🔥 Heatmap Asosiasi (Cramér\'s V)</p>', unsafe_allow_html=True)

    from scipy.stats import chi2_contingency

    cat_cols = [
        "uang_saku", "total_pengeluaran", "pengeluaran_makan",
        "pengeluaran_transport", "pengeluaran_hiburan", "pengeluaran_kuliah",
        "kehabisan_uang", "budgeting", "faktor_membengkak",
        "frekuensi_belanja_online", "jenis_kelamin",
    ]
    
    cat_labels = [
        "Uang Saku", "Total Pengeluaran", "Makan",
        "Transport", "Hiburan", "Kuliah",
        "Kehabisan", "Budgeting", "Faktor Membengkak",
        "Belanja Online", "Gender",
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
            colorscale="Viridis",
            zmin=0, zmax=1,
            text=np.round(matrix, 2),
            texttemplate="%{text}",
            textfont={"size": 9},
            hovertemplate="X: %{x}<br>Y: %{y}<br>Nilai: %{z:.2f}<extra></extra>",
        ))
        fig_heat.update_layout(
            height=600,
            xaxis=dict(tickangle=-45),
        )
        style_fig(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True)
        st.caption("💡 **Cramér's V**: 0 = tidak ada asosiasi, 1 = asosiasi sempurna")
    else:
        st.warning("⚠️ Data terlalu sedikit untuk menghitung Cramér's V. Hapus filter untuk melihat heatmap.")

    st.markdown("---")

    # Tabel data mentah
    st.markdown('<p class="section-title">📄 Data Mentah (Filtered)</p>', unsafe_allow_html=True)
    with st.expander("🔓 Klik untuk melihat data"):
        st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download CSV",
            data=csv,
            file_name="data_filtered_gen_z.csv",
            mime="text/csv",
        )

# ══════════════════════════════════════════════
# TAB 5 – SIMULASI MONTE CARLO (ENHANCED)
# ══════════════════════════════════════════════
with tab5:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h2 style='color: #e0e7ff; font-size: 2rem; margin: 0;'>🎲 Simulasi Monte Carlo</h2>
        <p style='color: #94a3b8; margin: 8px 0;'>Prediksi Risiko Keuangan dengan 10,000 Iterasi</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        sim_uang_saku = st.selectbox("💵 Pilih Range Uang Saku:", ORDER_UANG_SAKU, index=1)
    with col_sim2:
        sim_budgeting = st.selectbox("📒 Budgeting?", ["Ya", "Tidak"])
    
    if st.button("🚀 Jalankan Simulasi", type="primary", use_container_width=True):
        with st.spinner("🔄 Running 10,000 simulations..."):
            n_sim = 10000
            
            # Ambil data referensi
            ref_data = filtered[(filtered["uang_saku"] == sim_uang_saku) & (filtered["budgeting"] == sim_budgeting)]
            
            if len(ref_data) < 5:
                ref_data = filtered[filtered["uang_saku"] == sim_uang_saku]
            if len(ref_data) < 5:
                ref_data = filtered 
            
            # Fungsi mapping
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
            
            # Jalankan simulasi
            sampled_us = np.random.choice(ref_data["uang_saku"].values, size=n_sim)
            sampled_exp = np.random.choice(ref_data["total_pengeluaran"].values, size=n_sim)
            sampled_khabis = np.random.choice(ref_data["kehabisan_uang"].values, size=n_sim)
            
            vals_us = map_to_numeric(pd.Series(sampled_us), "uang_saku")
            vals_exp = map_to_numeric(pd.Series(sampled_exp), "pengeluaran")
            sisa_uang = vals_us - vals_exp
            
            # Hitung metrik
            prob_khabis = np.mean(sampled_khabis == "Ya") * 100
            mean_sisa = np.mean(sisa_uang)
            risk_sisa_negatif = np.mean(sisa_uang < 0) * 100
            p5_sisa = np.percentile(sisa_uang, 5)
            p95_sisa = np.percentile(sisa_uang, 95)
            median_sisa = np.median(sisa_uang)
            
            overall_khabis = np.mean(filtered["kehabisan_uang"] == "Ya") * 100
            delta_khabis = prob_khabis - overall_khabis
            
            # KPI Metrics dengan style modern
            st.markdown('<p class="section-title">📊 Hasil Simulasi</p>', unsafe_allow_html=True)
            
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            
            with kpi1:
                color_class = "badge-high" if prob_khabis > 50 else ("badge-medium" if prob_khabis > 30 else "badge-low")
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(244, 63, 94, 0.2), rgba(251, 113, 133, 0.1)); 
                            padding: 20px; border-radius: 16px; border: 1px solid rgba(244, 63, 94, 0.3);
                            text-align: center;'>
                    <div style='font-size: 2rem; font-weight: 800; color: #e0e7ff;'>{prob_khabis:.1f}%</div>
                    <div style='color: #fca5a5; font-size: 0.85rem; margin-top: 4px;'>Risiko Kehabisan</div>
                    <span class='badge {color_class}' style='margin-top: 8px;'>{delta_khabis:+.1f}% vs avg</span>
                </div>
                """, unsafe_allow_html=True)
            
            with kpi2:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(52, 211, 153, 0.1)); 
                            padding: 20px; border-radius: 16px; border: 1px solid rgba(16, 185, 129, 0.3);
                            text-align: center;'>
                    <div style='font-size: 2rem; font-weight: 800; color: #e0e7ff;'>Rp {mean_sisa:,.0f}</div>
                    <div style='color: #6ee7b7; font-size: 0.85rem; margin-top: 4px;'>Rata-rata Sisa</div>
                </div>
                """, unsafe_allow_html=True)
            
            with kpi3:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(251, 191, 36, 0.1)); 
                            padding: 20px; border-radius: 16px; border: 1px solid rgba(245, 158, 11, 0.3);
                            text-align: center;'>
                    <div style='font-size: 2rem; font-weight: 800; color: #e0e7ff;'>{risk_sisa_negatif:.1f}%</div>
                    <div style='color: #fcd34d; font-size: 0.85rem; margin-top: 4px;'>Risiko Defisit</div>
                </div>
                """, unsafe_allow_html=True)
            
            with kpi4:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.1)); 
                            padding: 20px; border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.3);
                            text-align: center;'>
                    <div style='font-size: 2rem; font-weight: 800; color: #e0e7ff;'>Rp {median_sisa:,.0f}</div>
                    <div style='color: #a5b4fc; font-size: 0.85rem; margin-top: 4px;'>Median Sisa</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Visualisasi Distribution
            st.markdown('<p class="section-title">📈 Distribusi Sisa Uang (10,000 Simulasi)</p>', unsafe_allow_html=True)
            
            df_sim = pd.DataFrame({"Sisa Uang": sisa_uang})
            
            # Histogram dengan KDE
            fig_sim = make_subplots(rows=2, cols=1, 
                                   shared_xaxes=True, 
                                   vertical_spacing=0.05,
                                   row_heights=[0.7, 0.3])
            
            # Histogram
            fig_sim.add_trace(
                go.Histogram(x=sisa_uang, nbinsx=60, 
                           name="Distribusi",
                           marker_color=WARNA_PRIMER,
                           opacity=0.7,
                           hovertemplate="Range: %{x:.0f}<br>Frekuensi: %{y}<extra></extra>"),
                row=1, col=1
            )
            
            # KDE line
            from scipy.stats import gaussian_kde
            kde = gaussian_kde(sisa_uang)
            x_kde = np.linspace(min(sisa_uang), max(sisa_uang), 200)
            y_kde = kde(x_kde) * len(sisa_uang) * (max(sisa_uang) - min(sisa_uang)) / 60
            
            fig_sim.add_trace(
                go.Scatter(x=x_kde, y=y_kde, 
                          name="Density Curve",
                          line=dict(color=WARNA_SEKUNDER, width=3),
                          hovertemplate="Nilai: %{x:.0f}<br>Density: %{y:.0f}<extra></extra>"),
                row=1, col=1
            )
            
            # Box plot
            fig_sim.add_trace(
                go.Box(y=sisa_uang, name="Box Plot", 
                      marker_color=WARNA_AKSEN,
                      hovertemplate="Min: %{ymin:.0f}<br>Q1: %{q1:.0f}<br>Median: %{median:.0f}<br>Q3: %{q3:.0f}<br>Max: %{ymax:.0f}<extra></extra>"),
                row=2, col=1
            )
            
            # Garis vertikal di 0
            fig_sim.add_vline(x=0, line_dash="dash", line_color=WARNA_PANAS, 
                            annotation_text="🚨 Titik Impas", 
                            annotation_position="top",
                            row=1, col=1)
            
            fig_sim.update_layout(
                height=600,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode="x unified",
            )
            
            fig_sim.update_xaxes(title_text="Sisa Uang (Rp)", row=2, col=1)
            fig_sim.update_yaxes(title_text="Frekuensi", row=1, col=1)
            fig_sim.update_yaxes(title_text="Nilai", row=2, col=1)
            
            style_fig(fig_sim)
            st.plotly_chart(fig_sim, use_container_width=True)
            
            # Gauge chart untuk risk level
            st.markdown('<p class="section-title">🎯 Risk Level Indicator</p>', unsafe_allow_html=True)
            
            col_g1, col_g2 = st.columns(2)
            
            with col_g1:
                # Gauge untuk probabilitas kehabisan
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=prob_khabis,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Risk Level Kehabisan Uang", 'font': {'size': 16, 'color': FONT_COLOR}},
                    delta={'reference': overall_khabis, 'increasing': {'color': WARNA_PANAS}, 'decreasing': {'color': WARNA_SUCESS}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': GRID_COLOR, 'tickfont': {'color': FONT_COLOR}},
                        'bar': {'color': WARNA_PRIMER},
                        'bgcolor': BG_PLOT,
                        'borderwidth': 2,
                        'bordercolor': GRID_COLOR,
                        'steps': [
                            {'range': [0, 30], 'color': 'rgba(16, 185, 129, 0.3)'},
                            {'range': [30, 60], 'color': 'rgba(245, 158, 11, 0.3)'},
                            {'range': [60, 100], 'color': 'rgba(244, 63, 94, 0.3)'}
                        ],
                    }
                ))
                style_fig(fig_gauge)
                fig_gauge.update_layout(height=300)
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with col_g2:
                # Gauge untuk risiko defisit
                fig_gauge2 = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=risk_sisa_negatif,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Risiko Defisit Bulanan", 'font': {'size': 16, 'color': FONT_COLOR}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': GRID_COLOR, 'tickfont': {'color': FONT_COLOR}},
                        'bar': {'color': WARNA_SEKUNDER},
                        'bgcolor': BG_PLOT,
                        'borderwidth': 2,
                        'bordercolor': GRID_COLOR,
                        'steps': [
                            {'range': [0, 30], 'color': 'rgba(16, 185, 129, 0.3)'},
                            {'range': [30, 60], 'color': 'rgba(245, 158, 11, 0.3)'},
                            {'range': [60, 100], 'color': 'rgba(244, 63, 94, 0.3)'}
                        ],
                    }
                ))
                style_fig(fig_gauge2)
                fig_gauge2.update_layout(height=300)
                st.plotly_chart(fig_gauge2, use_container_width=True)
            
            # Insight box
            st.markdown("---")
            st.markdown('<p class="section-title">💡 Insight & Rekomendasi</p>', unsafe_allow_html=True)
            
            risk_level = "🔴 HIGH" if prob_khabis > 50 else ("🟡 MEDIUM" if prob_khabis > 30 else "🟢 LOW")
            
            insight_text = f"""
            <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.15)); 
                        padding: 24px; border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.4);
                        color: #e0e7ff; line-height: 1.8;'>
                
                <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 16px;'>
                    <span style='font-size: 2rem;'>📊</span>
                    <h3 style='margin: 0; color: #e0e7ff;'>Analisis Profil Keuangan</h3>
                </div>
                
                <p><strong>Profil:</strong> Uang Saku <strong>{sim_uang_saku}</strong> | Budgeting: <strong>{sim_budgeting}</strong></p>
                
                <p><strong>Risk Level:</strong> <span style='font-size: 1.2rem;'>{risk_level}</span></p>
                
                <ul style='padding-left: 20px; margin: 16px 0;'>
                    <li>📉 Probabilitas kehabisan uang: <strong>{prob_khabis:.1f}%</strong> ({delta_khabis:+.1f}% dari rata-rata)</li>
                    <li>💰 Rata-rata sisa uang: <strong>Rp {mean_sisa:,.0f}</strong> (Median: Rp {median_sisa:,.0f})</li>
                    <li>⚠️ Risiko defisit (pengeluaran > pemasukan): <strong>{risk_sisa_negatif:.1f}%</strong></li>
                    <li>📊 90% Confidence Interval: <strong>Rp {p5_sisa:,.0f} - Rp {p95_sisa:,.0f}</strong></li>
                </ul>
                
                <div style='background: rgba(30, 41, 59, 0.6); padding: 16px; border-radius: 12px; margin-top: 16px; border-left: 4px solid {WARNA_PRIMER};'>
                    <strong>💡 Rekomendasi:</strong><br>
                    {f"❗ Risiko kehabisan uang cukup tinggi. Pertimbangkan untuk:<br>   • Membuat budgeting yang lebih ketat<br>   • Mengurangi pengeluaran hiburan<br>   • Mencari sumber pemasukan tambahan" if prob_khabis > 40 else 
                     "✅ Profil keuangan cukup stabil. Pertahankan pola pengeluaran saat ini dan terus lakukan budgeting!" if sim_budgeting == "Ya" else 
                     "💡 Mulai terapkan budgeting untuk mengoptimalkan pengelolaan keuangan!"}
                </div>
            </div>
            """
            st.markdown(insight_text, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 24px 0;'>
    <p style='color: #475569; font-size: 0.85rem; margin: 0;'>
        Made with 💜 for Gen Z | Dashboard Analisis Keuangan Mahasiswa
    </p>
    <p style='color: #64748b; font-size: 0.75rem; margin: 8px 0 0 0;'>
        Sains Data · 2026 · Data-Driven Decision Making
    </p>
</div>
""", unsafe_allow_html=True)
