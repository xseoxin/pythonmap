# Instrukcja Instalacji - Windows

## Krok po kroku dla początkujących

### 1. Zainstaluj Python

1. Wejdź na [python.org/downloads](https://www.python.org/downloads/)
2. Pobierz najnowszą wersję Python (np. Python 3.11)
3. Uruchom instalator
4. **WAŻNE:** Zaznacz opcję **"Add Python to PATH"** na pierwszym ekranie!
5. Kliknij "Install Now"
6. Poczekaj na zakończenie instalacji

### 2. Pobierz projekt

**Opcja A: Git (jeśli masz)**
```bash
git clone <URL_REPOZYTORIUM>
cd pythonmap
```

**Opcja B: Bez Git**
1. Pobierz ZIP z projektem
2. Rozpakuj do folderu (np. `C:\pythonmap`)
3. Otwórz folder

### 3. Zainstaluj zależności

**Metoda automatyczna (zalecana):**
1. W folderze projektu znajdź plik `install.bat`
2. Kliknij prawym przyciskiem myszy → "Uruchom jako administrator"
3. Poczekaj na zakończenie instalacji

**Metoda ręczna:**
1. Otwórz wiersz polecenia (Command Prompt):
   - Naciśnij `Windows + R`
   - Wpisz `cmd` i naciśnij Enter
2. Przejdź do folderu projektu:
   ```bash
   cd C:\sciezka\do\pythonmap
   ```
3. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Uruchom aplikację

**Metoda automatyczna:**
1. Kliknij dwukrotnie na `run.bat`

**Metoda ręczna:**
1. W wierszu polecenia wpisz:
   ```bash
   python main.py
   ```

## Weryfikacja instalacji

Po uruchomieniu powinieneś zobaczyć okno aplikacji z:
- Lista projektów (początkowo pusta)
- Przyciski "Nowy Projekt", "Edytuj", "Usuń"
- Panel szczegółów projektu

## Częste problemy

### "Python nie jest rozpoznawany..."

**Rozwiązanie:**
1. Odinstaluj Python
2. Zainstaluj ponownie, **ZAZNACZAJĄC** "Add Python to PATH"
3. Uruchom komputer ponownie
4. Spróbuj ponownie

### "pip nie jest rozpoznawany..."

**Rozwiązanie:**
```bash
python -m pip install -r requirements.txt
```

### Problemy z instalacją pakietów

**Rozwiązanie:**
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt --upgrade
```

### Aplikacja się nie uruchamia

1. Sprawdź plik `pythonmap.log` w folderze projektu
2. Upewnij się, że wszystkie zależności są zainstalowane
3. Spróbuj zainstalować ponownie:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

## Wymagania systemowe

- **System:** Windows 7/8/10/11 (64-bit zalecany)
- **RAM:** Minimum 2 GB (zalecane 4 GB)
- **Procesor:** Dowolny nowszy procesor
- **Miejsce na dysku:** ~500 MB
- **Internet:** Wymagane do sprawdzania pozycji

## Pierwsza konfiguracja

Po pierwszym uruchomieniu:

1. **Dodaj pierwszy projekt:**
   - Kliknij "Nowy Projekt"
   - Wpisz nazwę (np. "Moja Pizzeria")
   - Wpisz dokładną nazwę z Google Maps
   - Znajdź współrzędne swojej firmy w Google Maps
   - Wybierz promień (zacznij od 5 km)
   - Wybierz siatkę (zacznij od 5x5)

2. **Dodaj frazy:**
   - Wybierz projekt
   - Kliknij "Zarządzaj Frazami"
   - Dodaj frazy, np.: "pizza", "pizzeria", "restauracja"

3. **Sprawdź pozycje:**
   - Kliknij "Sprawdź Pozycje"
   - Poczekaj (może potrwać 2-5 minut dla siatki 5x5)

4. **Zobacz wyniki:**
   - Sprawdź tabelę z wynikami
   - Kliknij "Pokaż Mapę" aby zobaczyć wizualizację
   - Kliknij "Generuj Raport" aby zapisać wyniki

## Wsparcie

Jeśli masz problemy:
1. Przeczytaj README.md
2. Sprawdź plik pythonmap.log
3. Upewnij się, że Chrome/Chromium jest zainstalowany
4. Spróbuj uruchomić jako administrator

## Co dalej?

- Przeczytaj pełny README.md dla szczegółowych informacji
- Eksperymentuj z różnymi ustawieniami
- Dodaj więcej projektów i fraz
- Generuj regularne raporty
- Rozważ użycie proxy dla większej liczby sprawdzeń

---

Powodzenia! 🚀
