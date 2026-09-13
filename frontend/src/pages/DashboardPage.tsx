import React, { useState, useEffect } from 'react';
import { Play, Download, Trash2 } from 'lucide-react';
import axios from 'axios';

interface Video {
  id: string;
  title: string;
  createdAt: string;
  status: 'uploaded' | 'analyzing' | 'ready';
  shortsCount?: number;
}

const DashboardPage: React.FC = () => {
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchVideos();
  }, []);

  const fetchVideos = async () => {
    try {
      const response = await axios.get('/api/videos');
      setVideos(response.data);
    } catch (error) {
      console.error('Failed to fetch videos:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="py-12">
      <h1 className="text-4xl font-bold mb-8">Dashboard</h1>
      
      {loading ? (
        <div className="text-center py-12">Loading...</div>
      ) : videos.length === 0 ? (
        <div className="text-center py-12 text-gray-400">
          <p>No videos yet. Start by uploading one!</p>
        </div>
      ) : (
        <div className="grid gap-6">
          {videos.map((video) => (
            <div key={video.id} className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-blue-500 transition">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-xl font-semibold">{video.title}</h3>
                  <p className="text-sm text-gray-400">Status: {video.status}</p>
                  <p className="text-sm text-gray-400">Shorts: {video.shortsCount || 0}</p>
                </div>
                <div className="flex gap-2">
                  <button className="p-2 bg-blue-600 rounded hover:bg-blue-700 transition">
                    <Play className="w-5 h-5" />
                  </button>
                  <button className="p-2 bg-green-600 rounded hover:bg-green-700 transition">
                    <Download className="w-5 h-5" />
                  </button>
                  <button className="p-2 bg-red-600 rounded hover:bg-red-700 transition">
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DashboardPage;
