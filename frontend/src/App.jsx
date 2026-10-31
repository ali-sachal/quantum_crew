import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import FarmerUpload from './pages/FarmerUpload';
import StoreDashboard from './pages/StoreDashboard';
import MapView from './pages/MapView';
import NegotiationChat from './pages/NegotiationChat';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-surface text-stone-900 selection:bg-brand-500 selection:text-white">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<FarmerUpload />} />
            <Route path="/dashboard" element={<StoreDashboard />} />
            <Route path="/map" element={<MapView />} />
            <Route path="/negotiate/:dealId" element={<NegotiationChat />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <footer className="border-t border-stone-200/80 py-6 bg-white/50 text-center text-xs text-stone-500">
          <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
            <span>FoodMatch © 2025 • Urban Food Desert Supply Chain Matchmaker</span>
            <span className="font-mono text-[11px]">Powered by Google Gemma 4 • Snowflake CoCo • Solana Devnet</span>
          </div>
        </footer>
      </div>
    </BrowserRouter>
  );
}
