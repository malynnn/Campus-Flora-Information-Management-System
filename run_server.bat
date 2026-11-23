@echo off
title PUPQC Campus Plant Database Server
color 0A
echo ============================================
echo   PUPQC Campus Plant Database - Running
echo ============================================
echo.
echo Server is starting...
echo Open your browser and go to: http://127.0.0.1:5000
echo.
echo DO NOT CLOSE THIS WINDOW while using the site.
echo Press CTRL+C to stop the server.
echo.
cd /d "%~dp0"
python app.py
pause
