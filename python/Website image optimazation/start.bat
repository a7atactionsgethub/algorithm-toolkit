@echo off
title WebOptimizer - Image Optimizer for Web
color 0B

echo.
echo  ==========================================
echo   ^<^< WebOptimizer - Image Optimizer for Web ^>^>
echo  ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python is not installed or not in PATH.
    echo.
    echo  Please download and install Python from:
    echo  https://www.python.org/downloads/
    echo.
    echo  IMPORTANT: During setup, check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo  [OK] Python found.

:: Install / upgrade Pillow silently
echo  [..] Checking for Pillow...
python -m pip install --upgrade Pillow --quiet --disable-pip-version-check
if errorlevel 1 (
    echo  [WARN] Could not install Pillow automatically.
    echo         Try running: pip install Pillow
    echo.
    pause
    exit /b 1
)
echo  [OK] Pillow ready.

:: Check the main script exists
if not exist "%~dp0image_optimizer.py" (
    echo.
    echo  [ERROR] image_optimizer.py not found!
    echo  Make sure start.bat is in the same folder as image_optimizer.py
    echo.
    pause
    exit /b 1
)

echo  [OK] Launching app...
echo.

:: Test tkinter before launching
echo  [..] Checking Tkinter (GUI toolkit)...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [ERROR] Tkinter is missing from your Python installation!
    echo.
    echo  FIX: Re-install Python from https://www.python.org/downloads/
    echo       During setup, click "Customize installation"
    echo       Make sure "tcl/tk and IDLE" is CHECKED.
    echo.
    echo  Recommended: Use Python 3.11 or 3.12 for best compatibility.
    echo.
    pause
    exit /b 1
)
echo  [OK] Tkinter ready.

:: Launch the app and capture errors
echo.
python "%~dp0image_optimizer.py" 2>&1
if errorlevel 1 (
    echo.
    echo  [ERROR] The app closed with an error. See details above.
    echo.
    pause
)