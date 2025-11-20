"""
Configuration file for the Flask NLP Classification App
"""
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Model paths - adjust if your model is in a different location
MODEL_PATH = os.path.join(BASE_DIR, 'text_classification_model.pkl')

# Application settings
MAX_TEXT_LENGTH = 5000  # Maximum characters for input text
DEBUG = True  # Set to False in production
HOST = '0.0.0.0'
PORT = 5000

# Preprocessing settings
# These match the exact preprocessing from the notebook
REMOVE_PUNCTUATION = True
LOWERCASE = True
REMOVE_STOPWORDS = True

# Categories (for reference and validation)
CATEGORIES = ['ENTERTAINMENT', 'POLITICS', 'STYLE & BEAUTY', 'TRAVEL', 'WELLNESS']

# Number of top predictions to return
TOP_K_PREDICTIONS = 5
