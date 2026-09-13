import express from 'express';

const router = express.Router();

// Get all videos
router.get('/', (req, res) => {
  res.json([
    {
      id: '1',
      title: 'Sample Video',
      createdAt: new Date().toISOString(),
      status: 'ready',
      shortsCount: 5
    }
  ]);
});

// Get video by ID
router.get('/:id', (req, res) => {
  res.json({
    id: req.params.id,
    title: 'Sample Video',
    createdAt: new Date().toISOString(),
    status: 'ready'
  });
});

export default router;
