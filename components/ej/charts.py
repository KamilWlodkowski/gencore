import plotly.graph_objects as go
from collections import Counter

def create_frequency_chart(draws_df, number_columns):
    """
    Tworzy wykres słupkowy częstotliwości występowania liczb
    
    Args:
        draws_df: DataFrame z losowaniami
        number_columns: lista kolumn z liczbami do analizy
    
    Returns:
        plotly figure
    """
    # Zbierz wszystkie liczby
    all_numbers = []
    for col in number_columns:
        if col in draws_df.columns:
            all_numbers.extend(draws_df[col].dropna().tolist())
    
    # Policz częstotliwość
    frequency = Counter(all_numbers)
    
    # Przygotuj dane do wykresu
    numbers = sorted(frequency.keys())
    counts = [frequency[num] for num in numbers]
    
    # Przypisz kolory według dziesiątek
    colors = []
    for num in numbers:
        if 1 <= num <= 10:
            colors.append('#FFE5E5')
        elif 11 <= num <= 20:
            colors.append('#E5F5FF')
        elif 21 <= num <= 30:
            colors.append('#E5FFE5')
        elif 31 <= num <= 40:
            colors.append('#FFF5E5')
        elif 41 <= num <= 50:
            colors.append('#FFE5FF')
        else:
            colors.append('#CCCCCC')
    
    # Stwórz wykres
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


def create_frequency_line_chart(draws_df, number_columns):
    """
    Tworzy wykres liniowy częstotliwości występowania liczb
    
    Args:
        draws_df: DataFrame z losowaniami
        number_columns: lista kolumn z liczbami do analizy
    
    Returns:
        plotly figure
    """
    # Zbierz wszystkie liczby
    all_numbers = []
    for col in number_columns:
        if col in draws_df.columns:
            all_numbers.extend(draws_df[col].dropna().tolist())
    
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


def get_frequency_statistics(draws_df, number_columns):
    """
    Oblicza statystyki częstotliwości liczb
    
    Args:
        draws_df: DataFrame z losowaniami
        number_columns: lista kolumn z liczbami do analizy
    
    Returns:
        dict ze statystykami: {
            'frequency': Counter object,
            'most_common': list of tuples,
            'least_common': list of tuples,
            'average': float,
            'unique_count': int
        }
    """
    # Zbierz wszystkie liczby
    all_numbers = []
    for col in number_columns:
        if col in draws_df.columns:
            all_numbers.extend(draws_df[col].dropna().tolist())
    
    frequency = Counter(all_numbers)
    
    return {
        'frequency': frequency,
        'most_common': frequency.most_common(5),
        'least_common': frequency.most_common()[:-6:-1] if len(frequency) >= 5 else [],
        'average': sum(frequency.values()) / len(frequency) if frequency else 0,
        'unique_count': len(frequency)
    }