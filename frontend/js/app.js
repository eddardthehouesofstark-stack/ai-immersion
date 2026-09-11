/**
 * TrendLoom Master Frontend Controller
 * Boots realtime intelligence, routing, and view state
 */
import { realtime } from './realtime.js';
import { initDashboard, loadDashboardData, loadHealthStatus } from './dashboard.js';
import { initTrendExplorer } from './trends.js';
import { initTrendDetail } from './trend-detail.js';
import { initRegionalIntelligence } from './regional.js';
import { initForecastIntelligence } from './forecast.js';

document.addEventListener('DOMContentLoaded', async () => {
  // 1. Establish Realtime SSE stream
  realtime.connect();

  // 2. Identify active page view
  const pathname = window.location.pathname;

  if (pathname.includes('trends.html')) {
    setActiveNav('navTrends');
    await initTrendExplorer();
  } else if (pathname.includes('trend-detail.html')) {
    setActiveNav('navTrends');
    await initTrendDetail();
  } else if (pathname.includes('regional.html')) {
    setActiveNav('navRegional');
    await initRegionalIntelligence();
  } else if (pathname.includes('forecast.html')) {
    setActiveNav('navForecast');
    await initForecastIntelligence();
  } else {
    // Default: Dashboard
    setActiveNav('navDashboard');
    await initDashboard();
  }

  // 3. Listen for realtime background updates
  realtime.on('trends_updated', (data) => {
    console.log('[App] Auto-refreshing active view on live update event');
    if (pathname.includes('trends.html')) {
      initTrendExplorer();
    } else if (pathname.includes('regional.html')) {
      initRegionalIntelligence();
    } else if (pathname.includes('forecast.html')) {
      initForecastIntelligence();
    } else if (!pathname.includes('trend-detail.html')) {
      loadDashboardData();
      loadHealthStatus();
    }
  });
});

function setActiveNav(elementId) {
  document.querySelectorAll('.tl-nav-link').forEach(link => link.classList.remove('active'));
  const active = document.getElementById(elementId);
  if (active) active.classList.add('active');
}
