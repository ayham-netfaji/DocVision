import { useNavigate } from 'react-router';
import { History as HistoryIcon, ArrowRight } from 'lucide-react';

export const HistoryPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Scan History</h2>
          <p className="text-sm text-slate-400 mt-1">Review previously scanned and extracted documents.</p>
        </div>
      </div>

      <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-12 text-center">
        <div className="w-14 h-14 rounded-2xl bg-blue-600/10 border border-blue-500/20 text-blue-400 flex items-center justify-center mx-auto mb-4">
          <HistoryIcon className="w-7 h-7" />
        </div>
        <h3 className="text-lg font-semibold text-white mb-1">Persistent Storage (Phase 12)</h3>
        <p className="text-sm text-slate-400 max-w-md mx-auto mb-6">
          PostgreSQL persistence will store your scanned files, OCR logs, and extracted text records once core processing is stabilized.
        </p>
        <button
          onClick={() => navigate('/')}
          className="inline-flex items-center gap-2 px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-sm font-medium transition cursor-pointer"
        >
          <span>Scan a Document</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
