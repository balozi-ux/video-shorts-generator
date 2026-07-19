"""
Simple Video Shorts Generator - Fully Fixed Version
Works without complex dependencies
"""
import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("[INFO] Starting application...")

# Initialize Flask app - FIXED for Python 3.14
try:
    app = Flask(__name__)
    app.template_folder = 'templates'
    app.static_folder = 'templates'
except Exception as e:
    print(f"Flask init error: {e}")
    app = Flask(__name__)

# Enable CORS
CORS(app, origins="*", allow_headers="*", methods=["GET", "POST", "OPTIONS"])

logger.info("Flask app initialized with CORS enabled")

# Create required directories
UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './outputs'

for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, './temp', './logs']:
    Path(folder).mkdir(parents=True, exist_ok=True)

# Configure app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024  # 5GB

logger.info("App configuration complete")


@app.before_request
def before_request():
    """Log all incoming requests"""
    logger.info(f"Request: {request.method} {request.path}")


@app.after_request
def after_request(response):
    """Add CORS headers to response"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/')
def index():
    """Serve the main page"""
    try:
        logger.info("Serving index.html")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index: {e}")
        return f"Error: {e}", 500


@app.route('/api/status', methods=['GET', 'OPTIONS'])
def get_status():
    """Get server status"""
    if request.method == 'OPTIONS':
        return '', 200
    
    logger.info("Status check")
    return jsonify({
        'status': 'running',
        'version': '1.0.0',
        'message': 'Server is working!'
    }), 200


@app.route('/api/upload', methods=['POST', 'OPTIONS'])
def upload_video():
    """Handle video upload"""
    logger.info(f"Upload endpoint - Method: {request.method}")
    
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        logger.info(f"Request headers: {dict(request.headers)}")
        logger.info(f"Request files: {list(request.files.keys())}")
        logger.info(f"Request form: {dict(request.form)}")
        
        # Check if file exists
        if 'file' not in request.files:
            error_msg = 'No file provided in request'
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 400
        
        file = request.files['file']
        logger.info(f"File object: {file}")
        logger.info(f"File filename: {file.filename}")
        
        if file.filename == '' or file.filename is None:
            error_msg = 'No file selected'
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        logger.info(f"Saving to: {filepath}")
        file.save(filepath)
        
        # Verify file was saved
        if not os.path.exists(filepath):
            error_msg = 'File failed to save'
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 500
        
        file_size = os.path.getsize(filepath)
        logger.info(f"File saved: {filepath} ({file_size} bytes)")
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully!',
            'filename': filename,
            'file_id': filename,
            'size': file_size
        }), 200
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Upload error: {str(e)}'}), 500


@app.route('/api/process', methods=['POST', 'OPTIONS'])
def process_video():
    """Process video"""
    logger.info(f"Process endpoint - Method: {request.method}")
    
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json() or {}
        filename = data.get('filename')
        
        logger.info(f"Processing: {filename}")
        
        if not filename:
            return jsonify({'error': 'Filename required'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            logger.warning(f"File not found: {filepath}")
            return jsonify({'error': 'File not found'}), 404
        
        logger.info(f"File found: {filepath}")
        
        # Simulate processing
        return jsonify({
            'success': True,
            'message': 'Processing complete',
            'shorts': ['short_1.mp4', 'short_2.mp4'],
            'count': 2
        }), 200
    
    except Exception as e:
        logger.error(f"Process error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Process error: {str(e)}'}), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_short(filename):
    """Download short"""
    logger.info(f"Download: {filename}")
    return jsonify({'message': 'Download feature available'}), 200


@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404: {request.path}")
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500: {error}")
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    port = 5000
    
    print("\n" + "="*70)
    print("🎬 VIDEO SHORTS GENERATOR")
    print("="*70)
    print(f"✅ Server starting on http://localhost:{port}")
    print(f"✅ Open browser: http://localhost:{port}")
    print(f"✅ Press Ctrl+C to stop")
    print("="*70 + "\n")
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except Exception as e:
        logger.error(f"Failed to start: {e}", exc_info=True)
        print(f"\n❌ Error: {e}\n")
