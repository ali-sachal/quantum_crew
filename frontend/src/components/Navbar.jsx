import React from 'react';
import { NavLink } from 'react-router-dom';

export default function Navbar() {
  const linkClass = ({ isActive }) =>
    `px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-150 ${
      isActive
        ? 'bg-brand-600 text-white shadow-sm shadow-brand-600/30'
        : 'text-stone-600 hover:text-stone-900 hover:bg-stone-100'
    }`;

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-stone-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <NavLink to="/" className="flex items-center gap-2.5 group">
          <span className="w-10 h-10 rounded-2xl bg-brand-50 border border-brand-200 flex items-center justify-center text-xl shadow-inner group-hover:scale-105 transition-transform">
            🍅
          </span>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="text-lg font-black tracking-tight text-stone-900">FoodMatch</span>
              <span className="text-[10px] uppercase font-black tracking-widest px-1.5 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-200">
                AI + Solana
              </span>
            </div>
            <p className="text-[11px] font-medium text-stone-500 hidden sm:block">Urban Food Desert Matchmaker</p>
          </div>
        </NavLink>

        {/* Navigation Links */}
        <nav className="flex items-center gap-1.5 sm:gap-2">
          <NavLink to="/" className={linkClass}>
            🌱 Farmer Upload
          </NavLink>
          <NavLink to="/dashboard" className={linkClass}>
            🏪 Store Dashboard
          </NavLink>
          <NavLink to="/map" className={linkClass}>
            🗺️ Map View
          </NavLink>
          <NavLink to="/negotiate/1" className={linkClass}>
            💬 Negotiation Chat
          </NavLink>
        </nav>
      </div>
    </header>
  );
}

