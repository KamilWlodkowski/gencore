import streamlit as st
from settings import PAGE_CONFIG, APP_TITLE


st.set_page_config(**PAGE_CONFIG)

st.title(f"{APP_TITLE}")