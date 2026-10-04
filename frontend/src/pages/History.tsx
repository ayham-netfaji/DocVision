import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import {
  History as HistoryIcon,
  Trash2,
  ExternalLink,
  FileText,
  Calendar,
  Percent,
  Search,
  ArrowRight,
  Loader2,
  AlertCircle
} from 'lucide-react';
import { listDocuments, deleteDocumentById } from '../services/api';
import type { ProcessedDocument } from '../types/document';

export const HistoryPage: React.FC = () => {
  const navigate = useNavigate();
  const [documents, setDocuments] = useState<ProcessedDocument[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const backendHost = import.meta.env.VITE_BACKEND_HOST || 'http://127.0.0.1:8000';

  const fetchDocs = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await listDocuments();
      setDocuments(data);
    } catch (err: any) {
      console.error('Failed to load history:', err);
      setError('Could not connect to database history. Verify backend server is running.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this scanned document record?')) return;

    try {
      await deleteDocumentById(id);
      setDocuments((prev) => prev.filter((d) => d.document_id !== id));
    } catch (err) {
      alert('Failed to delete document.');
    }
  };

  const handleOpenDoc = (doc: ProcessedDocument) => {
    navigate('/result', {
      state: {
        result: doc,
        previewUrl: doc.original_image_url ? `${backendHost}${doc.original_image_url}` : null,
        fileName: (doc as any).filename || `Doc_${doc.document_id}`,
      },
    });
  };

  const filteredDocs = documents.filter((d) => {
    const q = searchQuery.toLowerCase();
    const name = ((d as any).filename || '').toLowerCase();
    const text = (d.text || '').toLowerCase();
    return name.includes(q) || text.includes(q) || d.document_id.toLowerCase().includes(q);
  });

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Scan History</h2>
          <p className="text-sm text-slate-400 mt-1">
            Persistent records of your processed documents and OCR extractions.
          </p>
        </div>

        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-sm font-medium transition cursor-pointer shadow-md shadow-blue-600/20"
        >
          <span>Scan New</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      {/* Search Bar */}
      <div className="relative mb-6">
        <Search className="w-4 h-4 text-slate-500 absolute left-4 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          placeholder="Search by filename, document ID, or extracted keywords..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full pl-11 pr-4 py-3 bg-slate-900/60 border border-slate-800 rounded-xl text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition"
        />
      </div>

      {isLoading ? (
        <div className="flex flex-col items-center justify-center py-20 text-slate-500">
          <Loader2 className="w-8 h-8 animate-spin text-blue-500 mb-3" />
          <span className="text-sm">Loading document history...</span>
        </div>
      ) : error ? (
        <div className="flex items-center gap-3 p-4 bg-red-950/40 border border-red-800/60 rounded-2xl text-red-300 text-sm">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      ) : filteredDocs.length === 0 ? (
        <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-16 text-center">
          <div className="w-14 h-14 rounded-2xl bg-blue-600/10 border border-blue-500/20 text-blue-400 flex items-center justify-center mx-auto mb-4">
            <HistoryIcon className="w-7 h-7" />
          </div>
          <h3 className="text-base font-semibold text-white mb-1">
            {searchQuery ? 'No matching documents found' : 'No documents in history'}
          </h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto mb-6">
            {searchQuery
              ? 'Try modifying your search keywords'
              : 'Scan your first document to see persistent history records here.'}
          </p>
          {!searchQuery && (
            <button
              onClick={() => navigate('/')}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-sm font-medium transition cursor-pointer"
            >
              Start Scanning
            </button>
          )}
        </div>
      ) : (
        /* History Grid */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDocs.map((doc) => {
            const previewSrc = doc.processed_image_url
              ? `${backendHost}${doc.processed_image_url}`
              : doc.original_image_url
              ? `${backendHost}${doc.original_image_url}`
              : null;

            return (
              <div
                key={doc.document_id}
                onClick={() => handleOpenDoc(doc)}
                className="group bg-slate-900/60 border border-slate-800 hover:border-slate-700/80 rounded-2xl p-4 flex flex-col transition cursor-pointer shadow-lg hover:shadow-xl"
              >
                {/* Thumbnail Preview */}
                <div className="w-full h-44 bg-slate-950 rounded-xl border border-slate-800/80 mb-3 overflow-hidden flex items-center justify-center relative">
                  {previewSrc ? (
                    <img
                      src={previewSrc}
                      alt="Thumbnail"
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  ) : (
                    <FileText className="w-8 h-8 text-slate-700" />
                  )}

                  <div className="absolute top-2 right-2 flex items-center gap-1 bg-slate-900/80 backdrop-blur-sm border border-slate-700/60 px-2 py-0.5 rounded-full text-[10px] text-blue-400 font-medium">
                    <Percent className="w-2.5 h-2.5" />
                    <span>{doc.confidence}%</span>
                  </div>
                </div>

                {/* Info Block */}
                <div className="flex-1 flex flex-col justify-between">
                  <div>
                    <h4 className="text-sm font-semibold text-white group-hover:text-blue-400 transition-colors line-clamp-1 mb-1">
                      {(doc as any).filename || `Doc ${doc.document_id}`}
                    </h4>
                    <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-3">
                      {doc.text || 'No text extracted'}
                    </p>
                  </div>

                  <div className="flex items-center justify-between pt-3 border-t border-slate-800/80 text-[11px] text-slate-500">
                    <div className="flex items-center gap-1.5">
                      <Calendar className="w-3 h-3 text-slate-600" />
                      <span>{doc.created_at ? new Date(doc.created_at).toLocaleDateString() : 'Recent'}</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={(e) => handleDelete(e, doc.document_id)}
                        title="Delete Document"
                        className="p-1 text-slate-500 hover:text-red-400 transition-colors"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                      <span className="text-blue-400 group-hover:translate-x-0.5 transition-transform">
                        <ExternalLink className="w-3.5 h-3.5" />
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
