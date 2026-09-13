import React from 'react';
import { useParams } from 'react-router-dom';

const AnalysisPage: React.FC = () => {
  const { videoId } = useParams<{ videoId: string }>();

  return (
    <div className="py-12">
      <h1 className="text-4xl font-bold mb-8">Analyzing Video</h1>
      <div className="bg-gray-800 rounded-lg p-8 text-center">
        <div className="animate-pulse">
          <div className="w-12 h-12 bg-blue-500 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-400">AI is analyzing your video to find the best moments...</p>
          <p className="text-sm text-gray-500 mt-2">Video ID: {videoId}</p>
        </div>
      </div>
    </div>
  );
};

export default AnalysisPage;
