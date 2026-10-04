import React from 'react';
import { useLocation, useNavigate } from 'react-router';
import { ArrowLeft, Play, RefreshCw, FileImage } from 'lucide-react';

export const Scanner: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const previewUrl = location.state?.previewUrl || sessionStorage.getItem('docvision_preview_url');
  const fileName = location.state?.file?.name || sessionStorage.getItem('docvision_current_file_name') || 'Document';

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <div className="flex items-center justify-between mb-8">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Upload</span>
        </button>
        <span className="text-sm text-slate-500">Document Scanner Workspace</span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Document Preview Pane */}
        <div className="lg:col-span-2 bg-slate-900/60 border border-slate-800 rounded-2xl p-4 flex flex-col items-center justify-center min-h-[420px] overflow-hidden">
          {previewUrl ? (
            <div className="relative w-full h-full flex flex-col items-center justify-center">
              <img
                src={previewUrl}
                alt="Document preview"
                className="max-h-[500px] w-auto object-contain rounded-lg shadow-2xl border border-slate-700/50"
              />
              <div className="mt-4 flex items-center gap-2 text-xs text-slate-400">
                <FileImage className="w-3.5 h-3.5 text-blue-400" />
                <span>{fileName}</span>
              </div>
            </div>
          ) : (
            <div className="text-center p-8">
              <div className="w-12 h-12 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center mx-auto mb-3">
                <FileImage className="w-6 h-6" />
              </div>
              <p className="text-slate-300 font-medium">No document uploaded</p>
              <p className="text-xs text-slate-500 mt-1 mb-4">Please upload an image from the home page to begin scanning</p>
              <button
                onClick={() => navigate('/')}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-sm font-medium transition cursor-pointer"
              >
                Upload Now
              </button>
            </div>
          )}
        </div>

        {/* Scan Actions & Options */}
        <div className="flex flex-col gap-6">
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6">
            <h3 className="text-base font-semibold text-white mb-4">Pipeline Actions</h3>
            <p className="text-sm text-slate-400 mb-6">
              Run automated computer vision preprocessing, perspective rectification, and OCR text extraction.
            </p>

            <button
              disabled={!previewUrl}
              onClick={() => navigate('/result', { state: { previewUrl, fileName } })}
              className="w-full flex items-center justify-center gap-2 px-5 py-3.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium rounded-xl transition shadow-lg shadow-blue-600/20 cursor-pointer"
            >
              <Play className="w-4 h-4 fill-white" />
              <span>Scan & Extract Text</span>
            </button>

            <button
              onClick={() => navigate('/')}
              className="w-full mt-3 flex items-center justify-center gap-2 px-5 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium rounded-xl text-sm transition cursor-pointer"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Change Image</span>
            </button>
          </div>

          <div className="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6">
            <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Pipeline Stages</h4>
            <ul className="text-xs space-y-2.5 text-slate-400">
              <li className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-blue-400"></span>
                <span>1. Resolution & Grayscale Normalization</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-blue-400"></span>
                <span>2. Canny Edge & Contour Detection</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-blue-400"></span>
                <span>3. 4-Corner Perspective Warp</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-blue-400"></span>
                <span>4. Image Adaptive Enhancement</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-blue-400"></span>
                <span>5. Tesseract OCR Engine</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
