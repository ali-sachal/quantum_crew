import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import { api } from '../api/client';
import TrustBadge from '../components/TrustBadge';
import LoadingSpinner from '../components/LoadingSpinner';

// Custom SVG Icons for Farms (Green) and Corner Stores (Orange)
const createMarkerIcon = (color, emoji) => {
  return L.divIcon({
    className: 'custom-leaflet-marker',
    html: `
      <div style="
        background: ${color};
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        border: 3px solid white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.25);
        cursor: pointer;
        transition: transform 0.2s;
      " onmouseover="this.style.transform='scale(1.15)'" onmouseout="this.style.transform='scale(1)'">
        ${emoji}
      </div>
    `,
    iconSize: [36, 36],
    iconAnchor: [18, 18],
    popupAnchor: [0, -18],
  });
};

const farmIcon = createMarkerIcon('#16a34a', '🌱');   // Green for Farms
const storeIcon = createMarkerIcon('#ea580c', '🏪');  // Orange for Corner Stores

export default function MapView() {
  const [agents, setAgents] = useState([]);
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);

  // Center of NYC Food Desert benchmark (South Bronx / Harlem)
  const mapCenter = [40.8160, -73.9250];

  useEffect(() => {
    async function loadMapData() {
      try {
        const [agentsRes, listingsRes] = await Promise.all([
          api.getAgents(),
          api.getListings()
        ]);
        setAgents(agentsRes);
        setListings(listingsRes);
      } catch (err) {
        console.error('Failed to load map agents:', err);
      } finally {
        setLoading(false);
      }
    }
    loadMapData();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header & Legend */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-3xl border border-stone-200/90 shadow-sm">
        <div>
          <h1 className="text-2xl font-black text-stone-900 tracking-tight">Food Desert Geospatial Matchmaker</h1>
          <p className="text-xs text-stone-500 mt-1">
            Visualizing verified urban community gardens and buyer corner stores in high-deficit zones
          </p>
        </div>

        {/* Legend */}
        <div className="flex items-center gap-3 bg-stone-50 border border-stone-200 px-4 py-2 rounded-2xl text-xs font-semibold">
          <div className="flex items-center gap-1.5">
            <span className="w-3.5 h-3.5 rounded-full bg-brand-600 inline-flex items-center justify-center text-[10px] text-white">🌱</span>
            <span className="text-stone-700">Urban Farm (Seller)</span>
          </div>
          <span className="text-stone-300">|</span>
          <div className="flex items-center gap-1.5">
            <span className="w-3.5 h-3.5 rounded-full bg-orange-600 inline-flex items-center justify-center text-[10px] text-white">🏪</span>
            <span className="text-stone-700">Corner Store (Buyer)</span>
          </div>
        </div>
      </div>

      {loading ? (
        <LoadingSpinner message="Plotting Geospatial Network on OpenStreetMap..." />
      ) : (
        <div className="bg-white p-3 rounded-3xl border border-stone-200/90 shadow-sm h-[600px] overflow-hidden relative">
          <MapContainer
            center={mapCenter}
            zoom={13}
            scrollWheelZoom={true}
            style={{ width: '100%', height: '100%', borderRadius: '1.25rem' }}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {agents.map((agent) => {
              const isSeller = agent.role === 'seller';
              const icon = isSeller ? farmIcon : storeIcon;

              // Find active produce for this farm
              const sellerListings = listings.filter(l => l.seller?.id === agent.id);

              return (
                <Marker
                  key={agent.id}
                  position={[agent.latitude, agent.longitude]}
                  icon={icon}
                >
                  <Popup className="custom-popup">
                    <div className="p-1 space-y-2 max-w-xs font-sans">
                      <div className="flex items-center gap-1.5">
                        <span className={`text-[10px] font-black uppercase px-2 py-0.5 rounded-full text-white ${
                          isSeller ? 'bg-brand-600' : 'bg-orange-600'
                        }`}>
                          {isSeller ? 'Farm Seller' : 'Store Buyer'}
                        </span>
                        <span className="text-xs font-bold text-stone-500 font-mono">ZIP {agent.zip_code}</span>
                      </div>

                      <h4 className="text-sm font-black text-stone-900">{agent.name}</h4>
                      <p className="text-xs text-stone-600 leading-tight">{agent.description}</p>

                      <div className="pt-2 border-t border-stone-200">
                        <TrustBadge
                          solanaAddress={agent.solana_address}
                          txSignature={agent.registry_tx}
                          reputation={agent.reputation_score}
                          compact
                        />
                      </div>

                      {isSeller && sellerListings.length > 0 && (
                        <div className="pt-2 border-t border-stone-100">
                          <span className="text-[10px] uppercase font-bold text-stone-400 block mb-1">Current Surplus Crops:</span>
                          <div className="space-y-1">
                            {sellerListings.map(l => (
                              <div key={l.id} className="flex justify-between text-xs font-medium text-stone-700 bg-stone-50 p-1.5 rounded-lg">
                                <span>{l.item_name} (Grade {l.grade})</span>
                                <span className="font-bold text-brand-700">${l.suggested_price}/kg</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </Popup>
                </Marker>
              );
            })}
          </MapContainer>
        </div>
      )}
    </div>
  );
}
