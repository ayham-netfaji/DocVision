import React, { useRef, useState } from 'react';
import { UploadCloud, FileImage, AlertCircle } from 'lucide-react';

interface UploadZoneProps {
  onFileSelect: (file: File) => void;
  isLoading?: boolean;
}

const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_SIZE = 10 * 1024 * 1024; // 10MB

export const UploadZone: React.FC<UploadZoneProps> = ({ onFileSelect, isLoading }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateAndHandle = (file: File) => {
    setError(null);
    if (!ALLOWED_TYPES.includes(file.type)) {
      setError('Invalid file type. Please upload a JPG, PNG, or WEBP image.');
      return;
    }
    if (file.size > MAX_SIZE) {
      setError('File is too large. Maximum size is 10MB.');
      return;
    }
    onFileSelect(file);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    if (isLoading) return;

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndHandle(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndHandle(e.target.files[0]);
    }
  };

  return (
    <div className="w-full">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragOver(true);
        }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
        onClick={() => !isLoading && fileInputRef.current?.click()}
        className={`relative flex flex-col items-center justify-center p-8 sm:p-12 border-2 border-dashed rounded-2xl cursor-pointer transition-all duration-200 group ${
          isDragOver
            ? 'border-blue-500 bg-blue-500/10 scale-[1.01]'
            : 'border-slate-800 bg-slate-900/40 hover:border-slate-700 hover:bg-slate-900/70'
        } ${isLoading ? 'opacity-50 cursor-not-allowed pointer-events-none' : ''}`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          className="hidden"
          onChange={handleChange}
        />

        <div className="p-4 rounded-2xl bg-blue-600/10 border border-blue-500/20 text-blue-400 mb-4 group-hover:scale-110 group-hover:bg-blue-600/20 transition-all duration-200 shadow-lg shadow-blue-500/5">
          <UploadCloud className="w-10 h-10" />
        </div>

        <h3 className="text-lg font-semibold text-slate-100 mb-1">
          Upload document image
        </h3>
        <p className="text-sm text-slate-400 mb-4 text-center max-w-sm">
          Drag & drop your document here, or click to browse files
        </p>

        <div className="flex items-center gap-2 text-xs text-slate-400 bg-slate-800/80 px-3 py-1.5 rounded-full border border-slate-700/60">
          <FileImage className="w-3.5 h-3.5 text-blue-400" />
          <span>Supports JPG, PNG, WEBP (Up to 10MB)</span>
        </div>
      </div>

      {error && (
        <div className="mt-3 flex items-center gap-2 p-3 bg-red-950/40 border border-red-800/60 rounded-xl text-red-300 text-sm">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};
