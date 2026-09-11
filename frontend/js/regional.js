/**
 * TrendLoom Regional Fashion Intelligence Module
 * Special focus on Tamil Nadu and key Indian textile hubs
 */
import { api } from './api.js';
import { renderTrendCards } from './dashboard.js';

export async function initRegionalIntelligence() {
  const regionSelector = document.getElementById('regionalSelect');
  const feedContainer = document.getElementById('regionalTrendFeed');
  const fabricsContainer = document.getElementById('popularFabricsList');
  const colorsContainer = document.getElementById('popularColorsList');
  const scoreCardVal = document.getElementById('regionalAvgScore');
  const regionNameEl = document.getElementById('currentRegionName');
  const heroBadge = document.getElementById('tamilNaduFocusBadge');

  async function loadRegion(region) {
    if (feedContainer) {
      feedContainer.innerHTML = `<div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: var(--text-muted);">Loading signals for ${region}...</div>`;
    }

    if (regionNameEl) regionNameEl.innerText = region;
    if (heroBadge) {
      heroBadge.style.display = (region === 'Tamil Nadu') ? 'inline-block' : 'none';
    }

    try {
      const data = await api.getRegionalTrends(region);
      const trends = data.trends || [];

      // Update Trend Cards
      renderTrendCards(trends, feedContainer);

      // Average score
      if (scoreCardVal) {
        const avg = trends.length > 0
          ? Math.round(trends.reduce((acc, t) => acc + t.trend_score, 0) / trends.length)
          : 'N/A';
        scoreCardVal.innerText = avg;
      }

      // Popular fabrics
      if (fabricsContainer) {
        if (data.popular_fabrics && data.popular_fabrics.length > 0) {
          fabricsContainer.innerHTML = data.popular_fabrics.map(f => `
            <div class="tl-chip" style="cursor: default;">
              <strong>${f.name}</strong> (${f.count} trends)
            </div>
          `).join('');
        } else {
          fabricsContainer.innerHTML = '<span style="font-size: 13px; color: var(--text-muted);">Grounded in regional handloom and organic cotton archives.</span>';
        }
      }

      // Popular colors
      if (colorsContainer) {
        if (data.popular_colors && data.popular_colors.length > 0) {
          colorsContainer.innerHTML = data.popular_colors.map(c => `
            <div class="tl-chip" style="cursor: default;">
              <span>${c.name}</span>
            </div>
          `).join('');
        } else {
          colorsContainer.innerHTML = '<span style="font-size: 13px; color: var(--text-muted);">Temple Gold, Vermilion, and Unbleached Ecru.</span>';
        }
      }

    } catch (err) {
      console.error('[Regional] Error loading regional data:', err);
      if (feedContainer) {
        feedContainer.innerHTML = '<div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: #A34839;">LIVE DATA UNAVAILABLE: Unable to load regional trends.</div>';
      }
    }
  }

  if (regionSelector) {
    regionSelector.addEventListener('change', (e) => {
      loadRegion(e.target.value);
    });
  }

  // Check URL param or default to Tamil Nadu
  const urlParams = new URLSearchParams(window.location.search);
  const initialRegion = urlParams.get('region') || 'Tamil Nadu';
  if (regionSelector) regionSelector.value = initialRegion;

  await loadRegion(initialRegion);
}
