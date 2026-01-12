@echo off
REM ============================================================
REM  Google Maps Position Checker - INSTALATOR AUTOMATYCZNY
REM  Ten plik wszystko zainstaluje i naprawi automatycznie!
REM ============================================================

title Instalator - Google Maps Position Checker
color 0B

REM Sprawdź czy uruchomiono jako Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    color 0C
    echo.
    echo ============================================================
    echo  UWAGA: Uruchom jako Administrator!
    echo ============================================================
    echo.
    echo Kliknij PRAWYM przyciskiem na ten plik
    echo i wybierz "Uruchom jako administrator"
    echo.
    echo Nacisnij dowolny klawisz aby zamknac...
    pause >nul
    exit /b 1
)

cls
echo.
echo ============================================================
echo.
echo          GOOGLE MAPS POSITION CHECKER
echo          Instalator Automatyczny
echo.
echo ============================================================
echo.
echo  Ten skrypt automatycznie:
echo  1. Sprawdzi Python
echo  2. Naprawi pip (jesli trzeba)
echo  3. Zainstaluje wszystkie pakiety
echo  4. Uruchomi aplikacje
echo.
echo  Zajmie to okolo 5-10 minut.
echo.
echo ============================================================
echo.
pause

REM ============================================================
REM  KROK 1: Sprawdzanie Python
REM ============================================================
cls
echo.
echo ============================================================
echo  [KROK 1/4] Sprawdzanie Python...
echo ============================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [X] BLAD: Python nie jest zainstalowany!
    echo.
    echo --------------------------------------------------------
    echo  CO ZROBIC:
    echo --------------------------------------------------------
    echo.
    echo  1. Otworz: https://www.python.org/downloads/
    echo  2. Pobierz Python (zolty przycisk)
    echo  3. Uruchom instalator
    echo  4. KONIECZNIE ZAZNACZ: "Add Python to PATH"
    echo  5. Zainstaluj Python
    echo  6. Zrestartuj komputer
    echo  7. Uruchom ten plik ponownie
    echo.
    echo --------------------------------------------------------
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python jest zainstalowany!
echo.
timeout /t 2 >nul

REM ============================================================
REM  KROK 2: Naprawa pip
REM ============================================================
cls
echo.
echo ============================================================
echo  [KROK 2/4] Sprawdzanie i naprawa pip...
echo ============================================================
echo.

REM Sprawdź czy pip działa
pip --version >nul 2>&1
if errorlevel 1 (
    echo [!] pip nie jest w PATH, probuje python -m pip...
    echo.

    REM Sprawdź python -m pip
    python -m pip --version >nul 2>&1
    if errorlevel 1 (
        color 0C
        echo [X] BLAD: pip nie jest zainstalowany w Pythonie!
        echo.
        echo Python jest zainstalowany, ale pip nie dziala.
        echo.
        echo Sprobuj przeinstalowac Python z pip zaznaczonym.
        echo.
        pause
        exit /b 1
    ) else (
        echo [OK] pip dziala przez "python -m pip"
    )
) else (
    echo [OK] pip jest w PATH
    python -m pip --version
)

echo.
echo Aktualizuje pip do najnowszej wersji...
echo.
python -m pip install --upgrade pip --quiet --disable-pip-version-check 2>nul
echo [OK] pip zaktualizowany!
echo.
timeout /t 2 >nul

REM ============================================================
REM  KROK 3: Instalacja pakietow
REM ============================================================
cls
echo.
echo ============================================================
echo  [KROK 3/4] Instalowanie pakietow...
echo ============================================================
echo.
echo  To moze potrwac 5-10 minut.
echo  Prosze czekac...
echo.
echo ============================================================
echo.

REM Sprawdź czy requirements.txt istnieje
if not exist "requirements.txt" (
    color 0C
    echo [X] BLAD: Brak pliku requirements.txt!
    echo.
    echo Upewnij sie, ze uruchamiasz ten plik w folderze projektu!
    echo.
    pause
    exit /b 1
)

REM Instaluj pakiety po kolei z progress
echo [1/10] Instaluje PyQt5...
python -m pip install PyQt5==5.15.10 --quiet --disable-pip-version-check
if errorlevel 1 (
    echo [!] Ostrzezenie: Problem z PyQt5, probuje ponownie...
    python -m pip install PyQt5 --quiet --disable-pip-version-check
)
echo       [OK] PyQt5 zainstalowany

echo [2/10] Instaluje PyQtWebEngine...
python -m pip install PyQtWebEngine==5.15.6 --quiet --disable-pip-version-check
if errorlevel 1 (
    python -m pip install PyQtWebEngine --quiet --disable-pip-version-check
)
echo       [OK] PyQtWebEngine zainstalowany

echo [3/10] Instaluje Selenium...
python -m pip install selenium --quiet --disable-pip-version-check
echo       [OK] Selenium zainstalowany

echo [4/10] Instaluje webdriver-manager...
python -m pip install webdriver-manager --quiet --disable-pip-version-check
echo       [OK] webdriver-manager zainstalowany

echo [5/10] Instaluje folium...
python -m pip install folium --quiet --disable-pip-version-check
echo       [OK] folium zainstalowany

echo [6/10] Instaluje pandas...
python -m pip install pandas --quiet --disable-pip-version-check
echo       [OK] pandas zainstalowany

echo [7/10] Instaluje openpyxl...
python -m pip install openpyxl --quiet --disable-pip-version-check
echo       [OK] openpyxl zainstalowany

echo [8/10] Instaluje reportlab...
python -m pip install reportlab --quiet --disable-pip-version-check
echo       [OK] reportlab zainstalowany

echo [9/10] Instaluje schedule...
python -m pip install schedule --quiet --disable-pip-version-check
echo       [OK] schedule zainstalowany

echo [10/10] Instaluje fake-useragent...
python -m pip install fake-useragent --quiet --disable-pip-version-check
echo       [OK] fake-useragent zainstalowany

echo.
echo [OK] Wszystkie pakiety zainstalowane!
echo.
timeout /t 2 >nul

REM ============================================================
REM  KROK 4: Weryfikacja instalacji
REM ============================================================
cls
echo.
echo ============================================================
echo  [KROK 4/4] Weryfikacja instalacji...
echo ============================================================
echo.

set ERRORS=0

echo Sprawdzam zainstalowane pakiety...
echo.

python -c "import PyQt5; print('[OK] PyQt5:', PyQt5.Qt.PYQT_VERSION_STR)" 2>nul
if errorlevel 1 (
    echo [X] PyQt5 - BLAD
    set /a ERRORS+=1
)

python -c "import PyQt5.QtWebEngineWidgets; print('[OK] PyQtWebEngine')" 2>nul
if errorlevel 1 (
    echo [X] PyQtWebEngine - BLAD
    set /a ERRORS+=1
)

python -c "import selenium; print('[OK] Selenium:', selenium.__version__)" 2>nul
if errorlevel 1 (
    echo [X] Selenium - BLAD
    set /a ERRORS+=1
)

python -c "import folium; print('[OK] Folium:', folium.__version__)" 2>nul
if errorlevel 1 (
    echo [X] Folium - BLAD
    set /a ERRORS+=1
)

python -c "import pandas; print('[OK] Pandas:', pandas.__version__)" 2>nul
if errorlevel 1 (
    echo [X] Pandas - BLAD
    set /a ERRORS+=1
)

python -c "import openpyxl; print('[OK] openpyxl')" 2>nul
if errorlevel 1 (
    echo [X] openpyxl - BLAD
    set /a ERRORS+=1
)

python -c "import reportlab; print('[OK] ReportLab')" 2>nul
if errorlevel 1 (
    echo [X] ReportLab - BLAD
    set /a ERRORS+=1
)

python -c "import schedule; print('[OK] schedule')" 2>nul
if errorlevel 1 (
    echo [X] schedule - BLAD
    set /a ERRORS+=1
)

python -c "import fake_useragent; print('[OK] fake-useragent')" 2>nul
if errorlevel 1 (
    echo [X] fake-useragent - BLAD
    set /a ERRORS+=1
)

echo.

if %ERRORS% gtr 0 (
    color 0E
    echo ============================================================
    echo  OSTRZEZENIE: %ERRORS% pakiety maja problemy
    echo ============================================================
    echo.
    echo Sprobuj uruchomic aplikacje - moze dzialac mimo to.
    echo.
    echo Jesli nie dziala, uruchom:
    echo   python -m pip install -r requirements.txt --force-reinstall
    echo.
    timeout /t 5 >nul
) else (
    color 0A
    echo ============================================================
    echo  Wszystkie pakiety zainstalowane poprawnie!
    echo ============================================================
    echo.
)

timeout /t 2 >nul

REM ============================================================
REM  SUKCES!
REM ============================================================
cls
color 0A
echo.
echo ============================================================
echo.
echo          INSTALACJA ZAKONCZONA POMYSLNIE!
echo.
echo ============================================================
echo.
echo  Aplikacja jest gotowa do uzycia!
echo.
echo ============================================================
echo  JAK URUCHOMIC APLIKACJE:
echo ============================================================
echo.
echo  Metoda 1 (najlatwiejsza):
echo    Kliknij dwukrotnie na: run.bat
echo.
echo  Metoda 2 (z linii polecen):
echo    Wpisz: python main.py
echo.
echo ============================================================
echo  PIERWSZE KROKI:
echo ============================================================
echo.
echo  1. Dodaj projekt (przycisk "Nowy Projekt")
echo  2. Znajdz wspolrzedne firmy w Google Maps
echo  3. Dodaj frazy do sprawdzenia
echo  4. Kliknij "Sprawdz Pozycje"
echo  5. Zobacz wyniki na mapie!
echo.
echo ============================================================
echo.
echo  Dokumentacja:
echo    - README.md (pelna dokumentacja)
echo    - QUICKSTART_PL.md (szybki start)
echo    - INSTALACJA_KROK_PO_KROKU.txt (pomoc)
echo.
echo ============================================================
echo.
echo.

REM Zapytaj czy uruchomic aplikacje
choice /c YN /m "Czy uruchomic aplikacje teraz? (Y=Tak, N=Nie)"
if errorlevel 2 goto end
if errorlevel 1 goto run_app

:run_app
echo.
echo Uruchamianie aplikacji...
echo.
timeout /t 2 >nul

REM Sprawdź czy main.py istnieje
if not exist "main.py" (
    color 0C
    echo [X] BLAD: Brak pliku main.py!
    echo.
    echo Upewnij sie, ze jestes w folderze projektu!
    echo.
    pause
    exit /b 1
)

REM Uruchom aplikację
python main.py

goto end

:end
echo.
echo Dziekujemy za uzycie instalatora!
echo.
timeout /t 3 >nul
exit /b 0
