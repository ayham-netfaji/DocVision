import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router';
import { ArrowLeft, Play, RefreshCw, FileImage, AlertCircle } from 'lucide-react';
import { scanDocumentImage } from '../services/api';
import { ProcessingStatus } from '../components/ProcessingStatus';
import type { ProcessingStep } from '../types/document';

const PIPELINE_STEPS: ProcessingStep[] = [
  { id: '1', label: '1. Image Upload & Validation', status: 'pending' },
  { id: '2', label: '2. Document Boundary Detection', status: 'pending' },
  { id: '3', label: '3. 4-Corner Homography Deskew', status: 'pending' },
  { id: '4', label: '4. Adaptive Pre-OCR Enhancement', status: 'pending' },
  { id: '5', label: '5. Text Extraction & Scoring', status: 'pending' },
];

export const Scanner: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const file = location.state?.file as File | undefined;
  const previewUrl = location.state?.previewUrl || sessionStorage.getItem('docvision_preview_url');
  const fileName = file?.name || sessionStorage.getItem('docvision_current_file_name') || 'Document';

  const [isScanning, setIsScanning] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const handleStartScan = async () => {
    if (!file && !previewUrl) return;
    setError(null);
    setIsScanning(true);
    setCurrentStep(0);

    try {
      // If we don't have file instance from navigation state (e.g. reload), fetch blob
      let uploadFile = file;
      if (!uploadFile && previewUrl) {
        const res = await fetch(previewUrl);
        const blob = await res.blob();
        uploadFile = new File([blob], fileName, { type: blob.type || 'image/jpeg' });
      }

      if (!uploadFile) {
        throw new Error('Document file is missing. Please re-upload.');
      }

      // Progress animation simulation across pipeline stages
      setCurrentStep(1);
      await new Promise((r) => setTimeout(r, 400));
      setCurrentStep(2);
      await new Promise((r) => setTimeout(r, 400));
      setCurrentStep(3);

      const result = await scanDocumentImage(uploadFile);

      setCurrentStep(4);
      await new Promise((r) => setTimeout(r, 300));

      navigate('/result', {
        state: {
          result,
          previewUrl,
          fileName,
        },
      });
    } catch (err: any) {
      console.error('Scan error:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to scan document.');
    } finally {
      setIsScanning(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <div className="flex items-center justify-between mb-8">
        <button
          onClick={() => navigate('/')}
          disabled={isScanning}
          className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors cursor-pointer disabled:opacity-50"
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

        {/* Scan Actions & Progress Pane */}
        <div className="flex flex-col gap-6">
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6">
            <h3 className="text-base font-semibold text-white mb-2">Execution Actions</h3>
            <p className="text-xs text-slate-400 mb-6 leading-relaxed">
              Triggers server-side multipart processing, boundary isolation, and character recognition.
            </p>

            <button
              disabled={!previewUrl || isScanning}
              onClick={handleStartScan}
              className="w-full flex items-center justify-center gap-2 px-5 py-3.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium rounded-xl transition shadow-lg shadow-blue-600/20 cursor-pointer"
            >
              <Play className="w-4 h-4 fill-white" />
              <span>{isScanning ? 'Processing Pipeline...' : 'Scan & Extract Text'}</span>
            </button>

            <button
              disabled={isScanning}
              onClick={() => navigate('/')}
              className="w-full mt-3 flex items-center justify-center gap-2 px-5 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium rounded-xl text-sm transition cursor-pointer disabled:opacity-50"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Change Image</span>
            </button>
          </div>

          {isScanning && (
            <ProcessingStatus steps={PIPELINE_STEPS} currentStepIndex={currentStep} />
          )}

          {error && (
            <div className="flex items-center gap-2 p-4 bg-red-950/40 border border-red-800/60 rounded-xl text-red-300 text-xs">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
