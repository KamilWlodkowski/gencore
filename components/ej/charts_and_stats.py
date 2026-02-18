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
    colors = [get_color_for_number(num) for num in numbers]
    
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
        title='Częstotliwość występowania liczb głównych',
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
    
    # Dodaj kolorowe tło według dziesiątek
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
    
    fig.update_layout(
        title='Częstotliwość występowania liczb głównych',
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
    'czestotliwosc': stat_czestotliwosc,
    'parzystosc': stat_parzystosc,
    'dziesiatki': stat_dziesiatki,
}

# Lista włączonych statystyk (komentuj/odkomentuj aby włączyć/wyłączyć)
ENABLED_STATS = [
    'czestotliwosc',
    'parzystosc',
    'dziesiatki',
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