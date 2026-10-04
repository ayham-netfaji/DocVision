import { BrowserRouter, Routes, Route, Navigate } from 'react-router';
import { Navbar } from './components/Navbar';
import { Home } from './pages/Home';
import { Scanner } from './pages/Scanner';
import { Result } from './pages/Result';
import { HistoryPage } from './pages/History';

export function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/scanner" element={<Scanner />} />
            <Route path="/result" element={<Result />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <footer className="border-t border-slate-900 py-6 text-center text-xs text-slate-500">
          DocVision &bull; Computer Vision &amp; OCR Document Intelligence
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;
