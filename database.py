from supabase import create_client, Client
from settings import SUPABASE_URL, SUPABASE_KEY

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

# Test
if __name__ == "__main__":
    client = get_supabase_client()