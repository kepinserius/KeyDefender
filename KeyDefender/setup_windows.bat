@echo off
echo Setting up KeyDefender development environment...
cd %~dp0

:: Cek Python tersedia
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python tidak ditemukan!
    echo Silakan install Python 3.7 atau lebih tinggi dan tambahkan ke PATH sistem.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Cek versi Python
python --version | findstr /r "3\.[789]"
if %ERRORLEVEL% NEQ 0 (
    python --version | findstr /r "3\.1[0-9]"
    if %ERRORLEVEL% NEQ 0 (
        echo WARNING: Python versi 3.7 atau lebih tinggi disarankan.
        echo Versi yang terinstal:
        python --version
        echo.
        echo Lanjutkan setup? (Y/N)
        set /p CONTINUE=
        if /i not "%CONTINUE%"=="Y" exit /b 1
    )
)

:: Buat virtual environment
echo Membuat virtual environment...
if exist venv (
    echo Virtual environment sudah ada. Hapus untuk membuat baru? (Y/N)
    set /p DELETE_VENV=
    if /i "%DELETE_VENV%"=="Y" (
        echo Menghapus virtual environment lama...
        rmdir /s /q venv
        python -m venv venv
    )
) else (
    python -m venv venv
)

:: Aktifkan virtual environment dan install dependencies
echo Menginstall dependensi...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Gagal menginstall dependensi.
    pause
    exit /b 1
)

echo.
echo Setup selesai!
echo Untuk menjalankan aplikasi, gunakan run_keydefender.bat
echo.

pause 