@echo off
title Diagnostyka Python
color 0B

echo ==========================================
echo Sprawdzanie instalacji Python
echo ==========================================
echo.

REM Check Python
echo [1/2] Sprawdzanie Python...
echo.
python --version 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo [X] Python NIE jest zainstalowany!
    echo.
    echo Co zrobic?
    echo 1. Pobierz Python z: https://www.python.org/downloads/
    echo 2. Podczas instalacji ZAZNACZ "Add Python to PATH"
    echo 3. Zrestartuj komputer
    echo 4. Uruchom ten skrypt ponownie
    echo.
    echo Nacisnij dowolny klawisz aby zamknac...
    pause >nul
    exit /b 1
)

echo [OK] Python jest zainstalowany!
echo.

REM Check pip
echo [2/2] Sprawdzanie pip...
echo.
pip --version 2>nul
if errorlevel 1 (
    echo [!] pip nie jest w PATH, probuje python -m pip...
    echo.
    python -m pip --version 2>nul
    if errorlevel 1 (
        color 0E
        echo [X] pip NIE jest zainstalowany!
        echo.
        echo ROZWIAZANIE:
        echo Zainstaluj Python ponownie z pip
        echo.
    ) else (
        echo [OK] pip dziala przez "python -m pip"!
        echo.
        echo UWAGA: To jest normalne. Instalator uzywa "python -m pip"
        echo.
    )
) else (
    echo [OK] pip jest zainstalowany i jest w PATH!
    pip --version
    echo.
)

REM Show Python path
echo Lokalizacja Python:
where python 2>nul
echo.

echo ==========================================
echo Diagnostyka zakonczona
echo ==========================================
echo.
echo Nastepny krok:
echo   Kliknij PRAWYM na: INSTALUJ_TUTAJ.bat
echo   Wybierz: "Uruchom jako administrator"
echo.
echo ==========================================
echo.

pause
