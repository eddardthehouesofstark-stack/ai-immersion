/**
 * TrendLoom Trend Explorer Module
 * Handles multi-criteria filtering, sorting, and debounced search
 */
import { api } from './api.js';
import { renderTrendCards } from './dashboard.js';
import { setupSearchInput } from './search.js';

export async function initTrendExplorer() {
  const container = document.getElementById('explorerTrendGrid');
  const searchInput = document.getElementById('explorerSearchInput');
  const countEl = document.getElementById('explorerCount');

  const filterCategory = document.getElementById('filterCategory');
  const filterGender = document.getElementById('filterGender');
  const filterRegion = document.getElementById('filterRegion');
  const filterStatus = document.getElementById('filterStatus');
  const filterMinScore = document.getElementById('filterMinScore');

  async function applyFilters() {
    if (container) {
      container.innerHTML = '<div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: var(--text-muted);">Filtering live trends...</div>';
    }

    const filters = {
      search: searchInput ? searchInput.value.trim() : undefined,
      category: filterCategory ? filterCategory.value : undefined,
      gender: filterGender ? filterGender.value : undefined,
      region: filterRegion ? filterRegion.value : undefined,
      status: filterStatus ? filterStatus.value : undefined,
      minScore: filterMinScore && filterMinScore.value ? Number(filterMinScore.value) : undefined,
    };

    try {
      const trends = await api.getTrends(filters);
      renderTrendCards(trends, container);
      if (countEl) {
        countEl.innerText = `${trends.length} ${trends.length === 1 ? 'Trend' : 'Trends'} Identified`;
      }
    } catch (err) {
      console.error('[Explorer] Filter error:', err);
      if (container) {
        container.innerHTML = '<div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: #A34839;">LIVE DATA UNAVAILABLE: Error loading trends.</div>';
      }
    }
  }

  // Setup debounced search
  if (searchInput) {
    setupSearchInput(searchInput, (results) => {
      renderTrendCards(results, container);
      if (countEl) {
        countEl.innerText = `${results.length} Trends Identified`;
      }
    });
  }

  // Setup dropdown filter triggers
  [filterCategory, filterGender, filterRegion, filterStatus, filterMinScore].forEach(select => {
    if (select) {
      select.addEventListener('change', applyFilters);
    }
  });

  // Initial load
  await applyFilters();
}
