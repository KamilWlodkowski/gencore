import streamlit as st
import random
from collections import Counter
from database import fetch_all_eurojackpot_results
import pandas as pd


def get_decade(num):
    """Zwraca numer dziesiątki dla liczby 1-50"""
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


def check_main_numbers_constraints(numbers, last_draw, historical_draws, used_numbers):
    """
    Sprawdza czy główne liczby spełniają wszystkie założenia
    
    Args:
        numbers: lista 5 liczb do sprawdzenia
        last_draw: ostatnie losowanie (5 liczb)
        historical_draws: wszystkie historyczne losowania
        used_numbers: już użyte liczby w tej sesji generowania
    """
    # Sprawdź czy liczby są unikalne w tej sesji
    if any(num in used_numbers for num in numbers):
        return False
    
    # 1. Max 2 liczby z jednej dziesiątki
    decades = [get_decade(num) for num in numbers]
    decade_counts = Counter(decades)
    if any(count > 2 for count in decade_counts.values()):
        return False
    
    # 2. Co najmniej jedna liczba z 2. dziesiątki (11-20)
    if not any(11 <= num <= 20 for num in numbers):
        return False
    
    # 3. Max 3 powtórzenia z historycznymi losowaniami
    for hist_draw in historical_draws[:10]:  # Sprawdź ostatnie 10
        common = len(set(numbers) & set(hist_draw))
        if common > 3:
            return False
    
    # 4. Max 2 powtórzenia z ostatnim losowaniem
    if last_draw:
        common_last = len(set(numbers) & set(last_draw))
        if common_last > 2:
            return False
    
    # 5. Tylko 3-2 lub 2-3 parzystości
    even_count = sum(1 for num in numbers if num % 2 == 0)
    if even_count not in [2, 3]:
        return False
    
    # 6. Unikaj schematu 1-2-3-4-5 (wszystkie dziesiątki)
    unique_decades = set(decades)
    if len(unique_decades) == 5:
        return False
    
    return True


def check_stars_constraints(stars, last_stars, top4_rare, top4_common, used_stars):
    """
    Sprawdza czy gwiazdki spełniają wszystkie założenia
    
    Args:
        stars: lista 2 gwiazdek do sprawdzenia
        last_stars: ostatnie 2 gwiazdki
        top4_rare: 4 najrzadsze gwiazdki
        top4_common: 4 najczęstsze gwiazdki
        used_stars: już użyte gwiazdki w tej sesji
    """
    # Sprawdź czy gwiazdki są unikalne w tej sesji
    if any(star in used_stars for star in stars):
        return False
    
    # 1. Jeśli możliwe: jedna z rare, jedna z common (nie obie z tej samej grupy)
    # (to jest "soft constraint" - jeśli nie da się, można pominąć)
    
    # 2. Tylko 1 parzysta, 1 nieparzysta
    even_count = sum(1 for star in stars if star % 2 == 0)
    if even_count != 1:
        return False
    
    # 3. Brak powtórek z ostatniego losowania
    if last_stars and any(star in last_stars for star in stars):
        return False
    
    # 4. Jedna z 1-6, druga z 7-12
    first_six = sum(1 for star in stars if 1 <= star <= 6)
    if first_six != 1:
        return False
    
    return True


def generate_main_numbers(last_draw, historical_draws, used_numbers, max_attempts=1000):
    """Generuje 5 głównych liczb spełniających wszystkie warunki"""
    for _ in range(max_attempts):
        numbers = sorted(random.sample(range(1, 51), 5))
        if check_main_numbers_constraints(numbers, last_draw, historical_draws, used_numbers):
            return numbers
    return None


def generate_stars(last_stars, top4_rare, top4_common, used_stars, max_attempts=1000):
    """Generuje 2 gwiazdki spełniające wszystkie warunki"""
    for _ in range(max_attempts):
        # Próbuj najpierw z constraint rare/common
        if random.random() < 0.7 and top4_rare and top4_common:  # 70% szans na spełnienie
            # Wybierz jedną z rare, jedną z common
            rare_pool = [s for s in top4_rare if s not in used_stars]
            common_pool = [s for s in top4_common if s not in used_stars]
            
            if rare_pool and common_pool:
                star1 = random.choice(rare_pool)
                star2 = random.choice(common_pool)
                stars = sorted([star1, star2])
                
                if check_stars_constraints(stars, last_stars, top4_rare, top4_common, used_stars):
                    return stars
        
        # Jeśli nie udało się z rare/common, losuj normalnie
        stars = sorted(random.sample(range(1, 13), 2))
        if check_stars_constraints(stars, last_stars, top4_rare, top4_common, used_stars):
            return stars
    
    return None


def render():
    st.title("🎲 Generator losowań Eurojackpot")
    
    st.markdown("""
    Generator tworzy losowania spełniające następujące warunki:
    
    **Główne liczby (5 z 50):**
    - Max 2 liczby z jednej dziesiątki
    - Co najmniej jedna liczba z zakresu 11-20
    - Max 3 powtórzenia z historycznymi losowaniami
    - Max 2 powtórzenia z ostatnim losowaniem
    - Parzystość: 3-2 lub 2-3
    - Unika schematu 1-2-3-4-5 (musi być powtórzenie dziesiątki)
    - Liczby nie powtarzają się między wygenerowanymi losowaniami
    
    **Gwiazdki (2 z 12):**
    - Preferuje pary: jedna z top 4 najrzadszych + jedna z top 4 najczęstszych
    - 1 parzysta, 1 nieparzysta
    - Brak powtórek z ostatnim losowaniem
    - Jedna z 1-6, druga z 7-12
    - Gwiazdki nie powtarzają się między wygenerowanymi losowaniami
    """)
    
    # Pobierz dane historyczne
    draws = fetch_all_eurojackpot_results()
    
    if not draws or len(draws) == 0:
        st.error("Brak danych historycznych. Generator wymaga historii losowań.")
        return
    
    df = pd.DataFrame(draws) if not isinstance(draws, pd.DataFrame) else draws
    
    # Przygotuj dane
    main_cols = ['liczba_1', 'liczba_2', 'liczba_3', 'liczba_4', 'liczba_5']
    star_cols = ['gwiazdka_1', 'gwiazdka_2']
    
    # Ostatnie losowanie
    last_main = [df.iloc[0][col] for col in main_cols if col in df.columns and pd.notna(df.iloc[0][col])]
    last_stars = [df.iloc[0][col] for col in star_cols if col in df.columns and pd.notna(df.iloc[0][col])]
    
    # Historyczne losowania (ostatnie 50)
    historical_main = []
    for i in range(min(50, len(df))):
        draw = [df.iloc[i][col] for col in main_cols if col in df.columns and pd.notna(df.iloc[i][col])]
        if len(draw) == 5:
            historical_main.append(draw)
    
    # Top 4 najrzadsze i najczęstsze gwiazdki
    all_stars = []
    for col in star_cols:
        if col in df.columns:
            all_stars.extend(df[col].dropna().tolist())
    
    star_freq = Counter(all_stars)
    top4_common = [num for num, _ in star_freq.most_common(4)]
    top4_rare = [num for num, _ in star_freq.most_common()[:-5:-1]]
    
    st.divider()
    
    # Input: ile losowań
    col1, col2 = st.columns([2, 1])
    
    with col1:
        num_draws = st.slider(
            "Ile losowań wygenerować?",
            min_value=1,
            max_value=20,
            value=5,
            help="Liczba unikalnych losowań do wygenerowania"
        )
    
    with col2:
        st.metric("Ostatnie losowanie", f"#{len(df)}")
        st.caption(f"Liczby: {', '.join(map(str, last_main))}")
        st.caption(f"Gwiazdki: {', '.join(map(str, last_stars))}")
    
    # Przycisk generowania
    if st.button("🎲 Generuj losowania", type="primary", use_container_width=True):
        
        with st.spinner("Generuję losowania spełniające wszystkie warunki..."):
            generated = []
            used_numbers = set()
            used_stars = set()
            
            failed_count = 0
            max_total_attempts = 100
            
            for i in range(num_draws):
                attempt = 0
                success = False
                
                while attempt < max_total_attempts and not success:
                    # Generuj główne liczby
                    main = generate_main_numbers(last_main, historical_main, used_numbers)
                    
                    if main is None:
                        attempt += 1
                        continue
                    
                    # Generuj gwiazdki
                    stars = generate_stars(last_stars, top4_rare, top4_common, used_stars)
                    
                    if stars is None:
                        attempt += 1
                        continue
                    
                    # Sukces!
                    generated.append({
                        'main': main,
                        'stars': stars
                    })
                    
                    # Dodaj do używanych
                    used_numbers.update(main)
                    used_stars.update(stars)
                    
                    success = True
                
                if not success:
                    failed_count += 1
            
            # Wyświetl wyniki
            if generated:
                st.success(f"✅ Wygenerowano {len(generated)} losowań!")
                
                if failed_count > 0:
                    st.warning(f"⚠️ Nie udało się wygenerować {failed_count} losowań (zbyt restrykcyjne warunki)")
                
                st.divider()
                st.subheader("📋 Wygenerowane losowania")
                
                # Wyświetl w tabeli
                table_data = []
                for idx, draw in enumerate(generated, 1):
                    main_str = ', '.join(map(str, draw['main']))
                    stars_str = ', '.join(map(str, draw['stars']))
                    
                    # Sprawdź schemat dziesiątek
                    decades = [get_decade(num) for num in draw['main']]
                    decade_counts = Counter(decades)
                    schema = '-'.join(str(d) for d in sorted(decades))
                    
                    # Sprawdź parzystość
                    even_count = sum(1 for num in draw['main'] if num % 2 == 0)
                    parity = f"{even_count}P-{5-even_count}N"
                    
                    table_data.append({
                        '#': idx,
                        'Główne liczby': main_str,
                        'Gwiazdki': stars_str,
                        'Schemat': schema,
                        'Parzystość': parity
                    })
                
                result_df = pd.DataFrame(table_data)
                st.dataframe(result_df, use_container_width=True, hide_index=True, height=400)
                
                # Statystyki wygenerowanych
                st.divider()
                st.subheader("📊 Statystyki wygenerowanych losowań")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    all_main = [num for draw in generated for num in draw['main']]
                    unique_main = len(set(all_main))
                    st.metric("Unikalne liczby główne", f"{unique_main}/50")
                
                with col2:
                    all_gen_stars = [star for draw in generated for star in draw['stars']]
                    unique_stars = len(set(all_gen_stars))
                    st.metric("Unikalne gwiazdki", f"{unique_stars}/12")
                
                with col3:
                    # Sprawdź ile par gwiazdek spełnia constraint rare/common
                    rare_common_pairs = 0
                    for draw in generated:
                        stars = draw['stars']
                        if any(s in top4_rare for s in stars) and any(s in top4_common for s in stars):
                            rare_common_pairs += 1
                    
                    percent = (rare_common_pairs / len(generated) * 100) if generated else 0
                    st.metric("Pary rare+common", f"{rare_common_pairs}/{len(generated)}")
                    st.caption(f"{percent:.0f}% spełnia constraint")
                
            else:
                st.error("❌ Nie udało się wygenerować żadnego losowania. Warunki są zbyt restrykcyjne.")
                st.info("💡 Spróbuj wygenerować mniej losowań lub zmodyfikuj warunki w kodzie.")
    
    else:
        st.info("👆 Kliknij przycisk aby wygenerować losowania")