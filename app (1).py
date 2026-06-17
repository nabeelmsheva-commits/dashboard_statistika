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
    page_title="FinScope · Analisis Keuangan Mahasiswa",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
# ─────────────────────────────────────────────
# DESIGN SYSTEM & CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
 
    /* ─── Base ─── */
    html, body, .stApp {
        background-color: #080C14;
        font-family: 'Space Grotesk', sans-serif;
    }
 
    /* ─── Subtle grid pattern on background ─── */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(99,102,241,.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(99,102,241,.04) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
    }
 
    /* ─── Sidebar ─── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1220 0%, #080C14 100%);
        border-right: 1px solid rgba(99,102,241,0.2);
    }
    [data-testid="stSidebar"] * { color: #CBD5E1; font-family: 'Space Grotesk', sans-serif; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label { color: #94A3B8 !important; font-size: 0.78rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; }
 
    /* Sidebar selectbox */
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
        background: rgba(99,102,241,0.08) !important;
        border: 1px solid rgba(99,102,241,0.25) !important;
        border-radius: 8px !important;
        color: #E2E8F0 !important;
    }
 
    /* ─── Metric cards ─── */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(13,18,32,0.9) 100%);
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 16px;
        padding: 20px 22px;
        position: relative;
        overflow: hidden;
        transition: border-color .2s;
    }
    [data-testid="metric-container"]::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #6366F1, #22D3EE);
        border-radius: 16px 16px 0 0;
    }
    [data-testid="metric-container"]:hover { border-color: rgba(99,102,241,0.5); }
    [data-testid="metric-container"] label {
        color: #64748B !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: .08em !important;
    }
    [data-testid="stMetricValue"] {
        color: #F1F5F9 !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    [data-testid="stMetricDelta"] { font-size: 0.8rem !important; }
 
    /* ─── Tabs ─── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(13,18,32,0.8);
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: 12px;
        padding: 5px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #64748B;
        border-radius: 9px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
        font-size: 0.88rem;
        padding: 8px 18px;
        transition: all .2s;
    }
    .stTabs [data-baseweb="tab"]:hover { color: #A5B4FC; background: rgba(99,102,241,0.08); }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366F1, #4F46E5) !important;
        color: #fff !important;
        box-shadow: 0 4px 15px rgba(99,102,241,0.4);
    }
 
    /* ─── Section titles ─── */
    .section-title {
        color: #CBD5E1;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .1em;
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 24px 0 14px 0;
    }
    .section-title::before {
        content: '';
        display: inline-block;
        width: 3px;
        height: 16px;
        background: linear-gradient(180deg, #6366F1, #22D3EE);
        border-radius: 2px;
    }
 
    /* ─── Insight cards ─── */
    .insight-card {
        background: linear-gradient(135deg, rgba(34,211,238,0.07), rgba(13,18,32,0.95));
        border: 1px solid rgba(34,211,238,0.2);
        border-radius: 14px;
        padding: 18px 22px;
        margin: 10px 0;
        font-size: 0.9rem;
        color: #CBD5E1;
        line-height: 1.7;
    }
    .insight-card strong { color: #67E8F9; }
    .insight-card .badge {
        display: inline-block;
        background: rgba(34,211,238,0.15);
        color: #67E8F9;
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 0.78rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
    }
 
    /* ─── Warning card ─── */
    .warn-card {
        background: linear-gradient(135deg, rgba(244,63,94,0.08), rgba(13,18,32,0.95));
        border: 1px solid rgba(244,63,94,0.25);
        border-radius: 14px;
        padding: 18px 22px;
        margin: 10px 0;
        color: #FDA4AF;
        font-size: 0.9rem;
        line-height: 1.7;
    }
 
    /* ─── Dividers ─── */
    hr { border: none; border-top: 1px solid rgba(99,102,241,0.15); margin: 28px 0; }
 
    /* ─── Dataframe ─── */
    .stDataFrame { border: 1px solid rgba(99,102,241,0.2); border-radius: 10px; overflow: hidden; }
    .stDataFrame [data-testid="stDataFrameResizable"] { background: #0D1220; }
 
    /* ─── Buttons ─── */
    .stButton button {
        background: linear-gradient(135deg, #6366F1, #4F46E5);
        color: white;
        border: none;
        border-radius: 10px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        padding: 10px 28px;
        font-size: 0.92rem;
        box-shadow: 0 4px 20px rgba(99,102,241,0.35);
        transition: all .2s;
    }
    .stButton button:hover {
        box-shadow: 0 6px 28px rgba(99,102,241,0.5);
        transform: translateY(-1px);
    }
 
    /* ─── Download button ─── */
    .stDownloadButton button {
        background: rgba(99,102,241,0.12);
        color: #A5B4FC;
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 8px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
    }
 
    /* ─── Selectbox & inputs ─── */
    .stSelectbox [data-baseweb="select"] > div {
        background: rgba(13,18,32,0.8) !important;
        border: 1px solid rgba(99,102,241,0.25) !important;
        border-radius: 10px !important;
        color: #E2E8F0 !important;
    }
    .stSelectbox label { color: #64748B !important; font-size: 0.78rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: .06em !important; }
 
    /* ─── Spinner ─── */
    .stSpinner > div { border-top-color: #6366F1 !important; }
 
    /* ─── Expander ─── */
    .streamlit-expanderHeader {
        background: rgba(13,18,32,0.6) !important;
        border: 1px solid rgba(99,102,241,0.2) !important;
        border-radius: 10px !important;
        color: #94A3B8 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
 
    /* ─── Caption ─── */
    .stCaption { color: #475569 !important; font-size: 0.78rem !important; }
 
    /* ─── Info box ─── */
    .stInfo { background: rgba(34,211,238,0.07) !important; border: 1px solid rgba(34,211,238,0.2) !important; border-radius: 12px !important; color: #CBD5E1 !important; }
 
    /* ─── Warning ─── */
    .stWarning { background: rgba(245,158,11,0.08) !important; border: 1px solid rgba(245,158,11,0.25) !important; border-radius: 12px !important; }
 
    /* Remove default streamlit padding weirdness */
    .block-container { padding-top: 2rem !important; }
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
# DESIGN TOKENS
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
 
PALETTE   = ["#6366F1", "#22D3EE", "#F59E0B", "#10B981", "#F43F5E", "#A78BFA", "#FB7185", "#34D399"]
BG_PLOT   = "#0D1220"
PAPER_BG  = "#080C14"
FONT_CLR  = "#CBD5E1"
GRID_CLR  = "rgba(99,102,241,0.1)"
ACCENT    = "#6366F1"
CYAN      = "#22D3EE"
RED       = "#F43F5E"
GREEN     = "#10B981"
 
def style_fig(fig, height=380):
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=BG_PLOT,
        font=dict(color=FONT_CLR, family="Space Grotesk, sans-serif", size=12),
        margin=dict(t=44, b=24, l=16, r=16),
        height=height,
        legend=dict(
            bgcolor="rgba(13,18,32,0.8)",
            bordercolor="rgba(99,102,241,0.2)",
            borderwidth=1,
            font=dict(size=11),
        ),
    )
    fig.update_xaxes(
        gridcolor=GRID_CLR, zerolinecolor=GRID_CLR,
        tickfont=dict(size=11), linecolor="rgba(99,102,241,0.15)"
    )
    fig.update_yaxes(
        gridcolor=GRID_CLR, zerolinecolor=GRID_CLR,
        tickfont=dict(size=11), linecolor="rgba(99,102,241,0.15)"
    )
    return fig
 
# ─────────────────────────────────────────────
# SIDEBAR – FILTER
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 20px 0;">
        <div style="font-size:1.25rem; font-weight:700; color:#E2E8F0; letter-spacing:-.02em;">
            📊 FinScope
        </div>
        <div style="font-size:0.72rem; color:#475569; margin-top:3px; text-transform:uppercase; letter-spacing:.1em;">
            Financial Analytics
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown('<div style="font-size:0.7rem;color:#475569;font-weight:600;text-transform:uppercase;letter-spacing:.1em;margin-bottom:12px;">Filter Data</div>', unsafe_allow_html=True)
 
    gender_options = ["Semua"] + sorted(df["jenis_kelamin"].unique().tolist())
    gender_filter = st.selectbox("Jenis Kelamin", gender_options)
 
    uang_saku_options = ["Semua"] + ORDER_UANG_SAKU
    uang_saku_filter = st.selectbox("Uang Saku", uang_saku_options)
 
    kehabisan_options = ["Semua", "Ya", "Tidak"]
    kehabisan_filter = st.selectbox("Pernah Kehabisan Uang", kehabisan_options)
 
    budgeting_options = ["Semua", "Ya", "Tidak"]
    budgeting_filter = st.selectbox("Melakukan Budgeting", budgeting_options)
 
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);border-radius:10px;padding:14px;">
        <div style="font-size:0.7rem;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px;">Dataset Info</div>
        <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
            <span style="color:#64748B;font-size:0.82rem;">Total Responden</span>
            <span style="color:#A5B4FC;font-weight:600;font-size:0.82rem;font-family:'JetBrains Mono',monospace">{len(df)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;">
            <span style="color:#64748B;font-size:0.82rem;">Sumber</span>
            <span style="color:#A5B4FC;font-weight:600;font-size:0.82rem;">Survei 2026</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("""
    <div style="margin-top:20px;padding:12px;border-radius:10px;background:rgba(34,211,238,0.06);border:1px solid rgba(34,211,238,0.15);">
        <div style="font-size:0.7rem;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;">Dibuat oleh</div>
        <div style="color:#CBD5E1;font-size:0.82rem;font-weight:600;">Muhammad Sheva Nabeel</div>
        <div style="color:#475569;font-size:0.75rem;margin-top:2px;">Sains Data · 60125001</div>
    </div>
    """, unsafe_allow_html=True)
 
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
<div style="margin-bottom:28px;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
        <div style="width:32px;height:32px;background:linear-gradient(135deg,#6366F1,#22D3EE);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1rem;">📊</div>
        <h1 style="color:#F1F5F9;font-size:1.6rem;font-weight:700;margin:0;letter-spacing:-.03em;font-family:'Space Grotesk',sans-serif;">
            Dashboard Analisis Keuangan Mahasiswa
        </h1>
    </div>
    <p style="color:#475569;margin:0 0 0 44px;font-size:0.88rem;font-family:'Space Grotesk',sans-serif;">
        Pola pengeluaran · Perilaku keuangan · Simulasi risiko berbasis data survei Mei–Juni 2026
    </p>
</div>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
pct_kehabisan    = round(filtered[filtered["kehabisan_uang"] == "Ya"].shape[0] / n * 100, 1) if n else 0
pct_budgeting    = round(filtered[filtered["budgeting"] == "Ya"].shape[0] / n * 100, 1) if n else 0
pct_belanja_sering = round(filtered[filtered["frekuensi_belanja_online"] == "3 kali atau lebih"].shape[0] / n * 100, 1) if n else 0
modus_pengeluaran = filtered["total_pengeluaran"].mode()[0] if n else "-"
 
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("👥 Responden",         f"{n} orang")
k2.metric("⚠️ Kehabisan Uang",    f"{pct_kehabisan}%",
          delta="Risiko sistemik" if pct_kehabisan > 35 else "Terkendali",
          delta_color="inverse" if pct_kehabisan > 35 else "normal")
k3.metric("📒 Pakai Budgeting",   f"{pct_budgeting}%")
k4.metric("🛒 Belanja Online ≥3x", f"{pct_belanja_sering}%")
k5.metric("💸 Pengeluaran Utama", modus_pengeluaran.replace("Rp ", "Rp\u00A0"))
 
st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
# TAB NAVIGASI
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📐 Demografi",
    "💳 Pengeluaran",
    "🔍 Perilaku Keuangan",
    "📈 Analisis Lanjutan",
    "🎲 Monte Carlo",
])
 
# ══════════════════════════════════════════════
# TAB 1 – DEMOGRAFI & DISTRIBUSI
# ══════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns(2)
 
    with col1:
        st.markdown('<p class="section-title">Distribusi Jenis Kelamin</p>', unsafe_allow_html=True)
        gender_cnt = filtered["jenis_kelamin"].value_counts().reset_index()
        gender_cnt.columns = ["Jenis Kelamin", "Jumlah"]
        fig = px.pie(gender_cnt, names="Jenis Kelamin", values="Jumlah",
                     color_discrete_sequence=PALETTE, hole=0.55)
        fig.update_traces(textfont_size=12, textinfo="percent+label",
                          marker=dict(line=dict(color=PAPER_BG, width=2)))
        fig.update_layout(showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
 
    with col2:
        st.markdown('<p class="section-title">Distribusi Uang Saku Bulanan</p>', unsafe_allow_html=True)
        uang_cnt = filtered["uang_saku"].value_counts().reindex(ORDER_UANG_SAKU, fill_value=0).reset_index()
        uang_cnt.columns = ["Uang Saku", "Jumlah"]
        fig2 = px.bar(uang_cnt, x="Uang Saku", y="Jumlah",
                      color="Jumlah", color_continuous_scale=[[0,"#1e1b4b"],[1,"#6366F1"]],
                      text="Jumlah")
        fig2.update_traces(textposition="outside", textfont_color=FONT_CLR,
                           marker_line_width=0)
        fig2.update_coloraxes(showscale=False)
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)
 
    st.markdown('<p class="section-title">Uang Saku Berdasarkan Jenis Kelamin</p>', unsafe_allow_html=True)
    cross = pd.crosstab(filtered["uang_saku"], filtered["jenis_kelamin"]).reindex(ORDER_UANG_SAKU, fill_value=0)
    fig3 = go.Figure()
    for i, col_name in enumerate(cross.columns):
        fig3.add_trace(go.Bar(
            name=col_name, x=cross.index, y=cross[col_name],
            marker=dict(color=PALETTE[i], line=dict(width=0)),
            text=cross[col_name], textposition="auto",
        ))
    fig3.update_layout(barmode="group", xaxis_title="Uang Saku", yaxis_title="Jumlah",
                       bargap=0.2, bargroupgap=0.05)
    style_fig(fig3, height=340)
    st.plotly_chart(fig3, use_container_width=True)
 
    # Insight
    st.markdown(f"""
    <div class="insight-card">
        💡 <strong>Insight Demografi:</strong> Mayoritas responden <span class="badge">{round(filtered[filtered["uang_saku"]=="Rp 500.000 - Rp 1.000.000"].shape[0]/n*100,1) if n else 0}%</span>
        berada di rentang uang saku Rp 500rb–Rp 1jt per bulan.
        Perempuan mendominasi sampel dengan proporsi lebih tinggi.
    </div>
    """, unsafe_allow_html=True)
 
# ══════════════════════════════════════════════
# TAB 2 – POLA PENGELUARAN
# ══════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns(2)
 
    with col1:
        st.markdown('<p class="section-title">Total Pengeluaran Bulanan</p>', unsafe_allow_html=True)
        tot_cnt = filtered["total_pengeluaran"].value_counts().reindex(ORDER_TOTAL_PENGELUARAN, fill_value=0).reset_index()
        tot_cnt.columns = ["Total Pengeluaran", "Jumlah"]
        fig = px.bar(tot_cnt, x="Total Pengeluaran", y="Jumlah",
                     color="Total Pengeluaran", color_discrete_sequence=PALETTE, text="Jumlah")
        fig.update_traces(textposition="outside", textfont_color=FONT_CLR,
                          showlegend=False, marker_line_width=0)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
 
    with col2:
        st.markdown('<p class="section-title">Faktor Pengeluaran Membengkak</p>', unsafe_allow_html=True)
        faktor_cnt = filtered["faktor_membengkak"].value_counts().reset_index()
        faktor_cnt.columns = ["Faktor", "Jumlah"]
        faktor_cnt["Faktor_short"] = faktor_cnt["Faktor"].str.extract(r'^([^(]+)').iloc[:, 0].str.strip()
        fig2 = px.bar(faktor_cnt, y="Faktor_short", x="Jumlah",
                      orientation="h",
                      color="Jumlah", color_continuous_scale=[[0,"#1e1b4b"],[0.5,"#6366F1"],[1,"#F43F5E"]],
                      text="Jumlah")
        fig2.update_traces(textposition="outside", textfont_color=FONT_CLR, marker_line_width=0)
        fig2.update_coloraxes(showscale=False)
        fig2.update_layout(yaxis_title="")
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)
 
    # Radar chart kategori pengeluaran
    st.markdown('<p class="section-title">Profil Pengeluaran per Kategori</p>', unsafe_allow_html=True)
    col_makan     = filtered["pengeluaran_makan"].value_counts()
    col_transport = filtered["pengeluaran_transport"].value_counts()
    col_hiburan   = filtered["pengeluaran_hiburan"].value_counts()
    col_kuliah    = filtered["pengeluaran_kuliah"].value_counts()
 
    all_cats = sorted(set(col_makan.index) | set(col_transport.index) | set(col_hiburan.index) | set(col_kuliah.index))
    breakdown_df = pd.DataFrame({
        "Makan": col_makan, "Transport": col_transport,
        "Hiburan": col_hiburan, "Kuliah": col_kuliah,
    }).fillna(0).reset_index().rename(columns={"index": "Kategori"})
    breakdown_melt = breakdown_df.melt(id_vars="Kategori", var_name="Jenis", value_name="Jumlah")
 
    fig3 = px.bar(breakdown_melt, x="Kategori", y="Jumlah", color="Jenis",
                  barmode="group", color_discrete_sequence=PALETTE, text="Jumlah")
    fig3.update_traces(textposition="outside", textfont_color=FONT_CLR, marker_line_width=0)
    fig3.update_layout(xaxis_title="Range Pengeluaran", yaxis_title="Jumlah Mahasiswa",
                       bargap=0.18, bargroupgap=0.04)
    style_fig(fig3, height=360)
    st.plotly_chart(fig3, use_container_width=True)
 
    # Frekuensi belanja online
    st.markdown('<p class="section-title">Frekuensi Belanja Online</p>', unsafe_allow_html=True)
    belanja_cnt = filtered["frekuensi_belanja_online"].value_counts().reset_index()
    belanja_cnt.columns = ["Frekuensi", "Jumlah"]
    col_a, col_b = st.columns([1, 2])
    with col_a:
        fig4 = px.pie(belanja_cnt, names="Frekuensi", values="Jumlah",
                      color_discrete_sequence=PALETTE, hole=0.55)
        fig4.update_traces(textfont_size=12, textinfo="percent+label",
                           marker=dict(line=dict(color=PAPER_BG, width=2)))
        style_fig(fig4)
        st.plotly_chart(fig4, use_container_width=True)
    with col_b:
        freq_tbl = belanja_cnt.copy()
        freq_tbl["Persentase (%)"] = (freq_tbl["Jumlah"] / n * 100).round(1)
        st.dataframe(freq_tbl, use_container_width=True, hide_index=True)
 
# ══════════════════════════════════════════════
# TAB 3 – PERILAKU KEUANGAN
# ══════════════════════════════════════════════
with tab3:
    col1, col2 = st.columns(2)
 
    with col1:
        st.markdown('<p class="section-title">Pernah Kehabisan Uang?</p>', unsafe_allow_html=True)
        kh_cnt = filtered["kehabisan_uang"].value_counts().reset_index()
        kh_cnt.columns = ["Status", "Jumlah"]
        fig = px.pie(kh_cnt, names="Status", values="Jumlah", hole=0.58,
                     color="Status",
                     color_discrete_map={"Ya": RED, "Tidak": GREEN})
        fig.update_traces(textfont_size=13, textinfo="percent+label",
                          marker=dict(line=dict(color=PAPER_BG, width=3)))
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)
 
    with col2:
        st.markdown('<p class="section-title">Melakukan Budgeting?</p>', unsafe_allow_html=True)
        bd_cnt = filtered["budgeting"].value_counts().reset_index()
        bd_cnt.columns = ["Status", "Jumlah"]
        fig2 = px.pie(bd_cnt, names="Status", values="Jumlah", hole=0.58,
                      color="Status",
                      color_discrete_map={"Ya": ACCENT, "Tidak": "#F59E0B"})
        fig2.update_traces(textfont_size=13, textinfo="percent+label",
                           marker=dict(line=dict(color=PAPER_BG, width=3)))
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)
 
    # Stacked bar: Budgeting vs Kehabisan
    st.markdown('<p class="section-title">Efek Budgeting terhadap Risiko Kehabisan Uang</p>', unsafe_allow_html=True)
    cross_bk = pd.crosstab(filtered["budgeting"], filtered["kehabisan_uang"])
    cross_bk_pct = (cross_bk.div(cross_bk.sum(axis=1), axis=0) * 100).round(1)
 
    fig3 = go.Figure()
    colors_map = {"Ya": RED, "Tidak": GREEN}
    for col_name in cross_bk_pct.columns:
        fig3.add_trace(go.Bar(
            name=f"Kehabisan: {col_name}",
            x=cross_bk_pct.index,
            y=cross_bk_pct[col_name],
            marker=dict(color=colors_map.get(col_name, ACCENT), line=dict(width=0)),
            text=cross_bk_pct[col_name].map(lambda v: f"{v:.1f}%"),
            textposition="inside", textfont=dict(size=13, color="white"),
        ))
    fig3.update_layout(barmode="stack", xaxis_title="Melakukan Budgeting",
                       yaxis_title="Persentase (%)", bargap=0.35)
    style_fig(fig3, height=320)
    st.plotly_chart(fig3, use_container_width=True)
 
    # Highlight
    no_budget_risk = cross_bk_pct.get("Ya", pd.Series()).get("Tidak", 0)
    yes_budget_risk = cross_bk_pct.get("Ya", pd.Series()).get("Ya", 0)
    delta = round(no_budget_risk - yes_budget_risk, 1)
    st.markdown(f"""
    <div class="insight-card">
        🔍 Mahasiswa yang <strong>tidak budgeting</strong> memiliki risiko kehabisan uang
        <span class="badge">{no_budget_risk:.1f}%</span> dibanding yang budgeting
        <span class="badge">{yes_budget_risk:.1f}%</span>.
        Selisih risiko: <strong>−{delta} poin persentase</strong> dengan budgeting aktif.
    </div>
    """, unsafe_allow_html=True)
 
    # Kehabisan uang per uang saku
    st.markdown('<p class="section-title">Risiko Kehabisan per Kelompok Uang Saku</p>', unsafe_allow_html=True)
    cross_us = pd.crosstab(filtered["uang_saku"], filtered["kehabisan_uang"]).reindex(ORDER_UANG_SAKU, fill_value=0)
    cross_us_pct = (cross_us.div(cross_us.sum(axis=1), axis=0) * 100).round(1)
 
    fig4 = go.Figure()
    for col_name in cross_us_pct.columns:
        fig4.add_trace(go.Bar(
            name=f"Kehabisan: {col_name}",
            x=cross_us_pct.index,
            y=cross_us_pct[col_name],
            marker=dict(color=colors_map.get(col_name, ACCENT), line=dict(width=0)),
            text=cross_us_pct[col_name].map(lambda v: f"{v:.1f}%"),
            textposition="inside", textfont=dict(size=13, color="white"),
        ))
    fig4.update_layout(barmode="stack", xaxis_title="Uang Saku",
                       yaxis_title="Persentase (%)", bargap=0.3)
    style_fig(fig4, height=320)
    st.plotly_chart(fig4, use_container_width=True)
 
# ══════════════════════════════════════════════
# TAB 4 – ANALISIS LANJUTAN
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-title">Tabel Frekuensi Variabel</p>', unsafe_allow_html=True)
    col_select = st.selectbox("Pilih Kolom:", [
        "uang_saku", "total_pengeluaran", "pengeluaran_makan",
        "pengeluaran_transport", "pengeluaran_hiburan", "pengeluaran_kuliah",
        "kehabisan_uang", "budgeting", "faktor_membengkak", "frekuensi_belanja_online",
        "jenis_kelamin",
    ])
 
    freq_df = filtered[col_select].value_counts().reset_index()
    freq_df.columns = ["Kategori", "Frekuensi"]
    freq_df["Persentase (%)"] = (freq_df["Frekuensi"] / n * 100).round(2)
    freq_df["Kumulatif"]  = freq_df["Frekuensi"].cumsum()
    modus_val = freq_df.iloc[0]["Kategori"]
 
    col_m, col_t = st.columns([2, 1])
    with col_m:
        fig_f = px.bar(freq_df, x="Kategori", y="Frekuensi",
                       color="Frekuensi",
                       color_continuous_scale=[[0,"#1e1b4b"],[1,"#6366F1"]],
                       text="Persentase (%)")
        fig_f.update_traces(texttemplate="%{text:.1f}%", textposition="outside",
                            textfont_color=FONT_CLR, marker_line_width=0)
        fig_f.update_coloraxes(showscale=False)
        style_fig(fig_f, height=360)
        st.plotly_chart(fig_f, use_container_width=True)
    with col_t:
        st.markdown(f"""
        <div style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);border-radius:12px;padding:16px;margin-bottom:12px;">
            <div style="font-size:0.7rem;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:.08em;">Modus</div>
            <div style="color:#A5B4FC;font-weight:700;font-size:0.95rem;margin-top:4px;font-family:'JetBrains Mono',monospace;">{modus_val}</div>
        </div>
        <div style="background:rgba(34,211,238,0.06);border:1px solid rgba(34,211,238,0.15);border-radius:12px;padding:16px;">
            <div style="font-size:0.7rem;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:.08em;">N Filtered</div>
            <div style="color:#67E8F9;font-weight:700;font-size:1.1rem;margin-top:4px;font-family:'JetBrains Mono',monospace;">{n}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
        st.dataframe(freq_df, use_container_width=True, hide_index=True)
 
    st.markdown("<hr>", unsafe_allow_html=True)
 
    # Heatmap Cramér's V
    st.markdown('<p class="section-title">Heatmap Asosiasi Antar Variabel (Cramér\'s V)</p>', unsafe_allow_html=True)
 
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
 
        # Custom purple-to-cyan colorscale
        purple_cyan = [
            [0.0,  "#080C14"],
            [0.25, "#1e1b4b"],
            [0.5,  "#4338ca"],
            [0.75, "#6366F1"],
            [1.0,  "#22D3EE"],
        ]
 
        fig_heat = go.Figure(data=go.Heatmap(
            z=np.round(matrix, 2),
            x=cat_labels, y=cat_labels,
            colorscale=purple_cyan,
            zmin=0, zmax=1,
            text=np.round(matrix, 2),
            texttemplate="%{text:.2f}",
            textfont={"size": 9, "color": "#CBD5E1"},
        ))
        fig_heat.update_layout(
            height=520,
            xaxis=dict(tickangle=-35, tickfont=dict(size=10)),
            yaxis=dict(tickfont=dict(size=10)),
        )
        style_fig(fig_heat, height=520)
        st.plotly_chart(fig_heat, use_container_width=True)
        st.caption("Cramér's V: 0 = tidak ada asosiasi · 1 = asosiasi sempurna")
    else:
        st.warning("Data terlalu sedikit untuk menghitung Cramér's V. Hapus filter untuk melihat heatmap.")
 
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">Data Mentah (Filtered)</p>', unsafe_allow_html=True)
    with st.expander("Tampilkan Tabel Data"):
        st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", data=csv,
                           file_name="data_filtered.csv", mime="text/csv")
 
# ══════════════════════════════════════════════
# TAB 5 – SIMULASI MONTE CARLO
# ══════════════════════════════════════════════
with tab5:
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(99,102,241,0.1),rgba(13,18,32,0.9));
                border:1px solid rgba(99,102,241,0.25);border-radius:14px;padding:20px 24px;margin-bottom:20px;">
        <div style="font-size:1rem;font-weight:700;color:#E2E8F0;margin-bottom:6px;">🎲 Simulasi Monte Carlo</div>
        <div style="color:#64748B;font-size:0.88rem;line-height:1.6;">
            Proyeksikan probabilitas kehabisan uang melalui <strong style="color:#A5B4FC;">10.000 iterasi bootstrap</strong>
            berdasarkan distribusi empiris dari data survei aktif (sesuai filter sidebar).
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        sim_uang_saku = st.selectbox("Skenario Uang Saku:", ORDER_UANG_SAKU, index=1)
    with col_sim2:
        sim_budgeting = st.selectbox("Skenario Budgeting:", ["Ya", "Tidak"])
 
    run_btn = st.button("🚀 Jalankan Simulasi", use_container_width=False)
 
    if run_btn:
        with st.spinner("Menjalankan 10.000 iterasi..."):
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
 
            sampled_us    = np.random.choice(ref_data["uang_saku"].values, size=n_sim)
            sampled_exp   = np.random.choice(ref_data["total_pengeluaran"].values, size=n_sim)
            sampled_khabis = np.random.choice(ref_data["kehabisan_uang"].values, size=n_sim)
 
            vals_us  = map_to_numeric(pd.Series(sampled_us), "uang_saku")
            vals_exp = map_to_numeric(pd.Series(sampled_exp), "pengeluaran")
            sisa_uang = vals_us - vals_exp
 
            prob_khabis      = np.mean(sampled_khabis == "Ya") * 100
            mean_sisa        = np.mean(sisa_uang)
            risk_sisa_negatif = np.mean(sisa_uang < 0) * 100
            p5_sisa          = np.percentile(sisa_uang, 5)
            p95_sisa         = np.percentile(sisa_uang, 95)
            overall_khabis   = np.mean(filtered["kehabisan_uang"] == "Ya") * 100
            delta_khabis     = prob_khabis - overall_khabis
 
        # KPI
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("📉 Probabilitas Kehabisan",
                    f"{prob_khabis:.1f}%",
                    delta=f"{delta_khabis:+.1f}% vs rata-rata",
                    delta_color="inverse" if prob_khabis > overall_khabis else "normal")
        kpi2.metric("💰 Rata-rata Sisa Uang", f"Rp {mean_sisa:,.0f}")
        kpi3.metric("⚠️ Risiko Defisit", f"{risk_sisa_negatif:.1f}%")
 
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<p class="section-title">Distribusi Sisa Uang Bulanan (10.000 Simulasi)</p>', unsafe_allow_html=True)
 
        df_sim = pd.DataFrame({"Sisa Uang": sisa_uang})
        fig_sim = px.histogram(df_sim, x="Sisa Uang", nbins=60,
                               color_discrete_sequence=[ACCENT],
                               marginal="box", opacity=0.85)
        fig_sim.add_vline(x=0, line_dash="dot", line_color=RED, line_width=2,
                          annotation_text="Titik Impas",
                          annotation_font_color=RED, annotation_font_size=11)
        fig_sim.add_vrect(x0=sisa_uang.min(), x1=0,
                          fillcolor=RED, opacity=0.04, line_width=0)
        fig_sim.update_layout(xaxis_title="Sisa Uang (Rp)", yaxis_title="Frekuensi",
                               showlegend=False, hovermode="x unified")
        style_fig(fig_sim, height=400)
        st.plotly_chart(fig_sim, use_container_width=True)
 
        # Interpretasi
        risk_color = "warn-card" if risk_sisa_negatif > 30 else "insight-card"
        st.markdown(f"""
        <div class="{risk_color}">
            <strong>Interpretasi Hasil Simulasi</strong><br>
            Profil <em>Uang Saku: {sim_uang_saku}</em> · <em>Budgeting: {sim_budgeting}</em><br><br>
            • Rata-rata sisa uang akhir bulan: <strong>Rp {mean_sisa:,.0f}</strong><br>
            • Risiko defisit (pengeluaran > uang saku): <strong>{risk_sisa_negatif:.1f}%</strong><br>
            • 90% confidence interval sisa uang: <strong>Rp {p5_sisa:,.0f} – Rp {p95_sisa:,.0f}</strong><br>
            • Area merah di kiri garis putus = skenario kehabisan uang sebelum akhir bulan.
        </div>
        """, unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;padding:4px 0 16px 0;">
    <div style="font-size:0.75rem;color:#1e293b;color:#334155;">
        FinScope · Dashboard Analisis Keuangan Mahasiswa
    </div>
    <div style="font-size:0.75rem;color:#334155;font-family:'JetBrains Mono',monospace;">
        Sains Data · UIN KH Abdurrahman Wahid · 2026
    </div>
</div>
""", unsafe_allow_html=True)
