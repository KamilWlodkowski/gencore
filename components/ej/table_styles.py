import streamlit as st
import pandas as pd

def color_by_decade(val):
    """Koloruje komórki według dziesiątek"""
    if pd.isna(val):
        return ''
    
    try:
        num = int(val)
    except (ValueError, TypeError):
        return ''
    
    if 1 <= num <= 10:
        return 'background-color: #35E8DF; color: black'
    elif 11 <= num <= 20:
        return 'background-color: #F578E2; color: black'
    elif 21 <= num <= 30:
        return 'background-color: #F5B538; color: black'
    elif 31 <= num <= 40:
        return 'background-color: #80F538; color: black'
    elif 41 <= num <= 50:
        return 'background-color: #FFE5FF; color: black'
    return ''

def color_extra_numbers(val):
    """Koloruje liczby dodatkowe (1-12)"""
    if pd.isna(val):
        return ''
    
    try:
        num = int(val)
    except (ValueError, TypeError):
        return ''
    
    if 1 <= num <= 6:
        return 'background-color: #35E8DF; color: black; font-weight: bold'
    elif 7 <= num <= 12:
        return 'background-color: #FFE4B5; color: black; font-weight: bold'
    return ''

def apply_eurojackpot_styles(df, main_number_cols=None, extra_number_cols=None):
    """
    Aplikuje style do DataFrame z wynikami Eurojackpot
    
    Args:
        df: pandas DataFrame
        main_number_cols: lista kolumn z liczbami głównymi (1-50)
        extra_number_cols: lista kolumn z liczbami dodatkowymi (1-12)
    
    Returns:
        Styled DataFrame
    """
    if main_number_cols is None:
        main_number_cols = []
    if extra_number_cols is None:
        extra_number_cols = []
    
    # Filtruj tylko istniejące kolumny
    main_cols_exist = [col for col in main_number_cols if col in df.columns]
    extra_cols_exist = [col for col in extra_number_cols if col in df.columns]
    
    styled_df = df.style
    
    if main_cols_exist:
        styled_df = styled_df.applymap(color_by_decade, subset=main_cols_exist)
    
    if extra_cols_exist:
        styled_df = styled_df.applymap(color_extra_numbers, subset=extra_cols_exist)
    
    return styled_df