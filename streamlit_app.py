import streamlit as st
from settings import PAGE_CONFIG, APP_TITLE
from database import fetch_all_eurojackpot_results

st.set_page_config(**PAGE_CONFIG)

st.title(f"{APP_TITLE}")

draws = fetch_all_eurojackpot_results()

if draws:
    st.write(f"Tabela z {len(draws)} wynikami")
    st.dataframe(draws)
else:
    st.info("Nie znalezionow danych w tabeli Eurojackpot")