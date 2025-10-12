@echo off
echo ============================================================
echo    Demand Forecasting API
echo ============================================================
echo.
echo Iniciando servidor en: http://localhost:8000
echo Documentacion: http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener
echo ============================================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause

