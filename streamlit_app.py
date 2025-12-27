import streamlit as st
from settings import PAGE_CONFIG, APP_TITLE
from database import update_all_lotteries

st.set_page_config(**PAGE_CONFIG)

st.title(APP_TITLE)

# === JEDEN WSPÓLNY GUZIK ===
if st.button("🔄 Aktualizuj wszystkie wyniki loterii", 
             use_container_width=True, 
             type="primary"):
    
    with st.spinner("Scrapowanie i aktualizacja wyników..."):
        result = update_all_lotteries()  # zwraca dict z poprzedniej wersji
    
    # Komunikat sukcesu
    if result["has_new"]:
        st.success(
            f"✅ Pobrano i dodano **{result['total']}** nowych losowań!\n\n"
            f"• Eurojackpot: **{result['eurojackpot']}**\n"
            f"• Mini Lotto: **{result['mini_lotto']}**\n"
            f"• Multi Multi: **{result['multi_multi']}**"
        )
    else:
        st.success("✅ Wszystkie wyniki są już aktualne – brak nowych losowań")

    