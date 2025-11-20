@echo off
REM Quick run script for the Flask app

echo Starting News Category Classifier...
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Check if model exists
if not exist "text_classification_model.pkl" (
    echo WARNING: Model file not found!
    echo The app may not work correctly without text_classification_model.pkl
    echo.
    echo Press any key to continue anyway, or Ctrl+C to cancel
    pause
)

REM Activate virtual environment and run app
call venv\Scripts\activate.bat
cd app
echo.
echo App starting at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py
