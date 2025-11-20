"""
Model utilities: loading, preprocessing, and prediction functions.
This module reproduces the exact preprocessing pipeline from the notebook.
"""
import joblib
import re
import os
from typing import Dict, List, Tuple
import numpy as np
from config import MODEL_PATH, MAX_TEXT_LENGTH, TOP_K_PREDICTIONS

# Import NLTK stopwords (same as notebook)
try:
    from nltk.corpus import stopwords
    STOP_WORDS = set(stopwords.words('english'))
except LookupError:
    # If stopwords not downloaded, download them
    import nltk
    nltk.download('stopwords', quiet=True)
    from nltk.corpus import stopwords
    STOP_WORDS = set(stopwords.words('english'))

# Global variable to cache the loaded model
_model = None
_label_encoder_classes = None


def load_model():
    """
    Load the trained model from disk.
    The model is a scikit-learn Pipeline containing:
    - TfidfVectorizer (with ngram_range=(1, 2))
    - MultinomialNB classifier
    
    Returns:
        The loaded model pipeline
    
    Raises:
        FileNotFoundError: If model file doesn't exist
        Exception: If model loading fails
    """
    global _model, _label_encoder_classes
    
    if _model is not None:
        return _model
    
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH}. "
            f"Please ensure the model is exported from the notebook."
        )
    
    try:
        _model = joblib.load(MODEL_PATH)
        
        # Extract label encoder classes from the pipeline
        # The model predicts encoded labels (0-4), we need to map them back
        # Based on the notebook: ENTERTAINMENT=0, POLITICS=1, STYLE & BEAUTY=2, TRAVEL=3, WELLNESS=4
        _label_encoder_classes = np.array(['ENTERTAINMENT', 'POLITICS', 'STYLE & BEAUTY', 'TRAVEL', 'WELLNESS'])
        
        print(f"✓ Model loaded successfully from {MODEL_PATH}")
        return _model
    
    except Exception as e:
        raise Exception(f"Failed to load model: {str(e)}")


def preprocess_text(text: str) -> str:
    """
    Preprocess text using the EXACT same steps from the notebook.
    
    Steps (matching notebook preprocessing):
    1. Convert to lowercase
    2. Remove punctuation (keep only word characters and spaces)
    3. Remove stopwords (NLTK English stopwords)
    
    Args:
        text: Raw input text
        
    Returns:
        Preprocessed text string
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Truncate if too long
    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH]
    
    # Step 1: Lowercase (matches notebook: balanced_data['headline'].str.lower())
    text = text.lower()
    
    # Step 2: Remove punctuation (matches notebook: str.replace('[^\w\s]', '', regex=True))
    # Keep only word characters (letters, digits, underscore) and whitespace
    text = re.sub(r'[^\w\s]', '', text)
    
    # Step 3: Remove stopwords (matches notebook: apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words])))
    words = text.split()
    filtered_words = [word for word in words if word not in STOP_WORDS]
    text = ' '.join(filtered_words)
    
    return text


def predict(text: str) -> Dict:
    """
    Make a prediction on input text.
    
    Args:
        text: Raw input text
        
    Returns:
        Dictionary with prediction results:
        {
            "label": "POLITICS",
            "confidence": 0.87,
            "all_probabilities": [
                {"label": "POLITICS", "probability": 0.87},
                {"label": "WELLNESS", "probability": 0.08},
                ...
            ],
            "preprocessed_text": "cleaned text here"
        }
    
    Raises:
        ValueError: If text is empty after preprocessing
        Exception: If prediction fails
    """
    global _model, _label_encoder_classes
    
    # Ensure model is loaded
    if _model is None:
        load_model()
    
    # Preprocess the text
    preprocessed = preprocess_text(text)
    
    if not preprocessed.strip():
        raise ValueError("Text is empty after preprocessing. Please provide meaningful text.")
    
    try:
        # Get prediction (encoded label)
        prediction = _model.predict([preprocessed])[0]
        
        # Get prediction probabilities for all classes
        probabilities = _model.predict_proba([preprocessed])[0]
        
        # Map encoded prediction to actual label
        predicted_label = _label_encoder_classes[prediction]
        predicted_confidence = float(probabilities[prediction])
        
        # Create list of all probabilities sorted by confidence
        all_probs = [
            {
                "label": _label_encoder_classes[i],
                "probability": float(probabilities[i])
            }
            for i in range(len(_label_encoder_classes))
        ]
        # Sort by probability descending
        all_probs.sort(key=lambda x: x['probability'], reverse=True)
        
        # Limit to top K
        top_probs = all_probs[:TOP_K_PREDICTIONS]
        
        return {
            "label": predicted_label,
            "confidence": predicted_confidence,
            "all_probabilities": top_probs,
            "preprocessed_text": preprocessed
        }
    
    except Exception as e:
        raise Exception(f"Prediction failed: {str(e)}")


def get_model_info() -> Dict:
    """
    Get information about the loaded model.
    
    Returns:
        Dictionary with model metadata
    """
    global _model, _label_encoder_classes
    
    if _model is None:
        load_model()
    
    return {
        "model_type": "Scikit-learn Pipeline",
        "vectorizer": "TfidfVectorizer",
        "classifier": "MultinomialNB",
        "ngram_range": "(1, 2)",
        "categories": _label_encoder_classes.tolist() if _label_encoder_classes is not None else [],
        "preprocessing_steps": [
            "1. Lowercase conversion",
            "2. Punctuation removal",
            "3. Stopword removal (NLTK English)"
        ]
    }
