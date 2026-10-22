@echo off
title House Price Prediction - Test Runner
echo ========================================================
echo   Running Automated Test Suite...
echo ========================================================
echo.
python -m unittest discover tests
echo.
pause
