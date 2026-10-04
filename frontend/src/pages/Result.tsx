import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router';
import { ArrowLeft, Copy, Check, Download, CheckCircle2, Hash, Percent } from 'lucide-react';
import type { ProcessedDocument } from '../types/document';

export const Result: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const previewUrl = location.state?.previewUrl || sessionStorage.getItem('docvision_preview_url');
  const result = location.state?.result as ProcessedDocument | undefined;
  
  const extractedText = result?.text || `[Default Preview]
Document scanner pipeline ready.
Scan your document from the Workspace to see live OCR text extraction.`;

  const confidence = result?.confidence ?? 98.5;
  const docId = result?.document_id ?? 'preview-doc';

  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(extractedText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([extractedText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `docvision_${docId}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
        <button
          onClick={() => navigate('/scanner')}
          className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Workspace</span>
        </button>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 text-xs bg-slate-800 text-slate-300 border border-slate-700/80 px-3 py-1.5 rounded-full">
            <Hash className="w-3.5 h-3.5 text-blue-400" />
            <span>ID: {docId}</span>
          </div>

          <div className="flex items-center gap-1.5 text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-3 py-1.5 rounded-full">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Status: {result?.status || 'Active'}</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Scanned/Enhanced Document View */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 flex flex-col">
          <h3 className="text-base font-semibold text-white mb-4">Input Document Image</h3>
          <div className="flex-1 min-h-[360px] bg-slate-950/60 border border-slate-800/80 rounded-xl flex items-center justify-center p-4 overflow-hidden">
            {previewUrl ? (
              <img
                src={previewUrl}
                alt="Scanned Preview"
                className="max-h-[460px] w-auto object-contain rounded shadow-lg"
              />
            ) : (
              <div className="text-sm text-slate-500">No document processed</div>
            )}
          </div>
        </div>

        {/* OCR Result View */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-semibold text-white">Extracted Text</h3>
              <div className="flex items-center gap-1 text-xs text-blue-400 mt-1">
                <Percent className="w-3 h-3" />
                <span>Confidence: {confidence}%</span>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={handleCopy}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg transition border border-slate-700 cursor-pointer"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>

              <button
                onClick={handleDownload}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition shadow cursor-pointer"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download TXT</span>
              </button>
            </div>
          </div>

          <div className="flex-1 min-h-[360px] bg-slate-950/80 border border-slate-800 rounded-xl p-4 font-mono text-xs text-slate-200 overflow-auto whitespace-pre-wrap leading-relaxed shadow-inner">
            {extractedText}
          </div>
        </div>
      </div>
    </div>
  );
};
