"""
Main application entry point for Video Shorts Generator
"""
import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from werkzeug.utils import secure_filename

from src.video_processor import VideoProcessor
from src.config_manager import ConfigManager
from src.utils import setup_directories, allowed_file, get_file_size

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
config = ConfigManager('config.yml')
app.config['MAX_CONTENT_LENGTH'] = config.get('uploads.max_file_size', 5368709120)
app.config['UPLOAD_FOLDER'] = config.get('uploads.upload_dir', './uploads')
app.config['OUTPUT_FOLDER'] = config.get('processing.output_dir', './outputs')

# Setup directories
setup_directories([
    app.config['UPLOAD_FOLDER'],
    app.config['OUTPUT_FOLDER'],
    config.get('processing.temp_dir', './temp'),
    './logs'
])

# Initialize video processor
video_processor = VideoProcessor(config)


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_video():
    """Handle video upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"File uploaded: {filepath}")
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully',
            'filename': filename,
            'file_id': filename,
            'size': get_file_size(filepath)
        }), 200
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/process', methods=['POST'])
def process_video():
    """Process video and generate shorts"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        shorts_duration = data.get('shorts_duration', 30)
        scene_detection = data.get('scene_detection', True)
        highlight_detection = data.get('highlight_detection', True)
        
        if not filename:
            return jsonify({'error': 'Filename required'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        logger.info(f"Processing video: {filepath}")
        
        # Process video
        shorts = video_processor.generate_shorts(
            video_path=filepath,
            shorts_duration=shorts_duration,
            enable_scene_detection=scene_detection,
            enable_highlight_detection=highlight_detection
        )
        
        # Save shorts
        output_files = []
        base_name = os.path.splitext(filename)[0]
        
        for idx, short in enumerate(shorts):
            output_filename = f"{base_name}_short_{idx}.mp4"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            short.save(output_path)
            output_files.append(output_filename)
        
        logger.info(f"Generated {len(output_files)} shorts")
        
        return jsonify({
            'success': True,
            'message': f'Generated {len(output_files)} shorts',
            'shorts': output_files,
            'count': len(output_files)
        }), 200
    
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_short(filename):
    """Download generated short"""
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get server status"""
    return jsonify({
        'status': 'running',
        'version': '1.0.0',
        'config': {
            'max_file_size': app.config['MAX_CONTENT_LENGTH'],
            'supported_formats': config.get('video.supported_formats'),
            'shorts_duration': config.get('shorts.default_duration')
        }
    }), 200


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('SERVER_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
