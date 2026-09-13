import logging
from typing import List, Dict
import os
import openai

logger = logging.getLogger(__name__)

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')


def generate_highlights(scenes: List[Dict], video_id: str) -> List[Dict]:
    """
    Use AI to identify and rank the most important highlights from detected scenes.
    Returns sorted list of highlights with importance scores.
    """
    try:
        logger.info(f"Generating highlights for video: {video_id}")

        if not scenes:
            return []

        # Create a summary of scenes for AI analysis
        scene_descriptions = format_scenes_for_ai(scenes)

        # Use OpenAI to identify highlights
        highlights = rank_highlights_with_ai(scene_descriptions, scenes)

        logger.info(f"Generated {len(highlights)} highlights")
        return highlights

    except Exception as e:
        logger.error(f"Highlight generation error: {str(e)}")
        return []


def format_scenes_for_ai(scenes: List[Dict]) -> str:
    """
    Format detected scenes for AI analysis.
    """
    descriptions = []
    for i, scene in enumerate(scenes):
        desc = f"Scene {i+1}: {scene.get('description', 'Detected scene')} at {scene.get('timestamp', 0):.2f}s"
        descriptions.append(desc)
    return "\n".join(descriptions)


def rank_highlights_with_ai(scene_summary: str, scenes: List[Dict]) -> List[Dict]:
    """
    Use GPT to analyze scenes and rank them by importance for video shorts.
    """
    try:
        prompt = f"""
You are a video content analyst. Given these detected scenes from a video, 
identify and rank the 5 most engaging moments that would make good short-form video content.

Scenes detected:
{scene_summary}

For each highlight, provide:
1. Timestamp (in seconds)
2. Duration (in seconds)
3. Title for the short clip
4. Why it's important (1-2 sentences)
5. Importance score (0-1)

Return as JSON array.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a video content expert specializing in short-form video."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )

        # Parse response
        content = response.choices[0].message.content
        highlights = parse_ai_response(content, scenes)
        return highlights

    except Exception as e:
        logger.error(f"AI ranking error: {str(e)}")
        # Fallback: return top scenes by confidence
        return [
            {
                'start': scene['timestamp'],
                'end': scene['timestamp'] + scene.get('duration', 5),
                'title': f"Highlight {i+1}",
                'description': scene.get('description', 'Key moment'),
                'importance': scene.get('confidence', 0.5)
            }
            for i, scene in enumerate(sorted(scenes, key=lambda x: x.get('confidence', 0), reverse=True)[:5])
        ]


def parse_ai_response(response_text: str, scenes: List[Dict]) -> List[Dict]:
    """
    Parse AI response and extract highlights.
    """
    try:
        import json
        import re

        # Extract JSON from response
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            highlights_data = json.loads(json_match.group())
            highlights = []
            for item in highlights_data:
                highlights.append({
                    'start': float(item.get('start', item.get('timestamp', 0))),
                    'end': float(item.get('end', float(item.get('timestamp', 0)) + 5)),
                    'title': item.get('title', 'Highlight'),
                    'description': item.get('description', ''),
                    'importance': float(item.get('importance', 0.5))
                })
            return sorted(highlights, key=lambda x: x['importance'], reverse=True)
    except Exception as e:
        logger.error(f"Response parsing error: {str(e)}")

    return []
