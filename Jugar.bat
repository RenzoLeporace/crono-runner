@echo off
setlocal
cd /d "%~dp0"
if exist "CRONO - Ecos del tiempo.exe" (
    start "" "CRONO - Ecos del tiempo.exe"
    exit /b
)
set "CRONO_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%CRONO_PYTHON%" (
    "%CRONO_PYTHON%" Main.py
    if errorlevel 1 pause
    exit /b
)
py -3 Main.py
if errorlevel 1 (
    echo.
    echo Instala Python y ejecuta: python -m pip install -r requirements.txt
    pause
)
