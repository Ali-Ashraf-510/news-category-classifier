# 🗞️ News Category Classifier

Flask web application for classifying news headlines into 5 categories using NLP and Machine Learning.

## 🎯 Supported Categories

- **POLITICS** - Political news
- **WELLNESS** - Health and wellness
- **ENTERTAINMENT** - Entertainment news
- **TRAVEL** - Travel articles
- **STYLE & BEAUTY** - Fashion and beauty

---

## 🚀 Quick Start

### Method 1: Automated (Recommended)

```cmd
setup.bat    # Run once
run.bat      # To start the app
```

### Method 2: Manual

```cmd
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download NLTK stopwords
python -c "import nltk; nltk.download('stopwords')"

# 4. Run the application
python app.py
```

Then open: **http://localhost:5000**

---

## 📁 Project Structure

```
text classification using N-gram/
├── app.py                       # Flask server
├── model_utils.py               # Text processing and classification
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── static/                      # CSS & JS files
├── templates/                   # HTML pages
├── tests/                       # Unit tests
├── data/                        # Dataset files
├── notebooks/                   # Jupyter notebooks
├── text_classification_model.pkl # Trained model
├── setup.bat                    # Environment setup
└── run.bat                      # Run application
```

---

## 🔧 Requirements

- Python 3.8+
- Model file: `text_classification_model.pkl`

**Note:** If you don't have the model, train it from the Notebook: `Category Classifier.ipynb`

---

## 📡 API Endpoints

### تصنيف نص
```bash
POST /predict
Content-Type: application/json

{
  "text": "Trump announces new economic policy"
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "label": "POLITICS",
    "confidence": 0.87,
    "all_probabilities": [...],
    "preprocessed_text": "trump announces new economic policy"
  }
}
```

### Health Check
```bash
GET /health
```

---

## 🧪 Testing

```cmd
pytest tests/test_app.py -v
```

---

## 🛠️ Text Preprocessing

The app applies the same preprocessing pipeline from the Notebook:

1. **Convert to lowercase**
2. **Remove punctuation**
3. **Remove stopwords** (NLTK)
4. **TF-IDF Vectorization** - ngram_range=(1,2)
5. **Multinomial Naive Bayes** - classification

---

## 🐛 Troubleshooting

### Model not found
```
FileNotFoundError: Model file not found
```
**Solution:** Ensure `text_classification_model.pkl` exists in the root directory

### NLTK stopwords error
```
LookupError: Resource stopwords not found
```
**Solution:**
```python
python -c "import nltk; nltk.download('stopwords')"
```

### Port already in use
```
OSError: Address already in use
```
**Solution:** Change the port in `config.py`:
```python
PORT = 5001
```

---

## 📝 Development

### Adding new categories
1. Retrain the model with new categories
2. Update `CATEGORIES` in `config.py`
3. Add colors in `static/styles.css`

### Modifying preprocessing
Edit the `preprocess_text()` function in `model_utils.py`

---

## 📄 License

MIT License - Feel free to use this project

---

## 👤 Built With

- **Flask** - Web framework
- **scikit-learn** - Machine Learning
- **Bootstrap 5** - Frontend design
- **NLTK** - Natural Language Processing

---

**Ready to use!** 🎉
