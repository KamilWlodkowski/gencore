import datetime
from supabase import create_client, Client
from settings import SUPABASE_URL, SUPABASE_KEY
# database.py
from utils.scraper import (
    scrape_latest_eurojackpot,
    scrape_latest_mini_lotto,
    scrape_latest_multi_multi,
    _parse_date  # jeśli chcesz użyć tej samej funkcji
)
from datetime import datetime

# Globalna zmienna przechowująca klienta (tylko raz inicjowana)
_supabase_client = None

def get_supabase_client() -> Client:
    """Zwraca klienta Supabase (tworzy tylko raz)."""
    global _supabase_client
    if _supabase_client is None:
        try:
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("✅ Połączono z Supabase")
        except Exception as e:
            print(f"❌ Błąd połączenia: {e}")
            raise
    return _supabase_client

# --------------------- EJ ---------------------
def fetch_all_eurojackpot_results() -> list[dict]:
    """
    Fetches all Eurojackpot draw results from the 'eurojackpot' table.
    Returns a list of dictionaries (each dict represents one row).
    """
    client = get_supabase_client()
    
    try:
        response = client.table("eurojackpot").select("*").order("data", desc=True).execute()
        return response.data or []
    except Exception as e:
        print(f"❌ Error fetching Eurojackpot results: {e}")
        raise

# --------------------- MM ---------------------
def fetch_all_multi_multi_results() -> list[dict]:
    """
    Fetches all Multi Multi draw results from the 'multi_multi' table.
    Returns a list of dictionaries (each dict represents one row).
    """
    client = get_supabase_client()
    
    try:
        response = client.table("multi_multi").select("*").order("data", desc=True).execute()
        return response.data or []
    except Exception as e:
        print(f"❌ Error fetching Multi Multi results: {e}")
        raise

# --------------------- ML ---------------------
def fetch_all_mini_lotto_results() -> list[dict]:
    """
    Fetches all mini lotto draw results from the 'mini_lotto' table.
    Returns a list of dictionaries (each dict represents one row).
    """
    client = get_supabase_client()
    
    try:
        response = client.table("mini_lotto").select("*").order("data", desc=True).execute()
        return response.data or []
    except Exception as e:
        print(f"❌ Error fetching Eurojackpot results: {e}")
        raise

# ========================================
# FUNKCJE SCRAPOWANIA I AKTUALIZACJI
# ========================================


def _get_last_draw_date(table_name: str, date_column: str = "data") -> str | None:
    """Pobiera datę ostatniego losowania z danej tabeli (do porównania)."""
    client = get_supabase_client()
    try:
        response = client.table(table_name).select(date_column).order(date_column, desc=True).limit(1).execute()
        if response.data:
            last_date_iso = response.data[0][date_column]
            # Konwertuj ISO na DD-MM-YYYY dla scrapera
            dt = datetime.strptime(last_date_iso, '%Y-%m-%d')
            return dt.strftime('%d-%m-%Y')
        return None
    except Exception as e:
        print(f"⚠️ Nie udało się pobrać ostatniej daty z {table_name}: {e}")
        return None


# --- Eurojackpot ---
def scrape_and_insert_eurojackpot():
    last_date = _get_last_draw_date("eurojackpot")
    new_draws = scrape_latest_eurojackpot(last_date_str=last_date)  # parametry nie używane w funkcji, ale zostawiamy

    if not new_draws:
        return 0

    client = get_supabase_client()
    inserted = 0

    for draw in new_draws:
        data_iso = _parse_date(draw['data'])
        if not data_iso:
            continue

        row = {
            'nr_losowania': draw['nr_losowania'],
            'data': data_iso,
            'liczba_1': draw['liczby_glowne'][0],
            'liczba_2': draw['liczby_glowne'][1],
            'liczba_3': draw['liczby_glowne'][2],
            'liczba_4': draw['liczby_glowne'][3],
            'liczba_5': draw['liczby_glowne'][4],
            'gwiazdka_1': draw['gwiazdki'][0],
            'gwiazdka_2': draw['gwiazdki'][1],
        }

        try:
            client.table("eurojackpot").insert(row).execute()
            inserted += 1
        except Exception as e:
            if "duplicate key" in str(e).lower():
                continue  # już istnieje
            print(f"❌ Błąd wstawiania Eurojackpot {draw['nr_losowania']}: {e}")

    return inserted


# --- Mini Lotto ---
def scrape_and_insert_mini_lotto():
    last_date = _get_last_draw_date("mini_lotto")
    new_draws = scrape_latest_mini_lotto(last_date_str=last_date)

    if not new_draws:
        return 0

    client = get_supabase_client()
    inserted = 0

    for draw in new_draws:
        data_iso = _parse_date(draw['data'])
        if not data_iso:
            continue

        row = {
            'nr_losowania': draw['nr_losowania'],
            'data': data_iso,
            'liczba_1': draw['liczby'][0],
            'liczba_2': draw['liczby'][1],
            'liczba_3': draw['liczby'][2],
            'liczba_4': draw['liczby'][3],
            'liczba_5': draw['liczby'][4],
            'rok': draw['rok'],
        }

        try:
            client.table("mini_lotto").insert(row).execute()
            inserted += 1
        except Exception as e:
            if "duplicate key" in str(e).lower():
                continue
            print(f"❌ Błąd wstawiania Mini Lotto {draw['nr_losowania']}: {e}")

    return inserted


# --- Multi Multi ---
def scrape_and_insert_multi_multi():
    last_date = _get_last_draw_date("multi_multi")
    new_draws = scrape_latest_multi_multi(last_date_str=last_date)

    if not new_draws:
        return 0

    client = get_supabase_client()
    inserted = 0

    for draw in new_draws:
        data_iso = _parse_date(draw['data'])
        if not data_iso:
            continue

        # Parsowanie 20 numerów z stringa
        numery_str = draw['wylosowane_numery'].replace(' ', '')
        numery = [int(n) for n in numery_str.split(',') if n.isdigit()]
        if len(numery) < 20:
            continue

        row = {
            'nr_losowania': draw['nr_losowania'],
            'data': data_iso,
            'godzina': draw['godzina'] or '',
            'rok': draw['rok'],
            'numer_1': numery[0], 'numer_2': numery[1], 'numer_3': numery[2],
            'numer_4': numery[3], 'numer_5': numery[4], 'numer_6': numery[5],
            'numer_7': numery[6], 'numer_8': numery[7], 'numer_9': numery[8],
            'numer_10': numery[9], 'numer_11': numery[10], 'numer_12': numery[11],
            'numer_13': numery[12], 'numer_14': numery[13], 'numer_15': numery[14],
            'numer_16': numery[15], 'numer_17': numery[16], 'numer_18': numery[17],
            'numer_19': numery[18], 'numer_20': numery[19],
        }

        try:
            client.table("multi_multi").insert(row).execute()
            inserted += 1
        except Exception as e:
            if "duplicate key" in str(e).lower():
                continue
            print(f"❌ Błąd wstawiania Multi Multi {draw['nr_losowania']}: {e}")

    return inserted


# --- Główna funkcja aktualizacji ---
def update_all_lotteries() -> dict:
    """
    Aktualizuje wyniki wszystkich trzech loterii (Eurojackpot, Mini Lotto, Multi Multi)
    poprzez scrapowanie i wstawianie nowych losowań do Supabase.
    
    Zwraca słownik z informacjami o liczbie dodanych losowań.
    Nie wyświetla żadnych komunikatów Streamlit (czysta logika).
    """
    euro = scrape_and_insert_eurojackpot()
    mini = scrape_and_insert_mini_lotto()
    multi = scrape_and_insert_multi_multi()
    
    total = euro + mini + multi
    
    return {
        "total": total,
        "eurojackpot": euro,
        "mini_lotto": mini,
        "multi_multi": multi,
        "has_new": total > 0
    }

# Test
if __name__ == "__main__":
    client = get_supabase_client()