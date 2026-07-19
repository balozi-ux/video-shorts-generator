# Video Shorts Generator - Usage Guide

## Basic Usage

### Web Interface

1. Open `http://localhost:5000` in your browser
2. Upload a video file (drag & drop or click to select)
3. Configure settings:
   - **Shorts Duration**: Length of each short (15-60 seconds)
   - **Scene Detection**: Automatically detect scene changes
   - **Highlight Detection**: Find the most interesting moments
4. Click "Generate Shorts"
5. Download your generated shorts

### Python API

```python
from src.video_processor import VideoProcessor
from src.config_manager import ConfigManager

# Load configuration
config = ConfigManager('config.yml')

# Initialize processor
processor = VideoProcessor(config)

# Generate shorts
shorts = processor.generate_shorts(
    video_path='input_video.mp4',
    shorts_duration=30,
    enable_scene_detection=True,
    enable_highlight_detection=True
)

# Save shorts
for idx, short in enumerate(shorts):
    short.save(f'output_short_{idx}.mp4')
```

## Advanced Configuration

### Scene Detection

Scene detection automatically cuts the video at scene changes. Adjust the threshold in `config.yml`:

```yaml
ai:
  scene_threshold: 25.0  # Range: 5-100, higher = fewer cuts
```

### Highlight Detection

Highlight detection finds the most interesting moments based on motion:

```yaml
ai:
  highlight_confidence: 0.7  # Range: 0-1, higher = stricter
```

### Custom Aspect Ratio

While the default is 9:16 (vertical), you can customize in `config.yml`:

```yaml
shorts:
  aspect_ratio: "16:9"  # For horizontal
  resolution: "1920x1080"
  frame_rate: 30
  codec: "h264"
  bitrate: "5000k"
```

## Examples

### Example 1: Basic Usage

```python
from src.video_processor import VideoProcessor
from src.config_manager import ConfigManager

config = ConfigManager('config.yml')
processor = VideoProcessor(config)

shorts = processor.generate_shorts('my_video.mp4')

for idx, short in enumerate(shorts):
    short.save(f'short_{idx}.mp4')
```

### Example 2: Batch Processing

```python
import os
from src.video_processor import VideoProcessor
from src.config_manager import ConfigManager

config = ConfigManager('config.yml')
processor = VideoProcessor(config)

video_dir = './videos'
for video_file in os.listdir(video_dir):
    if video_file.endswith(('.mp4', '.mov')):
        print(f"Processing {video_file}...")
        
        shorts = processor.generate_shorts(
            os.path.join(video_dir, video_file),
            shorts_duration=45
        )
        
        output_dir = f'./outputs/{video_file[:-4]}'
        os.makedirs(output_dir, exist_ok=True)
        
        for idx, short in enumerate(shorts):
            short.save(f'{output_dir}/short_{idx}.mp4')
```

### Example 3: Custom Processing

```python
from src.video_processor import VideoProcessor, VideoClip
from src.config_manager import ConfigManager

config = ConfigManager('config.yml')
processor = VideoProcessor(config)

# Load video
frames, fps = processor.load_video('input.mp4')

# Custom cropping
frames = processor.crop_to_shorts_aspect_ratio(frames)

# Create custom short (15 seconds)
short_frames = frames[:int(15 * fps)]
short = VideoClip(short_frames, fps=fps)

# Save
short.save('custom_short.mp4')
```

## API Endpoints

### Upload Video

```bash
POST /api/upload
Content-Type: multipart/form-data

file: <video file>
```

**Response:**
```json
{
  "success": true,
  "filename": "video.mp4",
  "file_id": "video.mp4",
  "size": 524288000
}
```

### Process Video

```bash
POST /api/process
Content-Type: application/json

{
  "filename": "video.mp4",
  "shorts_duration": 30,
  "scene_detection": true,
  "highlight_detection": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Generated 5 shorts",
  "shorts": [
    "video_short_0.mp4",
    "video_short_1.mp4",
    "video_short_2.mp4",
    "video_short_3.mp4",
    "video_short_4.mp4"
  ],
  "count": 5
}
```

### Download Short

```bash
GET /api/download/<filename>
```

### Get Status

```bash
GET /api/status
```

**Response:**
```json
{
  "status": "running",
  "version": "1.0.0",
  "config": {
    "max_file_size": 5368709120,
    "supported_formats": ["mp4", "mov", "avi", "webm", "mkv", "flv"],
    "shorts_duration": 30
  }
}
```

## Performance Tips

1. **Reduce Input Resolution**: Large videos take longer to process
2. **Disable Unnecessary Features**: Turn off scene/highlight detection if not needed
3. **Use GPU**: Enable CUDA for faster processing
4. **Adjust Worker Count**: Set `MAX_WORKERS` based on available cores

## Common Issues

### "Video could not be opened"
- Ensure FFmpeg is installed
- Check video format is supported
- Verify file is not corrupted

### "Out of memory"
- Reduce input video resolution
- Process shorter videos
- Increase available RAM

### "Slow processing"
- Enable GPU acceleration
- Increase worker count
- Reduce output quality

## File Size Limits

Default: 5GB
To change, modify in `config.yml`:

```yaml
uploads:
  max_file_size: 10737418240  # 10GB
```

## Supported Formats

- MP4
- MOV
- AVI
- WebM
- MKV
- FLV
- WMV

## Output Formats

Currently outputs in MP4 format with H.264 codec. Customize in `config.yml`:

```yaml
shorts:
  codec: "h264"
  bitrate: "5000k"
```
