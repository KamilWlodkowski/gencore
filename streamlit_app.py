import streamlit as st
from supabase import create_client, Client

# Konfiguracja Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

#testSS
# Inicjalizacja klienta Supabase
@st.cache_resource
def init_supabase() -> Client:
    """Inicjalizacja połączenia z Supabase (cachowane)"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_eurojackpot_data():
    """Pobiera dane z tabeli eurojackpot"""
    try:
        supabase = init_supabase()
        response = supabase.table("eurojackpot").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Błąd podczas pobierania danych: {e}")
        return None

# Główna aplikacja
def main():
    st.title("🎰 Eurojackpot - Dane z Supabase")
    
    # Pobierz dane
    with st.spinner("Ładowanie danych..."):
        data = get_eurojackpot_data()
    
    if data:
        st.success(f"Pobrano {len(data)} rekordów")
        
        # Wyświetl dane
        st.subheader("Dane z tabeli eurojackpot")
        st.dataframe(data, use_container_width=True)
        
        # Dodatkowe informacje
        with st.expander("📊 Szczegóły połączenia"):
            st.write(f"Liczba rekordów: {len(data)}")
            if data:
                st.write("Kolumny:", list(data[0].keys()))
    else:
        st.warning("Brak danych do wyświetlenia")

if __name__ == "__main__":
    main()