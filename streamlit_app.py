import streamlit as st
import requests
import pandas as pd

# Konfiguracja Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

def get_eurojackpot_data():
    try:
        url = f"{SUPABASE_URL}/rest/v1/eurojackpot"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Błąd podczas pobierania danych: {e}")
        return None

# Główna aplikacja
def main():
    st.title("EJ")
    
    # Sidebar z opcjami
    st.sidebar.header("Gry")
    action = st.sidebar.radio("Wybierz akcję:", ["EJ", "MM"])
    
    if action == "EJ":
        # Pobierz dane
        with st.spinner("Ładowanie danych..."):
            data = get_eurojackpot_data()
        
        if data:
            st.success(f"✅ Pobrano {len(data)} rekordów")
            
            # Konwersja do DataFrame dla lepszego wyświetlania
            df = pd.DataFrame(data)
            # Wyświetl dane
            st.subheader("Dane z tabeli")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Brak danych do wyświetlenia")
    elif action == "MM":
        st.subheader("Dane z MM")
    
   
if __name__ == "__main__":
    main()