@echo off
REM Whisper Desktop Setup Script
REM This script sets up the environment and installs all dependencies

echo ========================================
echo    Whisper Desktop - Setup
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check FFmpeg installation
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFmpeg not found!
    echo FFmpeg is required for audio processing.
    echo Please install FFmpeg and add it to PATH.
    echo.
    echo Installation options:
    echo 1. Manual: Download from https://ffmpeg.org/download.html
    echo 2. With Chocolatey: choco install ffmpeg
    echo.
    pause
    exit /b 1
)

echo FFmpeg found:
ffmpeg -version | findstr "version"
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist "whisper_env" (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv whisper_env
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call whisper_env\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies (this may take several minutes)...
echo.

echo [1/3] Installing PyTorch...
pip install torch torchvision torchaudio

echo.
echo [2/3] Installing OpenAI Whisper...
pip install openai-whisper

echo.
echo [3/3] Installing additional dependencies...
pip install numpy

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo You can now run the application using:
echo   run_whisper.bat
echo.
echo Or manually:
echo   1. whisper_env\Scripts\activate
echo   2. python whisper_desktop.py
echo.

REM Test import
echo Testing installation...
python -c "import whisper; print('Whisper successfully installed!')"

if errorlevel 1 (
    echo.
    echo WARNING: Import test failed!
    echo There may be an issue with the installation.
) else (
    echo.
    echo All tests passed! Installation successful.
)

echo.
pause
