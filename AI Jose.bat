@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Membuat virtual environment...
    py -m venv .venv
)

echo Memasang dependency...
".venv\Scripts\python.exe" -m pip install -r requirements.txt

echo Menjalankan aplikasi...
start "Flask Server" cmd /k ".venv\Scripts\python.exe app.py"

echo Membuka UI di browser...
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:5000/ui"

exit /b 0
