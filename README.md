# Video Shorts Generator

A web application that automatically creates short video clips from long videos by detecting and highlighting the main points.

## Features

- 🎬 Upload long-form videos (mp4, mov, webm)
- 🔍 AI-powered scene detection and summarization
- ✂️ Automatic clip extraction of key moments
- 📊 Visual timeline with detected highlights
- 💾 Download generated shorts in multiple formats
- 🎨 Customizable output settings (resolution, duration, effects)
- 📱 Responsive web interface

## Tech Stack

### Frontend
- **React** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **FFmpeg.js** - Video processing in browser

### Backend
- **Node.js + Express** - API server
- **Python** - AI/ML processing
- **FFmpeg** - Video encoding/decoding
- **OpenAI API / Gemini** - Scene analysis and summarization
- **MongoDB** - Data storage

## Project Structure

```
video-shorts-generator/
├── frontend/                 # React web application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API calls
│   │   ├── hooks/           # Custom React hooks
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile
├── backend/                  # Express API server
│   ├── src/
│   │   ├── routes/          # API endpoints
│   │   ├── controllers/      # Request handlers
│   │   ├── middleware/       # Custom middleware
│   │   ├── utils/           # Helper functions
│   │   └── server.ts
│   ├── package.json
│   └── Dockerfile
├── ai-service/              # Python ML service
│   ├── main.py              # Entry point
│   ├── analyzer.py          # Video analysis
│   ├── summarizer.py        # Scene summarization
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml       # Multi-container setup
└── docs/                    # Documentation
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- Docker & Docker Compose
- FFmpeg installed locally

### Quick Start (Docker)

```bash
docker-compose up -d
```

### Manual Setup

#### Frontend
```bash
cd frontend
npm install
npm start
```

#### Backend
```bash
cd backend
npm install
npm run dev
```

#### AI Service
```bash
cd ai-service
pip install -r requirements.txt
python main.py
```

## API Endpoints

- `POST /api/upload` - Upload a video
- `GET /api/videos/:id` - Get video details
- `POST /api/analyze/:id` - Analyze video for highlights
- `POST /api/generate-shorts/:id` - Generate short clips
- `GET /api/downloads/:id` - Download generated shorts

## Environment Variables

Create `.env` files in backend and ai-service directories:

```env
# Backend
OPENAI_API_KEY=your_key
MONGODB_URI=mongodb://localhost:27017/video-shorts
JWT_SECRET=your_secret

# AI Service
OPENAI_API_KEY=your_key
MODEL=gpt-4-vision
```

## Workflow

1. User uploads a long video
2. Backend stores video metadata in MongoDB
3. Video sent to AI service for analysis
4. AI service detects scenes, extracts transcripts, identifies key moments
5. Backend processes video with FFmpeg to create shorts
6. User can preview and download generated shorts

## Development

- `npm run dev` - Start with hot reload
- `npm run build` - Build for production
- `npm test` - Run tests

## Contributing

Pull requests welcome! Please create an issue first to discuss changes.

## License

MIT License - see LICENSE file for details

## Roadmap

- [ ] Multi-language subtitle support
- [ ] Custom highlight detection rules
- [ ] Batch processing
- [ ] Social media auto-posting
- [ ] Advanced editing features
- [ ] Real-time preview
