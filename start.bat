@echo off
echo ========================================
echo  Assistant IA CAN 2025 - Demarrage
echo ========================================
echo.

echo [1/2] Demarrage de l'API Backend...
start "API Backend" cmd /k "cd /d %~dp0 && venv\Scripts\activate && uvicorn api.main:app --reload"

timeout /t 3 /nobreak >nul

echo [2/2] Demarrage de l'interface Streamlit...
start "Interface Streamlit" cmd /k "cd /d %~dp0 && venv\Scripts\activate && streamlit run frontend/app.py"

echo.
echo ========================================
echo  Application demarree !
echo ========================================
echo  API Backend: http://localhost:8000
echo  Documentation: http://localhost:8000/docs
echo  Interface Web: http://localhost:8501
echo ========================================
echo.
pause
