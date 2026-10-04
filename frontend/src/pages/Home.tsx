import React from 'react';
import { useNavigate } from 'react-router';
import { UploadZone } from '../components/UploadZone';
import { Sparkles, CheckCircle2, ShieldCheck, Zap } from 'lucide-react';

export const Home: React.FC = () => {
  const navigate = useNavigate();

  const handleFileSelect = (file: File) => {
    // Store in temporary object URL and state for Workspace
    const previewUrl = URL.createObjectURL(file);
    sessionStorage.setItem('docvision_current_file_name', file.name);
    sessionStorage.setItem('docvision_current_file_type', file.type);
    sessionStorage.setItem('docvision_preview_url', previewUrl);
    navigate('/scanner', { state: { file, previewUrl } });
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
      {/* Hero Header */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold uppercase tracking-wider mb-6">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Next-Gen Computer Vision OCR</span>
        </div>
        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white mb-6">
          Scan. Extract.{' '}
          <span className="bg-gradient-to-r from-blue-400 via-sky-300 to-indigo-400 bg-clip-text text-transparent">
            Understand.
          </span>
        </h1>
        <p className="text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto">
          Convert camera photos and mobile scans into pristine, high-accuracy editable digital text using computer vision preprocessing.
        </p>
      </div>

      {/* Upload Zone Card */}
      <div className="max-w-2xl mx-auto mb-16">
        <UploadZone onFileSelect={handleFileSelect} />
      </div>

      {/* Feature Badges / Highlights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800/80">
          <div className="w-10 h-10 rounded-xl bg-blue-600/10 border border-blue-500/20 flex items-center justify-center text-blue-400 mb-4">
            <Zap className="w-5 h-5" />
          </div>
          <h3 className="text-base font-semibold text-white mb-2">Automated Boundary Detection</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            OpenCV edge and contour analysis locates the paper coordinates automatically and crops background clutter.
          </p>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800/80">
          <div className="w-10 h-10 rounded-xl bg-indigo-600/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-4">
            <CheckCircle2 className="w-5 h-5" />
          </div>
          <h3 className="text-base font-semibold text-white mb-2">Perspective Deskewing</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Applies 4-point homography transform to flatten angled shots directly into a straight, scan-quality document.
          </p>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800/80">
          <div className="w-10 h-10 rounded-xl bg-emerald-600/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-4">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <h3 className="text-base font-semibold text-white mb-2">OCR Enhancement</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Adaptive thresholding and noise filtering ensures Tesseract delivers high confidence text recognition.
          </p>
        </div>
      </div>
    </div>
  );
};
