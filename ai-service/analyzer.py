import logging
from typing import List, Dict
import subprocess
import json

logger = logging.getLogger(__name__)


def analyze_video(video_path: str) -> List[Dict]:
    """
    Analyze video for scenes, transitions, and key moments.
    Returns list of detected scenes with timestamps and metadata.
    """
    try:
        logger.info(f"Analyzing video: {video_path}")

        # Get video metadata (duration, fps, resolution)
        metadata = get_video_metadata(video_path)
        logger.info(f"Video metadata: {metadata}")

        # Detect scenes using FFmpeg and scene detection
        scenes = detect_scenes(video_path, metadata)

        # Extract frames from key moments
        frames = extract_key_frames(video_path, scenes)

        # Combine data
        results = [
            {
                'timestamp': scene['timestamp'],
                'duration': scene['duration'],
                'sceneType': scene['type'],
                'confidence': scene['confidence'],
                'description': scene.get('description', 'Scene detected')
            }
            for scene in scenes
        ]

        return results

    except Exception as e:
        logger.error(f"Video analysis error: {str(e)}")
        return []


def get_video_metadata(video_path: str) -> Dict:
    """
    Extract video metadata using FFprobe.
    """
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-show_entries', 'stream=width,height,r_frame_rate',
            '-of', 'json',
            video_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)

        return {
            'duration': float(data['format']['duration']),
            'width': data['streams'][0].get('width', 1920),
            'height': data['streams'][0].get('height', 1080),
            'fps': eval(data['streams'][0]['r_frame_rate'])
        }
    except Exception as e:
        logger.error(f"Metadata extraction error: {str(e)}")
        return {'duration': 0, 'width': 1920, 'height': 1080, 'fps': 30}


def detect_scenes(video_path: str, metadata: Dict) -> List[Dict]:
    """
    Detect scene boundaries and transitions using FFmpeg.
    """
    try:
        # Use FFmpeg to detect scene changes
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', 'select=\'gt(scene,0.4)\',showinfo',
            '-f', 'null',
            '-'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        scenes = []

        # Parse ffmpeg output for scene detection
        for line in result.stderr.split('\n'):
            if 'pts_time' in line:
                # Extract timestamp from ffmpeg output
                try:
                    parts = line.split('pts_time=')
                    if len(parts) > 1:
                        timestamp = float(parts[1].split()[0])
                        scenes.append({
                            'timestamp': timestamp,
                            'duration': 5,  # Default 5-second clips
                            'type': 'scene_change',
                            'confidence': 0.8
                        })
                except:
                    pass

        return scenes if scenes else [
            {'timestamp': i * 10, 'duration': 5, 'type': 'sampled', 'confidence': 0.5}
            for i in range(int(metadata['duration']) // 10)
        ]

    except Exception as e:
        logger.error(f"Scene detection error: {str(e)}")
        return []


def extract_key_frames(video_path: str, scenes: List[Dict]) -> List[str]:
    """
    Extract key frames from detected scenes.
    """
    try:
        frames = []
        for scene in scenes[:10]:  # Limit to first 10 scenes
            timestamp = scene['timestamp']
            # Extract frame at timestamp
            # This would use FFmpeg to extract and save frame
            frames.append(f"frame_{int(timestamp)}.jpg")
        return frames
    except Exception as e:
        logger.error(f"Frame extraction error: {str(e)}")
        return []
