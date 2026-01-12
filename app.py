from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from dotenv import load_dotenv
from ai_engine import (
    get_crop_advisory,
    analyze_crop_image,
    get_planning_advisory,
    get_scheme_explanation
)
from werkzeug.utils import secure_filename

load_dotenv()


app = Flask(__name__)
CORS(app)


app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    """Get database connection"""
    conn = sqlite3.connect('annadata_saathi.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==================== ROUTES ====================

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/api/states', methods=['GET'])
def get_states():
    """Get list of all states"""
    states = [
        'Maharashtra', 'Punjab', 'Uttar Pradesh', 'Karnataka',
        'Tamil Nadu', 'Telangana', 'Andhra Pradesh', 'Gujarat',
        'Madhya Pradesh', 'Rajasthan', 'Bihar', 'West Bengal',
        'Odisha', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir'
    ]
    return jsonify({'states': states})

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get list of supported languages"""
    languages = {
        'hindi': 'हिंदी',
        'marathi': 'मराठी',
        'tamil': 'தமிழ்',
        'telugu': 'తెలుగు',
        'punjabi': 'ਪੰਜਾਬੀ',
        'bengali': 'বাংলা',
        'english': 'English'
    }
    return jsonify({'languages': languages})

@app.route('/api/crops', methods=['GET'])
def get_crops():
    """Get list of crops"""
    crops = [
        'Rice', 'Wheat', 'Cotton', 'Sugarcane', 'Maize',
        'Pulses (Dal)', 'Potato', 'Onion', 'Tomato', 'Chilli',
        'Coffee', 'Tea', 'Coconut', 'Banana', 'Mango',
        'Groundnut', 'Soybean', 'Sorghum', 'Barley', 'Vegetable'
    ]
    return jsonify({'crops': crops})

# ==================== SECTION 1: TEXT CROP ADVISORY ====================

@app.route('/api/crop-advisory', methods=['POST'])
def crop_advisory():
    """
    Section 1: Get AI-powered crop advisory
    """
    try:
        data = request.get_json()
        problem_text = data.get('problem', '').strip()
        crop_type = data.get('crop', '').strip()
        language = data.get('language', 'hindi').lower()

        if not problem_text or not crop_type:
            return jsonify({'error': 'Missing problem or crop type'}), 400

        
        advisory = get_crop_advisory(problem_text, crop_type, language)

        return jsonify({
            'success': True,
            'advisory': advisory,
            'disclaimer': 'This is AI-based advisory. Please consult local agricultural officers for confirmation.'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== SECTION 2: IMAGE ANALYSIS ====================

@app.route('/api/analyze-image', methods=['POST'])
def analyze_image():
    """
    Section 2: Analyze crop/leaf image
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        image_file = request.files['image']
        language = request.form.get('language', 'hindi').lower()

        if image_file.filename == '':
            return jsonify({'error': 'No image selected'}), 400

        if not allowed_file(image_file.filename):
            return jsonify({'error': 'Invalid file type. Please upload image (png, jpg, jpeg, gif, webp)'}), 400

        
        analysis = analyze_crop_image(image_file, language)

        return jsonify({
            'success': True,
            'analysis': analysis,
            'disclaimer': 'This is an AI estimation. Please consult local agricultural officers for accurate diagnosis.'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== SECTION 3: PLANNING ADVISORY ====================

@app.route('/api/planning-advisory', methods=['POST'])
def planning_advisory():
    """
    Section 3: Get weather/market planning advisory
    """
    try:
        data = request.get_json()
        crop_type = data.get('crop', '').strip()
        planning_type = data.get('planning_type', 'weather') 
        language = data.get('language', 'hindi').lower()

        if not crop_type:
            return jsonify({'error': 'Crop type is required'}), 400

        if planning_type not in ['weather', 'market']:
            return jsonify({'error': 'Invalid planning type'}), 400

        
        advisory = get_planning_advisory(crop_type, planning_type, language)
        
        
        if advisory.startswith('Error'):
            return jsonify({'error': advisory}), 500

        return jsonify({
            'success': True,
            'advisory': advisory,
            'planning_type': planning_type,
            'disclaimer': 'This is general advisory. Check official sources for specific forecasts and market data.'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== SECTION 4: GOVERNMENT SCHEMES ====================

@app.route('/api/schemes', methods=['POST'])
def get_schemes():
    """
    Section 4: Get government schemes for state/crop
    """
    try:
        data = request.get_json()
        state = data.get('state', '').strip()
        crop = data.get('crop', '').strip()
        language = data.get('language', 'hindi').lower()

        if not state or not crop:
            return jsonify({'error': 'State and crop are required'}), 400

        
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM government_schemes
            WHERE state = ? AND crop = ?
        ''', (state, crop))

        schemes = cursor.fetchall()
        conn.close()

        schemes_list = []
        for scheme in schemes:
            scheme_data = {
                'scheme_name': scheme['scheme_name'],
                'description': scheme['description'],
                'benefits': scheme['benefits'],
                'eligibility': scheme['eligibility'],
                'how_to_apply': scheme['how_to_apply'],
                'ministry': scheme['ministry']
            }
            schemes_list.append(scheme_data)

        
        if schemes_list:
            explanations = []
            for scheme in schemes_list:
                explanation = get_scheme_explanation(scheme['scheme_name'], scheme, language)
                explanations.append({
                    'scheme_name': scheme['scheme_name'],
                    'raw_data': scheme,
                    'explanation': explanation
                })
            return jsonify({'success': True, 'schemes': explanations})
        else:
            return jsonify({
                'success': True,
                'schemes': [],
                'message': f'No schemes found for {crop} in {state}. Please check other crops or contact agricultural department.'
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/schemes/all', methods=['GET'])
def get_all_schemes():
    """
    Get all schemes for a given state
    """
    try:
        state = request.args.get('state', '').strip()

        if not state:
            return jsonify({'error': 'State is required'}), 400

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT DISTINCT crop FROM government_schemes
            WHERE state = ?
            ORDER BY crop
        ''', (state,))

        crops_with_schemes = [row[0] for row in cursor.fetchall()]
        conn.close()

        return jsonify({'success': True, 'crops': crops_with_schemes})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== UTILITY ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Annadata Saathi is running'}), 200

@app.route('/api/info', methods=['GET'])
def app_info():
    """Get app information"""
    return jsonify({
        'app_name': 'Annadata Saathi',
        'tagline': 'An AI Agricultural Assistant for Indian Farmers',
        'version': '1.0',
        'features': [
            'Text-based crop advisory',
            'Image-based crop analysis',
            'Weather & market planning',
            'Government scheme discovery',
            'Multilingual support'
        ]
    })

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    
    from database.init_db import init_db
    if not os.path.exists('annadata_saathi.db'):
        init_db()
    
    
    app.run(debug=True, host='0.0.0.0', port=5000)
