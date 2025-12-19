@echo off
REM Script de demarrage unifie pour l'Assistant CAN 2025

echo ============================================================
echo  ASSISTANT IA CAN 2025 - DEMARRAGE
echo ============================================================
echo.

REM Verifier l'environnement virtuel
if not exist "venv\" (
    echo [ERREUR] Environnement virtuel non trouve!
    echo Executez d'abord: python -m venv venv
    echo Puis: venv\Scripts\activate
    echo Puis: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
echo [1/3] Activation de l'environnement virtuel...
call venv\Scripts\activate

REM Verifier la configuration
echo [2/4] Verification de la configuration...
python -c "from dotenv import load_dotenv; import os; load_dotenv(); exit(0 if os.getenv('GROQ_API_KEY') else 1)" 2>nul
if errorlevel 1 (
    echo [ERREUR] GROQ_API_KEY manquante dans .env
    echo Editez .env et ajoutez votre cle API Groq
    pause
    exit /b 1
)

REM Verifier les donnees ChromaDB
echo [3/4] Verification des donnees...
python -c "import chromadb; c=chromadb.PersistentClient('./vectorstore/index'); exit(0 if c.get_collection('can2025_knowledge').count()>0 else 1)" 2>nul
if errorlevel 1 (
    echo Chargement des donnees CAN 2025...
    python scripts\load_data_to_vectorstore.py
)

REM Demarrer l'API en arriere-plan
echo [4/4] Demarrage de l'application...
echo.
start "CAN 2025 API" cmd /k "venv\Scripts\activate && uvicorn api.main:app --reload --host 0.0.0.0 --port 8000"

REM Attendre que l'API demarre
timeout /t 3 /nobreak >nul

REM Demarrer Streamlit
start "CAN 2025 Frontend" cmd /k "venv\Scripts\activate && streamlit run frontend/app.py --server.port 8501"

echo.
echo ============================================================
echo  APPLICATION DEMARREE !
echo ============================================================
echo.
echo  API Backend:    http://localhost:8000
echo  Documentation:  http://localhost:8000/docs
echo  Frontend:       http://localhost:8501
echo.
echo  Appuyez sur Ctrl+C dans chaque fenetre pour arreter
echo ============================================================
echo.

pause
