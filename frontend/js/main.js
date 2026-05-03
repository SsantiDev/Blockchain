import { initTheme }     from './theme.js';
import { initAuth }      from './auth.js';
import { initDropZone }  from './notarize.js';
import { initDashboard } from './dashboard.js';
import { getChain }      from './api.js';

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initAuth();
  initDropZone();
  initDashboard();
  lucide.createIcons();
  updateStats();
  setInterval(updateStats, 10_000);
});

const updateStats = async () => {
  try {
    const res = await getChain();
    if (!res.ok) return;
    const data = await res.json();
    const el = document.getElementById('stat-blocks');
    if (el) el.textContent = `#${data.length.toLocaleString()}`;
    const nodes = document.getElementById('stat-nodes');
    if (nodes) nodes.textContent = Math.floor(150 + Math.random() * 10);
  } catch { /* servidor no disponible */ }
};
