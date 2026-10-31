import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
});

export const api = {
  // Produce Listings
  getListings: () => apiClient.get('/listings/').then(r => r.data),
  getListing: (id) => apiClient.get(`/listings/${id}/`).then(r => r.data),
  createListing: (formData) => apiClient.post('/listings/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }).then(r => r.data),

  // Demand Deficit Prediction (Snowflake)
  getDemand: (zip = '10451') => apiClient.get(`/demand/?zip=${zip}`).then(r => r.data),

  // Store Matchmaking
  getMatches: (listingId) => apiClient.get(`/matches/${listingId}/`).then(r => r.data),

  // Negotiation Chat (Gemma 4)
  getChatHistory: (dealId) => apiClient.get(`/chat/${dealId}/`).then(r => r.data),
  sendMessage: (dealId, content) => apiClient.post(`/chat/${dealId}/`, { content }).then(r => r.data),

  // Deals & Solana Devnet Settlement
  acceptDeal: (dealId) => apiClient.post(`/deals/${dealId}/accept/`).then(r => r.data),
  startDeal: (listingId, buyerId, initialOffer) => apiClient.post('/deals/start/', null, {
    params: { listing_id: listingId, buyer_id: buyerId, initial_offer: initialOffer }
  }).then(r => r.data),

  // Agents & Onchain Registry
  getAgents: (role) => apiClient.get('/agents/', { params: { role } }).then(r => r.data),
  registerAgent: (agentData) => apiClient.post('/agents/register/', agentData).then(r => r.data),
};

export default apiClient;
