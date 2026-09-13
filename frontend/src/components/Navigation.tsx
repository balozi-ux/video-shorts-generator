import React from 'react';
import { Link } from 'react-router-dom';
import { Film } from 'lucide-react';

const Navigation: React.FC = () => {
  return (
    <nav className="bg-gray-900 bg-opacity-80 backdrop-blur border-b border-gray-800 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="flex items-center gap-2 text-2xl font-bold">
          <Film className="w-8 h-8 text-blue-400" />
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600">
            Shorts AI
          </span>
        </Link>
        <div className="flex gap-6">
          <Link to="/" className="hover:text-blue-400 transition">Home</Link>
          <Link to="/upload" className="hover:text-blue-400 transition">Upload</Link>
          <Link to="/dashboard" className="hover:text-blue-400 transition">Dashboard</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
