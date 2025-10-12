@echo off
echo ============================================================
echo    Setup Completo - Demand Forecasting API
echo ============================================================
echo.
echo Este script realiza el setup completo del proyecto:
echo   1. Crea entorno virtual
echo   2. Instala dependencias
echo   3. Genera datos de entrenamiento
echo   4. Entrena el modelo
echo.
echo Presiona cualquier tecla para continuar o Ctrl+C para cancelar
pause > nul
echo.

echo [1/4] Creando entorno virtual...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo ✓ Entorno virtual creado

echo.
echo [2/4] Instalando dependencias (esto puede tomar 1-2 minutos)...
call venv\Scripts\activate
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo ✓ Dependencias instaladas

echo.
echo [3/4] Generando datos de entrenamiento...
python scripts\generate_data.py
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron generar los datos
    pause
    exit /b 1
)
echo ✓ Datos generados

echo.
echo [4/4] Entrenando modelo de Machine Learning...
python scripts\train_model.py
if %errorlevel% neq 0 (
    echo ERROR: No se pudo entrenar el modelo
    pause
    exit /b 1
)
echo ✓ Modelo entrenado

echo.
echo ============================================================
echo    ✓ Setup completado exitosamente!
echo ============================================================
echo.
echo Proximos pasos:
echo   1. Iniciar API: start_api.bat
echo   2. Abrir navegador: http://localhost:8000/docs
echo   3. Probar API: python scripts\test_api.py
echo.
echo ============================================================
pause

