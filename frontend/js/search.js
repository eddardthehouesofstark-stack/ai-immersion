/**
 * TrendLoom Debounced Search Controller
 */
import { api } from './api.js';

export function setupSearchInput(inputElement, onResults, debounceMs = 350) {
  if (!inputElement) return;

  let timer = null;

  inputElement.addEventListener('input', (e) => {
    const query = e.target.value;
    clearTimeout(timer);

    timer = setTimeout(async () => {
      try {
        if (!query.trim()) {
          const defaultTrends = await api.getTrends();
          onResults(defaultTrends);
          return;
        }

        const results = await api.searchTrends(query);
        onResults(results);
      } catch (err) {
        console.error('[Search] Error querying trends:', err);
      }
    }, debounceMs);
  });
}
