/**
 * TrendLoom Centralized API Client
 * Connects to the backend REST API
 */

const API_BASE = '/api';

export const api = {
  async getHealth() {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
    return res.json();
  },

  async getTrends(filters = {}) {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '' && v !== 'All' && v !== 'All Regions' && v !== 'All Categories') {
        params.append(k, String(v));
      }
    });
    const url = `${API_BASE}/trends${params.toString() ? `?${params.toString()}` : ''}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Failed to load trends: ${res.statusText}`);
    return res.json();
  },

  async getLiveOverview() {
    const res = await fetch(`${API_BASE}/trends/live`);
    if (!res.ok) throw new Error(`Failed to load live overview: ${res.statusText}`);
    return res.json();
  },

  async searchTrends(query) {
    if (!query || !query.trim()) return [];
    const res = await fetch(`${API_BASE}/trends/search?q=${encodeURIComponent(query.trim())}`);
    if (!res.ok) throw new Error(`Search failed: ${res.statusText}`);
    return res.json();
  },

  async getRegionalTrends(region) {
    const res = await fetch(`${API_BASE}/trends/regional/${encodeURIComponent(region)}`);
    if (!res.ok) throw new Error(`Regional query failed: ${res.statusText}`);
    return res.json();
  },

  async getTrendDetail(trendId) {
    const res = await fetch(`${API_BASE}/trends/${encodeURIComponent(trendId)}`);
    if (!res.ok) throw new Error(`Failed to load trend detail: ${res.statusText}`);
    return res.json();
  },

  async getTrendHistory(trendId) {
    const res = await fetch(`${API_BASE}/trends/${encodeURIComponent(trendId)}/history`);
    if (!res.ok) throw new Error(`Failed to load history: ${res.statusText}`);
    return res.json();
  },

  async getTrendSources(trendId) {
    const res = await fetch(`${API_BASE}/trends/${encodeURIComponent(trendId)}/sources`);
    if (!res.ok) throw new Error(`Failed to load sources: ${res.statusText}`);
    return res.json();
  },

  async askAnalyst(question) {
    const res = await fetch(`${API_BASE}/intelligence/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    if (!res.ok) throw new Error(`Analyst query failed: ${res.statusText}`);
    return res.json();
  },

  async triggerCollection() {
    const res = await fetch(`${API_BASE}/collect/trigger`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`Collection trigger failed: ${res.statusText}`);
    return res.json();
  },

  async getLogs() {
    const res = await fetch(`${API_BASE}/logs`);
    if (!res.ok) return [];
    return res.json();
  }
};
