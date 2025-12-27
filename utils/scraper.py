# scraper.py
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from typing import List, Dict, Optional


def _parse_date(date_str: str) -> Optional[str]:
    """
    Parsuje datę z formatu DD-MM-YYYY na ISO (YYYY-MM-DD) dla Supabase.
    Zwraca None jeśli nie uda się sparsować.
    """
    try:
        dt = datetime.strptime(date_str.strip(), '%d-%m-%Y')
        return dt.date().isoformat()
    except ValueError:
        return None


def scrape_latest_eurojackpot(last_date_str: Optional[str] = None) -> List[Dict]:
    """Scrapuje najnowsze losowania Eurojackpot z bieżącego roku."""
    current_year = datetime.now().year
    url = f"https://megalotto.pl/wyniki/eurojackpot/losowania-z-roku-{current_year}"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        lista_losowan = soup.find('div', class_='lista_ostatnich_losowan')
        if not lista_losowan:
            return []

        uls = lista_losowan.find_all('ul')
        new_draws = []

        last_date_obj = datetime.strptime(last_date_str, '%d-%m-%Y').date() if last_date_str else None

        for ul in uls:
            try:
                nr_elem = ul.find('li', class_='nr_in_list')
                date_elem = ul.find('li', class_='date_in_list')
                if not nr_elem or not date_elem:
                    continue

                nr_losowania = int(nr_elem.get_text(strip=True).replace('.', '').strip())
                data_str = date_elem.get_text(strip=True)

                current_date_obj = datetime.strptime(data_str, '%d-%m-%Y').date()
                if last_date_obj and current_date_obj <= last_date_obj:
                    continue

                liczby_glowne = [int(li.get_text(strip=True)) for li in ul.find_all('li', class_='numbers_in_list') if li.get_text(strip=True).isdigit()]
                gwiazdki = []
                for li in ul.find_all('li', class_='tsn_number_in_list'):
                    strong = li.find('strong')
                    text = strong.get_text(strip=True) if strong else li.get_text(strip=True)
                    if text.isdigit():
                        gwiazdki.append(int(text))

                if len(liczby_glowne) == 5 and len(gwiazdki) == 2:
                    new_draws.append({
                        'nr_losowania': nr_losowania,
                        'data': data_str,  # zostawiamy DD-MM-YYYY – konwersja w database.py
                        'liczby_glowne': liczby_glowne,
                        'gwiazdki': gwiazdki,
                        'rok': current_year
                    })
            except Exception:
                continue

        return new_draws

    except Exception:
        return []


def scrape_latest_mini_lotto(last_date_str: Optional[str] = None) -> List[Dict]:
    """Scrapuje najnowsze losowania Mini Lotto."""
    current_year = datetime.now().year
    url = f"https://megalotto.pl/wyniki/mini-lotto/losowania-z-roku-{current_year}"

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        lista_losowan = soup.find('div', class_='lista_ostatnich_losowan')
        if not lista_losowan:
            return []

        uls = lista_losowan.find_all('ul')
        new_draws = []

        last_date_obj = datetime.strptime(last_date_str, '%d-%m-%Y').date() if last_date_str else None

        for ul in uls:
            try:
                nr_elem = ul.find('li', class_='nr_in_list')
                date_elem = ul.find('li', class_='date_in_list')
                if not nr_elem or not date_elem:
                    continue

                nr_losowania = int(nr_elem.get_text(strip=True).replace('.', '').strip())
                data_str = date_elem.get_text(strip=True)

                current_date_obj = datetime.strptime(data_str, '%d-%m-%Y').date()
                if last_date_obj and current_date_obj <= last_date_obj:
                    continue

                liczby = [int(li.get_text(strip=True)) for li in ul.find_all('li', class_='numbers_in_list') if li.get_text(strip=True).isdigit()]

                if len(liczby) == 5:
                    new_draws.append({
                        'nr_losowania': nr_losowania,
                        'data': data_str,
                        'liczby': liczby,
                        'rok': current_year
                    })
            except Exception:
                continue

        return new_draws

    except Exception:
        return []


def scrape_latest_multi_multi(last_date_str: Optional[str] = None) -> List[Dict]:
    """Scrapuje najnowsze losowania Multi Multi."""
    current_year = datetime.now().year
    url = f"https://megalotto.pl/wyniki/multi-multi/losowania-z-roku-{current_year}"

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        lista_losowan = soup.find('div', class_='lista_ostatnich_losowan')
        if not lista_losowan:
            return []

        uls = lista_losowan.find_all('ul')
        new_draws = []

        last_date_obj = datetime.strptime(last_date_str, '%d-%m-%Y').date() if last_date_str else None

        for ul in uls:
            try:
                nr_elem = ul.find('li', class_='nr_in_list')
                date_elem = ul.find('li', class_='date_in_list')
                if not nr_elem or not date_elem:
                    continue

                nr_losowania = int(nr_elem.get_text(strip=True).replace('.', '').strip())
                data_str = date_elem.get_text(strip=True)

                current_date_obj = datetime.strptime(data_str, '%d-%m-%Y').date()
                if last_date_obj and current_date_obj <= last_date_obj:
                    continue

                divs_with_balls = ul.find_all('div', class_=re.compile(r'wiersz_z_kulkami'))
                numery = []
                godzina = None

                for div in divs_with_balls:
                    godzina_span = div.find('span', class_='multi_multi_wyniki_godzina')
                    if godzina_span and not godzina:
                        godzina = godzina_span.get_text(strip=True)

                    for li in div.find_all('li', class_='numbers_in_list'):
                        text = li.get_text(strip=True).strip()
                        if text.isdigit():
                            numery.append(text)

                    for span in div.find_all('span', class_='pierwsza_liczba_w_nowym_wierszu'):
                        text = span.get_text(strip=True).strip()
                        if text.isdigit():
                            numery.append(text)

                if len(numery) >= 20:
                    new_draws.append({
                        'nr_losowania': nr_losowania,
                        'data': data_str,
                        'godzina': godzina or '',
                        'wylosowane_numery': ', '.join(numery),
                        'rok': current_year
                    })
            except Exception:
                continue

        return new_draws

    except Exception:
        return []