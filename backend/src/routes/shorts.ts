import express from 'express';

const router = express.Router();

// Generate shorts
router.post('/:videoId', (req, res) => {
  const videoId = req.params.videoId;
  res.json({
    videoId,
    shorts: [
      { id: 1, start: 0, end: 30, title: 'Highlight 1' },
      { id: 2, start: 45, end: 75, title: 'Highlight 2' },
      { id: 3, start: 90, end: 120, title: 'Highlight 3' }
    ]
  });
});

export default router;
