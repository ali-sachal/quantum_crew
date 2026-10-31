import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import TrustBadge from '../components/TrustBadge';

export default function FarmerUpload() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [quantity, setQuantity] = useState(40);
  const [floorPrice, setFloorPrice] = useState(2.10);
  const [sellerId, setSellerId] = useState(1);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileDrop = (e) => {
    e.preventDefault();
    const dropped = e.dataTransfer.files[0];
    if (dropped && dropped.type.startsWith('image/')) {
      setFile(dropped);
      setPreview(URL.createObjectURL(dropped));
    }
  };

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      setPreview(URL.createObjectURL(selected));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', file);
    formData.append('seller_id', sellerId);
    formData.append('quantity_kg', quantity);
    formData.append('floor_price', floorPrice);

    try {
      const data = await api.createListing(formData);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to analyze produce image with Gemma 4.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-3xl border border-stone-200/90 shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-stone-900 tracking-tight">Farmer Produce Upload</h1>
            <span className="text-xs uppercase font-mono px-2 py-0.5 rounded-full bg-brand-100 text-brand-800 font-bold">
              Google Gemma 4
            </span>
          </div>
          <p className="text-xs text-stone-500 mt-1">
            Upload your surplus produce photo. Gemma 4 will inspect quality, grade it, and recommend equitable market pricing.
          </p>
        </div>

        <TrustBadge
          solanaAddress="SolanaFarmBx1111111111111111111111111111111"
          txSignature="5xSeedRegBxFarm9876543210devnetExplorerTxHash1"
          reputation={4.9}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Upload Form */}
        <div className="lg:col-span-6 bg-white p-6 rounded-3xl border border-stone-200/90 shadow-sm space-y-6">
          <h2 className="text-base font-bold text-stone-900">1. Produce Details & Photo</h2>

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Drag & Drop Area */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-stone-600 mb-2">
                Produce Photo (Required)
              </label>
              <div
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleFileDrop}
                className="border-2 border-dashed border-stone-300 hover:border-brand-500 rounded-2xl p-6 text-center cursor-pointer transition-colors bg-stone-50/50 relative overflow-hidden group"
              >
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  className="absolute inset-0 opacity-0 cursor-pointer w-full h-full z-10"
                />

                {preview ? (
                  <div className="relative h-56 w-full rounded-xl overflow-hidden">
                    <img src={preview} alt="Upload Preview" className="w-full h-full object-cover" />
                    <div className="absolute inset-0 bg-black/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                      <span className="bg-white/90 text-stone-800 text-xs font-bold px-3 py-1.5 rounded-xl shadow">
                        Click to change photo
                      </span>
                    </div>
                  </div>
                ) : (
                  <div className="py-8 space-y-2">
                    <div className="text-4xl">📸</div>
                    <p className="text-sm font-bold text-stone-700">Drag & drop your produce photo here</p>
                    <p className="text-xs text-stone-400">or click to browse from device (JPG, PNG)</p>
                  </div>
                )}
              </div>
            </div>

            {/* Farm Profile Selection */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-stone-600 mb-1.5">
                Selling Garden / Farm Co-op
              </label>
              <select
                value={sellerId}
                onChange={(e) => setSellerId(Number(e.target.value))}
                className="w-full px-4 py-2.5 bg-stone-50 border border-stone-200 rounded-xl text-xs font-semibold text-stone-800 focus:ring-2 focus:ring-brand-500 outline-none"
              >
                <option value={1}>South Bronx Green Workers Co-op (Mott Haven)</option>
                <option value={2}>Harlem Roots Rooftop Farm (Central Harlem)</option>
                <option value={3}>East New York Farms! Collective (Brownsville)</option>
              </select>
            </div>

            {/* Quantity and Floor Price */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-stone-600 mb-1.5">
                  Surplus Quantity (kg)
                </label>
                <input
                  type="number"
                  min="1"
                  step="0.5"
                  value={quantity}
                  onChange={(e) => setQuantity(Number(e.target.value))}
                  className="w-full px-4 py-2.5 bg-stone-50 border border-stone-200 rounded-xl text-sm font-bold text-stone-800 focus:ring-2 focus:ring-brand-500 outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-stone-600 mb-1.5">
                  Seller Floor Price ($/kg)
                </label>
                <input
                  type="number"
                  min="0.5"
                  step="0.10"
                  value={floorPrice}
                  onChange={(e) => setFloorPrice(Number(e.target.value))}
                  className="w-full px-4 py-2.5 bg-stone-50 border border-stone-200 rounded-xl text-sm font-bold text-stone-800 focus:ring-2 focus:ring-brand-500 outline-none"
                  required
                />
                <span className="text-[10px] text-stone-400 block mt-1">Guardrail: AI agent will never sell below this</span>
              </div>
            </div>

            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-700 font-medium">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !file}
              className="w-full py-3.5 px-6 bg-brand-600 hover:bg-brand-700 active:scale-[0.99] text-white font-bold text-sm rounded-2xl shadow-sm shadow-brand-600/30 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  <span>Gemma 4 Inspecting Produce...</span>
                </>
              ) : (
                <>
                  <span>✨ Inspect with Gemma 4 & Publish Listing</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* AI Inspection Result Panel */}
        <div className="lg:col-span-6 space-y-6">
          <div className="bg-white p-6 rounded-3xl border border-stone-200/90 shadow-sm min-h-[460px] flex flex-col justify-center">
            <h2 className="text-base font-bold text-stone-900 mb-4">2. Gemma 4 AI Inspection Result</h2>

            {loading && (
              <div className="text-center py-16 space-y-4">
                <div className="w-12 h-12 border-4 border-brand-200 border-t-brand-600 rounded-full animate-spin mx-auto"></div>
                <div className="space-y-1">
                  <p className="text-sm font-black text-stone-800">Analyzing Produce via Gemini API</p>
                  <p className="text-xs text-stone-500 max-w-sm mx-auto">
                    Google Gemma 4 is scanning color tautness, ripeness defects, grade category, and urban price parity...
                  </p>
                </div>
              </div>
            )}

            {!loading && result && (
              <div className="space-y-5 animate-fadeIn">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <span className="text-[10px] uppercase font-mono font-bold tracking-widest text-brand-700 bg-brand-50 px-2 py-0.5 rounded-full border border-brand-200">
                      AI Verified Listing #{result.id}
                    </span>
                    <h3 className="text-xl font-black text-stone-900 mt-1">{result.item_name}</h3>
                  </div>

                  <span className={`text-sm font-black px-3.5 py-1.5 rounded-2xl shadow-sm text-white ${
                    result.grade === 'A' ? 'bg-brand-600' : (result.grade === 'B' ? 'bg-amber-500' : 'bg-orange-500')
                  }`}>
                    Grade {result.grade}
                  </span>
                </div>

                <p className="text-xs text-stone-600 leading-relaxed bg-stone-50 p-3 rounded-2xl border border-stone-200">
                  {result.description}
                </p>

                <div className="bg-brand-50/70 border border-brand-200 rounded-2xl p-4 space-y-1.5">
                  <span className="text-xs font-bold text-brand-900 block">🌱 AI Freshness Observations:</span>
                  <p className="text-xs text-brand-800 leading-relaxed font-medium">{result.freshness_notes}</p>
                </div>

                <div className="grid grid-cols-2 gap-4 pt-2">
                  <div className="bg-stone-50 p-3.5 rounded-2xl border border-stone-200">
                    <span className="text-[10px] uppercase font-bold text-stone-400 block tracking-wider">Suggested Price</span>
                    <span className="text-xl font-black text-brand-800">${result.suggested_price.toFixed(2)}</span>
                    <span className="text-xs text-stone-500"> / kg</span>
                  </div>

                  <div className="bg-stone-50 p-3.5 rounded-2xl border border-stone-200">
                    <span className="text-[10px] uppercase font-bold text-stone-400 block tracking-wider">Verified Identity</span>
                    <span className="text-xs font-bold text-stone-800 block truncate">
                      {result.seller?.name}
                    </span>
                    <span className="text-[10px] font-mono text-stone-400">Solana Devnet Active</span>
                  </div>
                </div>

                <div className="pt-3 border-t border-stone-100 flex gap-3">
                  <button
                    onClick={() => navigate('/dashboard')}
                    className="flex-1 py-3 bg-brand-600 hover:bg-brand-700 text-white text-xs font-black rounded-xl shadow-sm transition"
                  >
                    View in Store Dashboard ↗
                  </button>
                  <button
                    onClick={() => { setResult(null); setFile(null); setPreview(null); }}
                    className="px-4 py-3 bg-stone-100 hover:bg-stone-200 text-stone-700 text-xs font-bold rounded-xl transition"
                  >
                    Upload Another
                  </button>
                </div>
              </div>
            )}

            {!loading && !result && (
              <div className="text-center py-20 text-stone-400 space-y-3">
                <span className="text-5xl block">🥗</span>
                <p className="text-sm font-semibold text-stone-600">No produce analyzed yet</p>
                <p className="text-xs max-w-xs mx-auto">
                  Drag and drop a photo on the left to see Gemma 4 produce grade, pricing, and description.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
