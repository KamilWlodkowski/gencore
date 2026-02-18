import streamlit as st

def render_frequency_statistics(stats):
    """
    Wyświetla statystyki częstotliwości
    
    Args:
        stats: dict ze statystykami z get_frequency_statistics()
    """
    st.subheader("📈 Statystyki")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🔥 Top 5 najczęstszych:**")
        for num, count in stats['most_common']:
            st.write(f"**{num}**: {count}x")
    
    with col2:
        st.markdown("**❄️ Top 5 najrzadszych:**")
        for num, count in stats['least_common']:
            st.write(f"**{num}**: {count}x")
    
    with col3:
        st.metric("Średnia częstotliwość", f"{stats['average']:.1f}")

    st.subheader("Parzystość")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Parzyste**")
    
    with col2:
        st.markdown("**Nieparzyste**")

    with col3:
        st.markdown("**Inne**")
