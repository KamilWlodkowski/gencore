"""
Zakładka analizy Eurojackpot - ZREFAKTORYZOWANA WERSJA
Zmiany:
- Używa charts_and_stats.py zamiast charts.py + statistics.py
- Łatwiejsze dodawanie nowych wykresów i statystyk
- Mniej kodu, więcej czytelności
"""
import streamlit as st
import pandas as pd
from .table_styles import apply_eurojackpot_styles
from database import fetch_all_eurojackpot_results
from .charts_and_stats import CHARTS, STATISTICS, ENABLED_STATS


# Konfiguracja kolumn
MAIN_NUMBER_COLS = ['liczba_1', 'liczba_2', 'liczba_3', 'liczba_4', 'liczba_5']
EXTRA_NUMBER_COLS = ['gwiazdka_1', 'gwiazdka_2']


def render():
    """Główna funkcja renderująca zakładkę analizy"""
    
    # Pobierz dane
    draws = fetch_all_eurojackpot_results()
    
    if not draws:
        st.info("Nie znaleziono danych w tabeli Eurojackpot")
        return
    
    # Konwersja do DataFrame
    if not isinstance(draws, pd.DataFrame):
        df = pd.DataFrame(draws)
    else:
        df = draws.copy()
    
    # =========================================================================
    # SEKCJA 1: TABELA Z WYNIKAMI
    # =========================================================================
    
    # Suwak do wyboru liczby wierszy
    rows_to_show = st.slider(
        "Liczba wyświetlanych wierszy",
        min_value=5,
        max_value=len(df),
        value=min(10, len(df)),
        step=5
    )
    
    st.write(f"Wyświetlam **{rows_to_show}** z **{len(df)}** losowań")
    
    # Przygotuj dane do wyświetlenia
    display_data = df.head(rows_to_show)
    
    # Zastosuj kolorowanie
    styled_df = apply_eurojackpot_styles(
        display_data,
        main_number_cols=MAIN_NUMBER_COLS,
        extra_number_cols=EXTRA_NUMBER_COLS
    )
    
    # Wyświetl tabelę
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # =========================================================================
    # SEKCJA 2: WYKRESY
    # =========================================================================
    st.divider()
    st.subheader("📊 Wykres częstotliwości występowania głównych liczb")
    
    # Opcje wykresu
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        use_all_data = st.checkbox("Użyj wszystkich danych", value=True)
    
    with col2:
        chart_type = st.selectbox("Typ wykresu", list(CHARTS.keys()))
    
    # Wybierz dane do wykresu
    if use_all_data:
        chart_data = df
        st.info(f"Analiza oparta na wszystkich **{len(df)}** losowaniach")
    else:
        chart_data = df.head(rows_to_show)
        st.info(f"Analiza oparta na **{rows_to_show}** najnowszych losowaniach")
    
    # Stwórz i wyświetl wykres
    chart_function = CHARTS[chart_type]
    fig = chart_function(chart_data, MAIN_NUMBER_COLS)
    st.plotly_chart(fig, use_container_width=True)
    
    # =========================================================================
    # SEKCJA 3: STATYSTYKI
    # =========================================================================
    
    # Renderuj wszystkie włączone statystyki
    for stat_key in ENABLED_STATS:
        if stat_key in STATISTICS:
            stat_function = STATISTICS[stat_key]
            stat_function(chart_data, MAIN_NUMBER_COLS)


if __name__ == "__main__":
    render()
