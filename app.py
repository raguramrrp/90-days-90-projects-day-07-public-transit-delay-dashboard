"""Tirunelveli Transport Tracker (Nellai Transit).
Official municipal transportation tracking application for Tirunelveli, Tamil Nadu, India.
Faithfully renders the approved Google Stitch Civic Design System with:
- Top municipal command header and live telemetry status ribbon
- Bus Search with interactive Thamirabarani vector map and vehicle inspector
- Train Search with CRIS NTES telemetry, WAP-7 locomotive, and waypoint progression
- Station Hubs & Interchanges with terminal schematics, connecting buses, and auto tariffs
- About & Data Feeds with live data provenance, KPI metrics, and privacy policy
"""

from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

from src.db import check_health
from src.etl import TransitETLPipeline

# ----------------------------------------------------------------------------
# 1. PAGE SETUP & CIVIC APP IDENTITY
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Tirunelveli Transport Tracker",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------------------------------------------------------
# 2. SEAMLESS CHROME SUPPRESSION CSS
# ----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Completely hide Streamlit header, menu, footer, and borders */
    #MainMenu { visibility: hidden !important; display: none !important; }
    header[data-testid="stHeader"] { visibility: hidden !important; display: none !important; height: 0 !important; }
    footer { visibility: hidden !important; display: none !important; height: 0 !important; }
    [data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
    [data-testid="stDecoration"] { visibility: hidden !important; display: none !important; }
    .stApp > header { display: none !important; }
    .stApp { margin-top: 0 !important; }
    
    /* Remove padding and maximize iframe workspace */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100% !important;
        border: none !important;
        display: block !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# 3. DATABASE INITIALIZATION
# ----------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def ensure_database():
    """Verifies transit database health and seeds tables if empty."""
    health = check_health()
    if not health.get("connected") or health.get("tables", {}).get("actual_times", 0) == 0:
        pipeline = TransitETLPipeline()
        pipeline.run()
    return True

ensure_database()

# ----------------------------------------------------------------------------
# 4. LOAD & RENDER STITCH CIVIC UI
# ----------------------------------------------------------------------------
def load_stitch_ui():
    """Reads the unified Stitch HTML application template."""
    template_path = Path(__file__).resolve().parent / "src" / "stitch_template.html"
    if not template_path.exists():
        template_path = Path(__file__).resolve().parent / "stitch_tirunelveli_transit_tracker" / "bus_search_live_telemetry_2" / "code.html"
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

html_content = load_stitch_ui()

# Embed the responsive Stitch Single-Page App with native scrolling
components.html(html_content, height=1450, scrolling=True)
