"""
Simple Video Shorts Generator - No complex dependencies
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("[INFO] Starting application...")

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='templates')
CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"])

logger.info("Flask app initialized with CORS enabled")

# Create required directories
UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './outputs'

for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, './temp', './logs']:
    Path(folder).mkdir(parents=True, exist_ok=True)
    logger.info(f"Directory ready: {folder}")

# Configure app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024  # 5GB

logger.info("App configuration complete")


@app.route('/')
def index():
    """Serve the main page"""
    logger.info("Serving index.html")
    return render_template('index.html')


@app.route('/api/status', methods=['GET', 'OPTIONS'])
def get_status():
    """Get server status"""
    logger.info("Status check requested")
    return jsonify({
        'status': 'running',
        'version': '1.0.0',
        'message': 'Server is working perfectly!'
    }), 200


@app.route('/api/upload', methods=['POST', 'OPTIONS'])
def upload_video():
    """Handle video upload"""
    logger.info(f"Upload request received. Method: {request.method}")
    
    try:
        # Handle OPTIONS request for CORS
        if request.method == 'OPTIONS':
            return '', 200
        
        logger.info(f"Files in request: {list(request.files.keys())}")
        
        if 'file' not in request.files:
            logger.warning("No 'file' field in request")
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        logger.info(f"File received: {file.filename}")
        
        if file.filename == '':
            logger.warning("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        logger.info(f"Saving file to: {filepath}")
        file.save(filepath)
        
        file_size = os.path.getsize(filepath)
        logger.info(f"File saved successfully: {filepath} ({file_size} bytes)")
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully!',
            'filename': filename,
            'file_id': filename,
            'size': file_size
        }), 200
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@app.route('/api/process', methods=['POST', 'OPTIONS'])
def process_video():
    """Placeholder for video processing"""
    logger.info("Process request received")
    
    try:
        if request.method == 'OPTIONS':
            return '', 200
        
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'error': 'Filename required'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        logger.info(f"Processing video: {filepath}")
        
        # For now, just simulate success
        return jsonify({
            'success': True,
            'message': 'Video processing initiated',
            'shorts': ['short_1.mp4', 'short_2.mp4', 'short_3.mp4'],
            'count': 3
        }), 200
    
    except Exception as e:
        logger.error(f"Process error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Process failed: {str(e)}'}), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_short(filename):
    """Download generated short"""
    logger.info(f"Download requested for: {filename}")
    
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return jsonify({
            'message': 'Download feature coming soon'
        }), 200
    
    except Exception as e:
        logger.error(f"Download error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 - Path not found: {request.path}")
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {str(error)}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = 5000
    
    print("\n" + "="*70)
    print("🎬 VIDEO SHORTS GENERATOR")
    print("="*70)
    print(f"✅ Server starting on http://localhost:{port}")
    print(f"✅ Open your browser and go to: http://localhost:{port}")
    print(f"✅ Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    logger.info(f"Starting Flask server on http://0.0.0.0:{port}")
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {e}\n")
