@echo off
REM Setup script for News Category Classifier Flask App
REM Run this script to set up the environment automatically

echo ========================================
echo News Category Classifier - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Python detected: 
python --version
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo Virtual environment created.
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [4/5] Installing dependencies...
cd app
pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed.
echo.

REM Download NLTK stopwords
echo [5/5] Downloading NLTK stopwords...
python -c "import nltk; nltk.download('stopwords', quiet=False)"
echo.

REM Check if model exists
cd ..
if exist "text_classification_model.pkl" (
    echo [SUCCESS] Model file found: text_classification_model.pkl
) else (
    echo [WARNING] Model file not found: text_classification_model.pkl
    echo Please export the model from your Jupyter notebook:
    echo   import joblib
    echo   joblib.dump(model, 'text_classification_model.pkl'^)
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   1. cd app
echo   2. python app.py
echo.
echo Then open your browser to: http://localhost:5000
echo.
pause
