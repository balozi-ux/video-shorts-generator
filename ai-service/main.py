from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Import analyzers
from analyzer import analyze_video
from summarizer import generate_highlights

# Setup Flask
app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.getenv('AI_SERVICE_PORT', 5000))


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'ai-service'})


@app.route('/analyze', methods=['POST'])
def analyze():
    """Main analysis endpoint"""
    try:
        data = request.json
        video_id = data.get('videoId')
        video_path = data.get('videoPath')
        title = data.get('title', 'Untitled')

        logger.info(f"Starting analysis for video: {video_id}")

        # Step 1: Analyze video for scenes and objects
        scenes = analyze_video(video_path)

        # Step 2: Generate highlights based on analysis
        highlights = generate_highlights(scenes, video_id)

        logger.info(f"Analysis complete for video: {video_id}")

        return jsonify({
            'videoId': video_id,
            'title': title,
            'scenes': scenes,
            'highlights': highlights,
            'status': 'completed'
        })

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/extract-shorts', methods=['POST'])
def extract_shorts():
    """Extract and create short clips"""
    try:
        data = request.json
        video_id = data.get('videoId')
        highlights = data.get('highlights')
        duration = data.get('duration', 60)

        logger.info(f"Extracting shorts for video: {video_id}")

        # Process highlights and create shorts
        shorts = []
        for i, highlight in enumerate(highlights[:5]):
            short = {
                'id': f"{video_id}_short_{i}",
                'startTime': highlight['start'],
                'endTime': highlight['end'],
                'title': highlight['title'],
                'score': highlight['importance']
            }
            shorts.append(short)

        return jsonify({
            'videoId': video_id,
            'shorts': shorts,
            'status': 'ready'
        })

    except Exception as e:
        logger.error(f"Shorts extraction error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
