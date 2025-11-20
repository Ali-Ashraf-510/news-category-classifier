"""
Flask NLP News Category Classification Web App

This application loads a trained ML model and provides a web interface
for classifying news headlines into categories.
"""
from flask import Flask, render_template, request, jsonify
import logging
from model_utils import load_model, predict, get_model_info
from config import DEBUG, HOST, PORT, MAX_TEXT_LENGTH

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load model at startup
try:
    load_model()
    logger.info("✓ Model loaded successfully at startup")
except Exception as e:
    logger.error(f"✗ Failed to load model at startup: {str(e)}")
    logger.warning("App will start but predictions will fail until model is loaded")


@app.route('/')
def index():
    """
    Render the main page.
    
    Returns:
        Rendered HTML template
    """
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    
    Returns:
        JSON with health status and model information
    """
    try:
        model_info = get_model_info()
        return jsonify({
            "status": "healthy",
            "message": "Application is running",
            "model_loaded": True,
            "model_info": model_info
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "message": str(e),
            "model_loaded": False
        }), 500


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    """
    Prediction endpoint.
    
    Expected JSON payload:
    {
        "text": "Your news headline here"
    }
    
    Returns:
        JSON with prediction results:
        {
            "success": true,
            "prediction": {
                "label": "POLITICS",
                "confidence": 0.87,
                "all_probabilities": [...],
                "preprocessed_text": "..."
            }
        }
    """
    try:
        # Validate content type
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        # Get JSON data
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        if 'text' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'text' field in request"
            }), 400
        
        text = data['text']
        
        # Validate text
        if not text or not isinstance(text, str):
            return jsonify({
                "success": False,
                "error": "Text must be a non-empty string"
            }), 400
        
        if not text.strip():
            return jsonify({
                "success": False,
                "error": "Text cannot be empty or only whitespace"
            }), 400
        
        if len(text) > MAX_TEXT_LENGTH:
            return jsonify({
                "success": False,
                "error": f"Text exceeds maximum length of {MAX_TEXT_LENGTH} characters"
            }), 400
        
        # Make prediction
        logger.info(f"Making prediction for text: {text[:50]}...")
        result = predict(text)
        
        logger.info(f"Prediction successful: {result['label']} ({result['confidence']:.2%})")
        
        return jsonify({
            "success": True,
            "prediction": result
        }), 200
    
    except ValueError as e:
        # Validation errors
        logger.warning(f"Validation error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    
    except Exception as e:
        # Server errors
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "Internal server error occurred during prediction",
            "details": str(e) if DEBUG else None
        }), 500


@app.route('/model-info', methods=['GET'])
def model_info():
    """
    Get model information endpoint.
    
    Returns:
        JSON with model metadata
    """
    try:
        info = get_model_info()
        return jsonify({
            "success": True,
            "model_info": info
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        "success": False,
        "error": "Method not allowed"
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    logger.info(f"Starting Flask app on {HOST}:{PORT}")
    logger.info(f"Debug mode: {DEBUG}")
    logger.info("Access the app at: http://localhost:5000")
    
    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
