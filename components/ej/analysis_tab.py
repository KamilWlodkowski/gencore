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
    # SEKCJA 2B: WYKRES DLA LICZB DODATKOWYCH (GWIAZDEK)
    # =========================================================================
    st.divider()
    st.subheader("⭐ Wykres częstotliwości występowania liczb dodatkowych (gwiazdek)")
    
    # Opcje wykresu dla gwiazdek
    col1, col2 = st.columns([2, 2])
    
    with col1:
        use_all_data_stars = st.checkbox("Użyj wszystkich danych (gwiazdki)", value=True, key="stars_all_data")
    
    with col2:
        chart_type_stars = st.selectbox("Typ wykresu (gwiazdki)", list(CHARTS.keys()), key="stars_chart_type")
    
    # Wybierz dane do wykresu gwiazdek
    if use_all_data_stars:
        chart_data_stars = df
        st.info(f"Analiza gwiazdek oparta na wszystkich **{len(df)}** losowaniach")
    else:
        chart_data_stars = df.head(rows_to_show)
        st.info(f"Analiza gwiazdek oparta na **{rows_to_show}** najnowszych losowaniach")
    
    # Stwórz i wyświetl wykres dla gwiazdek
    chart_function_stars = CHARTS[chart_type_stars]
    fig_stars = chart_function_stars(chart_data_stars, EXTRA_NUMBER_COLS)
    st.plotly_chart(fig_stars, use_container_width=True)
    
    # =========================================================================
    # SEKCJA 3: STATYSTYKI
    # =========================================================================
    st.divider()
    st.header("📈 Statystyki")
    
    # Nowy suwak do wyboru zakresu danych dla statystyk
    st.markdown("### 🎚️ Zakres danych dla statystyk")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        stats_range = st.slider(
            "Analiza od losowania 1 do:",
            min_value=10,
            max_value=len(df),
            value=len(df),  # Domyślnie wszystkie
            step=10,
            help="Określa zakres losowań do analizy. Np. wartość 250 = losowania od 1 do 250"
        )
    
    with col2:
        st.metric("Zakres", f"1-{stats_range}")
        st.caption(f"{stats_range} losowań")
    
    # Przygotuj dane dla statystyk (od 1 do stats_range)
    stats_data = df.head(stats_range)
    
    st.info(f"📊 Statystyki obliczone na podstawie losowań od **1** do **{stats_range}** (łącznie **{stats_range}** losowań)")
    
    st.divider()
    
    # Renderuj wszystkie włączone statystyki
    for stat_key in ENABLED_STATS:
        if stat_key in STATISTICS:
            stat_function = STATISTICS[stat_key]
            
            # Statystyki gwiazdek używają kolumn gwiazdek
            if stat_key in ['parzystosc_gwiazdki', 'gwiazdki_szostki', 'powtorki_gwiazdki', 'top4_gwiazdki']:
                stat_function(stats_data, EXTRA_NUMBER_COLS)
            else:
                stat_function(stats_data, MAIN_NUMBER_COLS)


if __name__ == "__main__":
    render()