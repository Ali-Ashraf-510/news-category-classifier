/**
 * Main JavaScript for News Category Classifier
 * Handles UI interactions and API calls
 */

// DOM Elements
const textInput = document.getElementById('textInput');
const predictBtn = document.getElementById('predictBtn');
const clearBtn = document.getElementById('clearBtn');
const charCount = document.getElementById('charCount');
const copyBtn = document.getElementById('copyBtn');
const modelInfoBtn = document.getElementById('modelInfoBtn');

// Results sections
const resultsEmpty = document.getElementById('resultsEmpty');
const resultsLoading = document.getElementById('resultsLoading');
const resultsError = document.getElementById('resultsError');
const resultsSuccess = document.getElementById('resultsSuccess');

// Result elements
const predictedLabel = document.getElementById('predictedLabel');
const confidenceText = document.getElementById('confidenceText');
const confidenceBar = document.getElementById('confidenceBar');
const confidencePercent = document.getElementById('confidencePercent');
const allProbabilities = document.getElementById('allProbabilities');
const preprocessedText = document.getElementById('preprocessedText');
const errorMessage = document.getElementById('errorMessage');

// State
let currentPrediction = null;

/**
 * Initialize event listeners
 */
function init() {
    // Character counter
    textInput.addEventListener('input', updateCharCount);
    
    // Example buttons
    const exampleBtns = document.querySelectorAll('.example-btn');
    exampleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            textInput.value = btn.dataset.text;
            updateCharCount();
            textInput.focus();
        });
    });
    
    // Main action buttons
    predictBtn.addEventListener('click', handlePredict);
    clearBtn.addEventListener('click', handleClear);
    copyBtn.addEventListener('click', handleCopy);
    modelInfoBtn.addEventListener('click', handleModelInfo);
    
    // Enter key to predict
    textInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            handlePredict();
        }
    });
    
    console.log('✓ App initialized');
}

/**
 * Update character count
 */
function updateCharCount() {
    const count = textInput.value.length;
    charCount.textContent = count;
    
    // Change color based on length
    if (count > 4500) {
        charCount.style.color = '#e74c3c';
    } else if (count > 4000) {
        charCount.style.color = '#f39c12';
    } else {
        charCount.style.color = '#4a90e2';
    }
}

/**
 * Show specific results section
 */
function showResultsSection(section) {
    resultsEmpty.style.display = 'none';
    resultsLoading.style.display = 'none';
    resultsError.style.display = 'none';
    resultsSuccess.style.display = 'none';
    
    if (section) {
        section.style.display = 'block';
    }
}

/**
 * Handle prediction
 */
async function handlePredict() {
    const text = textInput.value.trim();
    
    // Validate input
    if (!text) {
        showError('Please enter a headline to classify');
        return;
    }
    
    if (text.length > 5000) {
        showError('Text exceeds maximum length of 5000 characters');
        return;
    }
    
    // Show loading state
    showResultsSection(resultsLoading);
    predictBtn.disabled = true;
    predictBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Classifying...';
    
    try {
        // Make API call
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Prediction failed');
        }
        
        if (data.success) {
            currentPrediction = data.prediction;
            displayPrediction(data.prediction);
        } else {
            throw new Error(data.error || 'Unknown error');
        }
        
    } catch (error) {
        console.error('Prediction error:', error);
        showError(error.message || 'Failed to classify headline. Please try again.');
    } finally {
        // Reset button
        predictBtn.disabled = false;
        predictBtn.innerHTML = '<i class="bi bi-magic"></i> Classify Headline';
    }
}

/**
 * Display prediction results
 */
function displayPrediction(prediction) {
    // Show success section
    showResultsSection(resultsSuccess);
    
    // Main prediction
    predictedLabel.textContent = prediction.label;
    
    // Confidence
    const confidenceValue = (prediction.confidence * 100).toFixed(1);
    confidenceText.textContent = `${confidenceValue}%`;
    confidenceBar.style.width = `${confidenceValue}%`;
    confidencePercent.textContent = `${confidenceValue}%`;
    
    // Color code confidence bar
    if (prediction.confidence >= 0.7) {
        confidenceBar.className = 'progress-bar progress-bar-striped progress-bar-animated bg-success';
    } else if (prediction.confidence >= 0.5) {
        confidenceBar.className = 'progress-bar progress-bar-striped progress-bar-animated bg-warning';
    } else {
        confidenceBar.className = 'progress-bar progress-bar-striped progress-bar-animated bg-danger';
    }
    
    // Update category badge color
    const categoryColors = {
        'ENTERTAINMENT': '#e74c3c',
        'POLITICS': '#3498db',
        'STYLE & BEAUTY': '#e91e63',
        'TRAVEL': '#00bcd4',
        'WELLNESS': '#4caf50'
    };
    const categoryBadge = document.querySelector('.category-badge');
    if (categoryColors[prediction.label]) {
        categoryBadge.style.background = `linear-gradient(135deg, ${categoryColors[prediction.label]} 0%, ${adjustColor(categoryColors[prediction.label], 20)} 100%)`;
    }
    
    // All probabilities
    displayAllProbabilities(prediction.all_probabilities);
    
    // Preprocessed text
    preprocessedText.textContent = prediction.preprocessed_text || 'N/A';
    
    // Smooth scroll to results (mobile)
    if (window.innerWidth < 768) {
        resultsSuccess.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

/**
 * Display all probability scores
 */
function displayAllProbabilities(probabilities) {
    allProbabilities.innerHTML = '';
    
    probabilities.forEach((item, index) => {
        const percentage = (item.probability * 100).toFixed(1);
        
        const itemDiv = document.createElement('div');
        itemDiv.className = 'probability-item';
        itemDiv.style.animationDelay = `${index * 0.1}s`;
        
        itemDiv.innerHTML = `
            <span class="probability-label">${item.label}</span>
            <div class="probability-bar-container">
                <div class="probability-bar">
                    <div class="probability-bar-fill" style="width: ${percentage}%"></div>
                </div>
            </div>
            <span class="probability-value">${percentage}%</span>
        `;
        
        allProbabilities.appendChild(itemDiv);
    });
}

/**
 * Show error message
 */
function showError(message) {
    showResultsSection(resultsError);
    errorMessage.textContent = message;
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (resultsError.style.display === 'block') {
            showResultsSection(resultsEmpty);
        }
    }, 5000);
}

/**
 * Handle clear button
 */
function handleClear() {
    textInput.value = '';
    updateCharCount();
    showResultsSection(resultsEmpty);
    currentPrediction = null;
    textInput.focus();
}

/**
 * Handle copy button
 */
function handleCopy() {
    if (!currentPrediction) return;
    
    const textToCopy = `Predicted Category: ${currentPrediction.label}\nConfidence: ${(currentPrediction.confidence * 100).toFixed(1)}%`;
    
    navigator.clipboard.writeText(textToCopy).then(() => {
        // Visual feedback
        copyBtn.classList.add('copied');
        copyBtn.innerHTML = '<i class="bi bi-check"></i> Copied!';
        
        setTimeout(() => {
            copyBtn.classList.remove('copied');
            copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy to clipboard');
    });
}

/**
 * Handle model info button
 */
async function handleModelInfo() {
    const modal = new bootstrap.Modal(document.getElementById('modelInfoModal'));
    const modalContent = document.getElementById('modelInfoContent');
    
    modal.show();
    
    try {
        const response = await fetch('/model-info');
        const data = await response.json();
        
        if (data.success) {
            const info = data.model_info;
            
            modalContent.innerHTML = `
                <div class="mb-3">
                    <h6 class="text-muted mb-2">Model Architecture</h6>
                    <ul class="list-unstyled">
                        <li><strong>Type:</strong> ${info.model_type}</li>
                        <li><strong>Vectorizer:</strong> ${info.vectorizer}</li>
                        <li><strong>Classifier:</strong> ${info.classifier}</li>
                        <li><strong>N-gram Range:</strong> ${info.ngram_range}</li>
                    </ul>
                </div>
                
                <div class="mb-3">
                    <h6 class="text-muted mb-2">Categories</h6>
                    <div class="d-flex flex-wrap gap-2">
                        ${info.categories.map(cat => `<span class="badge bg-secondary">${cat}</span>`).join('')}
                    </div>
                </div>
                
                <div>
                    <h6 class="text-muted mb-2">Preprocessing Pipeline</h6>
                    <ol class="mb-0">
                        ${info.preprocessing_steps.map(step => `<li>${step}</li>`).join('')}
                    </ol>
                </div>
            `;
        } else {
            modalContent.innerHTML = `
                <div class="alert alert-danger">
                    Failed to load model information
                </div>
            `;
        }
    } catch (error) {
        console.error('Failed to fetch model info:', error);
        modalContent.innerHTML = `
            <div class="alert alert-danger">
                Error loading model information: ${error.message}
            </div>
        `;
    }
}

/**
 * Utility: Adjust color brightness
 */
function adjustColor(color, percent) {
    const num = parseInt(color.replace("#", ""), 16);
    const amt = Math.round(2.55 * percent);
    const R = (num >> 16) + amt;
    const G = (num >> 8 & 0x00FF) + amt;
    const B = (num & 0x0000FF) + amt;
    return "#" + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 +
        (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 +
        (B < 255 ? B < 1 ? 0 : B : 255))
        .toString(16).slice(1);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
