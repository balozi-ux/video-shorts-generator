import React from 'react';
import { useParams } from 'react-router-dom';
import { Download, Share2 } from 'lucide-react';

const ShortsPage: React.FC = () => {
  const { videoId } = useParams<{ videoId: string }>();

  return (
    <div className="py-12">
      <h1 className="text-4xl font-bold mb-8">Generated Shorts</h1>
      <div className="grid md:grid-cols-2 gap-6">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="bg-gray-800 rounded-lg overflow-hidden border border-gray-700 hover:border-blue-500 transition">
            <div className="aspect-video bg-gray-900 flex items-center justify-center">
              <div className="text-center">
                <p className="text-gray-400">Short #{i}</p>
                <p className="text-sm text-gray-500 mt-2">00:30 - 00:45</p>
              </div>
            </div>
            <div className="p-4 space-y-3">
              <h3 className="font-semibold">Highlight {i}</h3>
              <div className="flex gap-2">
                <button className="flex-1 py-2 bg-blue-600 rounded hover:bg-blue-700 transition flex items-center justify-center gap-2">
                  <Download className="w-4 h-4" /> Download
                </button>
                <button className="flex-1 py-2 bg-purple-600 rounded hover:bg-purple-700 transition flex items-center justify-center gap-2">
                  <Share2 className="w-4 h-4" /> Share
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ShortsPage;
