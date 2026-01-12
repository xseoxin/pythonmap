@echo off
title Diagnostyka - Google Maps Position Checker
color 0E

cls
echo ========================================================
echo    DIAGNOSTYKA PROBLEMOW
echo ========================================================
echo.
echo Ten skrypt sprawdzi konfiguracje i pomoze znalezc problemy.
echo.
pause

cls
echo ========================================================
echo [1/6] Sprawdzanie systemu operacyjnego...
echo ========================================================
echo.
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
echo.
pause

cls
echo ========================================================
echo [2/6] Sprawdzanie Python...
echo ========================================================
echo.
python --version 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo [BLAD] Python nie jest zainstalowany lub nie jest w PATH!
    echo.
    echo ROZWIAZANIE:
    echo 1. Zainstaluj Python z: https://www.python.org/downloads/
    echo 2. Zaznacz "Add Python to PATH" podczas instalacji
    echo 3. Zrestartuj komputer
    echo.
) else (
    echo [OK] Python dziala!
)
echo.

echo Lokalizacja Python:
where python 2>&1
echo.
pause

cls
echo ========================================================
echo [3/6] Sprawdzanie pip...
echo ========================================================
echo.
pip --version 2>&1
if errorlevel 1 (
    echo [BLAD] pip nie dziala!
    echo.
    echo Sprobuj:
    echo python -m pip --version
    echo.
) else (
    echo [OK] pip dziala!
)
echo.
pause

cls
echo ========================================================
echo [4/6] Sprawdzanie zainstalowanych pakietow...
echo ========================================================
echo.
echo Sprawdzam kluczowe pakiety...
echo.

python -c "import PyQt5; print('PyQt5:', PyQt5.Qt.PYQT_VERSION_STR)" 2>nul
if errorlevel 1 (
    echo [BRAK] PyQt5 - zainstaluj: python -m pip install PyQt5
) else (
    echo [OK] PyQt5
)

python -c "import selenium; print('Selenium:', selenium.__version__)" 2>&1
if errorlevel 1 (
    echo [BRAK] Selenium - zainstaluj: pip install selenium
) else (
    echo [OK] Selenium
)

python -c "import folium; print('Folium:', folium.__version__)" 2>&1
if errorlevel 1 (
    echo [BRAK] Folium - zainstaluj: pip install folium
) else (
    echo [OK] Folium
)

python -c "import pandas; print('Pandas:', pandas.__version__)" 2>&1
if errorlevel 1 (
    echo [BRAK] Pandas - zainstaluj: pip install pandas
) else (
    echo [OK] Pandas
)

echo.
pause

cls
echo ========================================================
echo [5/6] Sprawdzanie Google Chrome...
echo ========================================================
echo.

where chrome.exe 2>nul
if errorlevel 1 (
    echo [OSTRZEZENIE] Chrome nie znaleziony w PATH
    echo.
    echo Sprawdzam typowe lokalizacje...
    if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
        echo [OK] Znaleziono: C:\Program Files\Google\Chrome\Application\chrome.exe
    ) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
        echo [OK] Znaleziono: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
    ) else (
        echo [BLAD] Chrome nie jest zainstalowany!
        echo.
        echo Pobierz Chrome: https://www.google.com/chrome/
    )
) else (
    echo [OK] Chrome znaleziony!
    where chrome.exe
)
echo.
pause

cls
echo ========================================================
echo [6/6] Sprawdzanie plikow projektu...
echo ========================================================
echo.

if exist "main.py" (
    echo [OK] main.py
) else (
    echo [BLAD] Brak main.py!
)

if exist "requirements.txt" (
    echo [OK] requirements.txt
) else (
    echo [BLAD] Brak requirements.txt!
)

if exist "models" (
    echo [OK] Folder models/
) else (
    echo [BLAD] Brak folderu models/
)

if exist "services" (
    echo [OK] Folder services/
) else (
    echo [BLAD] Brak folderu services/
)

if exist "ui" (
    echo [OK] Folder ui/
) else (
    echo [BLAD] Brak folderu ui/
)

echo.
pause

cls
echo ========================================================
echo    PODSUMOWANIE DIAGNOSTYKI
echo ========================================================
echo.
echo Diagnostyka zakonczona.
echo.
echo --------------------------------------------------------
echo NAJCZESTSZE PROBLEMY I ROZWIAZANIA:
echo --------------------------------------------------------
echo.
echo 1. Python nie jest zainstalowany:
echo    - Pobierz z python.org
echo    - Zaznacz "Add Python to PATH"
echo    - Zrestartuj komputer
echo.
echo 2. Brakuje pakietow:
echo    - Kliknij PRAWYM na: INSTALUJ_TUTAJ.bat
echo    - Wybierz: "Uruchom jako administrator"
echo.
echo 3. Chrome nie jest zainstalowany:
echo    - Pobierz z google.com/chrome
echo.
echo 4. Aplikacja sie nie uruchamia:
echo    - Zobacz plik pythonmap.log
echo    - Sprobuj: python main.py (w cmd)
echo    - Zainstaluj ponownie pakiety (INSTALUJ_TUTAJ.bat)
echo.
echo --------------------------------------------------------
echo DALSZE KROKI:
echo --------------------------------------------------------
echo.
echo Jesli wszystko OK:
echo   1. Kliknij PRAWYM na: INSTALUJ_TUTAJ.bat
echo   2. Wybierz: "Uruchom jako administrator"
echo   3. Po instalacji uruchom: run.bat
echo.
echo Jesli sa bledy:
echo   1. Napraw problemy z powyzszej listy
echo   2. Przeczytaj PRZECZYTAJ_MNIE.txt
echo   3. Uruchom ten skrypt ponownie
echo.
echo ========================================================
echo.
pause
