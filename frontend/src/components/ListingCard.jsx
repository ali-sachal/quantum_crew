import React from 'react';
import { useNavigate } from 'react-router-dom';
import TrustBadge from './TrustBadge';

export default function ListingCard({ listing, onBargain }) {
  const navigate = useNavigate();

  const handleBargainClick = () => {
    if (onBargain) {
      onBargain(listing);
    } else {
      navigate(`/negotiate/${listing.id}`);
    }
  };

  const gradeColor = {
    A: 'bg-brand-600 text-white border-brand-700',
    B: 'bg-amber-500 text-white border-amber-600',
    C: 'bg-orange-500 text-white border-orange-600',
  }[listing.grade] || 'bg-brand-600 text-white';

  return (
    <div className="bg-white rounded-3xl border border-stone-200/90 shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden flex flex-col group">
      {/* Produce Image & Badges */}
      <div className="relative h-48 w-full bg-stone-100 overflow-hidden">
        <img
          src={listing.image_url}
          alt={listing.item_name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          onError={(e) => {
            e.target.src = 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600&auto=format&fit=crop';
          }}
        />

        {/* Grade Badge */}
        <div className="absolute top-3 left-3 flex items-center gap-2">
          <span className={`px-2.5 py-1 rounded-xl text-xs font-black shadow-md border ${gradeColor}`}>
            Grade {listing.grade}
          </span>
          <span className="bg-black/60 backdrop-blur-md text-white text-[11px] font-bold px-2 py-1 rounded-xl">
            {listing.quantity_kg} kg left
          </span>
        </div>

        {/* Status */}
        <div className="absolute top-3 right-3">
          <span className="bg-white/90 backdrop-blur-md text-stone-800 text-[11px] font-bold px-2.5 py-1 rounded-xl border border-stone-200 shadow-sm">
            Fresh Surplus
          </span>
        </div>
      </div>

      {/* Card Content */}
      <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
        <div>
          {/* Seller Trust Badge */}
          <div className="mb-2">
            <TrustBadge
              solanaAddress={listing.seller?.solana_address}
              txSignature={listing.seller?.registry_tx}
              reputation={listing.seller?.reputation_score || 4.8}
              compact
            />
          </div>

          <h4 className="text-base font-black text-stone-900 group-hover:text-brand-700 transition-colors">
            {listing.item_name}
          </h4>

          <p className="text-xs text-stone-500 font-medium mt-0.5 line-clamp-1">
            By {listing.seller?.name || 'Local Community Farm'}
          </p>

          <p className="text-xs text-stone-600 mt-2 line-clamp-2 leading-relaxed">
            {listing.description}
          </p>
        </div>

        {/* Freshness Note */}
        {listing.freshness_notes && (
          <div className="bg-brand-50/60 border border-brand-100 rounded-xl p-2.5 text-[11px] text-brand-900">
            <span className="font-bold block mb-0.5">🌱 AI Inspection:</span>
            <span className="line-clamp-2">{listing.freshness_notes}</span>
          </div>
        )}

        {/* Price & Action Button */}
        <div className="pt-3 border-t border-stone-100 flex items-center justify-between gap-3">
          <div>
            <span className="text-[10px] uppercase font-bold text-stone-400 block tracking-wider">Suggested</span>
            <div className="text-xl font-black text-stone-900">
              ${listing.suggested_price.toFixed(2)}
              <span className="text-xs font-normal text-stone-500"> / kg</span>
            </div>
          </div>

          <button
            onClick={handleBargainClick}
            className="px-4 py-2.5 bg-brand-600 hover:bg-brand-700 active:scale-95 text-white text-xs font-black rounded-xl shadow-sm shadow-brand-600/30 transition-all flex items-center gap-1.5"
          >
            <span>💬 Bargain</span>
          </button>
        </div>
      </div>
    </div>
  );
}
