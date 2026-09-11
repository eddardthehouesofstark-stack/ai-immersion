/**
 * TrendLoom Chart.js Renderer
 * Visualizes real historical observation points (24h, 7d, 30d, 90d)
 * NEVER renders fabricated data.
 */

let activeChart = null;

export function renderTrendHistoryChart(canvasId, historyPoints, selectedRange = 'all') {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  if (activeChart) {
    activeChart.destroy();
    activeChart = null;
  }

  if (!historyPoints || historyPoints.length === 0) {
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.font = '14px Plus Jakarta Sans, sans-serif';
      ctx.fillStyle = '#7A7975';
      ctx.textAlign = 'center';
      ctx.fillText('Historical observations will appear as continuous signals accumulate.', canvas.width / 2, 80);
    }
    return;
  }

  // Filter based on selected time range
  const now = Date.now();
  let filtered = [...historyPoints].sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());

  if (selectedRange === '24h') {
    filtered = filtered.filter(p => now - new Date(p.timestamp).getTime() <= 24 * 3600 * 1000);
  } else if (selectedRange === '7d') {
    filtered = filtered.filter(p => now - new Date(p.timestamp).getTime() <= 7 * 24 * 3600 * 1000);
  } else if (selectedRange === '30d') {
    filtered = filtered.filter(p => now - new Date(p.timestamp).getTime() <= 30 * 24 * 3600 * 1000);
  } else if (selectedRange === '90d') {
    filtered = filtered.filter(p => now - new Date(p.timestamp).getTime() <= 90 * 24 * 3600 * 1000);
  }

  if (filtered.length === 0) {
    filtered = historyPoints.slice(-1); // Show latest observation if range has no older points
  }

  const labels = filtered.map(p => {
    const d = new Date(p.timestamp);
    return `${d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} ${d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}`;
  });

  const scores = filtered.map(p => p.score);

  // Check if Chart.js is available in window
  if (typeof window.Chart !== 'undefined') {
    const ctx = canvas.getContext('2d');
    activeChart = new window.Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Real Trend Score (0-100)',
          data: scores,
          borderColor: '#8B3A2B', // Editorial terracotta
          backgroundColor: 'rgba(139, 58, 43, 0.04)',
          borderWidth: 2.5,
          tension: 0.25,
          fill: true,
          pointBackgroundColor: '#8B3A2B',
          pointBorderColor: '#FFFFFF',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#141414',
            titleFont: { family: 'Plus Jakarta Sans', size: 12 },
            bodyFont: { family: 'Plus Jakarta Sans', size: 13, weight: 'bold' },
            padding: 10,
            cornerRadius: 4,
            displayColors: false,
            callbacks: {
              label: (context) => `Score: ${context.parsed.y}/100`
            }
          }
        },
        scales: {
          y: {
            min: 0,
            max: 100,
            grid: { color: '#EFECE6' },
            ticks: {
              font: { family: 'Plus Jakarta Sans', size: 11 },
              color: '#7A7975',
              stepSize: 20
            }
          },
          x: {
            grid: { display: false },
            ticks: {
              font: { family: 'Plus Jakarta Sans', size: 11 },
              color: '#7A7975',
              maxRotation: 0,
              autoSkip: true,
              maxTicksLimit: 6
            }
          }
        }
      }
    });
  }
}
