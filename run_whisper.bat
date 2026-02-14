@echo off
REM Whisper Desktop Launcher
REM This script activates the virtual environment and runs the application

echo ========================================
echo    Whisper Desktop Application
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "whisper_env\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call whisper_env\Scripts\activate.bat

REM Check if whisper is installed
python -c "import whisper" 2>nul
if errorlevel 1 (
    echo ERROR: Whisper not installed!
    echo Please run setup.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

REM Run the application
echo Starting Whisper Desktop...
echo.
python whisper_desktop.py

REM Deactivate when done
call whisper_env\Scripts\deactivate.bat

echo.
echo Application closed.
pause
