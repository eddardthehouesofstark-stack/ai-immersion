/**
 * TrendLoom Main Dashboard Module
 */
import { api } from './api.js';

export async function initDashboard() {
  await Promise.all([
    loadHealthStatus(),
    loadDashboardData()
  ]);

  setupAnalystPanel();
  setupRefreshButton();
}

export async function loadHealthStatus() {
  try {
    const health = await api.getHealth();
    const container = document.getElementById('healthIndicators');
    if (!container) return;

    const services = health.services || {};
    container.innerHTML = Object.entries(services).map(([name, status]) => {
      const isOnline = status.includes('ONLINE');
      return `
        <div class="tl-health-item">
          <span class="tl-health-dot ${isOnline ? '' : 'offline'}"></span>
          <span>${name}</span>
          <span style="font-size: 10px; color: ${isOnline ? 'var(--status-online)' : '#A34839'};">●</span>
        </div>
      `;
    }).join('');
  } catch (err) {
    console.warn('[Dashboard] Health status error:', err);
  }
}

export async function loadDashboardData() {
  const feedContainer = document.getElementById('liveTrendFeed');
  if (feedContainer) {
    feedContainer.innerHTML = '<div style="padding: 40px; text-align: center; color: var(--text-muted);">Loading real-time fashion signals...</div>';
  }

  try {
    const data = await api.getLiveOverview();
    const trends = data.trends || [];
    const stats = data.stats || {};

    // 1. Update KPI tiles
    const activeEl = document.getElementById('kpiActiveTrends');
    const risingEl = document.getElementById('kpiRisingTrends');
    const fastestEl = document.getElementById('kpiFastestGrowing');
    const sourcesEl = document.getElementById('kpiSourcesTracked');
    const updatedEl = document.getElementById('kpiLastUpdated');

    if (activeEl) activeEl.innerText = stats.active_trends_count || trends.length;
    if (risingEl) risingEl.innerText = stats.rising_trends_count || trends.filter(t => t.status === 'RISING' || t.status === 'EXPLODING').length;
    if (fastestEl) {
      const fastest = stats.fastest_growing || [...trends].sort((a, b) => b.growth_rate - a.growth_rate)[0];
      fastestEl.innerHTML = fastest ? `+${fastest.growth_rate}% <span style="font-size: 14px; font-family: var(--font-sans); color: var(--text-secondary); font-weight: normal;">(${fastest.name.slice(0, 20)}...)</span>` : 'N/A';
    }
    if (sourcesEl) sourcesEl.innerText = stats.sources_count || 6;
    if (updatedEl && stats.last_updated) {
      const d = new Date(stats.last_updated);
      updatedEl.innerText = d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }

    // 2. Render Live Trends Feed
    renderTrendCards(trends, feedContainer);
  } catch (err) {
    console.error('[Dashboard] Error loading data:', err);
    if (feedContainer) {
      feedContainer.innerHTML = `
        <div style="padding: 40px; text-align: center; color: #A34839;">
          LIVE DATA UNAVAILABLE: Unable to retrieve signals from live sources.
          <div style="margin-top: 12px;">
            <button class="tl-btn tl-btn-outline" onclick="window.triggerRefresh()">Retry Collection</button>
          </div>
        </div>
      `;
    }
  }
}

export function renderTrendCards(trends, container) {
  if (!container) return;

  if (!trends || trends.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1 / -1; padding: 60px 20px; text-align: center; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md);">
        <h3 class="tl-h3" style="margin-bottom: 8px;">No trends match your criteria</h3>
        <p style="color: var(--text-muted); font-size: 14px;">Try adjusting your filters or search keywords.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = trends.map(t => {
    const updated = new Date(t.last_updated).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    return `
      <a href="/trend-detail.html?id=${encodeURIComponent(t.id)}" class="tl-trend-card" data-trend-id="${t.id}">
        <div class="tl-card-media">
          <img src="${t.image_url || 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=800&q=80'}" alt="${t.name}" class="tl-card-img" loading="lazy">
          <div class="tl-card-badge-top">
            <span class="tl-status-badge tl-status-${t.status}">${t.status}</span>
          </div>
          <div class="tl-card-score-pill">
            <span>${t.trend_score}</span>
            <span style="font-size: 10px; color: #BBB;">/100</span>
          </div>
        </div>
        <div class="tl-card-body">
          <div class="tl-card-meta">
            <span>${t.category}</span>
            <span>${t.region}</span>
          </div>
          <h3 class="tl-card-title">${t.name}</h3>
          <p class="tl-card-desc">${t.description}</p>
          <div class="tl-card-footer">
            <span class="tl-card-growth">+${t.growth_rate}% 7d Momentum</span>
            <span class="tl-card-region-tag">${t.source_count} Verified Sources</span>
          </div>
        </div>
      </a>
    `;
  }).join('');
}

function setupAnalystPanel() {
  const input = document.getElementById('analystInput');
  const btn = document.getElementById('analystSubmitBtn');
  const output = document.getElementById('analystOutput');
  const textEl = document.getElementById('analystAnswerText');
  const metaEl = document.getElementById('analystEvidenceMeta');
  const chips = document.querySelectorAll('.tl-chip');

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      const q = chip.getAttribute('data-question');
      if (input && q) {
        input.value = q;
        submitQuestion(q);
      }
    });
  });

  if (btn && input) {
    btn.addEventListener('click', () => {
      if (input.value.trim()) {
        submitQuestion(input.value.trim());
      }
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && input.value.trim()) {
        submitQuestion(input.value.trim());
      }
    });
  }

  async function submitQuestion(question) {
    if (!output || !textEl) return;
    output.classList.add('active');
    textEl.innerHTML = '<span style="color: var(--text-muted);">Analyzing current database observations and live market signals...</span>';
    if (metaEl) metaEl.innerHTML = '';
    if (btn) btn.disabled = true;

    try {
      const res = await api.askAnalyst(question);
      textEl.innerText = res.answer;
      if (metaEl) {
        metaEl.innerHTML = `
          <span>Confidence: <strong>${res.confidence}%</strong></span>
          <span>Verified Sources: <strong>${res.sourcesCount} feeds</strong></span>
          <span>Grounding: <strong>Current TrendLoom Database</strong></span>
        `;
      }
    } catch (err) {
      textEl.innerText = 'LIVE DATA UNAVAILABLE: Unable to query AI Analyst at this moment. Database trends remain live in explorer.';
    } finally {
      if (btn) btn.disabled = false;
    }
  }
}

function setupRefreshButton() {
  const btn = document.getElementById('refreshPipelineBtn');
  if (!btn) return;

  btn.addEventListener('click', async () => {
    btn.disabled = true;
    const origHtml = btn.innerHTML;
    btn.innerHTML = 'Scanning Live Feeds...';
    try {
      const res = await api.triggerCollection();
      await loadDashboardData();
      await loadHealthStatus();
      btn.innerHTML = `Updated (${res.trendsUpdated || 0} Trends)`;
      setTimeout(() => {
        btn.innerHTML = origHtml;
        btn.disabled = false;
      }, 2500);
    } catch (err) {
      console.error('Manual refresh failed:', err);
      btn.innerHTML = 'Scan Failed';
      setTimeout(() => {
        btn.innerHTML = origHtml;
        btn.disabled = false;
      }, 2500);
    }
  });

  window.triggerRefresh = () => btn.click();
}
