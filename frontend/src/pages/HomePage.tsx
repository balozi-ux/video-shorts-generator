import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Zap, Clock, Download } from 'lucide-react';

const HomePage: React.FC = () => {
  const features = [
    {
      icon: Sparkles,
      title: 'AI-Powered Analysis',
      description: 'Advanced AI detects and extracts the most engaging moments from your videos'
    },
    {
      icon: Zap,
      title: 'One-Click Processing',
      description: 'Upload your video and get shorts in minutes, not hours'
    },
    {
      icon: Clock,
      title: 'Customizable Duration',
      description: 'Create shorts of any length - perfect for YouTube Shorts, TikTok, and Reels'
    },
    {
      icon: Download,
      title: 'Multiple Formats',
      description: 'Download in MP4, WebM, and more. Ready to post on any platform'
    }
  ];

  return (
    <div className="space-y-16 py-12">
      {/* Hero Section */}
      <section className="text-center space-y-6">
        <h1 className="text-5xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600">
          Create Video Shorts Instantly
        </h1>
        <p className="text-xl text-gray-300 max-w-3xl mx-auto">
          Transform long-form content into engaging short clips. Our AI automatically detects key moments and creates perfectly-timed shorts for social media.
        </p>
        <div className="flex gap-4 justify-center flex-wrap">
          <Link
            to="/upload"
            className="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg font-semibold hover:shadow-lg transition"
          >
            Get Started →
          </Link>
          <Link
            to="/dashboard"
            className="px-8 py-3 border-2 border-gray-400 rounded-lg font-semibold hover:bg-gray-700 transition"
          >
            View Examples
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section>
        <h2 className="text-4xl font-bold text-center mb-12">Why Choose Us?</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <div key={idx} className="bg-gray-800 bg-opacity-50 backdrop-blur rounded-lg p-6 border border-gray-700 hover:border-blue-500 transition">
                <Icon className="w-12 h-12 text-blue-400 mb-4" />
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* How It Works */}
      <section>
        <h2 className="text-4xl font-bold text-center mb-12">How It Works</h2>
        <div className="max-w-4xl mx-auto space-y-8">
          {[
            { step: 1, title: 'Upload Video', desc: 'Select your long-form video (MP4, MOV, WebM)' },
            { step: 2, title: 'AI Analysis', desc: 'Our AI analyzes scenes, detects highlights, and extracts key moments' },
            { step: 3, title: 'Review & Customize', desc: 'Preview detected shorts and customize settings' },
            { step: 4, title: 'Download & Share', desc: 'Download your shorts and share instantly on social media' }
          ].map((item) => (
            <div key={item.step} className="flex items-start gap-6">
              <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center text-xl font-bold">
                {item.step}
              </div>
              <div>
                <h3 className="text-2xl font-semibold mb-2">{item.title}</h3>
                <p className="text-gray-400 text-lg">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default HomePage;
