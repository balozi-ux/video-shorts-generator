import express from 'express';

const router = express.Router();

// Analyze video
router.post('/:videoId', (req, res) => {
  const videoId = req.params.videoId;
  res.json({
    videoId,
    status: 'analyzing',
    message: 'Video analysis started'
  });
});

export default router;
