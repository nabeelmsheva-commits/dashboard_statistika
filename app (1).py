import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ────────────────────────────────────────────
st.set_page_config(
    page_title="FinScope · Analisis Keuangan Mahasiswa",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# DESIGN SYSTEM & CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ═══════════════════════════════════════
       KEYFRAME ANIMATIONS
    ═══════════════════════════════════════ */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes floatUp {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }

    @keyframes floatSlow {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-5px) rotate(1deg); }
        66% { transform: translateY(3px) rotate(-1deg); }
    }

    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(99,102,241,0.3), 0 0 40px rgba(34,211,238,0.1); }
        50% { box-shadow: 0 0 35px rgba(99,102,241,0.5), 0 0 70px rgba(34,211,238,0.25); }
    }

    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    @keyframes borderGlow {
        0%, 100% { border-color: rgba(99,102,241,0.4); }
        25% { border-color: rgba(34,211,238,0.6); }
        50% { border-color: rgba(168,85,247,0.5); }
        75% { border-color: rgba(244,114,182,0.5); }
    }

    @keyframes slideInFromLeft {
        0% { opacity: 0; transform: translateX(-30px); }
        100% { opacity: 1; transform: translateX(0); }
    }

    @keyframes slideInFromBottom {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes scaleIn {
        0% { transform: scale(0.9); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }

    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }

    @keyframes waveHand {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(20deg); }
        75% { transform: rotate(-15deg); }
    }

    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 0 5px #a855f7, 0 0 10px #a855f7, 0 0 15px #a855f7; }
        50% { box-shadow: 0 0 10px #a855f7, 0 0 20px #a855f7, 0 0 30px #a855f7; }
    }

    /* ═══════════════════════════════════════
       BASE STYLES
    ═══════════════════════════════════════ */
    html, body, .stApp {
        background: #030014;
        font-family: 'Inter', 'Space Grotesk', sans-serif;
        overflow-x: hidden;
    }

    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse at 20% 20%, rgba(99,102,241,0.12) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, rgba(168,85,247,0.1) 0%, transparent 50%),
            radial-gradient(ellipse at 40% 70%, rgba(34,211,238,0.08) 0%, transparent 40%),
            radial-gradient(ellipse at 70% 20%, rgba(244,114,182,0.06) 0%, transparent 40%);
        animation: gradientShift 15s ease infinite;
        background-size: 200% 200%;
        pointer-events: none;
        z-index: 0;
    }

    .stApp::after {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(99,102,241,.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(99,102,241,.03) 1px, transparent 1px);
        background-size: 60px 60px;
        pointer-events: none;
        z-index: 0;
    }

    /* ═══════════════════════════════════════
       FIX KEYBOARD_DOUBLE BUG
    ═══════════════════════════════════════ */
    header[data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
    }

    [data-testid="stTooltipContent"],
    [class*="keyboard"],
    [class*="Keyboard"],
    .stKeyboardShortcut,
    .stTooltipHoverTarget {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* ═══════════════════════════════════════
       SIDEBAR - SESUAI SCREENSHOT
    ═══════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f3a 0%, #141830 50%, #0f1225 100%) !important;
        border-right: 1px solid rgba(99,102,241,0.15);
    }

    [data-testid="stSidebar"] * {
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }

    /* Filter title besar dan bold */
    .filter-title {
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: #f1f5f9 !important;
        margin-bottom: 20px !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        letter-spacing: -0.02em !important;
    }

    /* Label selectbox dengan emoji - besar dan bold */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        color: #e2e8f0 !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        margin-bottom: 8px !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }

    /* Selectbox styling - dark mode clean */
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
        background: #0d1117 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div:hover {
        border-color: rgba(168,85,247,0.5) !important;
        box-shadow: 0 0 15px rgba(168,85,247,0.15) !important;
    }

    /* ═══════════════════════════════════════
       METRIC CARDS
    ═══════════════════════════════════════ */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg,
            rgba(99,102,241,0.15) 0%,
            rgba(168,85,247,0.1) 50%,
            rgba(13,18,32,0.9) 100%);
        border: 1px solid rgba(168,85,247,0.3);
        border-radius: 20px;
        padding: 22px 24px;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        animation: slideInFromBottom 0.6s ease-out;
    }

    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(168,85,247,0.1), transparent, rgba(34,211,238,0.1), transparent);
        animation: spin 8s linear infinite;
        opacity: 0;
        transition: opacity 0.4s;
    }

    [data-testid="metric-container"]:hover {
        border-color: rgba(168,85,247,0.6);
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 20px 40px rgba(168,85,247,0.2), 0 0 30px rgba(99,102,241,0.15);
    }

    [data-testid="metric-container"]:hover::before { opacity: 1; }

    [data-testid="metric-container"]::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #a855f7, #06b6d4, #f472b6);
        background-size: 200% 100%;
        animation: gradientShift 3s ease infinite;
        border-radius: 20px 20px 0 0;
    }

    [data-testid="metric-container"] label {
        color: #7c3aed !important;
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: .12em !important;
    }

    [data-testid="stMetricValue"] {
        color: #f1f5f9 !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    [data-testid="stMetricDelta"] { font-size: 0.75rem !important; font-weight: 600 !important; }

    /* ═══════════════════════════════════════
       TABS
    ═══════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15,10,40,0.7);
        border: 1px solid rgba(168,85,247,0.2);
        border-radius: 16px;
        padding: 6px;
        gap: 4px;
        backdrop-filter: blur(10px);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #6b7280;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 10px 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stTabs [data-baseweb="tab"]:hover { color: #c4b5fd; }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed, #a855f7, #06b6d4) !important;
        color: #fff !important;
        box-shadow: 0 4px 20px rgba(168,85,247,0.4), 0 0 40px rgba(168,85,247,0.15) !important;
        animation: bounceIn 0.4s ease-out;
    }

    /* ═══════════════════════════════════════
       SECTION TITLES
    ═══════════════════════════════════════ */
    .section-title {
        color: #e9d5ff;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .15em;
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 28px 0 16px 0;
        animation: slideInFromLeft 0.5s ease-out;
    }

    .section-title::before {
        content: '';
        display: inline-block;
        width: 4px;
        height: 18px;
        background: linear-gradient(180deg, #a855f7, #06b6d4);
        border-radius: 4px;
        animation: floatUp 3s ease-in-out infinite;
        box-shadow: 0 0 10px rgba(168,85,247,0.5);
    }

    /* ═══════════════════════════════════════
       INSIGHT & WARN CARDS
    ═══════════════════════════════════════ */
    .insight-card {
        background: linear-gradient(135deg, rgba(34,211,238,0.08) 0%, rgba(168,85,247,0.05) 50%, rgba(15,10,40,0.9) 100%);
        border: 1px solid rgba(34,211,238,0.25);
        border-radius: 18px;
        padding: 20px 24px;
        margin: 14px 0;
        font-size: 0.88rem;
        color: #c4b5fd;
        line-height: 1.8;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(8px);
        animation: slideInFromBottom 0.6s ease-out;
        transition: all 0.3s ease;
    }

    .insight-card:hover {
        border-color: rgba(34,211,238,0.5);
        box-shadow: 0 10px 30px rgba(34,211,238,0.1);
        transform: translateY(-2px);
    }

    .insight-card strong { color: #67e8f9; text-shadow: 0 0 10px rgba(103,232,249,0.3); }

    .insight-card .badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(168,85,247,0.2), rgba(34,211,238,0.15));
        color: #67e8f9;
        border-radius: 8px;
        padding: 3px 10px;
        font-size: 0.76rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        border: 1px solid rgba(168,85,247,0.3);
        animation: floatSlow 4s ease-in-out infinite;
    }

    .warn-card {
        background: linear-gradient(135deg, rgba(244,63,94,0.1) 0%, rgba(168,85,247,0.05) 50%, rgba(15,10,40,0.9) 100%);
        border: 1px solid rgba(244,63,94,0.3);
        border-radius: 18px;
        padding: 20px 24px;
        margin: 14px 0;
        color: #fda4af;
        font-size: 0.88rem;
        line-height: 1.8;
        animation: slideInFromBottom 0.6s ease-out;
        transition: all 0.3s ease;
    }

    .warn-card:hover {
        border-color: rgba(244,63,94,0.5);
        box-shadow: 0 10px 30px rgba(244,63,94,0.1);
    }

    /* ═══════════════════════════════════════
       DIVIDERS
    ═══════════════════════════════════════ */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(168,85,247,0.3), rgba(34,211,238,0.3), transparent) !important;
        margin: 32px 0 !important;
    }

    /* ═══════════════════════════════════════
       DATAFRAME
    ═══════════════════════════════════════ */
    .stDataFrame {
        border: 1px solid rgba(168,85,247,0.2) !important;
        border-radius: 14px !important;
        overflow: hidden !important;
    }

    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: rgba(15,10,40,0.95) !important;
    }

    /* ═══════════════════════════════════════
       BUTTONS
    ═══════════════════════════════════════ */
    .stButton button {
        background: linear-gradient(135deg, #7c3aed, #a855f7, #06b6d4) !important;
        background-size: 200% 200% !important;
        animation: gradientShift 3s ease infinite !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        padding: 12px 32px !important;
        font-size: 0.9rem !important;
        box-shadow: 0 4px 25px rgba(168,85,247,0.35) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stButton button:hover {
        box-shadow: 0 8px 35px rgba(168,85,247,0.5) !important;
        transform: translateY(-3px) scale(1.03) !important;
    }

    .stDownloadButton button {
        background: rgba(168,85,247,0.12) !important;
        color: #c4b5fd !important;
        border: 1px solid rgba(168,85,247,0.3) !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }

    .stDownloadButton button:hover {
        background: rgba(168,85,247,0.2) !important;
        transform: translateY(-2px) !important;
    }

    /* ═══════════════════════════════════════
       SELECTBOX MAIN CONTENT
    ═══════════════════════════════════════ */
    .stSelectbox [data-baseweb="select"] > div {
        background: rgba(15,10,40,0.8) !important;
        border: 1px solid rgba(168,85,247,0.25) !important;
        border-radius: 12px !important;
        color: #e9d5ff !important;
    }

    .stSelectbox label {
        color: #7c3aed !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: .1em !important;
    }

    /* ═══════════════════════════════════════
       SPINNER
    ═══════════════════════════════════════ */
    .stSpinner > div {
        border-top-color: #a855f7 !important;
        border-right-color: #06b6d4 !important;
    }

    /* ═══════════════════════════════════════
       EXPANDER
    ═══════════════════════════════════════ */
    .streamlit-expanderHeader {
        background: rgba(15,10,40,0.7) !important;
        border: 1px solid rgba(168,85,247,0.2) !important;
        border-radius: 14px !important;
        color: #c4b5fd !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }

    .streamlit-expanderHeader:hover {
        background: rgba(15,10,40,0.9) !important;
        border-color: rgba(168,85,247,0.4) !important;
    }

    .stCaption { color: #4b5563 !important; font-size: 0.75rem !important; }

    .stInfo {
        background: rgba(34,211,238,0.07) !important;
        border: 1px solid rgba(34,211,238,0.2) !important;
        border-radius: 14px !important;
        color: #c4b5fd !important;
    }

    .stWarning {
        background: rgba(245,158,11,0.08) !important;
        border: 1px solid rgba(245,158,11,0.25) !important;
        border-radius: 14px !important;
    }

    /* ═══════════════════════════════════════
       CUSTOM COMPONENTS
    ═══════════════════════════════════════ */
    .neon-text {
        background: linear-gradient(135deg, #a855f7, #06b6d4, #f472b6);
        background-size: 200% 200%;
        animation: gradientShift 4s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .emoji-float { display: inline-block; animation: floatUp 3s ease-in-out infinite; }
    .emoji-wave { display: inline-block; animation: waveHand 2s ease-in-out infinite; }

    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #22d3ee;
        animation: pulseGlow 2s ease-in-out infinite;
        display: inline-block;
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, #7c3aed, #a855f7, #06b6d4) !important;
        background-size: 200% 100% !important;
        animation: gradientShift 2s ease infinite !important;
    }

    .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(15,10,40,0.5); border-radius: 3px; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #7c3aed, #a855f7); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #a855f7, #06b6d4); }

    .stTabs [data-baseweb="tab-panel"] { animation: scaleIn 0.4s ease-out; }

    /* ═══════════════════════════════════════
       PROFILE CARD
    ═══════════════════════════════════════ */
    .profile-card {
        background: linear-gradient(135deg, rgba(168,85,247,0.15) 0%, rgba(6,182,212,0.1) 50%, rgba(15,10,40,0.95) 100%);
        border: 2px solid rgba(168,85,247,0.3);
        border-radius: 20px;
        padding: 28px;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(12px);
        animation: slideInFromBottom 0.8s ease-out, borderGlow 5s ease infinite;
        box-shadow: 0 10px 40px rgba(168,85,247,0.2);
    }

    .profile-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #a855f7, #06b6d4, #f472b6, #a855f7);
        background-size: 300% 100%;
        animation: gradientShift 3s ease infinite;
    }

    .profile-avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: linear-gradient(135deg, #7c3aed, #a855f7, #06b6d4);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        margin: 0 auto 16px auto;
        animation: floatUp 4s ease-in-out infinite, glowPulse 3s ease-in-out infinite;
        box-shadow: 0 8px 30px rgba(168,85,247,0.4);
    }

    .profile-name {
        font-size: 1.4rem;
        font-weight: 800;
        color: #e9d5ff;
        text-align: center;
        margin-bottom: 8px;
        text-shadow: 0 0 20px rgba(168,85,247,0.4);
    }

    .profile-nim {
        font-size: 0.85rem;
        color: #67e8f9;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .profile-program { font-size: 0.8rem; color: #c4b5fd; text-align: center; margin-bottom: 16px; }
    .profile-university { font-size: 0.75rem; color: #9ca3af; text-align: center; font-style: italic; }

    .profile-stats {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid rgba(168,85,247,0.2);
    }

    .profile-stat-item { text-align: center; }
    .profile-stat-value { font-size: 1.2rem; font-weight: 700; color: #a855f7; display: block; }
    .profile-stat-label { font-size: 0.7rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; }

    .social-links { display: flex; justify-content: center; gap: 12px; margin-top: 16px; }

    .social-icon {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: rgba(168,85,247,0.1);
        border: 1px solid rgba(168,85,247,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .social-icon:hover {
        background: rgba(168,85,247,0.3);
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(168,85,247,0.3);
    }

    /* Sidebar divider */
    .sidebar-divider {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent) !important;
        margin: 24px 0 !important;
    }

</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────
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

PALETTE   = ["#a855f7", "#06b6d4", "#f59e0b", "#10b981", "#f472b6", "#8b5cf6", "#fb7185", "#34d399"]
BG_PLOT   = "rgba(15,10,40,0.95)"
PAPER_BG  = "#030014"
FONT_CLR  = "#c4b5fd"
GRID_CLR  = "rgba(168,85,247,0.08)"
ACCENT    = "#a855f7"
CYAN      = "#06b6d4"
RED       = "#f43f5e"
GREEN     = "#10b981"
PINK      = "#f472b6"

def style_fig(fig, height=380):
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=BG_PLOT,
        font=dict(color=FONT_CLR, family="Inter, sans-serif", size=12),
        margin=dict(t=44, b=24, l=16, r=16),
        height=height,
        legend=dict(
            bgcolor="rgba(15,10,40,0.9)",
            bordercolor="rgba(168,85,247,0.2)",
            borderwidth=1,
            font=dict(size=11, color="#c4b5fd"),
        ),
    )
    fig.update_xaxes(
        gridcolor=GRID_CLR, zerolinecolor=GRID_CLR,
        tickfont=dict(size=11, color="#a78bfa"),
        linecolor="rgba(168,85,247,0.15)",
    )
    fig.update_yaxes(
        gridcolor=GRID_CLR, zerolinecolor=GRID_CLR,
        tickfont=dict(size=11, color="#a78bfa"),
        linecolor="rgba(168,85,247,0.15)",
    )
    return fig

# ─────────────────────────────────────────────
# SIDEBAR – FILTER & PROFIL (SESUAI SCREENSHOT)
# ─────────────────────────────────────────────
with st.sidebar:
    # ═══════════════════════════════════════
    # FILTER TITLE (BESAR & BOLD)
    # ═══════════════════════════════════════
    st.markdown("""
    <div style="padding: 20px 0 10px 0;">
        <div class="filter-title">
            <span style="font-size:1.6rem;">🎛️</span>
            <span>Filter Data</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # FILTER SELECTBOXES DENGAN EMOJI
    # ═══════════════════════════════════════
    gender_options = ["Semua"] + sorted(df["jenis_kelamin"].unique().tolist())
    gender_filter = st.selectbox("👤 Jenis Kelamin", gender_options)

    uang_saku_options = ["Semua"] + ORDER_UANG_SAKU
    uang_saku_filter = st.selectbox("💵 Uang Saku", uang_saku_options)

    kehabisan_options = ["Semua", "Ya", "Tidak"]
    kehabisan_filter = st.selectbox("️ Pernah Kehabisan Uang", kehabisan_options)

    budgeting_options = ["Semua", "Ya", "Tidak"]
    budgeting_filter = st.selectbox("📒 Melakukan Budgeting", budgeting_options)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # DATASET INFO
    # ═══════════════════════════════════════
    st.markdown(f"""
    <div style="background:rgba(168,85,247,0.08);border:1px solid rgba(168,85,247,0.2);border-radius:14px;padding:16px;animation:borderGlow 5s ease infinite;">
        <div style="font-size:0.65rem;color:#7c3aed;font-weight:700;text-transform:uppercase;letter-spacing:.12em;margin-bottom:12px;">📊 Dataset Info</div>
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;align-items:center;">
            <span style="color:#6b7280;font-size:0.8rem;">Total Responden</span>
            <span style="color:#c4b5fd;font-weight:700;font-size:0.85rem;font-family:'JetBrains Mono',monospace;">{len(df)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="color:#6b7280;font-size:0.8rem;">Sumber</span>
            <span style="color:#c4b5fd;font-weight:700;font-size:0.8rem;">Survei 2026</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # PROFIL SECTION
    # ═══════════════════════════════════════
    st.markdown("""
    <div class="profile-card" style="margin-top:24px;">
        <div class="profile-avatar">‍💻</div>
        <div class="profile-name">Muhammad Sheva Nabeel</div>
        <div class="profile-nim">NIM: 60125001</div>
        <div class="profile-program">📚 Sains Data</div>
        <div class="profile-university">🎓 UIN KH Abdurrahman Wahid</div>
        
        <div class="profile-stats">
            <div class="profile-stat-item">
                <span class="profile-stat-value">5</span>
                <span class="profile-stat-label">Tabs</span>
            </div>
            <div class="profile-stat-item">
                <span class="profile-stat-value">10K</span>
                <span class="profile-stat-label">Simulasi</span>
            </div>
            <div class="profile-stat-item">
                <span class="profile-stat-value">100%</span>
                <span class="profile-stat-label">Python</span>
            </div>
        </div>
        
        <div class="social-links">
            <div class="social-icon">📧</div>
            <div class="social-icon">💼</div>
            <div class="social-icon">🐙</div>
        </div>
        
        <div style="margin-top:16px;text-align:center;font-size:0.65rem;color:#6b7280;">
            <span class="emoji-float"></span> Built with Streamlit + Plotly
        </div>
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
<div style="margin-bottom:32px;animation:slideInFromLeft 0.8s ease-out;">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
        <div style="width:42px;height:42px;background:linear-gradient(135deg,#7c3aed,#a855f7,#06b6d4);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.2rem;box-shadow:0 4px 20px rgba(168,85,247,0.4);animation:floatUp 4s ease-in-out infinite;">
            <span class="emoji-wave">✨</span>
        </div>
        <div>
            <h1 style="color:#f1f5f9;font-size:1.7rem;font-weight:800;margin:0;letter-spacing:-.04em;font-family:'Inter',sans-serif;">
                Dashboard Analisis Keuangan <span class="neon-text">Mahasiswa</span>
            </h1>
            <p style="color:#6b7280;margin:4px 0 0 0;font-size:0.82rem;font-family:'Inter',sans-serif;font-weight:500;">
                <span class="pulse-dot" style="width:6px;height:6px;margin-right:6px;"></span>
                Pola pengeluaran · Perilaku keuangan · Simulasi risiko berbasis data survei Mei–Juni 2026
            </p>
        </div>
    </div>
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
k2.metric("️ Kehabisan Uang",    f"{pct_kehabisan}%",
          delta="Risiko sistemik" if pct_kehabisan > 35 else "Terkendali",
          delta_color="inverse" if pct_kehabisan > 35 else "normal")
k3.metric("📒 Pakai Budgeting",   f"{pct_budgeting}%")
k4.metric("🛒 Belanja Online ≥3x", f"{pct_belanja_sering}%")
k5.metric("💸 Pengeluaran Utama", modus_pengeluaran.replace("Rp ", "Rp\u00A0"))

st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB NAVIGASI
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📐 Demografi",
    "💳 Pengeluaran",
    "🔍 Perilaku",
    "📈 Advanced",
    "🎲 Monte Carlo",
])

# ═════════════════════════════════════════════
# TAB 1 – DEMOGRAFI & DISTRIBUSI
# ══════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-title">Distribusi Jenis Kelamin</p>', unsafe_allow_html=True)
        gender_cnt = filtered["jenis_kelamin"].value_counts().reset_index()
        gender_cnt.columns = ["Jenis Kelamin", "Jumlah"]
        fig = px.pie(gender_cnt, names="Jenis Kelamin", values="Jumlah",
                     color_discrete_sequence=PALETTE, hole=0.6)
        fig.update_traces(textfont_size=12, textinfo="percent+label",
                          marker=dict(line=dict(color=PAPER_BG, width=3)),
                          pull=[0.05] * len(gender_cnt))
        fig.update_layout(showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Distribusi Uang Saku Bulanan</p>', unsafe_allow_html=True)
        uang_cnt = filtered["uang_saku"].value_counts().reindex(ORDER_UANG_SAKU, fill_value=0).reset_index()
        uang_cnt.columns = ["Uang Saku", "Jumlah"]
        fig2 = px.bar(uang_cnt, x="Uang Saku", y="Jumlah",
                      color="Jumlah", color_continuous_scale=[[0,"#1e1b4b"],[0.5,"#7c3aed"],[1,"#06b6d4"]],
                      text="Jumlah")
        fig2.update_traces(textposition="outside", textfont_color=FONT_CLR,
                           marker_line_width=0, marker=dict(cornerradius=8))
        fig2.update_coloraxes(showscale=False)
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Uang Saku Berdasarkan Jenis Kelamin</p>', unsafe_allow_html=True)
    cross = pd.crosstab(filtered["uang_saku"], filtered["jenis_kelamin"]).reindex(ORDER_UANG_SAKU, fill_value=0)
    fig3 = go.Figure()
    for i, col_name in enumerate(cross.columns):
        fig3.add_trace(go.Bar(
            name=col_name, x=cross.index, y=cross[col_name],
            marker=dict(color=PALETTE[i], line=dict(width=0), cornerradius=6),
            text=cross[col_name], textposition="auto",
        ))
    fig3.update_layout(barmode="group", xaxis_title="Uang Saku", yaxis_title="Jumlah",
                       bargap=0.2, bargroupgap=0.05)
    style_fig(fig3, height=340)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(f"""
    <div class="insight-card">
        💡 <strong>Insight Demografi:</strong> Mayoritas responden <span class="badge">{round(filtered[filtered['uang_saku']=='Rp 500.000 - Rp 1.000.000'].shape[0]/n*100,1) if n else 0}%</span>
        berada di rentang uang saku Rp 500rb–Rp 1jt per bulan.
        <br>Perempuan mendominasi sampel dengan proporsi lebih tinggi.
        <br><span class="emoji-float">📊</span> Data ini menunjukkan representasi yang cukup baik untuk analisis finansial mahasiswa.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 2 – POLA PENGELUARAN
# ═════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-title">Total Pengeluaran Bulanan</p>', unsafe_allow_html=True)
        tot_cnt = filtered["total_pengeluaran"].value_counts().reindex(ORDER_TOTAL_PENGELUARAN, fill_value=0).reset_index()
        tot_cnt.columns = ["Total Pengeluaran", "Jumlah"]
        fig = px.bar(tot_cnt, x="Total Pengeluaran", y="Jumlah",
                     color="Total Pengeluaran", color_discrete_sequence=PALETTE, text="Jumlah")
        fig.update_traces(textposition="outside", textfont_color=FONT_CLR,
                          showlegend=False, marker_line_width=0, marker=dict(cornerradius=8))
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Faktor Pengeluaran Membengkak</p>', unsafe_allow_html=True)
        faktor_cnt = filtered["faktor_membengkak"].value_counts().reset_index()
        faktor_cnt.columns = ["Faktor", "Jumlah"]
        faktor_cnt["Faktor_short"] = faktor_cnt["Faktor"].str.extract(r'^([^(]+)').iloc[:, 0].str.strip()
        fig2 = px.bar(faktor_cnt, y="Faktor_short", x="Jumlah",
                      orientation="h",
                      color="Jumlah", color_continuous_scale=[[0,"#1e1b4b"],[0.5,"#a855f7"],[1,"#f472b6"]],
                      text="Jumlah")
        fig2.update_traces(textposition="outside", textfont_color=FONT_CLR, marker_line_width=0)
        fig2.update_coloraxes(showscale=False)
        fig2.update_layout(yaxis_title="")
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Profil Pengeluaran per Kategori</p>', unsafe_allow_html=True)
    col_makan     = filtered["pengeluaran_makan"].value_counts()
    col_transport = filtered["pengeluaran_transport"].value_counts()
    col_hiburan   = filtered["pengeluaran_hiburan"].value_counts()
    col_kuliah    = filtered["pengeluaran_kuliah"].value_counts()

    breakdown_df = pd.DataFrame({
        "Makan": col_makan, "Transport": col_transport,
        "Hiburan": col_hiburan, "Kuliah": col_kuliah,
    }).fillna(0).reset_index().rename(columns={"index": "Kategori"})
    breakdown_melt = breakdown_df.melt(id_vars="Kategori", var_name="Jenis", value_name="Jumlah")

    fig3 = px.bar(breakdown_melt, x="Kategori", y="Jumlah", color="Jenis",
                  barmode="group", color_discrete_sequence=PALETTE, text="Jumlah")
    fig3.update_traces(textposition="outside", textfont_color=FONT_CLR, marker_line_width=0,
                       marker=dict(cornerradius=5))
    fig3.update_layout(xaxis_title="Range Pengeluaran", yaxis_title="Jumlah Mahasiswa",
                       bargap=0.18, bargroupgap=0.04)
    style_fig(fig3, height=360)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<p class="section-title">Frekuensi Belanja Online</p>', unsafe_allow_html=True)
    belanja_cnt = filtered["frekuensi_belanja_online"].value_counts().reset_index()
    belanja_cnt.columns = ["Frekuensi", "Jumlah"]
    col_a, col_b = st.columns([1, 2])
    with col_a:
        fig4 = px.pie(belanja_cnt, names="Frekuensi", values="Jumlah",
                      color_discrete_sequence=PALETTE, hole=0.6)
        fig4.update_traces(textfont_size=12, textinfo="percent+label",
                           marker=dict(line=dict(color=PAPER_BG, width=3)))
        style_fig(fig4)
        st.plotly_chart(fig4, use_container_width=True)
    with col_b:
        freq_tbl = belanja_cnt.copy()
        freq_tbl["Persentase (%)"] = (freq_tbl["Jumlah"] / n * 100).round(1)
        st.dataframe(freq_tbl, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════
# TAB 3 – PERILAKU KEUANGAN
# ═════════════════════════════════════════════
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-title">Pernah Kehabisan Uang? 💸</p>', unsafe_allow_html=True)
        kh_cnt = filtered["kehabisan_uang"].value_counts().reset_index()
        kh_cnt.columns = ["Status", "Jumlah"]
        fig = px.pie(kh_cnt, names="Status", values="Jumlah", hole=0.6,
                     color="Status",
                     color_discrete_map={"Ya": RED, "Tidak": GREEN})
        fig.update_traces(textfont_size=13, textinfo="percent+label",
                          marker=dict(line=dict(color=PAPER_BG, width=4)))
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Melakukan Budgeting? 📒</p>', unsafe_allow_html=True)
        bd_cnt = filtered["budgeting"].value_counts().reset_index()
        bd_cnt.columns = ["Status", "Jumlah"]
        fig2 = px.pie(bd_cnt, names="Status", values="Jumlah", hole=0.6,
                      color="Status",
                      color_discrete_map={"Ya": ACCENT, "Tidak": "#f59e0b"})
        fig2.update_traces(textfont_size=13, textinfo="percent+label",
                           marker=dict(line=dict(color=PAPER_BG, width=4)))
        style_fig(fig2)
        st.plotly_chart(fig2, use_container_width=True)

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
            marker=dict(color=colors_map.get(col_name, ACCENT), line=dict(width=0), cornerradius=8),
            text=cross_bk_pct[col_name].map(lambda v: f"{v:.1f}%"),
            textposition="inside", textfont=dict(size=13, color="white"),
        ))
    fig3.update_layout(barmode="stack", xaxis_title="Melakukan Budgeting",
                       yaxis_title="Persentase (%)", bargap=0.35)
    style_fig(fig3, height=320)
    st.plotly_chart(fig3, use_container_width=True)

    no_budget_risk = cross_bk_pct.get("Ya", pd.Series()).get("Tidak", 0)
    yes_budget_risk = cross_bk_pct.get("Ya", pd.Series()).get("Ya", 0)
    delta = round(no_budget_risk - yes_budget_risk, 1)
    st.markdown(f"""
    <div class="insight-card">
        🔍 Mahasiswa yang <strong>tidak budgeting</strong> memiliki risiko kehabisan uang
        <span class="badge">{no_budget_risk:.1f}%</span> dibanding yang budgeting
        <span class="badge">{yes_budget_risk:.1f}%</span>.
        <br>Selisih risiko: <strong>−{delta} poin persentase</strong> dengan budgeting aktif.
        <br><span class="emoji-float">💡</span> Budgeting terbukti efektif menurunkan risiko financial stress!
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-title">Risiko Kehabisan per Kelompok Uang Saku</p>', unsafe_allow_html=True)
    cross_us = pd.crosstab(filtered["uang_saku"], filtered["kehabisan_uang"]).reindex(ORDER_UANG_SAKU, fill_value=0)
    cross_us_pct = (cross_us.div(cross_us.sum(axis=1), axis=0) * 100).round(1)

    fig4 = go.Figure()
    for col_name in cross_us_pct.columns:
        fig4.add_trace(go.Bar(
            name=f"Kehabisan: {col_name}",
            x=cross_us_pct.index,
            y=cross_us_pct[col_name],
            marker=dict(color=colors_map.get(col_name, ACCENT), line=dict(width=0), cornerradius=8),
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
                       color_continuous_scale=[[0,"#1e1b4b"],[0.5,"#7c3aed"],[1,"#06b6d4"]],
                       text="Persentase (%)")
        fig_f.update_traces(texttemplate="%{text:.1f}%", textposition="outside",
                            textfont_color=FONT_CLR, marker_line_width=0, marker=dict(cornerradius=8))
        fig_f.update_coloraxes(showscale=False)
        style_fig(fig_f, height=360)
        st.plotly_chart(fig_f, use_container_width=True)
    with col_t:
        st.markdown(f"""
        <div style="background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.25);border-radius:14px;padding:18px;margin-bottom:14px;animation:borderGlow 5s ease infinite;">
            <div style="font-size:0.65rem;color:#7c3aed;font-weight:700;text-transform:uppercase;letter-spacing:.12em;">🏆 Modus</div>
            <div style="color:#c4b5fd;font-weight:800;font-size:0.92rem;margin-top:6px;font-family:'JetBrains Mono',monospace;">{modus_val}</div>
        </div>
        <div style="background:rgba(34,211,238,0.08);border:1px solid rgba(34,211,238,0.2);border-radius:14px;padding:18px;animation:borderGlow 6s ease infinite;">
            <div style="font-size:0.65rem;color:#06b6d4;font-weight:700;text-transform:uppercase;letter-spacing:.12em;"> N Filtered</div>
            <div style="color:#67e8f9;font-weight:800;font-size:1.15rem;margin-top:6px;font-family:'JetBrains Mono',monospace;">{n}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
        st.dataframe(freq_df, use_container_width=True, hide_index=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<p class="section-title">Heatmap Asosiasi Antar Variabel (Cramér\'s V) 🔥</p>', unsafe_allow_html=True)

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

    def cramers_v_numpy(x, y):
        confusion_matrix = pd.crosstab(x, y)
        n_obs = confusion_matrix.sum().sum()
        
        chi2 = 0.0
        row_sums = confusion_matrix.sum(axis=1)
        col_sums = confusion_matrix.sum(axis=0)
        
        for i in range(confusion_matrix.shape[0]):
            for j in range(confusion_matrix.shape[1]):
                observed = confusion_matrix.iloc[i, j]
                expected = (row_sums.iloc[i] * col_sums.iloc[j]) / n_obs
                if expected > 0:
                    chi2 += (observed - expected)**2 / expected
        
        r, k = confusion_matrix.shape
        phi2 = chi2 / n_obs
        
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
                        v = cramers_v_numpy(filtered[c1], filtered[c2])
                    except Exception:
                        v = 0.0
                    matrix[i][j] = v
                    matrix[j][i] = v

        purple_cyan = [
            [0.0,  "#030014"],
            [0.2,  "#1e1b4b"],
            [0.4,  "#4338ca"],
            [0.6,  "#7c3aed"],
            [0.8,  "#a855f7"],
            [1.0,  "#06b6d4"],
        ]

        fig_heat = go.Figure(data=go.Heatmap(
            z=np.round(matrix, 2),
            x=cat_labels, y=cat_labels,
            colorscale=purple_cyan,
            zmin=0, zmax=1,
            text=np.round(matrix, 2),
            texttemplate="%{text:.2f}",
            textfont={"size": 9, "color": "#e9d5ff"},
            hovertemplate="Asosiasi: %{z:.2f}<extra></extra>",
        ))
        fig_heat.update_layout(
            height=520,
            xaxis=dict(tickangle=-35, tickfont=dict(size=10, color="#a78bfa")),
            yaxis=dict(tickfont=dict(size=10, color="#a78bfa")),
        )
        style_fig(fig_heat, height=520)
        st.plotly_chart(fig_heat, use_container_width=True)
        st.caption("Cramér's V: 0 = tidak ada asosiasi · 1 = asosiasi sempurna")
    else:
        st.warning("Data terlalu sedikit untuk menghitung Cramér's V. Hapus filter untuk melihat heatmap.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">Data Mentah (Filtered)</p>', unsafe_allow_html=True)
    with st.expander("📂 Tampilkan Tabel Data"):
        st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("️ Download CSV", data=csv,
                           file_name="data_filtered.csv", mime="text/csv")

# ══════════════════════════════════════════════
# TAB 5 – SIMULASI MONTE CARLO
# ══════════════════════════════════════════════
with tab5:
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(168,85,247,0.12),rgba(6,182,212,0.08),rgba(15,10,40,0.9));
                border:1px solid rgba(168,85,247,0.25);border-radius:18px;padding:24px 28px;margin-bottom:24px;
                animation:borderGlow 5s ease infinite;position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#a855f7,#06b6d4,#f472b6);background-size:200% 100%;animation:gradientShift 3s ease infinite;border-radius:18px 18px 0 0;"></div>
        <div style="font-size:1.1rem;font-weight:800;color:#e9d5ff;margin-bottom:8px;display:flex;align-items:center;gap:10px;">
            <span class="emoji-float">🎲</span> Simulasi Monte Carlo
        </div>
        <div style="color:#6b7280;font-size:0.85rem;line-height:1.7;">
            Proyeksikan probabilitas kehabisan uang melalui <strong style="color:#c4b5fd;">10.000 iterasi bootstrap</strong>
            berdasarkan distribusi empiris dari data survei aktif (sesuai filter sidebar).
            <br><span class="emoji-float">⚡</span> Powered by statistical simulation engine.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        sim_uang_saku = st.selectbox("Skenario Uang Saku:", ORDER_UANG_SAKU, index=1)
    with col_sim2:
        sim_budgeting = st.selectbox("Skenario Budgeting:", ["Ya", "Tidak"])

    run_btn = st.button("🚀 Jalankan Simulasi", use_container_width=True)

    if run_btn:
        with st.spinner("⚡ Menjalankan 10.000 iterasi..."):
            time.sleep(0.5)
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

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(" Probabilitas Kehabisan",
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
                          fillcolor=RED, opacity=0.05, line_width=0)
        fig_sim.update_layout(xaxis_title="Sisa Uang (Rp)", yaxis_title="Frekuensi",
                               showlegend=False, hovermode="x unified")
        style_fig(fig_sim, height=400)
        st.plotly_chart(fig_sim, use_container_width=True)

        risk_color = "warn-card" if risk_sisa_negatif > 30 else "insight-card"
        st.markdown(f"""
        <div class="{risk_color}">
            <strong>🧠 Interpretasi Hasil Simulasi</strong><br>
            Profil <em>Uang Saku: {sim_uang_saku}</em> · <em>Budgeting: {sim_budgeting}</em><br><br>
            • Rata-rata sisa uang akhir bulan: <strong>Rp {mean_sisa:,.0f}</strong><br>
            • Risiko defisit (pengeluaran > uang saku): <strong>{risk_sisa_negatif:.1f}%</strong><br>
            • 90% confidence interval sisa uang: <strong>Rp {p5_sisa:,.0f} – Rp {p95_sisa:,.0f}</strong><br>
            • <span class="emoji-float"></span> Area merah di kiri garis putus = skenario kehabisan uang sebelum akhir bulan.
            <br><br><span class="badge">💡 Pro Tip</span> Tingkatkan budgeting dan kurangi pengeluaran impulsif untuk menurunkan risiko defisit!
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0 20px 0;animation:slideInFromBottom 0.8s ease-out;">
    <div style="font-size:0.72rem;color:#4b5563;display:flex;align-items:center;gap:8px;">
        <span class="pulse-dot" style="width:6px;height:6px;"></span>
        FinScope · Dashboard Analisis Keuangan Mahasiswa
    </div>
    <div style="font-size:0.72rem;color:#4b5563;font-family:'JetBrains Mono',monospace;display:flex;align-items:center;gap:8px;">
        <span class="emoji-float">💜</span>
        Sains Data · UIN KH Abdurrahman Wahid · 2026
    </div>
</div>
""", unsafe_allow_html=True)
