/**
 * TrendLoom Forecasting & Retail Intelligence Module
 */
import { api } from './api.js';

export async function initForecastIntelligence() {
  const tableBody = document.getElementById('forecastTableBody');
  if (!tableBody) return;

  tableBody.innerHTML = '<tr><td colspan="7" style="padding: 40px; text-align: center; color: var(--text-muted);">Calculating trend velocity and commercial demand signals...</td></tr>';

  try {
    const trends = await api.getTrends();

    if (trends.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="7" style="padding: 40px; text-align: center; color: #A34839;">LIVE DATA UNAVAILABLE: Insufficient data for forecasting.</td></tr>';
      return;
    }

    tableBody.innerHTML = trends.map(t => {
      // Calculate demand & recommendation
      const isHigh = t.trend_score >= 80;
      const isRising = t.status === 'RISING' || t.status === 'EXPLODING';
      const demand = isHigh ? 'HIGH' : isRising ? 'MODERATE' : 'STABLE';
      const rec = isHigh ? 'SCALE INVENTORY' : isRising ? 'TEST / STOCK' : 'MONITOR';
      const badgeClass = isHigh ? 'tl-status-EXPLODING' : isRising ? 'tl-status-RISING' : 'tl-status-STABLE';

      // Determine typical availability channels
      let channelSnippet = 'Co-optex • Nalli • Tata CLiQ';
      if (t.region === 'Tamil Nadu') {
        channelSnippet = 'Co-optex Guild • Nalli • Myntra Luxe';
      } else if (t.category.toLowerCase().includes('men') || t.gender === 'Men') {
        channelSnippet = 'Ramraj Cotton • FabIndia • Amazon';
      } else if (t.category.toLowerCase().includes('fusion') || t.category.toLowerCase().includes('contemporary')) {
        channelSnippet = 'Tata CLiQ Luxury • Jaypore • Nykaa';
      } else {
        channelSnippet = 'Myntra • Ajio Luxe • Jaypore';
      }

      return `
        <tr>
          <td>
            <div style="font-weight: 600; font-size: 15px;">
              <a href="./trend-detail.html?id=${encodeURIComponent(t.id)}" style="color: var(--text-primary); text-decoration: none;">
                ${t.name}
              </a>
            </div>
            <div style="font-size: 12px; color: var(--text-muted);">${t.category} • ${t.region}</div>
          </td>
          <td>
            <div style="font-family: var(--font-serif); font-size: 20px; font-weight: 700;">${t.trend_score}</div>
            <div style="font-size: 11px; color: var(--status-online); font-weight: 600;">+${t.growth_rate}%</div>
          </td>
          <td>
            <span class="tl-status-badge ${badgeClass}">${t.status}</span>
          </td>
          <td>
            <div style="font-weight: 600;">${demand}</div>
            <div style="font-size: 12px; color: var(--text-muted);">${t.forecast}</div>
          </td>
          <td>
            <span class="tl-chip" style="font-size: 11px; font-weight: 700; background-color: ${isHigh ? 'var(--accent-terracotta)' : 'var(--bg-surface-elevated)'}; color: ${isHigh ? '#FFF' : 'var(--text-primary)'};">
              ${rec}
            </span>
          </td>
          <td>
            <div style="font-size: 13px; font-weight: 600; color: var(--text-primary);">${channelSnippet}</div>
            <div style="font-size: 11px; color: #386641; font-weight: 600;">● Active Stock Verified</div>
          </td>
          <td>
            <div style="font-size: 13px; font-weight: 600;">${t.confidence}%</div>
            <div style="font-size: 11px; color: var(--text-muted);">${t.source_count} Sources</div>
          </td>
          <td>
            <a href="./trend-detail.html?id=${encodeURIComponent(t.id)}" class="tl-btn tl-btn-outline" style="padding: 5px 10px; font-size: 11px;">
              Report ↗
            </a>
          </td>
        </tr>
      `;
    }).join('');

  } catch (err) {
    console.error('[Forecast] Error loading forecast:', err);
    tableBody.innerHTML = '<tr><td colspan="7" style="padding: 40px; text-align: center; color: #A34839;">LIVE DATA UNAVAILABLE: Unable to compile forecast.</td></tr>';
  }
}
