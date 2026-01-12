# Google Maps - Sprawdzanie Pozycji Fraz

Profesjonalna aplikacja desktop do monitorowania pozycji fraz kluczowych w wynikach wyszukiwania Google Maps.

## Funkcje

✅ **Zarządzanie Projektami**
- Dodawanie wizytówek Google Business
- Definiowanie lokalizacji (współrzędne GPS)
- Konfiguracja promienia sprawdzania (1-50 km)
- Wybór siatki punktów: 5x5, 7x7, 9x9, 12x12

✅ **Sprawdzanie Pozycji**
- Automatyczne sprawdzanie pozycji w wielu punktach
- Wsparcie dla wielu fraz kluczowych
- System siatki dla dokładnego mapowania
- Wykrywanie pozycji w wynikach wyszukiwania

✅ **Wsparcie Proxy**
- Dodawanie serwerów proxy
- Rotacja proxy podczas sprawdzania
- Testowanie połączeń proxy

✅ **Wizualizacja Mapy**
- Interaktywna mapa z markerami
- Kolorowe oznaczenia (znaleziono/nie znaleziono)
- Siatka punktów sprawdzania
- Wizualizacja promienia

✅ **Harmonogram Sprawdzania**
- Automatyczne sprawdzanie według harmonogramu
- Konfigurowalna częstotliwość (1-168 godzin)
- Sprawdzanie w tle

✅ **Generowanie Raportów**
- Raporty Excel z szczegółowymi danymi
- Raporty PDF z podsumowaniem
- Statystyki dla każdej frazy
- Historia sprawdzania

## Wymagania

- **System operacyjny:** Windows 7/8/10/11
- **Python:** 3.8 lub nowszy
- **Chrome/Chromium:** Wymagany dla Selenium
- **Połączenie internetowe:** Wymagane do sprawdzania

## Instalacja

### 1. Zainstaluj Python

Pobierz Python z [python.org](https://www.python.org/downloads/) i zainstaluj:
- Zaznacz opcję "Add Python to PATH" podczas instalacji
- Wybierz "Install Now"

### 2. Pobierz projekt

```bash
git clone <repository_url>
cd pythonmap
```

### 3. Zainstaluj zależności

Otwórz wiersz polecenia (Command Prompt) w folderze projektu i wykonaj:

```bash
pip install -r requirements.txt
```

### 4. Uruchom aplikację

```bash
python main.py
```

## Szybki Start

### 1. Dodaj Nowy Projekt

1. Kliknij **"➕ Nowy Projekt"**
2. Wypełnij formularz:
   - **Nazwa projektu:** Twoja nazwa (np. "Pizzeria Mario")
   - **Nazwa firmy:** Dokładna nazwa z Google Maps
   - **Współrzędne:** Znajdź w Google Maps (kliknij prawym → "Co tu jest?")
   - **Promień:** Odległość sprawdzania w km
   - **Siatka:** Gęstość punktów sprawdzania

### 2. Dodaj Frazy

1. Wybierz projekt z listy
2. Kliknij **"📝 Zarządzaj Frazami"**
3. Dodaj frazy pojedynczo lub zbiorczo
4. Przykładowe frazy:
   - "pizza"
   - "restauracja włoska"
   - "najlepsza pizza w warszawie"

### 3. Sprawdź Pozycje

1. Wybierz projekt
2. Kliknij **"▶️ Sprawdź Pozycje"**
3. Poczekaj na zakończenie (może potrwać kilka minut)
4. Zobacz wyniki w tabeli

### 4. Zobacz Mapę

1. Po sprawdzeniu kliknij **"🗺️ Pokaż Mapę"**
2. Wybierz frazę z listy
3. Zobacz, gdzie Twoja firma jest widoczna:
   - 🔴 = Lokalizacja firmy
   - 🔵 = Znaleziono w wynikach
   - ⚪ = Nie znaleziono
   - 🟩 = Punkt centralny

### 5. Generuj Raport

1. Kliknij **"📄 Generuj Raport"**
2. Wybierz format (Excel lub PDF)
3. Raport zostanie zapisany w folderze `reports/`

## Konfiguracja Proxy

Jeśli chcesz używać serwerów proxy:

1. Kliknij **"🔒 Proxy"**
2. Dodaj serwery w formatach:
   - `host:port`
   - `http://host:port`
   - `http://user:pass@host:port`
3. Testuj połączenie przed użyciem

## Siatka Punktów

Aplikacja sprawdza pozycje w siatce punktów wokół lokalizacji:

- **5x5** = 25 punktów (szybkie, podstawowe)
- **7x7** = 49 punktów (zalecane)
- **9x9** = 81 punktów (dokładne)
- **12x12** = 144 punkty (bardzo dokładne, wolne)

Im większa siatka, tym dokładniejsze wyniki, ale dłuższy czas sprawdzania.

## Struktura Projektu

```
pythonmap/
├── main.py                 # Punkt wejścia aplikacji
├── requirements.txt        # Zależności Python
├── config/                 # Konfiguracja
│   └── settings.py
├── models/                 # Modele bazy danych
│   ├── database.py
│   ├── project.py
│   ├── keyword.py
│   ├── check_result.py
│   └── proxy.py
├── services/               # Logika biznesowa
│   ├── google_maps_checker.py
│   ├── grid_calculator.py
│   ├── proxy_manager.py
│   └── report_generator.py
├── ui/                     # Interfejs graficzny
│   ├── main_window.py
│   ├── project_dialog.py
│   ├── keyword_dialog.py
│   ├── proxy_dialog.py
│   └── map_view.py
├── utils/                  # Narzędzia pomocnicze
│   └── scheduler.py
├── data/                   # Baza danych (auto-tworzony)
└── reports/                # Wygenerowane raporty (auto-tworzony)
```

## Baza Danych

Aplikacja używa SQLite. Baza jest automatycznie tworzona przy pierwszym uruchomieniu w folderze `data/pythonmap.db`.

### Tabele:
- **projects** - Projekty z lokalizacjami
- **keywords** - Frazy kluczowe
- **check_results** - Wyniki sprawdzania
- **proxies** - Serwery proxy
- **schedules** - Harmonogramy sprawdzania

## Rozwiązywanie Problemów

### Aplikacja nie uruchamia się

1. Sprawdź wersję Python: `python --version` (minimum 3.8)
2. Zainstaluj ponownie zależności: `pip install -r requirements.txt --force-reinstall`
3. Sprawdź logi w pliku `pythonmap.log`

### Chrome Driver nie działa

Aplikacja automatycznie pobiera odpowiedni ChromeDriver. Jeśli wystąpią problemy:
1. Upewnij się, że Chrome/Chromium jest zainstalowany
2. Zaktualizuj Chrome do najnowszej wersji
3. Usuń folder cache: `~/.wdm/` (Linux/Mac) lub `%USERPROFILE%\.wdm\` (Windows)

### Sprawdzanie jest wolne

1. Zmniejsz rozmiar siatki (np. z 9x9 na 5x5)
2. Zmniejsz liczbę fraz
3. Zwiększ opóźnienie między sprawdzeniami w `config/settings.py`

### Firma nie jest wykrywana

1. Upewnij się, że nazwa firmy jest dokładnie taka sama jak w Google Maps
2. Sprawdź współrzędne (powinna być lokalizacja firmy)
3. Zwiększ promień sprawdzania
4. Użyj różnych fraz kluczowych

### Problemy z proxy

1. Testuj proxy przed użyciem (przycisk "Testuj")
2. Sprawdź format: `host:port` lub `protocol://host:port`
3. Upewnij się, że proxy obsługuje HTTPS

## Wskazówki

💡 **Optymalne ustawienia:**
- Siatka: 7x7
- Promień: 3-5 km
- Częstotliwość: 24 godziny
- Opóźnienie: 2-3 sekundy

💡 **Dobre praktyki:**
- Używaj konkretnych, lokalnych fraz
- Regularnie sprawdzaj pozycje (codziennie lub co kilka dni)
- Monitoruj konkurencję (dodaj jako osobne projekty)
- Generuj raporty do analizy trendów

💡 **Unikaj:**
- Zbyt częstego sprawdzania (może być postrzegane jako spam)
- Zbyt małych opóźnień (<1 sekundy)
- Sprawdzania bez proxy przy dużej liczbie żądań

## API i Integracje

Aplikacja może być rozszerzona o:
- Google Places API (opcjonalnie)
- Automatyczne wysyłanie raportów email
- Integrację z Google Analytics
- Webhook do powiadomień

## Licencja

Ten projekt jest przeznaczony do użytku edukacyjnego i komercyjnego.

## Wsparcie

W razie problemów:
1. Sprawdź ten README
2. Zobacz logi w `pythonmap.log`
3. Sprawdź Issues na GitHub

## Changelog

### v1.0.0 (2026-01-12)
- Pierwsza wersja
- Zarządzanie projektami i frazami
- Sprawdzanie pozycji w Google Maps
- System siatki punktów
- Wsparcie proxy
- Wizualizacja mapy
- Generowanie raportów Excel/PDF
- Harmonogram sprawdzania

## Roadmap

Planowane funkcje:
- [ ] Eksport danych do CSV
- [ ] Porównanie zmian w czasie (wykresy)
- [ ] Powiadomienia email
- [ ] Integracja z Google Places API
- [ ] Panel statystyk i dashboards
- [ ] Eksport map do PNG
- [ ] Wsparcie dla wielu języków

---

**Autor:** PythonMap Team
**Wersja:** 1.0.0
**Data:** 2026-01-12
