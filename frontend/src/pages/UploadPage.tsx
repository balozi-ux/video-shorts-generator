import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import { Upload, FileVideo } from 'lucide-react';
import { toast } from 'react-toastify';
import axios from 'axios';

const UploadPage: React.FC = () => {
  const [uploading, setUploading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const navigate = useNavigate();

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (files) => {
      if (files.length > 0) {
        setFile(files[0]);
      }
    },
    accept: {
      'video/*': ['.mp4', '.mov', '.webm', '.avi']
    },
    maxFiles: 1
  });

  const handleUpload = async () => {
    if (!file) {
      toast.error('Please select a video file');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('video', file);
    formData.append('title', file.name.replace(/\.[^/.]+$/, ''));

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const percent = Math.round((progressEvent.loaded / (progressEvent.total || 1)) * 100);
          console.log(`Upload progress: ${percent}%`);
        }
      });

      toast.success('Video uploaded successfully!');
      navigate(`/analysis/${response.data.videoId}`);
    } catch (error) {
      toast.error('Failed to upload video');
      console.error(error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-12">
      <h1 className="text-4xl font-bold text-center mb-8">Upload Your Video</h1>
      
      <div
        {...getRootProps()}
        className={`border-4 border-dashed rounded-lg p-12 text-center cursor-pointer transition ${
          isDragActive
            ? 'border-blue-500 bg-blue-500 bg-opacity-10'
            : 'border-gray-600 hover:border-gray-500'
        }`}
      >
        <input {...getInputProps()} />
        <Upload className="w-16 h-16 mx-auto mb-4 text-blue-400" />
        <h2 className="text-2xl font-semibold mb-2">
          {isDragActive ? 'Drop your video here' : 'Drag and drop your video'}
        </h2>
        <p className="text-gray-400 mb-4">or click to select from your computer</p>
        <p className="text-sm text-gray-500">Supported: MP4, MOV, WebM, AVI (Max 2GB)</p>
      </div>

      {file && (
        <div className="mt-8 bg-gray-800 rounded-lg p-6 border border-gray-700">
          <div className="flex items-center gap-4 mb-4">
            <FileVideo className="w-8 h-8 text-blue-400" />
            <div className="flex-grow">
              <p className="font-semibold">{file.name}</p>
              <p className="text-sm text-gray-400">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          </div>
          <button
            onClick={handleUpload}
            disabled={uploading}
            className="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg font-semibold hover:shadow-lg transition disabled:opacity-50"
          >
            {uploading ? 'Uploading...' : 'Upload & Analyze'}
          </button>
        </div>
      )}
    </div>
  );
};

export default UploadPage;
