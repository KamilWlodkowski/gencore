import streamlit as st
from components.ej import analysis_tab, generator_tab, checker_tab

st.title("EJ")

# Tworzenie zakładek
tab1, tab2, tab3 = st.tabs(["Analiza", "Generator", "Sprawdzenie"])

# WAŻNE: NIE używaj st.subheader ani innych elementów poza kontekstem 'with'
with tab1:
    analysis_tab.render()

with tab2:
    generator_tab.render()

with tab3:
    checker_tab.render()