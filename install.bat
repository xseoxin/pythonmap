@echo off
echo ============================================
echo Google Maps Position Checker - Instalacja
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [BLAD] Python nie jest zainstalowany!
    echo.
    echo Pobierz Python z: https://www.python.org/downloads/
    echo Pamietaj, aby zaznaczyc "Add Python to PATH" podczas instalacji!
    echo.
    pause
    exit /b 1
)

echo [OK] Python jest zainstalowany
python --version
echo.

echo Instalowanie zaleznosci...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [BLAD] Instalacja zaleznosci nie powiodla sie!
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo Instalacja zakonczona pomyslnie!
echo ============================================
echo.
echo Aby uruchomic aplikacje, uzyj: run.bat
echo lub wpisz: python main.py
echo.
pause
