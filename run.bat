@echo off
cd /d "%~dp0"
title House Price Prediction - Web Application
echo ========================================================
echo   Starting House Price Prediction Web Application...
echo ========================================================
echo.
python app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Application stopped with error code %ERRORLEVEL%.
    pause
)
