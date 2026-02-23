"""
Konfiguracja wykresów i statystyk - WSZYSTKO W JEDNYM MIEJSCU
Zrefaktoryzowane z: charts.py + statistics.py

Aby dodać nowy wykres:
1. Napisz funkcję wykres_nazwa(df, columns) -> zwraca plotly figure
2. Dodaj do słownika CHARTS

Aby dodać nową statystykę:
1. Napisz funkcję stat_nazwa(df, columns) -> renderuje w Streamlit
2. Dodaj do słownika STATISTICS
3. Dodaj klucz do listy ENABLED_STATS
"""
import streamlit as st
import plotly.graph_objects as go
from collections import Counter


# =============================================================================
# HELPER FUNCTIONS - używane przez wiele wykresów/statystyk
# =============================================================================

def zbierz_liczby(df, columns):
    """
    Zbiera wszystkie liczby z podanych kolumn
    
    Args:
        df: DataFrame z losowaniami
        columns: lista kolumn do przeszukania
    
    Returns:
        lista wszystkich liczb
    """
    all_numbers = []
    for col in columns:
        if col in df.columns:
            all_numbers.extend(df[col].dropna().tolist())
    return all_numbers


def get_color_for_number(num):
    """
    Zwraca kolor dla liczby według dziesiątek
    
    Args:
        num: liczba (1-50)
    
    Returns:
        hex color string
    """
    if 1 <= num <= 10:
        return '#35E8DF'
    elif 11 <= num <= 20:
        return '#F578E2'
    elif 21 <= num <= 30:
        return '#F5B538'
    elif 31 <= num <= 40:
        return '#80F538'
    elif 41 <= num <= 50:
        return '#FFE5FF'
    return '#CCCCCC'


# =============================================================================
# WYKRESY - każda funkcja przyjmuje (df, columns) i zwraca plotly figure
# =============================================================================

def wykres_slupkowy(df, columns):
    """
    Wykres słupkowy częstotliwości występowania liczb
    Oryginalnie: create_frequency_chart()
    """
    all_numbers = zbierz_liczby(df, columns)
    frequency = Counter(all_numbers)
    
    numbers = sorted(frequency.keys())
    counts = [frequency[num] for num in numbers]
    
    # Sprawdź czy to gwiazdki (1-12) czy liczby główne (1-50)
    max_num = max(numbers) if numbers else 0
    is_stars = max_num <= 12
    
    if is_stars:
        # Kolory dla gwiazdek (1-12)
        colors = []
        for num in numbers:
            if 1 <= num <= 6:
                colors.append('#35E8DF')
            elif 7 <= num <= 12:
                colors.append('#FFE4B5')
            else:
                colors.append('#CCCCCC')
        title = 'Częstotliwość występowania liczb dodatkowych (gwiazdek)'
    else:
        # Kolory dla liczb głównych (1-50)
        colors = [get_color_for_number(num) for num in numbers]
        title = 'Częstotliwość występowania liczb głównych'
    
    fig = go.Figure(data=[
        go.Bar(
            x=numbers,
            y=counts,
            marker=dict(
                color=colors,
                line=dict(color='#333333', width=1)
            ),
            text=counts,
            textposition='outside',
            hovertemplate='<b>Liczba:</b> %{x}<br><b>Wystąpienia:</b> %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title='Liczba',
        yaxis_title='Liczba wystąpień',
        xaxis=dict(
            tickmode='linear',
            tick0=1,
            dtick=1
        ),
        height=500,
        showlegend=False,
        hovermode='x'
    )
    
    return fig


def wykres_liniowy(df, columns):
    """
    Wykres liniowy częstotliwości występowania liczb
    Oryginalnie: create_frequency_line_chart()
    """
    all_numbers = zbierz_liczby(df, columns)
    frequency = Counter(all_numbers)
    
    numbers = sorted(frequency.keys())
    counts = [frequency[num] for num in numbers]
    
    # Sprawdź czy to gwiazdki (1-12) czy liczby główne (1-50)
    max_num = max(numbers) if numbers else 0
    is_stars = max_num <= 12
    
    fig = go.Figure()
    
    # Dodaj linię
    fig.add_trace(go.Scatter(
        x=numbers,
        y=counts,
        mode='lines+markers',
        line=dict(color='#4A90E2', width=2),
        marker=dict(size=8, color='#4A90E2'),
        hovertemplate='<b>Liczba:</b> %{x}<br><b>Wystąpienia:</b> %{y}<extra></extra>'
    ))
    
    shapes = []
    title = ''
    
    if is_stars:
        # Tło dla gwiazdek (1-12)
        shapes = [
            dict(type="rect", xref="x", yref="paper", x0=1, x1=6, y0=0, y1=1,
                 fillcolor="#E5F5FF", opacity=0.3, layer="below", line_width=0),
            dict(type="rect", xref="x", yref="paper", x0=7, x1=12, y0=0, y1=1,
                 fillcolor="#FFF5E5", opacity=0.3, layer="below", line_width=0),
        ]
        title = 'Częstotliwość występowania liczb dodatkowych (gwiazdek)'
    else:
        # Tło dla liczb głównych (1-50)
        shapes = [
            dict(type="rect", xref="x", yref="paper", x0=1, x1=10, y0=0, y1=1,
                 fillcolor="#FFE5E5", opacity=0.3, layer="below", line_width=0),
            dict(type="rect", xref="x", yref="paper", x0=11, x1=20, y0=0, y1=1,
                 fillcolor="#E5F5FF", opacity=0.3, layer="below", line_width=0),
            dict(type="rect", xref="x", yref="paper", x0=21, x1=30, y0=0, y1=1,
                 fillcolor="#E5FFE5", opacity=0.3, layer="below", line_width=0),
            dict(type="rect", xref="x", yref="paper", x0=31, x1=40, y0=0, y1=1,
                 fillcolor="#FFF5E5", opacity=0.3, layer="below", line_width=0),
            dict(type="rect", xref="x", yref="paper", x0=41, x1=50, y0=0, y1=1,
                 fillcolor="#FFE5FF", opacity=0.3, layer="below", line_width=0),
        ]
        title = 'Częstotliwość występowania liczb głównych'
    
    fig.update_layout(
        title=title,
        xaxis_title='Liczba',
        yaxis_title='Liczba wystąpień',
        height=500,
        shapes=shapes,
        hovermode='x'
    )
    
    return fig


# =============================================================================
# STATYSTYKI - każda funkcja przyjmuje (df, columns) i renderuje w Streamlit
# =============================================================================

def stat_top4_gwiazdki(df, columns):
    """
    Analiza Top 4 najczęstszych/najrzadszych gwiazdek (prognostyczna)
    Dla każdego losowania od #51 sprawdza ile gwiazdek było z top 4 najczęstszych/najrzadszych
    obliczonych PRZED tym losowaniem
    """
    import pandas as pd
    from collections import Counter
    
    if len(df) < 51:
        st.warning("Za mało danych do analizy Top 4 gwiazdek (potrzeba minimum 51 losowań)")
        return
    
    if len(columns) < 2:
        st.warning("Za mało kolumn dla analizy Top 4 gwiazdek")
        return
    
    st.subheader("📈 Analiza Top 4 najczęstszych/najrzadszych gwiazdek")
    st.caption(f"Analiza prognostyczna od losowania #51 do #{len(df)} ({len(df)-50} losowań)")
    
    # Zliczanie dla top 4 najczęstszych i najrzadszych
    hot_counts = {0: 0, 1: 0, 2: 0}
    cold_counts = {0: 0, 1: 0, 2: 0}
    
    hot_matches_all = []
    cold_matches_all = []
    
    # Dla każdego losowania od 51 wzwyż
    for i in range(50, len(df)):
        # Pobierz wszystkie gwiazdki PRZED tym losowaniem (1 do i-1)
        historical_numbers = []
        for j in range(i):
            numbers = [df.iloc[j][col] for col in columns 
                      if col in df.columns and pd.notna(df.iloc[j][col])]
            historical_numbers.extend(numbers)
        
        # Oblicz częstotliwość
        frequency = Counter(historical_numbers)
        
        # Top 4 najczęstszych
        top_4_hot = set([num for num, _ in frequency.most_common(4)])
        
        # Top 4 najrzadszych (least common)
        top_4_cold = set([num for num, _ in frequency.most_common()[:-5:-1]])
        
        # Pobierz gwiazdki z bieżącego losowania
        current_numbers = set([df.iloc[i][col] for col in columns 
                              if col in df.columns and pd.notna(df.iloc[i][col])])
        
        # Sprawdź ile gwiazdek jest z top 4 hot i cold
        hot_matches = len(current_numbers & top_4_hot)
        cold_matches = len(current_numbers & top_4_cold)
        
        hot_counts[hot_matches] += 1
        cold_counts[cold_matches] += 1
        
        hot_matches_all.append(hot_matches)
        cold_matches_all.append(cold_matches)
    
    # Oblicz średnie
    total_analyzed = len(hot_matches_all)
    avg_hot = sum(hot_matches_all) / total_analyzed if total_analyzed > 0 else 0
    avg_cold = sum(cold_matches_all) / total_analyzed if total_analyzed > 0 else 0
    
    # Metryki podsumowujące
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "🔥 Średnio z TOP 4 najczęstszych",
            f"{avg_hot:.2f} gwiazdek",
            help="Ile średnio gwiazdek z top 4 najczęstszych pojawia się w losowaniu"
        )
    
    with col2:
        st.metric(
            "❄️ Średnio z TOP 4 najrzadszych",
            f"{avg_cold:.2f} gwiazdek",
            help="Ile średnio gwiazdek z top 4 najrzadszych pojawia się w losowaniu"
        )
    
    # Wykresy obok siebie
    col1, col2 = st.columns(2)
    
    with col1:
        # Wykres dla top 4 najczęstszych
        colors_hot = ['#FF6B6B', '#FF8E72', '#FFA07A']
        
        fig_hot = go.Figure(data=[
            go.Bar(
                x=[0, 1, 2],
                y=[hot_counts[i] for i in range(3)],
                marker=dict(
                    color=colors_hot,
                    line=dict(color='#333333', width=1)
                ),
                text=[hot_counts[i] for i in range(3)],
                textposition='outside',
                hovertemplate='<b>Gwiazdek z TOP 4:</b> %{x}<br><b>Losowań:</b> %{y}<extra></extra>'
            )
        ])
        
        max_hot = max(hot_counts.values())
        y_max_hot = max_hot * 1.15
        
        fig_hot.update_layout(
            title='🔥 TOP 4 najczęstszych',
            xaxis_title='Liczba trafień',
            yaxis_title='Liczba losowań',
            yaxis=dict(range=[0, y_max_hot]),
            height=400,
            showlegend=False,
            margin=dict(t=60)
        )
        
        st.plotly_chart(fig_hot, use_container_width=True)
    
    with col2:
        # Wykres dla top 4 najrzadszych
        colors_cold = ['#3498DB', '#5DADE2', '#85C1E9']
        
        fig_cold = go.Figure(data=[
            go.Bar(
                x=[0, 1, 2],
                y=[cold_counts[i] for i in range(3)],
                marker=dict(
                    color=colors_cold,
                    line=dict(color='#333333', width=1)
                ),
                text=[cold_counts[i] for i in range(3)],
                textposition='outside',
                hovertemplate='<b>Gwiazdek z TOP 4:</b> %{x}<br><b>Losowań:</b> %{y}<extra></extra>'
            )
        ])
        
        max_cold = max(cold_counts.values())
        y_max_cold = max_cold * 1.15
        
        fig_cold.update_layout(
            title='❄️ TOP 4 najrzadszych',
            xaxis_title='Liczba trafień',
            yaxis_title='Liczba losowań',
            yaxis=dict(range=[0, y_max_cold]),
            height=400,
            showlegend=False,
            margin=dict(t=60)
        )
        
        st.plotly_chart(fig_cold, use_container_width=True)
    
    # Tabele szczegółowe
    st.markdown("---")
    st.markdown("### 📊 Szczegóły rozkładu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔥 TOP 4 najczęstszych**")
        hot_data = []
        most_common_hot = max(hot_counts, key=hot_counts.get)
        for i in range(3):
            count = hot_counts[i]
            percent = (count / total_analyzed * 100) if total_analyzed > 0 else 0
            is_most = (i == most_common_hot)
            
            hot_data.append({
                'Trafień': f"{i} {'⭐' if is_most else ''}",
                'Losowań': count,
                'Procent': f"{percent:.1f}%"
            })
        
        hot_df = pd.DataFrame(hot_data)
        st.dataframe(hot_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**❄️ TOP 4 najrzadszych**")
        cold_data = []
        most_common_cold = max(cold_counts, key=cold_counts.get)
        for i in range(3):
            count = cold_counts[i]
            percent = (count / total_analyzed * 100) if total_analyzed > 0 else 0
            is_most = (i == most_common_cold)
            
            cold_data.append({
                'Trafień': f"{i} {'⭐' if is_most else ''}",
                'Losowań': count,
                'Procent': f"{percent:.1f}%"
            })
        
        cold_df = pd.DataFrame(cold_data)
        st.dataframe(cold_df, use_container_width=True, hide_index=True)
    
    # Wnioski
    st.markdown("---")
    st.markdown("### 💡 Wnioski")
    
    if avg_hot > avg_cold:
        ratio = avg_hot / avg_cold if avg_cold > 0 else 0
        st.info(f"📊 Gwiazdki z TOP 4 najczęstszych pojawiają się **{ratio:.1f}x częściej** niż gwiazdki z TOP 4 najrzadszych")
    else:
        st.info("📊 Gwiazdki z TOP 4 najrzadszych pojawiają się podobnie często jak gwiazdki z TOP 4 najczęstszych")
    
    # Najczęstsze kombinacje
    st.caption(f"🔥 Najczęściej: {most_common_hot} gwiazdek z TOP 4 najczęstszych ({hot_counts[most_common_hot]} losowań, {hot_counts[most_common_hot]/total_analyzed*100:.1f}%)")
    st.caption(f"❄️ Najczęściej: {most_common_cold} gwiazdek z TOP 4 najrzadszych ({cold_counts[most_common_cold]} losowań, {cold_counts[most_common_cold]/total_analyzed*100:.1f}%)")


def stat_powtorki_gwiazdki(df, columns):
    """
    Analiza powtórek gwiazdek z poprzedniego losowania
    Pokazuje ile gwiazdek powtarza się między kolejnymi losowaniami
    """
    import pandas as pd
    
    if len(df) < 2:
        st.warning("Za mało danych do analizy powtórek gwiazdek (potrzeba minimum 2 losowań)")
        return
    
    if len(columns) < 2:
        st.warning("Za mało kolumn dla analizy powtórek gwiazdek")
        return
    
    # Zlicz powtórki dla każdego losowania
    repeats_count = {0: 0, 1: 0, 2: 0}
    all_repeats = []
    
    for i in range(1, len(df)):
        # Pobierz gwiazdki z bieżącego losowania
        current_numbers = set([df.iloc[i][col] for col in columns 
                               if col in df.columns and pd.notna(df.iloc[i][col])])
        
        # Pobierz gwiazdki z poprzedniego losowania
        previous_numbers = set([df.iloc[i-1][col] for col in columns 
                                if col in df.columns and pd.notna(df.iloc[i-1][col])])
        
        # Policz powtórki
        repeats = len(current_numbers & previous_numbers)
        repeats_count[repeats] += 1
        all_repeats.append(repeats)
    
    # Oblicz statystyki
    total_analyzed = len(all_repeats)
    avg_repeats = sum(all_repeats) / total_analyzed if total_analyzed > 0 else 0
    most_common_repeats = max(repeats_count, key=repeats_count.get)
    most_common_count = repeats_count[most_common_repeats]
    most_common_percent = (most_common_count / total_analyzed * 100) if total_analyzed > 0 else 0
    
    st.subheader("🔁 Powtórki gwiazdek z poprzedniego losowania")
    st.caption(f"Analiza oparta na {total_analyzed} losowaniach")
    
    # Statystyki podsumowujące
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Średnia liczba powtórek gwiazdek", f"{avg_repeats:.2f}")
    
    with col2:
        st.metric(
            "Najczęściej", 
            f"{most_common_repeats} powtórek",
            delta=f"{most_common_percent:.1f}% losowań"
        )
    
    # Wykres słupkowy
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    fig = go.Figure(data=[
        go.Bar(
            x=[0, 1, 2],
            y=[repeats_count[i] for i in range(3)],
            marker=dict(
                color=colors,
                line=dict(color='#333333', width=1)
            ),
            text=[repeats_count[i] for i in range(3)],
            textposition='outside',
            hovertemplate='<b>Powtórek:</b> %{x}<br><b>Losowań:</b> %{y}<extra></extra>'
        )
    ])
    
    # Oblicz maksymalną wartość i dodaj margines
    max_value = max(repeats_count.values())
    y_max = max_value * 1.15
    
    fig.update_layout(
        title='Rozkład liczby powtórek gwiazdek z poprzedniego losowania',
        xaxis_title='Liczba powtórek',
        yaxis_title='Liczba losowań',
        yaxis=dict(range=[0, y_max]),
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1
        ),
        height=500,
        showlegend=False,
        margin=dict(t=80)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela szczegółowa
    st.markdown("---")
    st.markdown("### 📊 Szczegóły")
    
    detail_data = []
    for i in range(3):
        count = repeats_count[i]
        percent = (count / total_analyzed * 100) if total_analyzed > 0 else 0
        is_most_common = (i == most_common_repeats)
        
        detail_data.append({
            'Liczba powtórek': f"{i} {'⭐' if is_most_common else ''}",
            'Liczba losowań': count,
            'Procent': f"{percent:.1f}%"
        })
    
    detail_df = pd.DataFrame(detail_data)
    st.dataframe(detail_df, use_container_width=True, hide_index=True)


def stat_gwiazdki_szostki(df, columns):
    """
    Statystyki gwiazdek - Pierwsza szóstka (1-6) vs Druga szóstka (7-12)
    Pokazuje schematy: 1,1 / 1,2 / 2,2
    """
    import pandas as pd
    
    if len(columns) < 2:
        st.warning("Za mało kolumn dla analizy szóstek gwiazdek")
        return
    
    st.subheader("⭐ Gwiazdki: Pierwsza vs Druga szóstka")
    st.caption("Analiza schematów: 1-6 vs 7-12")
    
    # Zlicz schematy
    schemas = {
        '1,1': 0,  # obie z pierwszej szóstki (1-6)
        '1,2': 0,  # różne (jedna 1-6, jedna 7-12)
        '2,2': 0,  # obie z drugiej szóstki (7-12)
    }
    
    for _, row in df.iterrows():
        # Pobierz 2 gwiazdki
        numbers = [row[col] for col in columns if col in df.columns and pd.notna(row[col])]
        
        if len(numbers) == 2:
            # Sprawdź do której szóstki należą
            first_six_count = sum(1 for num in numbers if 1 <= num <= 6)
            
            if first_six_count == 2:
                schemas['1,1'] += 1
            elif first_six_count == 1:
                schemas['1,2'] += 1
            else:  # first_six_count == 0
                schemas['2,2'] += 1
    
    total_draws = len(df)
    max_count = max(schemas.values()) if schemas.values() else 0
    
    # Wyświetl w 3 kolumnach
    cols = st.columns(3)
    
    for idx, (schema, count) in enumerate(schemas.items()):
        with cols[idx]:
            percent = (count / total_draws * 100) if total_draws > 0 else 0
            is_max = (count == max_count and count > 0)
            
            # Opisy
            if schema == '1,1':
                label = "1,1 (obie 1-6)"
                example = "np. 2, 5"
                color = "#35E8DF"
            elif schema == '1,2':
                label = "1,2 (różne)"
                example = "np. 3, 9"
                color = "#9B59B6"
            else:  # 2,2
                label = "2,2 (obie 7-12)"
                example = "np. 8, 11"
                color = "#FFE4B5"
            
            st.markdown(f"**{label}** {'⭐' if is_max else ''}")
            st.metric(
                label="Losowania",
                value=count,
                delta=f"{percent:.1f}%"
            )
            st.caption(example)
    
    # Wykres
    st.markdown("---")
    
    colors = ['#35E8DF', '#9B59B6', '#FFE4B5']
    
    fig = go.Figure(data=[
        go.Bar(
            x=['1,1', '1,2', '2,2'],
            y=[schemas['1,1'], schemas['1,2'], schemas['2,2']],
            marker=dict(
                color=colors,
                line=dict(color='#333333', width=1)
            ),
            text=[schemas['1,1'], schemas['1,2'], schemas['2,2']],
            textposition='outside',
            hovertemplate='<b>Schemat:</b> %{x}<br><b>Losowań:</b> %{y}<extra></extra>'
        )
    ])
    
    max_value = max(schemas.values())
    y_max = max_value * 1.15
    
    fig.update_layout(
        title='Rozkład schematów: Pierwsza szóstka (1-6) vs Druga szóstka (7-12)',
        xaxis_title='Schemat',
        yaxis_title='Liczba losowań',
        yaxis=dict(range=[0, y_max]),
        height=400,
        showlegend=False,
        margin=dict(t=80)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela szczegółowa
    st.markdown("### 📊 Szczegóły")
    
    detail_data = []
    for schema, count in schemas.items():
        percent = (count / total_draws * 100) if total_draws > 0 else 0
        is_max = (count == max_count and count > 0)
        
        if schema == '1,1':
            description = "Obie z pierwszej szóstki (1-6)"
        elif schema == '1,2':
            description = "Jedna z każdej szóstki"
        else:
            description = "Obie z drugiej szóstki (7-12)"
        
        detail_data.append({
            'Schemat': f"{schema} {'⭐' if is_max else ''}",
            'Opis': description,
            'Liczba losowań': count,
            'Procent': f"{percent:.1f}%"
        })
    
    detail_df = pd.DataFrame(detail_data)
    st.dataframe(detail_df, use_container_width=True, hide_index=True)


def stat_parzystosc_gwiazdki(df, columns):
    """
    Statystyki parzystości gwiazdek (liczb dodatkowych)
    Pokazuje schematy: P,P / P,N / N,N
    """
    import pandas as pd
    
    if len(columns) < 2:
        st.warning("Za mało kolumn dla analizy parzystości gwiazdek")
        return
    
    st.subheader("⭐ Parzystość gwiazdek")
    st.caption("Analiza schematów parzystości dla 2 liczb dodatkowych")
    
    # Zlicz schematy
    schemas = {
        'P,P': 0,  # obie parzyste
        'P,N': 0,  # różne (jedna parzysta, jedna nieparzysta)
        'N,N': 0,  # obie nieparzyste
    }
    
    for _, row in df.iterrows():
        # Pobierz 2 gwiazdki
        numbers = [row[col] for col in columns if col in df.columns and pd.notna(row[col])]
        
        if len(numbers) == 2:
            # Sprawdź parzystość
            even_count = sum(1 for num in numbers if num % 2 == 0)
            
            if even_count == 2:
                schemas['P,P'] += 1
            elif even_count == 1:
                schemas['P,N'] += 1
            else:  # even_count == 0
                schemas['N,N'] += 1
    
    total_draws = len(df)
    max_count = max(schemas.values()) if schemas.values() else 0
    
    # Wyświetl w 3 kolumnach
    cols = st.columns(3)
    
    for idx, (schema, count) in enumerate(schemas.items()):
        with cols[idx]:
            percent = (count / total_draws * 100) if total_draws > 0 else 0
            is_max = (count == max_count and count > 0)
            
            # Opisy
            if schema == 'P,P':
                label = "P,P (obie parzyste)"
                example = "np. 2, 8"
            elif schema == 'P,N':
                label = "P,N (różne)"
                example = "np. 2, 7"
            else:  # N,N
                label = "N,N (obie nieparzyste)"
                example = "np. 3, 9"
            
            st.markdown(f"**{label}** {'⭐' if is_max else ''}")
            st.metric(
                label="Losowania",
                value=count,
                delta=f"{percent:.1f}%"
            )
            st.caption(example)
    
    # Wykres
    st.markdown("---")
    
    colors = ['#3498DB', '#9B59B6', '#E74C3C']
    
    fig = go.Figure(data=[
        go.Bar(
            x=['P,P', 'P,N', 'N,N'],
            y=[schemas['P,P'], schemas['P,N'], schemas['N,N']],
            marker=dict(
                color=colors,
                line=dict(color='#333333', width=1)
            ),
            text=[schemas['P,P'], schemas['P,N'], schemas['N,N']],
            textposition='outside',
            hovertemplate='<b>Schemat:</b> %{x}<br><b>Losowań:</b> %{y}<extra></extra>'
        )
    ])
    
    max_value = max(schemas.values())
    y_max = max_value * 1.15
    
    fig.update_layout(
        title='Rozkład schematów parzystości gwiazdek',
        xaxis_title='Schemat',
        yaxis_title='Liczba losowań',
        yaxis=dict(range=[0, y_max]),
        height=400,
        showlegend=False,
        margin=dict(t=80)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela szczegółowa
    st.markdown("### 📊 Szczegóły")
    
    detail_data = []
    for schema, count in schemas.items():
        percent = (count / total_draws * 100) if total_draws > 0 else 0
        is_max = (count == max_count and count > 0)
        
        detail_data.append({
            'Schemat': f"{schema} {'⭐' if is_max else ''}",
            'Liczba losowań': count,
            'Procent': f"{percent:.1f}%"
        })
    
    detail_df = pd.DataFrame(detail_data)
    st.dataframe(detail_df, use_container_width=True, hide_index=True)


def stat_korelacje(df, columns):
    """
    Analiza korelacji - które liczby często występują razem
    Pokazuje najpopularniejsze pary i trójki liczb
    """
    import pandas as pd
    from itertools import combinations
    from collections import Counter
    
    if len(df) < 10:
        st.warning("Za mało danych do analizy korelacji (potrzeba minimum 10 losowań)")
        return
    
    st.subheader("🔗 Korelacje - liczby występujące razem")
    st.caption(f"Analiza współwystępowania liczb w {len(df)} losowaniach")
    
    # Zbierz wszystkie pary i trójki
    pairs = Counter()
    triplets = Counter()
    
    for _, row in df.iterrows():
        numbers = sorted([row[col] for col in columns 
                         if col in df.columns and pd.notna(row[col])])
        
        if len(numbers) >= 2:
            # Wszystkie pary w tym losowaniu
            for pair in combinations(numbers, 2):
                pairs[pair] += 1
        
        if len(numbers) >= 3:
            # Wszystkie trójki w tym losowaniu
            for triplet in combinations(numbers, 3):
                triplets[triplet] += 1
    
    # Top pary i trójki
    top_pairs = pairs.most_common(20)
    top_triplets = triplets.most_common(15)
    
    total_draws = len(df)
    
    # Tabs dla par i trójek
    tab1, tab2 = st.tabs(["👥 Pary liczb", "👨‍👩‍👦 Trójki liczb"])
    
    with tab1:
        st.markdown("### 🥇 Top 20 par liczb")
        st.caption("Pary które najczęściej występują razem w jednym losowaniu")
        
        if top_pairs:
            # Podział na 2 kolumny
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Top 1-10**")
                pair_data_1 = []
                for idx, (pair, count) in enumerate(top_pairs[:10], 1):
                    percent = (count / total_draws * 100)
                    pair_data_1.append({
                        '#': idx,
                        'Para': f"{pair[0]}, {pair[1]}",
                        'Razem': count,
                        '%': f"{percent:.1f}%"
                    })
                
                df_pairs_1 = pd.DataFrame(pair_data_1)
                st.dataframe(df_pairs_1, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("**Top 11-20**")
                pair_data_2 = []
                for idx, (pair, count) in enumerate(top_pairs[10:20], 11):
                    percent = (count / total_draws * 100)
                    pair_data_2.append({
                        '#': idx,
                        'Para': f"{pair[0]}, {pair[1]}",
                        'Razem': count,
                        '%': f"{percent:.1f}%"
                    })
                
                df_pairs_2 = pd.DataFrame(pair_data_2)
                st.dataframe(df_pairs_2, use_container_width=True, hide_index=True)
            
            # Wykres top 10 par
            st.markdown("---")
            st.markdown("### 📊 Wizualizacja top 10 par")
            
            top_10_pairs = top_pairs[:10]
            pair_labels = [f"{p[0]}-{p[1]}" for p, _ in top_10_pairs]
            pair_counts = [count for _, count in top_10_pairs]
            
            fig_pairs = go.Figure(data=[
                go.Bar(
                    x=pair_labels,
                    y=pair_counts,
                    marker=dict(
                        color='#3498DB',
                        line=dict(color='#333333', width=1)
                    ),
                    text=pair_counts,
                    textposition='outside',
                    hovertemplate='<b>Para:</b> %{x}<br><b>Wystąpienia:</b> %{y}<extra></extra>'
                )
            ])
            
            max_val = max(pair_counts)
            y_max = max_val * 1.15
            
            fig_pairs.update_layout(
                title='Top 10 najczęstszych par liczb',
                xaxis_title='Para liczb',
                yaxis_title='Liczba wystąpień razem',
                yaxis=dict(range=[0, y_max]),
                height=400,
                showlegend=False,
                margin=dict(t=60)
            )
            
            st.plotly_chart(fig_pairs, use_container_width=True)
        else:
            st.info("Brak danych o parach")
    
    with tab2:
        st.markdown("### 🥇 Top 15 trójek liczb")
        st.caption("Trójki które najczęściej występują razem w jednym losowaniu")
        
        if top_triplets:
            triplet_data = []
            for idx, (triplet, count) in enumerate(top_triplets, 1):
                percent = (count / total_draws * 100)
                
                if idx <= 3:
                    medal = ['🥇', '🥈', '🥉'][idx-1]
                else:
                    medal = ''
                
                triplet_data.append({
                    '#': f"{idx} {medal}",
                    'Trójka': f"{triplet[0]}, {triplet[1]}, {triplet[2]}",
                    'Razem': count,
                    '%': f"{percent:.1f}%"
                })
            
            df_triplets = pd.DataFrame(triplet_data)
            st.dataframe(df_triplets, use_container_width=True, hide_index=True, height=400)
            
            # Wykres top 10 trójek
            st.markdown("---")
            st.markdown("### 📊 Wizualizacja top 10 trójek")
            
            top_10_triplets = top_triplets[:10]
            triplet_labels = [f"{t[0]}-{t[1]}-{t[2]}" for t, _ in top_10_triplets]
            triplet_counts = [count for _, count in top_10_triplets]
            
            fig_triplets = go.Figure(data=[
                go.Bar(
                    x=triplet_labels,
                    y=triplet_counts,
                    marker=dict(
                        color='#E74C3C',
                        line=dict(color='#333333', width=1)
                    ),
                    text=triplet_counts,
                    textposition='outside',
                    hovertemplate='<b>Trójka:</b> %{x}<br><b>Wystąpienia:</b> %{y}<extra></extra>'
                )
            ])
            
            max_val = max(triplet_counts)
            y_max = max_val * 1.15
            
            fig_triplets.update_layout(
                title='Top 10 najczęstszych trójek liczb',
                xaxis_title='Trójka liczb',
                yaxis_title='Liczba wystąpień razem',
                yaxis=dict(range=[0, y_max]),
                height=400,
                showlegend=False,
                margin=dict(t=60),
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig_triplets, use_container_width=True)
        else:
            st.info("Brak danych o trójkach")
    
    # Sekcja z praktycznymi wskazówkami
    st.markdown("---")
    st.markdown("### 💡 Jak to wykorzystać?")
    
    if top_pairs:
        top_pair = top_pairs[0]
        pair_percent = (top_pair[1] / total_draws * 100)
        
        st.info(
            f"📊 **Najsilniejsza korelacja:** Para {top_pair[0][0]}-{top_pair[0][1]} "
            f"wystąpiła razem {top_pair[1]} razy ({pair_percent:.1f}% losowań). "
            f"Jeśli obstawiasz {top_pair[0][0]}, rozważ dodanie {top_pair[0][1]}!"
        )
    
    if top_triplets:
        top_triplet = top_triplets[0]
        triplet_percent = (top_triplet[1] / total_draws * 100)
        
        st.success(
            f"🎯 **Najsilniejsza trójka:** {top_triplet[0][0]}-{top_triplet[0][1]}-{top_triplet[0][2]} "
            f"wystąpiła razem {top_triplet[1]} razy ({triplet_percent:.1f}% losowań). "
            f"To silny wzorzec współwystępowania!"
        )


def stat_top10_analiza(df, columns):
    """
    Analiza Top 10 najczęstszych/najrzadszych (prognostyczna)
    Dla każdego losowania od #101 sprawdza ile liczb było z top 10 najczęstszych/najrzadszych
    obliczonych PRZED tym losowaniem
    """
    import pandas as pd
    from collections import Counter
    
    if len(df) < 101:
        st.warning("Za mało danych do analizy Top 10 (potrzeba minimum 101 losowań)")
        return
    
    st.subheader("📈 Analiza Top 10 najczęstszych/najrzadszych")
    st.caption(f"Analiza prognostyczna od losowania #101 do #{len(df)} ({len(df)-100} losowań)")
    
    # Zliczanie dla top 10 najczęstszych i najrzadszych
    hot_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    cold_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    hot_matches_all = []
    cold_matches_all = []
    
    # Dla każdego losowania od 101 wzwyż
    for i in range(100, len(df)):
        # Pobierz wszystkie liczby PRZED tym losowaniem (1 do i-1)
        historical_numbers = []
        for j in range(i):
            numbers = [df.iloc[j][col] for col in columns 
                      if col in df.columns and pd.notna(df.iloc[j][col])]
            historical_numbers.extend(numbers)
        
        # Oblicz częstotliwość
        frequency = Counter(historical_numbers)
        
        # Top 10 najczęstszych
        top_10_hot = set([num for num, _ in frequency.most_common(10)])
        
        # Top 10 najrzadszych (least common)
        top_10_cold = set([num for num, _ in frequency.most_common()[:-11:-1]])
        
        # Pobierz liczby z bieżącego losowania
        current_numbers = set([df.iloc[i][col] for col in columns 
                              if col in df.columns and pd.notna(df.iloc[i][col])])
        
        # Sprawdź ile liczb jest z top 10 hot i cold
        hot_matches = len(current_numbers & top_10_hot)
        cold_matches = len(current_numbers & top_10_cold)
        
        hot_counts[hot_matches] += 1
        cold_counts[cold_matches] += 1
        
        hot_matches_all.append(hot_matches)
        cold_matches_all.append(cold_matches)
    
    # Oblicz średnie
    total_analyzed = len(hot_matches_all)
    avg_hot = sum(hot_matches_all) / total_analyzed if total_analyzed > 0 else 0
    avg_cold = sum(cold_matches_all) / total_analyzed if total_analyzed > 0 else 0
    
    # Metryki podsumowujące
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "🔥 Średnio z TOP 10 najczęstszych",
            f"{avg_hot:.2f} liczb",
            help="Ile średnio liczb z top 10 najczęstszych pojawia się w losowaniu"
        )
    
    with col2:
        st.metric(
            "❄️ Średnio z TOP 10 najrzadszych",
            f"{avg_cold:.2f} liczb",
            help="Ile średnio liczb z top 10 najrzadszych pojawia się w losowaniu"
        )
    
    # Wykresy obok siebie
    col1, col2 = st.columns(2)
    
    with col1:
        # Wykres dla top 10 najczęstszych
        colors_hot = ['#FF6B6B', '#FF8E72', '#FFA07A', '#FFB399', '#FFC5B8', '#FFD7CC']
        
        fig_hot = go.Figure(data=[
            go.Bar(
                x=[0, 1, 2, 3, 4, 5],
                y=[hot_counts[i] for i in range(6)],
                marker=dict(
                    color=colors_hot,
                    line=dict(color='#333333', width=1)
                ),
                text=[hot_counts[i] for i in range(6)],
                textposition='outside',
                hovertemplate='<b>Liczb z TOP 10:</b> %{x}<br><b>Losowań:</b> %{y}<extra></extra>'
            )
        ])
        
        max_hot = max(hot_counts.values())
        y_max_hot = max_hot * 1.15
        
        fig_hot.update_layout(
            title='🔥 TOP 10 najczęstszych',
            xaxis_title='Liczba trafień',
            yaxis_title='Liczba losowań',
            yaxis=dict(range=[0, y_max_hot]),
            height=400,
            showlegend=False,
            margin=dict(t=60)
        )
        
        st.plotly_chart(fig_hot, use_container_width=True)
    
    with col2:
        # Wykres dla top 10 najrzadszych
        colors_cold = ['#3498DB', '#5DADE2', '#85C1E9', '#AED6F1', '#D6EAF8', '#EBF5FB']
        
        fig_cold = go.Figure(data=[
            go.Bar(
                x=[0, 1, 2, 3, 4, 5],
                y=[cold_counts[i] for i in range(6)],
                marker=dict(
                    color=colors_cold,
                    line=dict(color='#333333', width=1)
                ),
                text=[cold_counts[i] for i in range(6)],
                textposition='outside',
                hovertemplate='<b>Liczb z TOP 10:</b> %{x}<br><b>Losowań:</b> %{y}<extra></extra>'
            )
        ])
        
        max_cold = max(cold_counts.values())
        y_max_cold = max_cold * 1.15
        
        fig_cold.update_layout(
            title='❄️ TOP 10 najrzadszych',
            xaxis_title='Liczba trafień',
            yaxis_title='Liczba losowań',
            yaxis=dict(range=[0, y_max_cold]),
            height=400,
            showlegend=False,
            margin=dict(t=60)
        )
        
        st.plotly_chart(fig_cold, use_container_width=True)
    
    # Tabele szczegółowe
    st.markdown("---")
    st.markdown("### 📊 Szczegóły rozkładu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔥 TOP 10 najczęstszych**")
        hot_data = []
        most_common_hot = max(hot_counts, key=hot_counts.get)
        for i in range(6):
            count = hot_counts[i]
            percent = (count / total_analyzed * 100) if total_analyzed > 0 else 0
            is_most = (i == most_common_hot)
            
            hot_data.append({
                'Trafień': f"{i} {'⭐' if is_most else ''}",
                'Losowań': count,
                'Procent': f"{percent:.1f}%"
            })
        
        hot_df = pd.DataFrame(hot_data)
        st.dataframe(hot_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**❄️ TOP 10 najrzadszych**")
        cold_data = []
        most_common_cold = max(cold_counts, key=cold_counts.get)
        for i in range(6):
            count = cold_counts[i]
            percent = (count / total_analyzed * 100) if total_analyzed > 0 else 0
            is_most = (i == most_common_cold)
            
            cold_data.append({
                'Trafień': f"{i} {'⭐' if is_most else ''}",
                'Losowań': count,
                'Procent': f"{percent:.1f}%"
            })
        
        cold_df = pd.DataFrame(cold_data)
        st.dataframe(cold_df, use_container_width=True, hide_index=True)
    
    # Wnioski
    st.markdown("---")
    st.markdown("### 💡 Wnioski")
    
    if avg_hot > avg_cold:
        ratio = avg_hot / avg_cold if avg_cold > 0 else 0
        st.info(f"📊 Liczby z TOP 10 najczęstszych pojawiają się **{ratio:.1f}x częściej** niż liczby z TOP 10 najrzadszych")
    else:
        st.info("📊 Liczby z TOP 10 najrzadszych pojawiają się podobnie często jak liczby z TOP 10 najczęstszych")
    
    # Najczęstsze kombinacje
    st.caption(f"🔥 Najczęściej: {most_common_hot} liczb z TOP 10 najczęstszych ({hot_counts[most_common_hot]} losowań, {hot_counts[most_common_hot]/total_analyzed*100:.1f}%)")
    st.caption(f"❄️ Najczęściej: {most_common_cold} liczb z TOP 10 najrzadszych ({cold_counts[most_common_cold]} losowań, {cold_counts[most_common_cold]/total_analyzed*100:.1f}%)")


def stat_kombinacje_powtorki(df, columns):
    """
    Analiza powtarzających się kombinacji liczb
    Pokazuje ile losowań miało 5/5, 4/5, 3/5, 2/5, 1/5, 0/5 identycznych liczb
    z innymi losowaniami
    """
    import pandas as pd
    from itertools import combinations
    
    if len(df) < 2:
        st.warning("Za mało danych do analizy kombinacji (potrzeba minimum 2 losowań)")
        return
    
    st.subheader("🎲 Powtarzające się kombinacje liczb")
    st.caption(f"Analiza {len(df)} losowań - szukanie identycznych kombinacji")
    
    # Przygotuj wszystkie zestawy liczb z każdego losowania
    all_draws = []
    for i in range(len(df)):
        numbers = set([df.iloc[i][col] for col in columns 
                      if col in df.columns and pd.notna(df.iloc[i][col])])
        all_draws.append(numbers)
    
    # Dla każdego losowania znajdź maksymalną liczbę wspólnych liczb z innymi
    match_counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0: 0}
    
    for i in range(len(all_draws)):
        max_matches = 0
        
        # Porównaj z wszystkimi innymi losowaniami
        for j in range(len(all_draws)):
            if i != j:  # Nie porównuj z samym sobą
                common = len(all_draws[i] & all_draws[j])
                max_matches = max(max_matches, common)
        
        # Zapisz maksymalną liczbę dopasowań dla tego losowania
        match_counts[max_matches] += 1
    
    total_draws = len(df)
    
    # Metryki podsumowujące
    col1, col2, col3 = st.columns(3)
    
    with col1:
        full_matches = match_counts[5]
        st.metric(
            "Pełne powtórki (5/5)",
            full_matches,
            delta=f"{(full_matches/total_draws*100):.1f}%" if total_draws > 0 else "0%"
        )
    
    with col2:
        unique_draws = match_counts[0]
        st.metric(
            "Unikalne zestawy (0/5)",
            unique_draws,
            delta=f"{(unique_draws/total_draws*100):.1f}%" if total_draws > 0 else "0%"
        )
    
    with col3:
        most_common = max(match_counts, key=match_counts.get)
        most_common_count = match_counts[most_common]
        st.metric(
            "Najczęściej",
            f"{most_common}/5 liczb",
            delta=f"{(most_common_count/total_draws*100):.1f}%" if total_draws > 0 else "0%"
        )
    
    # Wykres słupkowy
    colors = ['#E74C3C', '#E67E22', '#F39C12', '#52BE80', '#3498DB', '#9B59B6']
    
    fig = go.Figure(data=[
        go.Bar(
            x=['5/5', '4/5', '3/5', '2/5', '1/5', '0/5'],
            y=[match_counts[5], match_counts[4], match_counts[3], 
               match_counts[2], match_counts[1], match_counts[0]],
            marker=dict(
                color=colors,
                line=dict(color='#333333', width=1)
            ),
            text=[match_counts[5], match_counts[4], match_counts[3], 
                  match_counts[2], match_counts[1], match_counts[0]],
            textposition='outside',
            hovertemplate='<b>Dopasowanie:</b> %{x}<br><b>Losowań:</b> %{y}<extra></extra>'
        )
    ])
    
    # Oblicz maksymalną wartość i dodaj margines
    max_value = max(match_counts.values())
    y_max = max_value * 1.15
    
    fig.update_layout(
        title='Rozkład powtarzających się kombinacji liczb',
        xaxis_title='Liczba identycznych liczb',
        yaxis_title='Liczba losowań',
        yaxis=dict(range=[0, y_max]),
        height=500,
        showlegend=False,
        margin=dict(t=80)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela szczegółowa
    st.markdown("---")
    st.markdown("### 📊 Szczegóły")
    
    detail_data = []
    for i in [5, 4, 3, 2, 1, 0]:
        count = match_counts[i]
        percent = (count / total_draws * 100) if total_draws > 0 else 0
        is_most_common = (count == max(match_counts.values()) and count > 0)
        
        if i == 5:
            label = "5/5 (pełna powtórka)"
        elif i == 0:
            label = "0/5 (unikalne)"
        else:
            label = f"{i}/5 liczb"
        
        detail_data.append({
            'Typ kombinacji': f"{label} {'⭐' if is_most_common else ''}",
            'Liczba losowań': count,
            'Procent': f"{percent:.1f}%"
        })
    
    detail_df = pd.DataFrame(detail_data)
    st.dataframe(detail_df, use_container_width=True, hide_index=True)
    
    # Dodatkowa informacja
    if match_counts[5] > 0:
        st.info(f"🎯 Znaleziono {match_counts[5]} pełnych powtórek (identyczne 5 liczb w różnych losowaniach)!")
    if match_counts[0] > 0:
        st.success(f"✨ {match_counts[0]} losowań to unikalne zestawy - nie dzielą nawet 1 liczby z żadnym innym losowaniem!")


def stat_powtorki(df, columns):
    """
    Analiza powtórek z poprzedniego losowania
    Pokazuje ile liczb powtarza się między kolejnymi losowaniami
    """
    import pandas as pd
    
    if len(df) < 2:
        st.warning("Za mało danych do analizy powtórek (potrzeba minimum 2 losowań)")
        return
    
    # Zlicz powtórki dla każdego losowania
    repeats_count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    all_repeats = []
    
    for i in range(1, len(df)):
        # Pobierz liczby z bieżącego losowania
        current_numbers = set([df.iloc[i][col] for col in columns 
                               if col in df.columns and pd.notna(df.iloc[i][col])])
        
        # Pobierz liczby z poprzedniego losowania
        previous_numbers = set([df.iloc[i-1][col] for col in columns 
                                if col in df.columns and pd.notna(df.iloc[i-1][col])])
        
        # Policz powtórki
        repeats = len(current_numbers & previous_numbers)
        repeats_count[repeats] += 1
        all_repeats.append(repeats)
    
    # Oblicz statystyki
    total_analyzed = len(all_repeats)
    avg_repeats = sum(all_repeats) / total_analyzed if total_analyzed > 0 else 0
    most_common_repeats = max(repeats_count, key=repeats_count.get)
    most_common_count = repeats_count[most_common_repeats]
    most_common_percent = (most_common_count / total_analyzed * 100) if total_analyzed > 0 else 0
    
    st.subheader("🔁 Powtórki z poprzedniego losowania")
    st.caption(f"Analiza oparta na {total_analyzed} losowaniach")
    
    # Statystyki podsumowujące
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Średnia liczba powtórek", f"{avg_repeats:.2f}")
    
    with col2:
        st.metric(
            "Najczęściej", 
            f"{most_common_repeats} powtórek",
            delta=f"{most_common_percent:.1f}% losowań"
        )
    
    # Wykres słupkowy
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
    
    fig = go.Figure(data=[
        go.Bar(
            x=[0, 1, 2, 3, 4, 5],
            y=[repeats_count[i] for i in range(6)],
            marker=dict(
                color=colors,
                line=dict(color='#333333', width=1)
            ),
            text=[repeats_count[i] for i in range(6)],
            textposition='outside',
            hovertemplate='<b>Powtórek:</b> %{x}<br><b>Losowań:</b> %{y}<extra></extra>'
        )
    ])
    
    # Oblicz maksymalną wartość i dodaj margines
    max_value = max(repeats_count.values())
    y_max = max_value * 1.15
    
    fig.update_layout(
        title='Rozkład liczby powtórek z poprzedniego losowania',
        xaxis_title='Liczba powtórek',
        yaxis_title='Liczba losowań',
        yaxis=dict(range=[0, y_max]),
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1
        ),
        height=500,
        showlegend=False,
        margin=dict(t=80)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela szczegółowa
    st.markdown("---")
    st.markdown("### 📊 Szczegóły")
    
    detail_data = []
    for i in range(6):
        count = repeats_count[i]
        percent = (count / total_analyzed * 100) if total_analyzed > 0 else 0
        is_most_common = (i == most_common_repeats)
        
        detail_data.append({
            'Liczba powtórek': f"{i} {'⭐' if is_most_common else ''}",
            'Liczba losowań': count,
            'Procent': f"{percent:.1f}%"
        })
    
    detail_df = pd.DataFrame(detail_data)
    st.dataframe(detail_df, use_container_width=True, hide_index=True)


def stat_hot_cold(df, columns):
    """
    Analiza Hot & Cold - które liczby są w trendzie wzrostowym/spadkowym
    Porównuje ostatnie 20% losowań z poprzednimi 20%
    """
    import pandas as pd
    
    total_draws = len(df)
    
    # Podziel dane na dwie równe części (ostatnie 20% vs poprzednie 20%)
    split_size = max(10, int(total_draws * 0.2))  # Minimum 10 losowań
    
    recent = df.head(split_size)
    previous = df.iloc[split_size:split_size*2] if len(df) > split_size else df.iloc[split_size:]
    
    if len(previous) == 0:
        st.warning("Za mało danych do analizy Hot & Cold (potrzeba minimum 20 losowań)")
        return
    
    # Policz częstotliwości
    recent_freq = Counter()
    previous_freq = Counter()
    
    for col in columns:
        if col in df.columns:
            recent_freq.update(recent[col].dropna().tolist())
            previous_freq.update(previous[col].dropna().tolist())
    
    # Oblicz różnice (trend)
    hot_numbers = []
    cold_numbers = []
    
    all_numbers = set(range(1, 51))  # Dla Eurojackpot 1-50
    
    for num in all_numbers:
        recent_count = recent_freq.get(num, 0)
        previous_count = previous_freq.get(num, 0)
        diff = recent_count - previous_count
        
        if diff > 0:
            hot_numbers.append((num, diff, recent_count, previous_count))
        elif diff < 0:
            cold_numbers.append((num, abs(diff), recent_count, previous_count))
    
    # Sortuj
    hot_numbers.sort(key=lambda x: (x[1], x[2]), reverse=True)
    cold_numbers.sort(key=lambda x: (x[1], -x[2]), reverse=True)
    
    st.subheader("🔥❄️ Hot & Cold Numbers")
    st.caption(f"Porównanie ostatnich {split_size} losowań z poprzednimi {len(previous)} losowaniami")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔥 HOT - Trend wzrostowy")
        st.caption("Liczby które występują częściej ostatnio")
        
        if hot_numbers[:10]:
            # Wyświetl top 10 jako tabelę
            hot_data = []
            for num, diff, recent, previous in hot_numbers[:10]:
                hot_data.append({
                    'Liczba': num,
                    'Trend': f"+{diff}",
                    'Ostatnio': recent,
                    'Wcześniej': previous
                })
            
            hot_df = pd.DataFrame(hot_data)
            st.dataframe(hot_df, use_container_width=True, hide_index=True, height=400)
        else:
            st.info("Brak liczb w trendzie wzrostowym")
    
    with col2:
        st.markdown("### ❄️ COLD - Trend spadkowy")
        st.caption("Liczby które występują rzadziej ostatnio")
        
        if cold_numbers[:10]:
            # Wyświetl top 10 jako tabelę
            cold_data = []
            for num, diff, recent, previous in cold_numbers[:10]:
                cold_data.append({
                    'Liczba': num,
                    'Trend': f"-{diff}",
                    'Ostatnio': recent,
                    'Wcześniej': previous
                })
            
            cold_df = pd.DataFrame(cold_data)
            st.dataframe(cold_df, use_container_width=True, hide_index=True, height=400)
        else:
            st.info("Brak liczb w trendzie spadkowym")


def stat_czestotliwosc(df, columns):
    """
    Statystyki częstotliwości - top 5 najczęstszych i najrzadszych
    Oryginalnie: render_frequency_statistics() + get_frequency_statistics()
    """
    all_numbers = zbierz_liczby(df, columns)
    frequency = Counter(all_numbers)
    
    most_common = frequency.most_common(5)
    least_common = frequency.most_common()[:-6:-1] if len(frequency) >= 5 else []
    average = sum(frequency.values()) / len(frequency) if frequency else 0
    
    st.subheader("📈 Statystyki częstotliwości")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🔥 Top 5 najczęstszych:**")
        for num, count in most_common:
            st.write(f"**{num}**: {count}x")
    
    with col2:
        st.markdown("**❄️ Top 5 najrzadszych:**")
        for num, count in least_common:
            st.write(f"**{num}**: {count}x")
    
    with col3:
        st.metric("Średnia częstotliwość", f"{average:.1f}")


def stat_parzystosc(df, columns):
    """
    Statystyki parzystości liczb
    Rozszerzona wersja niepełnej implementacji z oryginalnego pliku
    + Analiza schematów Parzyste-Nieparzyste (5-0, 4-1, 3-2, etc.)
    """
    all_numbers = zbierz_liczby(df, columns)
    
    even = sum(1 for num in all_numbers if num % 2 == 0)
    odd = len(all_numbers) - even
    total = len(all_numbers)
    
    st.subheader("⚖️ Parzystość")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Parzyste**")
        st.metric("Liczba", even)
        st.caption(f"{even/total*100:.1f}%" if total > 0 else "0%")
    
    with col2:
        st.markdown("**Nieparzyste**")
        st.metric("Liczba", odd)
        st.caption(f"{odd/total*100:.1f}%" if total > 0 else "0%")
    
    with col3:
        st.markdown("**Razem**")
        st.metric("Wszystkich", total)
    
    # =========================================================================
    # NOWA SEKCJA: Analiza schematów Parzyste-Nieparzyste
    # =========================================================================
    st.markdown("---")
    st.markdown("### 📊 Schematy Parzyste-Nieparzyste")
    st.caption("Analiza rozkładu parzystych i nieparzystych liczb w każdym losowaniu")
    
    # Zlicz schematy dla każdego losowania
    schemas = {
        '5-0': 0,  # 5 parzystych, 0 nieparzystych
        '4-1': 0,  # 4 parzyste, 1 nieparzysta
        '3-2': 0,  # 3 parzyste, 2 nieparzyste
        '2-3': 0,  # 2 parzyste, 3 nieparzyste
        '1-4': 0,  # 1 parzysta, 4 nieparzyste
        '0-5': 0,  # 0 parzystych, 5 nieparzystych
    }
    
    import pandas as pd
    
    for _, row in df.iterrows():
        # Pobierz liczby z danego losowania
        numbers = [row[col] for col in columns if col in df.columns and pd.notna(row[col])]
        
        # Policz parzyste w tym losowaniu
        even_count = sum(1 for num in numbers if num % 2 == 0)
        odd_count = len(numbers) - even_count
        
        # Dodaj do odpowiedniego schematu
        schema_key = f"{even_count}-{odd_count}"
        if schema_key in schemas:
            schemas[schema_key] += 1
    
    # Znajdź najczęstszy schemat
    total_draws = len(df)
    max_count = max(schemas.values()) if schemas.values() else 0
    
    # Wyświetl schematy w kolumnach
    cols = st.columns(6)
    
    for idx, (schema, count) in enumerate(schemas.items()):
        with cols[idx]:
            percent = (count / total_draws * 100) if total_draws > 0 else 0
            
            # Wyróżnij najczęstszy schemat
            is_max = (count == max_count and count > 0)
            
            if is_max:
                st.markdown(f"**{schema}** ⭐")
                st.metric(
                    label="Losowania",
                    value=count,
                    delta=f"{percent:.1f}%"
                )
            else:
                st.markdown(f"**{schema}**")
                st.metric(
                    label="Losowania",
                    value=count
                )
                st.caption(f"{percent:.1f}%")
    
    # =========================================================================
    # NOWA SEKCJA: 10 ostatnich losowań z schematami
    # =========================================================================
    st.markdown("---")
    st.markdown("### 📋 10 ostatnich losowań - schematy parzystości")
    
    # Przygotuj dane dla ostatnich 10 losowań
    last_10 = df.head(10)
    
    data_for_table = []
    for idx, row in last_10.iterrows():
        numbers = [row[col] for col in columns if col in df.columns and pd.notna(row[col])]
        
        # Policz parzyste
        even_count = sum(1 for num in numbers if num % 2 == 0)
        odd_count = len(numbers) - even_count
        schema = f"{even_count}-{odd_count}"
        
        # Formatuj liczby z oznaczeniem P/N
        formatted_numbers = []
        for num in numbers:
            if num % 2 == 0:
                formatted_numbers.append(f"{num}(P)")
            else:
                formatted_numbers.append(f"{num}(N)")
        
        # Dodaj datę jeśli istnieje
        date_col = None
        for col in ['data', 'data_losowania', 'date']:
            if col in row.index:
                date_col = row[col]
                break
        
        data_for_table.append({
            'Data': date_col if date_col else f"#{idx}",
            'Liczby': ', '.join(formatted_numbers),
            'Schemat': schema,
            'Parzyste': even_count,
            'Nieparzyste': odd_count
        })
    
    # Wyświetl jako tabelę
    table_df = pd.DataFrame(data_for_table)
    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )


def stat_dziesiatki(df, columns):
    """
    Analiza dziesiątek - które dziesiątki najczęściej występowały
    oraz w jakich schematach (np. 1-2-3-4-5, 1-2-2-4-5, etc.)
    """
    import pandas as pd
    
    def get_decade(num):
        """Zwraca numer dziesiątki (1-5) dla liczby 1-50"""
        if 1 <= num <= 10:
            return 1
        elif 11 <= num <= 20:
            return 2
        elif 21 <= num <= 30:
            return 3
        elif 31 <= num <= 40:
            return 4
        elif 41 <= num <= 50:
            return 5
        return 0
    
    # =========================================================================
    # CZĘŚĆ 1: Częstotliwość dziesiątek (wykres)
    # =========================================================================
    
    all_numbers = zbierz_liczby(df, columns)
    decades_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for num in all_numbers:
        decade = get_decade(num)
        if decade in decades_count:
            decades_count[decade] += 1
    
    st.subheader("📊 Analiza dziesiątek")
    
    # Wykres słupkowy częstotliwości dziesiątek
    colors_map = {
        1: '#35E8DF',
        2: '#F578E2',
        3: '#F5B538',
        4: '#80F538',
        5: '#FFE5FF'
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=['1-10', '11-20', '21-30', '31-40', '41-50'],
            y=[decades_count[i] for i in range(1, 6)],
            marker=dict(
                color=[colors_map[i] for i in range(1, 6)],
                line=dict(color='#333333', width=1)
            ),
            text=[decades_count[i] for i in range(1, 6)],
            textposition='outside',
            hovertemplate='<b>Zakres:</b> %{x}<br><b>Wystąpienia:</b> %{y}<extra></extra>'
        )
    ])
    
    # Oblicz maksymalną wartość i dodaj margines
    max_value = max(decades_count.values())
    y_max = max_value * 1.15  # 15% marginesu nad najwyższym słupkiem
    
    fig.update_layout(
        title='Częstotliwość występowania dziesiątek',
        xaxis_title='Zakres liczb',
        yaxis_title='Liczba wystąpień',
        yaxis=dict(range=[0, y_max]),  # Ustawienie zakresu osi Y
        height=400,
        showlegend=False,
        margin=dict(t=80)  # Zwiększony margines górny
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # =========================================================================
    # CZĘŚĆ 2: Schematy dziesiątek (lista)
    # =========================================================================
    
    st.markdown("---")
    st.markdown("### 🎯 Najczęstsze schematy dziesiątek")
    st.caption("Schemat pokazuje z jakich dziesiątek pochodzą liczby w losowaniu (np. 1-2-3-4-5)")
    
    # Zbierz schematy dla każdego losowania
    schemas = []
    
    for _, row in df.iterrows():
        numbers = [row[col] for col in columns if col in df.columns and pd.notna(row[col])]
        
        # Zamień liczby na dziesiątki i posortuj
        decades = sorted([get_decade(num) for num in numbers])
        
        # Stwórz schemat jako string
        schema = '-'.join(map(str, decades))
        schemas.append(schema)
    
    # Policz częstotliwość schematów
    from collections import Counter
    schema_counts = Counter(schemas)
    
    # Top 15 najczęstszych schematów
    top_schemas = schema_counts.most_common(15)
    total_draws = len(df)
    
    # Wyświetl w 3 kolumnach
    cols = st.columns(3)
    
    for idx, (schema, count) in enumerate(top_schemas):
        col_idx = idx % 3
        with cols[col_idx]:
            percent = (count / total_draws * 100) if total_draws > 0 else 0
            
            # Wyróżnij top 3
            if idx == 0:
                st.markdown(f"**{schema}** 🥇")
            elif idx == 1:
                st.markdown(f"**{schema}** 🥈")
            elif idx == 2:
                st.markdown(f"**{schema}** 🥉")
            else:
                st.markdown(f"**{schema}**")
            
            st.metric(
                label=f"#{idx + 1}",
                value=f"{count} losowań",
                delta=f"{percent:.1f}%"
            )
    
    # =========================================================================
    # NOWA SEKCJA: 10 ostatnich losowań z schematami dziesiątek
    # =========================================================================
    st.markdown("---")
    st.markdown("### 📋 10 ostatnich losowań - schematy dziesiątek")
    
    # Najpierw zbierz wszystkie schematy ze wszystkich losowań (już mamy w schema_counts)
    
    # Przygotuj dane dla ostatnich 10 losowań
    last_10 = df.head(10)
    
    data_for_table = []
    for idx, row in last_10.iterrows():
        numbers = sorted([row[col] for col in columns if col in df.columns and pd.notna(row[col])])
        
        # Zamień liczby na dziesiątki
        decades = [get_decade(num) for num in numbers]
        sorted_decades = sorted(decades)
        schema = '-'.join(map(str, sorted_decades))
        
        # Pobierz częstotliwość tego schematu z wcześniejszych obliczeń
        schema_frequency = schema_counts.get(schema, 0)
        schema_percent = (schema_frequency / total_draws * 100) if total_draws > 0 else 0
        
        # Formatuj liczby z oznaczeniem dziesiątki
        formatted_numbers = []
        for num in numbers:
            decade = get_decade(num)
            formatted_numbers.append(f"{num}({decade})")
        
        # Dodaj datę jeśli istnieje
        date_col = None
        for col in ['data', 'data_losowania', 'date']:
            if col in row.index:
                date_col = row[col]
                break
        
        # Policz ile razy każda dziesiątka wystąpiła
        decade_counts = {}
        for d in range(1, 6):
            count = decades.count(d)
            if count > 0:
                decade_counts[f"Dz.{d}"] = count
        
        data_for_table.append({
            'Data': date_col if date_col else f"#{idx}",
            'Liczby': ', '.join(formatted_numbers),
            'Schemat': schema,
            'Wystąpień': schema_frequency,
            'Procent': f"{schema_percent:.1f}%",
            **decade_counts
        })
    
    # Wyświetl jako tabelę
    table_df = pd.DataFrame(data_for_table)
    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )


# =============================================================================
# REJESTR WYKRESÓW I STATYSTYK
# =============================================================================

# Słownik wykresów - klucz to nazwa w selectbox
CHARTS = {
    'Słupkowy': wykres_slupkowy,
    'Liniowy': wykres_liniowy,
}

# Słownik statystyk - klucz to identyfikator
STATISTICS = {
    'korelacje': stat_korelacje,
    'top10_analiza': stat_top10_analiza,
    'kombinacje_powtorki': stat_kombinacje_powtorki,
    'powtorki': stat_powtorki,
    'hot_cold': stat_hot_cold,
    'czestotliwosc': stat_czestotliwosc,
    'parzystosc': stat_parzystosc,
    'dziesiatki': stat_dziesiatki,
    'parzystosc_gwiazdki': stat_parzystosc_gwiazdki,
    'gwiazdki_szostki': stat_gwiazdki_szostki,
    'powtorki_gwiazdki': stat_powtorki_gwiazdki,
    'top4_gwiazdki': stat_top4_gwiazdki,
}

# Lista włączonych statystyk (komentuj/odkomentuj aby włączyć/wyłączyć)
ENABLED_STATS = [
    'korelacje',
    'top10_analiza',
    'kombinacje_powtorki',
    'powtorki',
    'hot_cold',
    'czestotliwosc',
    'parzystosc',
    'dziesiatki',
    'parzystosc_gwiazdki',
    'gwiazdki_szostki',
    'powtorki_gwiazdki',
    'top4_gwiazdki',
]


# =============================================================================
# JAK DODAĆ NOWY WYKRES - PRZYKŁAD
# =============================================================================
"""
def wykres_histogram(df, columns):
    '''Histogram rozkładu liczb'''
    import plotly.express as px
    all_numbers = zbierz_liczby(df, columns)
    
    fig = px.histogram(
        x=all_numbers,
        nbins=50,
        title='Histogram rozkładu liczb'
    )
    fig.update_layout(
        xaxis_title='Liczba',
        yaxis_title='Częstotliwość',
        height=500
    )
    return fig

# Następnie dodaj do CHARTS:
CHARTS = {
    'Słupkowy': wykres_slupkowy,
    'Liniowy': wykres_liniowy,
    'Histogram': wykres_histogram,  # ← Dodaj tutaj
}
"""


# =============================================================================
# JAK DODAĆ NOWĄ STATYSTYKĘ - PRZYKŁAD
# =============================================================================
"""
def stat_suma(df, columns):
    '''Statystyki sumy wylosowanych liczb'''
    sums = []
    for _, row in df.iterrows():
        numbers = [row[col] for col in columns if col in df.columns and pd.notna(row[col])]
        if numbers:
            sums.append(sum(numbers))
    
    if sums:
        st.subheader("➕ Suma liczb")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Minimalna suma", min(sums))
        with col2:
            st.metric("Średnia suma", f"{sum(sums)/len(sums):.1f}")
        with col3:
            st.metric("Maksymalna suma", max(sums))

# Następnie dodaj do STATISTICS:
STATISTICS = {
    'czestotliwosc': stat_czestotliwosc,
    'parzystosc': stat_parzystosc,
    'suma': stat_suma,  # ← Dodaj tutaj
}

# I włącz w ENABLED_STATS:
ENABLED_STATS = [
    'czestotliwosc',
    'parzystosc',
    'suma',  # ← Dodaj tutaj
]
"""