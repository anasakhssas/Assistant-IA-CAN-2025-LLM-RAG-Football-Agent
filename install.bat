@echo off
REM Script d'installation et de configuration

echo ============================================================
echo  INSTALLATION - ASSISTANT IA CAN 2025
echo ============================================================
echo.

REM Verifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    pause
    exit /b 1
)

echo [1/5] Creation de l'environnement virtuel...
python -m venv venv
if errorlevel 1 (
    echo [ERREUR] Echec creation environnement virtuel
    pause
    exit /b 1
)

echo [2/5] Activation de l'environnement virtuel...
call venv\Scripts\activate

echo [3/5] Installation des dependances...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERREUR] Echec installation des dependances
    pause
    exit /b 1
)

echo [4/5] Configuration de l'environnement...
if not exist ".env" (
    echo Creation du fichier .env...
    copy .env.example .env
    echo [ATTENTION] Editez .env et ajoutez votre cle GROQ_API_KEY
)

echo [5/5] Initialisation des donnees...
if not exist "logs" mkdir logs
if not exist "vectorstore\index" mkdir vectorstore\index

echo Chargement des donnees CAN 2025 dans ChromaDB...
python scripts\load_data_to_vectorstore.py
if errorlevel 1 (
    echo [ATTENTION] Erreur lors du chargement des donnees
)

echo.
echo ============================================================
echo  INSTALLATION TERMINEE !
echo ============================================================
echo.
echo Prochaines etapes :
echo 1. Editez le fichier .env et ajoutez vos cles API
echo    - GROQ_API_KEY (obligatoire - https://console.groq.com)
echo    - FOOTBALL_API_KEY (optionnel - https://dashboard.api-football.com)
echo 2. Lancez l'application : run.bat
echo.
pause
echo  Documentation: README.md
echo ============================================================
echo.

pause
