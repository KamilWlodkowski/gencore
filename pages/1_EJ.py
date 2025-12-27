import streamlit as st
from database import fetch_all_eurojackpot_results

st.title("EJ")

draws = fetch_all_eurojackpot_results()





if draws:
    rows_to_show = st.slider(
    "Liczba wyświetlanych wierszy",
    min_value=5,
    max_value=len(draws),
    value=min(50, len(draws)),  # domyślnie 50 lub mniej
    step=5
)
    st.write(f"Wyświetlam {rows_to_show} z {len(draws)} losowań")
    display_data = draws[:rows_to_show]
    st.dataframe(display_data, use_container_width=True)

    # st.write(f"Tabela z {len(draws)} wynikami")
    # st.dataframe(draws)
else:
    st.info("Nie znalezionow danych w tabeli Eurojackpot")