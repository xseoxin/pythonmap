@echo off
echo ==========================================
echo Sprawdzanie instalacji Python
echo ==========================================
echo.

REM Check Python
python --version 2>&1
if errorlevel 1 (
    echo.
    echo [X] Python NIE jest zainstalowany!
    echo.
    echo Co zrobic?
    echo 1. Pobierz Python z: https://www.python.org/downloads/
    echo 2. Podczas instalacji ZAZNACZ "Add Python to PATH"
    echo 3. Zrestartuj komputer
    echo 4. Uruchom ten skrypt ponownie
    echo.
    goto end
)

echo [OK] Python jest zainstalowany!
echo.

REM Check pip
echo Sprawdzanie pip...
pip --version 2>&1
if errorlevel 1 (
    echo [X] pip NIE jest zainstalowany!
    echo.
    goto end
)

echo [OK] pip jest zainstalowany!
echo.

REM Show Python path
echo Lokalizacja Python:
where python
echo.

echo ==========================================
echo Wszystko jest OK! Mozesz instalowac aplikacje.
echo ==========================================
echo.
echo Nastepny krok: Uruchom install.bat
echo.

:end
pause
