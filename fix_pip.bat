@echo off
title Naprawa pip
color 0E

cls
echo ========================================================
echo    NAPRAWA pip
echo ========================================================
echo.
echo Ten skrypt naprawi problem z pip.
echo.
pause

cls
echo ========================================================
echo [1/3] Sprawdzanie Python...
echo ========================================================
echo.

python --version 2>&1
if errorlevel 1 (
    color 0C
    echo [BLAD] Python nie jest zainstalowany!
    echo.
    pause
    exit /b 1
)

echo [OK] Python dziala!
echo.
pause

cls
echo ========================================================
echo [2/3] Sprawdzanie pip przez Python...
echo ========================================================
echo.

echo Probuje: python -m pip --version
echo.
python -m pip --version 2>&1

if errorlevel 1 (
    color 0C
    echo.
    echo [BLAD] pip nie jest zainstalowany w Pythonie!
    echo.
    echo ROZWIAZANIE:
    echo 1. Odinstaluj Python
    echo 2. Pobierz ponownie z python.org
    echo 3. Podczas instalacji zaznacz:
    echo    - Add Python to PATH
    echo    - pip (powinno byc domyslnie zaznaczone)
    echo 4. Zrestartuj komputer
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] pip dziala przez Python!
echo.
pause

cls
echo ========================================================
echo [3/3] Aktualizacja pip...
echo ========================================================
echo.

echo Aktualizuje pip do najnowszej wersji...
echo.
python -m pip install --upgrade pip

echo.
echo ========================================================
echo    pip zostal naprawiony!
echo ========================================================
echo.
echo Od teraz uzywaj:
echo   python -m pip install [pakiet]
echo.
echo Zamiast:
echo   pip install [pakiet]
echo.
echo --------------------------------------------------------
echo DALSZE KROKI:
echo --------------------------------------------------------
echo.
echo 1. Zamknij to okno
echo 2. Uruchom: install_with_python_pip.bat
echo    (lub install_step_by_step.bat)
echo.
echo ========================================================
echo.
pause
