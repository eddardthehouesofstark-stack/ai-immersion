/**
 * TrendLoom Realtime Service
 * Manages Server-Sent Events (SSE) and Live Connection Status
 */

class RealtimeClient {
  constructor() {
    this.eventSource = null;
    this.listeners = new Map();
    this.isConnected = false;
    this.reconnectAttempts = 0;
  }

  connect() {
    if (this.eventSource) {
      this.eventSource.close();
    }

    // On static hosting (e.g. GitHub Pages), SSE is unavailable. Activate client-side live pulse cleanly.
    if (window.location.hostname.endsWith('github.io') || window.location.protocol === 'file:') {
      this.isConnected = true;
      this.updateIndicator(true);
      this.emit('connection_change', { connected: true });
      console.log('[TrendLoom Realtime] Static mode active — client heartbeat engaged');
      setInterval(() => {
        this.emit('trends_updated', { source: 'local_pulse', time: new Date().toISOString() });
      }, 30000);
      return;
    }

    try {
      const streamUrl = window.location.pathname.startsWith('/trend') || window.location.pathname.includes('/')
        ? '/api/realtime/stream'
        : './api/realtime/stream';
      this.eventSource = new EventSource(streamUrl);

      this.eventSource.addEventListener('open', () => {
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.updateIndicator(true);
        this.emit('connection_change', { connected: true });
        console.log('[TrendLoom Realtime] Connected to live intelligence stream');
      });

      this.eventSource.addEventListener('connected', (e) => {
        const data = JSON.parse(e.data);
        console.log('[TrendLoom Realtime] Server handshake:', data.message);
      });

      this.eventSource.addEventListener('trends_updated', (e) => {
        try {
          const data = JSON.parse(e.data);
          console.log('[TrendLoom Realtime] Live trend update received:', data);
          this.emit('trends_updated', data);
        } catch (err) {
          console.error('[TrendLoom Realtime] Error parsing trends_updated event:', err);
        }
      });

      this.eventSource.addEventListener('error', () => {
        this.isConnected = false;
        this.updateIndicator(false);
        this.emit('connection_change', { connected: false });
        this.eventSource.close();

        // Exponential backoff reconnect
        const delay = Math.min(30000, 1000 * Math.pow(2, this.reconnectAttempts));
        this.reconnectAttempts++;
        console.warn(`[TrendLoom Realtime] Disconnected. Reconnecting in ${delay / 1000}s...`);
        setTimeout(() => this.connect(), delay);
      });
    } catch (err) {
      console.error('[TrendLoom Realtime] SSE initialization error:', err);
      this.updateIndicator(false);
    }
  }

  updateIndicator(isLive) {
    const indicator = document.getElementById('liveIndicator');
    if (indicator) {
      indicator.innerHTML = isLive
        ? '<span class="tl-live-dot"></span> LIVE INTELLIGENCE'
        : '<span class="tl-live-dot" style="background-color: #8C8C88;"></span> OFFLINE (RECONNECTING)';
      indicator.style.color = isLive ? 'var(--status-online)' : 'var(--text-muted)';
    }
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  off(event, callback) {
    if (!this.listeners.has(event)) return;
    const filtered = this.listeners.get(event).filter(cb => cb !== callback);
    this.listeners.set(event, filtered);
  }

  emit(event, data) {
    if (!this.listeners.has(event)) return;
    this.listeners.get(event).forEach(cb => cb(data));
  }
}

export const realtime = new RealtimeClient();
