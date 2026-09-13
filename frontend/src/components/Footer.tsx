import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 border-t border-gray-800 mt-16">
      <div className="container mx-auto px-4 py-8 text-center text-gray-400">
        <p>&copy; 2024 Video Shorts Generator. All rights reserved.</p>
        <p className="mt-2 text-sm">Powered by AI • Built with React, Node.js, and Python</p>
      </div>
    </footer>
  );
};

export default Footer;
