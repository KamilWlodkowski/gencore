import streamlit as st
import pandas as pd
from .table_styles import apply_eurojackpot_styles
from database import fetch_all_eurojackpot_results
from .charts import create_frequency_chart, create_frequency_line_chart, get_frequency_statistics
from .statistics import render_frequency_statistics

def render():

    # Główny kod
    draws = fetch_all_eurojackpot_results()

    if draws:
        # Konwersja do DataFrame
        if not isinstance(draws, pd.DataFrame):
            df = pd.DataFrame(draws)
        else:
            df = draws.copy()

        # Suwak
        rows_to_show = st.slider(
            "Liczba wyświetlanych wierszy",
            min_value=5,
            max_value=len(draws),
            value=min(10, len(draws)),  
            step=5
        )
        
        st.write(f"Wyświetlam **{rows_to_show}** z **{len(draws)}** losowań")
        
        # Przygotowanie danych do tabeli
        display_data = df.head(rows_to_show)
        
        # Określ kolumny do kolorowania
        main_number_cols = ['liczba_1', 'liczba_2', 'liczba_3', 'liczba_4', 'liczba_5']  
        extra_number_cols = ['gwiazdka_1', 'gwiazdka_2']
        
        # Zastosuj style
        styled_df = apply_eurojackpot_styles(
            display_data, 
            main_number_cols=main_number_cols,
            extra_number_cols=extra_number_cols
        )
        
        # Wyświetl tabelę
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        # WYKRES
        st.divider()
        st.subheader("📊 Wykres częstotliwości występowania głównych liczb")
        
        # Opcje wykresu
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            use_all_data = st.checkbox("Użyj wszystkich danych", value=True)
        with col2:
            chart_type = st.selectbox("Typ wykresu", ["Słupkowy", "Liniowy"])
        
        # Wybierz dane do wykresu
        if use_all_data:
            chart_data = df
            st.info(f"Analiza oparta na wszystkich **{len(df)}** losowaniach")
        else:
            chart_data = df.head(rows_to_show)
            st.info(f"Analiza oparta na **{rows_to_show}** najnowszych losowaniach")
        
        # Stwórz i wyświetl wykres
        if chart_type == "Słupkowy":
            fig = create_frequency_chart(chart_data, main_number_cols)
        else:
            fig = create_frequency_line_chart(chart_data, main_number_cols)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # STATYSTYKI
        stats = get_frequency_statistics(chart_data, main_number_cols)
        render_frequency_statistics(stats)
        
    else:
        st.info("Nie znaleziono danych w tabeli Eurojackpot")

            