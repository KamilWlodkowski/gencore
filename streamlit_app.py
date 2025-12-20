import streamlit as st
import requests
import pandas as pd

# Konfiguracja Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

def get_eurojackpot_data():
    """Pobiera dane z tabeli eurojackpot przez REST API"""
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

def insert_eurojackpot_data(data):
    """Wstawia nowe dane do tabeli eurojackpot"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/eurojackpot"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Błąd podczas dodawania danych: {e}")
        return None

# Główna aplikacja
def main():
    st.title("🎰 Eurojackpot - Dane z Supabase")
    
    # Sidebar z opcjami
    st.sidebar.header("Opcje")
    action = st.sidebar.radio("Wybierz akcję:", ["Wyświetl dane", "Dodaj nowy rekord"])
    
    if action == "Wyświetl dane":
        # Pobierz dane
        with st.spinner("Ładowanie danych..."):
            data = get_eurojackpot_data()
        
        if data:
            st.success(f"✅ Pobrano {len(data)} rekordów")
            
            # Konwersja do DataFrame dla lepszego wyświetlania
            df = pd.DataFrame(data)
            
            # Wyświetl dane
            st.subheader("Dane z tabeli eurojackpot")
            st.dataframe(df, use_container_width=True)
            
            # Dodatkowe informacje
            with st.expander("📊 Szczegóły"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Liczba rekordów", len(data))
                with col2:
                    st.metric("Liczba kolumn", len(df.columns))
                st.write("**Kolumny:**", ", ".join(df.columns.tolist()))
        else:
            st.warning("Brak danych do wyświetlenia")
    
    elif action == "Dodaj nowy rekord":
        st.subheader("➕ Dodaj nowy rekord")
        st.info("Dostosuj pola zgodnie ze strukturą twojej tabeli")
        
        # Przykładowy formularz - dostosuj do swoich kolumn
        with st.form("add_record"):
            col1, col2 = st.columns(2)
            
            # Przykładowe pola - zmień je zgodnie z twoją strukturą tabeli
            field1 = col1.text_input("Pole 1")
            field2 = col2.text_input("Pole 2")
            
            submit = st.form_submit_button("Dodaj rekord")
            
            if submit:
                new_data = {
                    "field1": field1,
                    "field2": field2
                    # Dodaj więcej pól zgodnie z twoją strukturą
                }
                
                result = insert_eurojackpot_data(new_data)
                if result:
                    st.success("✅ Rekord został dodany!")
                    st.json(result)

if __name__ == "__main__":
    main()