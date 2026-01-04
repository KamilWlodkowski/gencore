import streamlit as st
import pandas as pd
from .table_styles import render_legend, apply_eurojackpot_styles
from database import fetch_all_eurojackpot_results

def render():

    # Główny kod
    draws = fetch_all_eurojackpot_results()

    if draws:
        # Wyświetl legendę
        render_legend()
        st.divider()
        
        # Suwak
        rows_to_show = st.slider(
            "Liczba wyświetlanych wierszy",
            min_value=5,
            max_value=len(draws),
            value=min(10, len(draws)),  
            step=5
        )
        
        st.write(f"Wyświetlam **{rows_to_show}** z **{len(draws)}** losowań")
        
        # Przygotowanie danych
        display_data = draws[:rows_to_show]
        
        # Konwersja do DataFrame jeśli nie jest
        if not isinstance(display_data, pd.DataFrame):
            df = pd.DataFrame(display_data)
        else:
            df = display_data.copy()
        
        # Określ kolumny do kolorowania
        main_number_cols = ['liczba_1', 'liczba_2', 'liczba_3', 'liczba_4', 'liczba_5']  
        extra_number_cols = ['gwiazdka_1', 'gwiazdka_2']
        
        # Zastosuj style
        styled_df = apply_eurojackpot_styles(
            df, 
            main_number_cols=main_number_cols,
            extra_number_cols=extra_number_cols
        )
        
        # Wyświetl tabelę
        st.dataframe(styled_df, use_container_width=True, height=400)
        
    else:
        st.info("Nie znaleziono danych w tabeli Eurojackpot")

            