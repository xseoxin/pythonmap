# 🚀 SZYBKI START - Instalacja Python i Aplikacji

## Krok 1: Zainstaluj Python (5 minut)

### A. Pobierz Python

1. Otwórz przeglądarkę
2. Wejdź na: **https://www.python.org/downloads/**
3. Kliknij duży żółty przycisk **"Download Python 3.x.x"** (najnowsza wersja)
4. Poczekaj na pobranie pliku (około 25 MB)

### B. Zainstaluj Python

**⚠️ BARDZO WAŻNE:**

1. **Uruchom pobrany plik** (np. `python-3.11.x.exe`)

2. **NA PIERWSZYM EKRANIE:**
   - ✅ **ZAZNACZ** checkbox: **"Add Python to PATH"** (na dole okna!)
   - ✅ **ZAZNACZ** checkbox: **"Add Python to environment variables"**
   - To jest KLUCZOWE! Bez tego aplikacja nie będzie działać!

3. **Kliknij:** "Install Now" (instalacja dla wszystkich użytkowników)

4. **Poczekaj** na instalację (2-3 minuty)

5. **Kliknij:** "Close" gdy instalacja się zakończy

### C. Zrestartuj komputer (zalecane)

Po instalacji Pythona najlepiej zrestartować komputer, aby zmienne środowiskowe zostały załadowane.

---

## Krok 2: Sprawdź instalację Python

### Metoda 1: Automatyczna
1. W folderze projektu znajdź plik: **`check_python.bat`**
2. Kliknij dwukrotnie
3. Jeśli zobaczysz numer wersji Python - wszystko OK!

### Metoda 2: Ręczna
1. Naciśnij **`Windows + R`**
2. Wpisz: **`cmd`** i naciśnij Enter
3. Wpisz: **`python --version`** i naciśnij Enter
4. Powinieneś zobaczyć: `Python 3.11.x` (lub podobne)

**Jeśli widzisz błąd:**
- Sprawdź, czy zaznaczyłeś "Add Python to PATH" podczas instalacji
- Zrestartuj komputer
- Jeśli dalej nie działa, odinstaluj Python i zainstaluj ponownie (z zaznaczonym PATH!)

---

## Krok 3: Zainstaluj aplikację

### Metoda Automatyczna (zalecana):
1. W folderze projektu znajdź: **`install.bat`**
2. **Kliknij prawym przyciskiem myszy** → **"Uruchom jako administrator"**
3. Poczekaj na instalację (2-5 minut)
4. Gdy zobaczysz "Instalacja zakonczona pomyslnie!" - gotowe!

### Metoda Ręczna (jeśli automatyczna nie działa):
1. Naciśnij **`Windows + R`**
2. Wpisz: **`cmd`** i naciśnij Enter
3. Przejdź do folderu projektu:
   ```
   cd C:\ścieżka\do\pythonmap
   ```
   (Zamień `C:\ścieżka\do\pythonmap` na rzeczywistą ścieżkę)

4. Zainstaluj zależności:
   ```
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Poczekaj na instalację wszystkich pakietów

---

## Krok 4: Uruchom aplikację

### Metoda 1: Najszybsza
1. Kliknij dwukrotnie na: **`run.bat`**

### Metoda 2: Z wiersza poleceń
1. Otwórz wiersz poleceń (cmd) w folderze projektu
2. Wpisz: **`python main.py`**

**Sukces!** Powinieneś zobaczyć okno aplikacji! 🎉

---

## 🆘 Rozwiązywanie problemów

### Problem: "Python nie jest rozpoznawany..."

**Rozwiązanie 1:**
1. Odinstaluj Python (Panel Sterowania → Programy → Odinstaluj)
2. Pobierz ponownie ze strony python.org
3. Przy instalacji **KONIECZNIE zaznacz "Add Python to PATH"**
4. Zainstaluj
5. **Zrestartuj komputer**

**Rozwiązanie 2:** Dodaj Python ręcznie do PATH:
1. Znajdź gdzie jest Python (zazwyczaj: `C:\Users\TwojaNazwa\AppData\Local\Programs\Python\Python311`)
2. Naciśnij `Windows + R` → wpisz `sysdm.cpl` → Enter
3. Zakładka "Zaawansowane" → "Zmienne środowiskowe"
4. W "Zmienne systemowe" znajdź "Path" → Edytuj
5. Dodaj ścieżkę do Pythona (np. `C:\Users\...\Python311`)
6. Dodaj też ścieżkę do Scripts (np. `C:\Users\...\Python311\Scripts`)
7. OK → OK → Zrestartuj komputer

### Problem: "pip nie jest rozpoznawany..."

**Rozwiązanie:**
```
python -m pip install -r requirements.txt
```

### Problem: "No module named 'PyQt5'" lub podobne

**Rozwiązanie:**
```
pip install PyQt5 PyQtWebEngine
pip install -r requirements.txt --force-reinstall
```

### Problem: Aplikacja się nie uruchamia

1. Sprawdź plik `pythonmap.log` (jeśli istnieje)
2. Spróbuj uruchomić z cmd:
   ```
   cd C:\ścieżka\do\pythonmap
   python main.py
   ```
3. Przeczytaj komunikaty błędów
4. Zainstaluj ponownie wszystkie zależności:
   ```
   pip install -r requirements.txt --force-reinstall
   ```

### Problem: Brak Google Chrome

Aplikacja wymaga Chrome/Chromium:
1. Pobierz Chrome: https://www.google.com/chrome/
2. Zainstaluj
3. Uruchom aplikację ponownie

---

## 📋 Checklist przed pierwszym uruchomieniem

- [ ] Python 3.8+ zainstalowany
- [ ] Zaznaczone "Add Python to PATH" podczas instalacji
- [ ] Komputer zrestartowany po instalacji Python
- [ ] Wszystkie zależności zainstalowane (`pip install -r requirements.txt`)
- [ ] Google Chrome zainstalowany
- [ ] Połączenie z internetem działa

---

## 🎯 Pierwsze kroki w aplikacji

Po uruchomieniu:

### 1. Dodaj pierwszy projekt
- Kliknij: **"➕ Nowy Projekt"**
- Wpisz nazwę (np. "Moja Pizzeria")
- Wpisz nazwę firmy z Google Maps
- **Jak znaleźć współrzędne?**
  1. Otwórz Google Maps
  2. Znajdź swoją firmę
  3. Kliknij prawym na pinezce
  4. Kliknij współrzędne (np. "50.0647, 19.9450")
  5. Współrzędne zostaną skopiowane!

### 2. Dodaj frazy
- Wybierz projekt
- Kliknij: **"📝 Zarządzaj Frazami"**
- Dodaj frazy, np.:
  - pizza
  - pizzeria kraków
  - najlepsza pizza

### 3. Sprawdź pozycje
- Kliknij: **"▶️ Sprawdź Pozycje"**
- Poczekaj (może potrwać 2-10 minut)
- Zobacz wyniki!

### 4. Zobacz mapę
- Kliknij: **"🗺️ Pokaż Mapę"**
- Wybierz frazę
- Zobacz gdzie jesteś widoczny!

---

## 💡 Wskazówki

✅ **Pierwsze testy:**
- Zacznij od małej siatki (5x5)
- Użyj 2-3 fraz
- Promień 3-5 km

✅ **Optymalne ustawienia:**
- Siatka: 7x7
- Promień: 5 km
- Sprawdzaj raz dziennie

⚠️ **Unikaj:**
- Zbyt częstego sprawdzania (możesz zostać zablokowany)
- Siatki 12x12 bez proxy (zbyt wiele zapytań)

---

## 📞 Potrzebujesz pomocy?

1. Przeczytaj **README.md** - pełna dokumentacja
2. Zobacz **INSTALL_PL.md** - szczegółowa instalacja
3. Sprawdź plik `pythonmap.log` - logi błędów

---

## ✅ Gotowe!

Jeśli wszystko działa - gratulacje! 🎉

Możesz teraz:
- Dodawać więcej projektów
- Monitorować konkurencję
- Generować raporty
- Automatyzować sprawdzanie

**Powodzenia!** 🚀
