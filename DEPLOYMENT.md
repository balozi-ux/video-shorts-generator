# Deployment Guide

## Local Development

### Prerequisites
- Python 3.8+
- FFmpeg installed on your system
- 4GB+ RAM recommended

### Setup

1. Clone the repository
```bash
git clone https://github.com/balozi-ux/video-shorts-generator.git
cd video-shorts-generator
```

2. Create and activate virtual environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file
```bash
cp .env.example .env
```

5. Create necessary directories
```bash
mkdir -p uploads outputs temp logs
```

6. Run the application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Docker Deployment

### Build Docker Image

```bash
docker build -t video-shorts-generator .
```

### Run with Docker

```bash
docker run -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  video-shorts-generator
```

## Production Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Nginx (Reverse Proxy)

Create `/etc/nginx/sites-available/shorts-generator`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 5G;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/shorts-generator /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Environment Variables

Key configuration variables:

- `FLASK_ENV`: Set to `production` for production
- `FLASK_DEBUG`: Set to `False` for production
- `SERVER_PORT`: Port to run the server on (default: 5000)
- `USE_GPU`: Enable GPU acceleration (default: true)
- `MAX_WORKERS`: Number of processing workers (default: 4)

## Performance Optimization

1. **GPU Acceleration**: Enable CUDA support for faster processing
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Increase Workers**: Adjust `MAX_WORKERS` based on available CPU cores

3. **Cache Management**: Regularly clean up temp directory

## Monitoring

View logs:
```bash
tail -f logs/app.log
```

## Health Check

```bash
curl http://localhost:5000/api/status
```

Expected response:
```json
{
  "status": "running",
  "version": "1.0.0",
  "config": { ... }
}
```
