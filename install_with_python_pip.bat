@echo off
title Google Maps Position Checker - Instalator (pip fix)
color 0A

:start
cls
echo ========================================================
echo    Google Maps Position Checker - Instalator
echo    (Wersja dla problemow z pip)
echo ========================================================
echo.
echo Ten skrypt uzywa "python -m pip" zamiast "pip"
echo.
echo ========================================================
echo.

REM Step 1: Check Python
echo [KROK 1/3] Sprawdzanie Python...
echo.
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [BLAD] Python nie jest zainstalowany!
    echo.
    echo --------------------------------------------------------
    echo JAK ZAINSTALOWAC PYTHON:
    echo --------------------------------------------------------
    echo.
    echo 1. Otworz: https://www.python.org/downloads/
    echo 2. Pobierz Python (duzy zolty przycisk)
    echo 3. Uruchom instalator
    echo 4. KONIECZNIE zaznacz: "Add Python to PATH"
    echo 5. Kliknij "Install Now"
    echo 6. Zrestartuj komputer
    echo 7. Uruchom ten skrypt ponownie
    echo.
    echo --------------------------------------------------------
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python jest zainstalowany!
echo.
timeout /t 1 >nul

REM Step 2: Upgrade pip using python -m pip
echo [KROK 2/3] Aktualizacja pip (przez python -m pip)...
echo.
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [OSTRZEZENIE] Nie udalo sie zaktualizowac pip
    echo Kontynuuje mimo to...
    echo.
)
echo [OK] pip gotowy!
echo.
timeout /t 1 >nul

REM Step 3: Install dependencies using python -m pip
echo [KROK 3/3] Instalowanie zaleznosci (python -m pip)...
echo.
echo To moze potrwac 3-5 minut. Prosze czekac...
echo.
echo Instaluje pakiety:
echo - PyQt5 (interfejs graficzny)
echo - Selenium (sprawdzanie Google Maps)
echo - Folium (mapy)
echo - ReportLab (raporty PDF)
echo - i inne...
echo.

python -m pip install -r requirements.txt

if errorlevel 1 (
    color 0C
    echo.
    echo [BLAD] Instalacja zaleznosci nie powiodla sie!
    echo.
    echo --------------------------------------------------------
    echo ROZWIAZANIE:
    echo --------------------------------------------------------
    echo.
    echo 1. Sprawdz polaczenie z internetem
    echo 2. Sprobuj ponownie jako Administrator:
    echo    - Kliknij prawym na ten plik
    echo    - Wybierz "Uruchom jako administrator"
    echo.
    echo 3. Lub zainstaluj recznie:
    echo    python -m pip install PyQt5
    echo    python -m pip install PyQtWebEngine
    echo    python -m pip install selenium
    echo    python -m pip install -r requirements.txt
    echo.
    echo 4. Jesli dalej nie dziala, sprobuj:
    echo    python -m pip install --upgrade setuptools wheel
    echo    python -m pip install -r requirements.txt
    echo.
    echo --------------------------------------------------------
    echo.
    pause
    exit /b 1
)

cls
color 0A
echo ========================================================
echo           INSTALACJA ZAKONCZONA POMYSLNIE!
echo ========================================================
echo.
echo Aplikacja jest gotowa do uzycia!
echo.
echo --------------------------------------------------------
echo WAZNA INFORMACJA:
echo --------------------------------------------------------
echo.
echo Twoj pip nie jest w PATH, ale to nie problem!
echo.
echo Jesli kiedykolwiek bedziesz chcial zainstalowac
echo dodatkowe pakiety, uzywaj:
echo.
echo   python -m pip install [nazwa_pakietu]
echo.
echo Zamiast:
echo   pip install [nazwa_pakietu]
echo.
echo --------------------------------------------------------
echo JAK URUCHOMIC APLIKACJE:
echo --------------------------------------------------------
echo.
echo Metoda 1 (najlatwiejsza):
echo   - Kliknij dwukrotnie na: run.bat
echo.
echo Metoda 2 (z linii polecen):
echo   - Wpisz: python main.py
echo.
echo --------------------------------------------------------
echo.
echo Wiecej informacji w README.md i QUICKSTART_PL.md
echo.
echo ========================================================
echo.
echo Nacisnij dowolny klawisz aby uruchomic aplikacje...
pause >nul

REM Ask if user wants to run the app
cls
echo Czy chcesz teraz uruchomic aplikacje?
echo.
echo 1 = TAK, uruchom aplikacje
echo 2 = NIE, zamknij
echo.
choice /c 12 /n /m "Wybierz opcje (1 lub 2): "

if errorlevel 2 goto end
if errorlevel 1 goto run_app

:run_app
echo.
echo Uruchamianie aplikacji...
echo.
python main.py
goto end

:end
exit /b 0
