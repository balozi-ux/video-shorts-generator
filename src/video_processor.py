"""
Video processor module - handles video analysis and shorts generation
"""
import cv2
import numpy as np
from pathlib import Path
import logging
from typing import List, Optional
import torch
from torchvision import transforms
from PIL import Image

logger = logging.getLogger(__name__)


class VideoClip:
    """Represents a video clip/short"""
    
    def __init__(self, frames: List[np.ndarray], audio: Optional[np.ndarray] = None, fps: float = 30):
        self.frames = frames
        self.audio = audio
        self.fps = fps
        self.duration = len(frames) / fps
    
    def save(self, output_path: str, codec: str = 'mp4v', bitrate: str = '5000k'):
        """Save clip to file"""
        if not self.frames:
            raise ValueError("No frames to save")
        
        height, width = self.frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*codec.replace('4', '').ljust(4))
        
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (width, height))
        
        for frame in self.frames:
            out.write(frame)
        
        out.release()
        logger.info(f"Saved clip to {output_path}")


class SceneDetector:
    """Detects scene changes in video"""
    
    def __init__(self, threshold: float = 25.0):
        self.threshold = threshold
    
    def detect_scenes(self, frames: List[np.ndarray]) -> List[int]:
        """Detect scene changes and return frame indices"""
        scenes = [0]
        
        if len(frames) < 2:
            return scenes
        
        prev_frame = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        
        for i in range(1, len(frames)):
            curr_frame = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
            
            # Calculate histogram difference
            hist_prev = cv2.calcHist([prev_frame], [0], None, [256], [0, 256])
            hist_curr = cv2.calcHist([curr_frame], [0], None, [256], [0, 256])
            
            diff = cv2.compareHist(hist_prev, hist_curr, cv2.HISTCMP_BHATTACHARYYA)
            
            if diff > self.threshold / 100:
                scenes.append(i)
            
            prev_frame = curr_frame
        
        return scenes


class HighlightDetector:
    """Detects highlights/interesting moments in video"""
    
    def __init__(self, confidence_threshold: float = 0.7):
        self.confidence_threshold = confidence_threshold
    
    def detect_highlights(self, frames: List[np.ndarray]) -> List[tuple]:
        """Detect highlights and return (start_frame, end_frame, score)"""
        highlights = []
        
        # Simple motion-based detection
        if len(frames) < 2:
            return highlights
        
        prev_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        motion_scores = [0]
        
        for i in range(1, len(frames)):
            curr_gray = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
            
            # Calculate optical flow
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
            )
            
            magnitude = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
            avg_motion = np.mean(magnitude)
            motion_scores.append(avg_motion)
            
            prev_gray = curr_gray
        
        # Find peaks in motion
        threshold = np.mean(motion_scores) + np.std(motion_scores)
        
        in_highlight = False
        start = 0
        
        for i, score in enumerate(motion_scores):
            if score > threshold and not in_highlight:
                start = i
                in_highlight = True
            elif score <= threshold and in_highlight:
                highlights.append((start, i, np.mean(motion_scores[start:i])))
                in_highlight = False
        
        if in_highlight:
            highlights.append((start, len(motion_scores) - 1, np.mean(motion_scores[start:])))
        
        return highlights


class VideoProcessor:
    """Main video processor class"""
    
    def __init__(self, config):
        self.config = config
        self.scene_detector = SceneDetector(
            threshold=config.get('ai.scene_threshold', 25.0)
        )
        self.highlight_detector = HighlightDetector(
            confidence_threshold=config.get('ai.highlight_confidence', 0.7)
        )
    
    def load_video(self, video_path: str) -> tuple:
        """Load video and extract frames"""
        logger.info(f"Loading video: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        
        cap.release()
        logger.info(f"Loaded {len(frames)} frames at {fps} FPS")
        
        return frames, fps
    
    def crop_to_shorts_aspect_ratio(self, frames: List[np.ndarray]) -> List[np.ndarray]:
        """Crop frames to 9:16 aspect ratio"""
        cropped = []
        
        for frame in frames:
            h, w = frame.shape[:2]
            target_aspect = 9 / 16
            current_aspect = w / h
            
            if current_aspect > target_aspect:
                # Width is too wide
                new_w = int(h * target_aspect)
                x_offset = (w - new_w) // 2
                cropped_frame = frame[:, x_offset:x_offset + new_w]
            else:
                # Height is too tall
                new_h = int(w / target_aspect)
                y_offset = (h - new_h) // 2
                cropped_frame = frame[y_offset:y_offset + new_h, :]
            
            # Resize to target resolution
            target_size = self.config.get('shorts.resolution', '1080x1920').split('x')
            target_w, target_h = int(target_size[0]), int(target_size[1])
            cropped_frame = cv2.resize(cropped_frame, (target_w, target_h))
            cropped.append(cropped_frame)
        
        return cropped
    
    def generate_shorts(
        self,
        video_path: str,
        shorts_duration: int = 30,
        enable_scene_detection: bool = True,
        enable_highlight_detection: bool = True
    ) -> List[VideoClip]:
        """Generate shorts from video"""
        
        # Load video
        frames, fps = self.load_video(video_path)
        
        # Crop to shorts aspect ratio
        frames = self.crop_to_shorts_aspect_ratio(frames)
        
        # Calculate frames per short
        frames_per_short = int(shorts_duration * fps)
        
        # Detect scenes/highlights
        cut_points = [0]
        
        if enable_scene_detection:
            scene_cuts = self.scene_detector.detect_scenes(frames)
            cut_points.extend(scene_cuts)
        
        if enable_highlight_detection:
            highlights = self.highlight_detector.detect_highlights(frames)
            for start, end, score in highlights:
                cut_points.append(start)
                cut_points.append(end)
        
        # Remove duplicates and sort
        cut_points = sorted(list(set(cut_points)))
        cut_points.append(len(frames))
        
        # Generate shorts
        shorts = []
        
        for i in range(len(cut_points) - 1):
            start = cut_points[i]
            end = min(cut_points[i + 1], start + frames_per_short)
            
            if end - start >= frames_per_short * 0.5:  # At least 50% of target duration
                short_frames = frames[start:end]
                short = VideoClip(short_frames, fps=fps)
                shorts.append(short)
        
        # If no shorts generated, create uniform shorts
        if not shorts:
            for i in range(0, len(frames), frames_per_short):
                end = min(i + frames_per_short, len(frames))
                short_frames = frames[i:end]
                if short_frames:
                    short = VideoClip(short_frames, fps=fps)
                    shorts.append(short)
        
        logger.info(f"Generated {len(shorts)} shorts")
        return shorts
