import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router';
import {
  ArrowLeft,
  Copy,
  Check,
  Download,
  CheckCircle2,
  Hash,
  Percent,
  Layers,
  FileText,
  Sparkles,
  AlignLeft,
  Tag,
  Loader2
} from 'lucide-react';
import type { ProcessedDocument } from '../types/document';

export const Result: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const previewUrl = location.state?.previewUrl || sessionStorage.getItem('docvision_preview_url');
  const result = location.state?.result as ProcessedDocument | undefined;

  const [activeTab, setActiveTab] = useState<'scan' | 'stages'>('scan');
  const [copied, setCopied] = useState(false);
  const [fontSize, setFontSize] = useState<'sm' | 'base' | 'lg'>('sm');

  const backendHost = import.meta.env.VITE_BACKEND_HOST || 'http://127.0.0.1:8000';

  const processedImageUrl = result?.processed_image_url
    ? `${backendHost}${result.processed_image_url}`
    : previewUrl;

  const originalImageUrl = result?.original_image_url
    ? `${backendHost}${result.original_image_url}`
    : previewUrl;

  const defaultText = result?.text || `[Default Preview]
Document scanner pipeline ready.
Scan your document from Workspace to see live OCR text extraction.`;

  const [currentText, setCurrentText] = useState(defaultText);
  const [classification, setClassification] = useState<string | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [isAiLoading, setIsAiLoading] = useState(false);

  const confidence = result?.confidence ?? 98.5;
  const docId = result?.document_id ?? 'preview-doc';
  const wordCount = result?.word_count ?? currentText.split(/\s+/).filter(Boolean).length;
  const charCount = result?.character_count ?? currentText.length;
  const stages = result?.stages || [];

  const handleAIAction = async (action: 'correct' | 'summarize' | 'classify') => {
    setIsAiLoading(true);
    try {
      const response = await fetch(`${backendHost}/api/v1/ai/${action}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: currentText }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'AI request failed. The model might be experiencing high demand (503).');
      
      if (action === 'correct') setCurrentText(data.result);
      if (action === 'summarize') setSummary(data.result);
      if (action === 'classify') setClassification(data.result);
    } catch (error: any) {
      console.error(error);
      alert(`AI Action Failed: ${error.message}`);
    } finally {
      setIsAiLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(currentText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([currentText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `docvision_${docId}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadPDF = () => {
    const pdfUrl = `${backendHost}/api/v1/export/${docId}/pdf?confidence=${confidence}&text=${encodeURIComponent(currentText)}`;
    const link = document.createElement('a');
    link.href = pdfUrl;
    link.download = `DocVision_${docId}.pdf`;
    link.target = '_blank';
    link.click();
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      {/* Top Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <button
          onClick={() => navigate('/scanner')}
          className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Workspace</span>
        </button>

        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-1.5 text-xs bg-slate-800 text-slate-300 border border-slate-700/80 px-3 py-1.5 rounded-full">
            <Hash className="w-3.5 h-3.5 text-blue-400" />
            <span>ID: {docId}</span>
          </div>

          <div className="flex items-center gap-1.5 text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-3 py-1.5 rounded-full">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Pipeline: Complete</span>
          </div>

          <div className="flex items-center gap-1 text-xs bg-blue-500/10 text-blue-400 border border-blue-500/20 px-3 py-1.5 rounded-full">
            <Percent className="w-3.5 h-3.5" />
            <span>Confidence: {confidence}%</span>
          </div>

          {classification && (
            <div className="flex items-center gap-1 text-xs bg-purple-500/10 text-purple-400 border border-purple-500/20 px-3 py-1.5 rounded-full">
              <Tag className="w-3.5 h-3.5" />
              <span>Type: {classification}</span>
            </div>
          )}
        </div>
      </div>

      {/* Mode Navigation Tabs */}
      <div className="flex items-center gap-2 mb-8 border-b border-slate-800 pb-3">
        <button
          onClick={() => setActiveTab('scan')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition cursor-pointer ${
            activeTab === 'scan'
              ? 'bg-blue-600 text-white shadow-md shadow-blue-600/20'
              : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Extracted Text & Document</span>
        </button>

        <button
          onClick={() => setActiveTab('stages')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition cursor-pointer ${
            activeTab === 'stages'
              ? 'bg-blue-600 text-white shadow-md shadow-blue-600/20'
              : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>Show Processing (Academic CV Demo)</span>
          {stages.length > 0 && (
            <span className="ml-1 text-xs px-2 py-0.5 rounded-full bg-slate-900 border border-slate-700 text-slate-300">
              {stages.length} Stages
            </span>
          )}
        </button>
      </div>

      {activeTab === 'scan' ? (
        /* Primary Split View: Document vs OCR Text */
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Enhanced Document Scan */}
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 flex flex-col">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-semibold text-white">Enhanced Document Scan</h3>
              <span className="text-xs text-slate-400">Deskewed & Binarized</span>
            </div>

            <div className="flex-1 min-h-[420px] bg-slate-950 border border-slate-800/80 rounded-xl flex items-center justify-center p-4 overflow-hidden relative group">
              {processedImageUrl ? (
                <img
                  src={processedImageUrl}
                  alt="Enhanced Document Scan"
                  className="max-h-[500px] w-auto object-contain rounded shadow-2xl"
                />
              ) : (
                <div className="text-sm text-slate-500">No document processed</div>
              )}
            </div>
          </div>

          {/* OCR Extracted Text Pane */}
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 flex flex-col">
            <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
              <div>
                <h3 className="text-base font-semibold text-white">Extracted Digital Text</h3>
                <div className="flex items-center gap-3 text-xs text-slate-400 mt-1">
                  <span>{wordCount} words</span>
                  <span>&bull;</span>
                  <span>{charCount} characters</span>
                </div>
              </div>

              <div className="flex items-center gap-2">
                {/* AI Actions */}
                <button
                  onClick={() => handleAIAction('summarize')}
                  disabled={isAiLoading}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-purple-600/20 hover:bg-purple-600/30 text-purple-400 border border-purple-500/30 rounded-lg transition disabled:opacity-50 cursor-pointer"
                  title="Generate a summary"
                >
                  {isAiLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <AlignLeft className="w-3.5 h-3.5" />}
                  <span className="hidden sm:inline">Summarize</span>
                </button>

                <div className="w-px h-6 bg-slate-700 mx-1"></div>
                {/* Font Size Selector */}
                <div className="flex items-center bg-slate-800/80 border border-slate-700 rounded-lg p-0.5 text-xs">
                  <button
                    onClick={() => setFontSize('sm')}
                    className={`px-2 py-1 rounded cursor-pointer ${fontSize === 'sm' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'}`}
                  >
                    S
                  </button>
                  <button
                    onClick={() => setFontSize('base')}
                    className={`px-2 py-1 rounded cursor-pointer ${fontSize === 'base' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'}`}
                  >
                    M
                  </button>
                  <button
                    onClick={() => setFontSize('lg')}
                    className={`px-2 py-1 rounded cursor-pointer ${fontSize === 'lg' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'}`}
                  >
                    L
                  </button>
                </div>

                <button
                  onClick={handleCopy}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg transition border border-slate-700 cursor-pointer"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? 'Copied' : 'Copy'}</span>
                </button>

                <button
                  onClick={handleDownload}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg transition border border-slate-700 cursor-pointer"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>TXT</span>
                </button>

                <button
                  onClick={handleDownloadPDF}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition shadow-md shadow-blue-600/20 cursor-pointer font-medium"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download PDF</span>
                </button>
              </div>
            </div>

            <div
              className={`flex-1 min-h-[420px] bg-slate-950/90 border border-slate-800 rounded-xl p-5 font-mono text-slate-200 overflow-auto whitespace-pre-wrap leading-relaxed shadow-inner ${
                fontSize === 'sm' ? 'text-xs' : fontSize === 'base' ? 'text-sm' : 'text-base'
              }`}
            >
              {currentText}
            </div>
          </div>

          {/* AI Summary Panel */}
          {summary && (
            <div className="col-span-1 lg:col-span-2 bg-gradient-to-r from-purple-900/20 to-slate-900/60 border border-purple-500/20 rounded-2xl p-6">
              <h3 className="text-base font-semibold text-purple-400 mb-3 flex items-center gap-2">
                <Sparkles className="w-4 h-4" /> AI Summary
              </h3>
              <div className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
                {summary}
              </div>
            </div>
          )}
        </div>
      ) : (
        /* Academic CV Showcase: All Computer Vision Stages */
        <div className="space-y-8">
          <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-6">
            <h3 className="text-lg font-bold text-white mb-1">Academic CV Pipeline Decomposition</h3>
            <p className="text-sm text-slate-400">
              Visualizes step-by-step mathematical transformations from camera input to clean binarized machine characters.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Raw Input Card */}
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 flex flex-col">
              <span className="text-xs font-semibold text-blue-400 mb-1">Step 0 &bull; Input</span>
              <h4 className="text-sm font-medium text-white mb-3">Original Capture</h4>
              <div className="flex-1 bg-slate-950 rounded-xl border border-slate-800/80 p-2 min-h-[220px] flex items-center justify-center overflow-hidden">
                {originalImageUrl ? (
                  <img src={originalImageUrl} alt="Original" className="max-h-[220px] w-auto object-contain rounded" />
                ) : (
                  <span className="text-xs text-slate-600">No original image</span>
                )}
              </div>
            </div>

            {/* Generated Intermediate Pipeline Stages */}
            {stages.map((stage, idx) => (
              <div key={stage.id} className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 flex flex-col">
                <span className="text-xs font-semibold text-indigo-400 mb-1">
                  Step {idx + 1} &bull; OpenCV
                </span>
                <h4 className="text-sm font-medium text-white mb-1">{stage.name}</h4>
                <p className="text-xs text-slate-400 mb-3">{stage.description}</p>
                <div className="flex-1 bg-slate-950 rounded-xl border border-slate-800/80 p-2 min-h-[220px] flex items-center justify-center overflow-hidden">
                  <img
                    src={`${backendHost}${stage.image_url}`}
                    alt={stage.name}
                    className="max-h-[220px] w-auto object-contain rounded"
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
