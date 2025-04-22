from flask import Flask, request, jsonify, render_template
import os
import json
from dotenv import load_dotenv
from backend.agent import run_translation
from backend.utils import load_frame_data

# Load environment variables
load_dotenv()

app = Flask(__name__, 
            static_folder='../frontend/static',
            template_folder='../frontend/templates')

# Default Frame path
DEFAULT_FRAME_PATH = 'commerce-buy-frame.json'

@app.route('/')
def index():
    """Render homepage"""
    return render_template('index.html')

@app.route('/api/frame-info', methods=['GET'])
def get_frame_info():
    """Get Frame information"""
    frame_path = request.args.get('path', DEFAULT_FRAME_PATH)
    
    try:
        frame_data = load_frame_data(frame_path)
        return jsonify({
            'status': 'success',
            'data': {
                'frame_name': frame_data.get('frame_name', ''),
                'description': frame_data.get('description', ''),
                'lexical_units': [lu.get('lemma', '') for lu in frame_data.get('lexical_units', [])],
                'core_elements': [
                    {'name': el.get('name', ''), 'description': el.get('description', '')}
                    for el in frame_data.get('frame_elements', {}).get('core_elements', [])
                ],
                'non_core_elements': [
                    {'name': el.get('name', ''), 'description': el.get('description', '')}
                    for el in frame_data.get('frame_elements', {}).get('non_core_elements', [])
                ]
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Unable to load Frame data: {str(e)}'
        }), 500

@app.route('/api/translate', methods=['POST'])
def translate():
    """Perform translation"""
    data = request.json
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Request data is empty'
        }), 400
    
    source_text = data.get('source_text', '')
    source_language = data.get('source_language', '')
    target_language = data.get('target_language', '')
    frame_path = data.get('frame_path', DEFAULT_FRAME_PATH)
    
    if not source_text:
        return jsonify({
            'status': 'error',
            'message': 'Source text cannot be empty'
        }), 400
    
    if source_language not in ['English', 'Japanese']:
        return jsonify({
            'status': 'error',
            'message': 'Source language must be English or Japanese'
        }), 400
    
    if target_language not in ['English', 'Japanese']:
        return jsonify({
            'status': 'error',
            'message': 'Target language must be English or Japanese'
        }), 400
    
    if source_language == target_language:
        return jsonify({
            'status': 'error',
            'message': 'Source and target languages cannot be the same'
        }), 400
    
    try:
        # Execute translation
        result = run_translation(
            source_text=source_text,
            source_language=source_language,
            target_language=target_language,
            frame_path=frame_path
        )
        
        return jsonify({
            'status': 'success',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error during translation: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Ensure Frame file exists
    if not os.path.exists(DEFAULT_FRAME_PATH):
        print(f"Warning: Default Frame file {DEFAULT_FRAME_PATH} does not exist")
    
    # Start application
    app.run(debug=True, port=5000)
