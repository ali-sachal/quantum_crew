import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import DeficitChart from '../components/DeficitChart';
import ListingCard from '../components/ListingCard';
import TrustBadge from '../components/TrustBadge';
import LoadingSpinner from '../components/LoadingSpinner';
import EmptyState from '../components/EmptyState';
import ErrorState from '../components/ErrorState';

export default function StoreDashboard() {
  const navigate = useNavigate();
  const [zip, setZip] = useState('10451');
  const [inputZip, setInputZip] = useState('10451');
  const [demandData, setDemandData] = useState([]);
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async (targetZip) => {
    setLoading(true);
    setError(null);
    try {
      const [demandRes, listingsRes] = await Promise.all([
        api.getDemand(targetZip),
        api.getListings()
      ]);
      setDemandData(demandRes);
      setListings(listingsRes);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to load store dashboard data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(zip);
  }, [zip]);

  const handleZipSubmit = (e) => {
    e.preventDefault();
    if (inputZip.trim()) {
      setZip(inputZip.trim());
    }
  };

  const handleBargain = (listing) => {
    navigate(`/negotiate/${listing.id}`);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-3xl border border-stone-200/90 shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-stone-900 tracking-tight">Corner Store Produce Portal</h1>
            <span className="text-[10px] font-mono font-bold uppercase px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
              Devnet Buyer Agent
            </span>
          </div>
          <p className="text-xs text-stone-500 mt-1">
            Access hyper-local community farm surplus and predict neighborhood demand deficit before the weekend.
          </p>
        </div>

        {/* ZIP Code Search Control */}
        <form onSubmit={handleZipSubmit} className="flex items-center gap-2 w-full md:w-auto">
          <div className="relative flex-1 md:w-48">
            <span className="absolute inset-y-0 left-3 flex items-center text-stone-400 text-xs">📍 ZIP:</span>
            <input
              type="text"
              value={inputZip}
              onChange={(e) => setInputZip(e.target.value)}
              placeholder="e.g. 10451"
              className="w-full pl-12 pr-4 py-2 bg-stone-50 border border-stone-200 rounded-xl text-xs font-bold text-stone-800 focus:ring-2 focus:ring-brand-500 outline-none"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 bg-stone-900 hover:bg-black text-white text-xs font-bold rounded-xl transition"
          >
            Predict
          </button>
        </form>
      </div>

      {loading ? (
        <LoadingSpinner message="Calculating Snowflake Deficit Model & Produce Matches..." />
      ) : error ? (
        <ErrorState error={error} onRetry={() => fetchData(zip)} />
      ) : (
        <>
          {/* Deficit Chart (Snowflake Marketplace Demand Score) */}
          <DeficitChart data={demandData} selectedZip={zip} />

          {/* Matched Produce Listings Section */}
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
              <div>
                <h2 className="text-lg font-black text-stone-900 tracking-tight">
                  Available Fresh Produce from Local Gardens
                </h2>
                <p className="text-xs text-stone-500">
                  AI-graded listings ranked for high-deficit corner stores within 15 km
                </p>
              </div>

              <div className="text-xs text-stone-500 font-medium">
                Showing <span className="font-bold text-stone-800">{listings.length}</span> active listings
              </div>
            </div>

            {listings.length === 0 ? (
              <EmptyState
                icon="🥬"
                title="No produce listings yet"
                description="Use the Farmer Upload page to post fresh surplus crops from local gardens."
              />
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {listings.map((listing) => (
                  <ListingCard
                    key={listing.id}
                    listing={listing}
                    onBargain={handleBargain}
                  />
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}

