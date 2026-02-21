@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo Executando testes...
echo.
python -m pytest tests/ -v --tb=short

pause
