import streamlit as st
from pathlib import Path

# Ścieżki
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Podstawowa konfiguracja
APP_TITLE = "GenCore"
APP_VERSION = "0.1.0"

# Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Streamlit config
PAGE_CONFIG = {
    "page_title": APP_TITLE,
    "page_icon": "💶",
    "layout": "wide",
}

print("✅ Config załadowany")  # Debug