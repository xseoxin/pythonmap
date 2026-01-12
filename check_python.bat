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
    echo [X] pip nie jest w PATH, probuje python -m pip...
    echo.
    python -m pip --version 2>&1
    if errorlevel 1 (
        echo [X] pip NIE jest zainstalowany!
        echo.
        echo ROZWIAZANIE:
        echo 1. Uruchom: fix_pip.bat
        echo 2. Lub zainstaluj Python ponownie z pip
        echo.
        goto end
    ) else (
        echo [OK] pip dziala przez "python -m pip"!
        echo.
        echo UWAGA: Uzywaj "python -m pip" zamiast "pip"
        echo.
    )
) else (
    echo [OK] pip jest zainstalowany i jest w PATH!
    echo.
)

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
