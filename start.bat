@echo off
chcp 65001 >nul
title Converter All-in-One

cd /d "%~dp0backend"

echo.
echo ========================================
echo   Converter All-in-One
echo ========================================
echo.
echo Iniciando servidor em http://127.0.0.1:8000
echo Pressione Ctrl+C para encerrar.
echo.
echo.

python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

pause
