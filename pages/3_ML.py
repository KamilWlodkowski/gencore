import streamlit as st
from database import fetch_all_mini_lotto_results

st.title("ML")

draws = fetch_all_mini_lotto_results()

if draws:
    rows_to_show = st.slider(
    "Liczba wyświetlanych wierszy",
    min_value=5,
    max_value=len(draws),
    value=min(50, len(draws)),  
    step=5
)
    st.write(f"Wyświetlam {rows_to_show} z {len(draws)} losowań")
    display_data = draws[:rows_to_show]
    st.dataframe(display_data, use_container_width=True)

else:
    st.info("Nie znalezionow danych w tabeli Mni lotto")