@echo off
echo Starting KeyDefender Application...
cd %~dp0

:: Cek apakah venv ada dan gunakan jika tersedia
if exist venv\Scripts\python.exe (
    echo Using virtual environment...
    call venv\Scripts\activate.bat
    venv\Scripts\python.exe src\main.py
) else (
    :: Coba gunakan python dari sistem
    echo Using system Python...
    python src\main.py
    
    :: Jika gagal, coba dengan python3
    if %ERRORLEVEL% NEQ 0 (
        echo Trying with python3...
        python3 src\main.py
    )
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Tidak dapat menjalankan aplikasi KeyDefender.
    echo Pastikan Python (3.7+) sudah terinstal dan tersedia di PATH sistem.
    echo Anda juga dapat membuat virtual environment dengan menjalankan:
    echo.
    echo python -m venv venv
    echo venv\Scripts\pip install -r requirements.txt
    echo.
)

pause 