/* ═══════════════════════════════════════════════════════════════
   dashboard.js — Charts, Drag-and-Drop Widgets, Live Feed
   ═══════════════════════════════════════════════════════════════ */

const CHART_DEFAULTS = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim() || '#94a3b8',
        font: { family: 'Inter', size: 12 },
        padding: 16,
      }
    },
    tooltip: {
      backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--bg-card').trim() || 'rgba(17,24,39,0.9)',
      borderColor:     'rgba(99,102,241,0.3)',
      borderWidth: 1,
      titleColor:  '#e2e8f0',
      bodyColor:   '#94a3b8',
      padding: 12,
      cornerRadius: 8,
    }
  },
  scales: {
    x: {
      grid:  { color: 'rgba(255,255,255,0.04)' },
      ticks: { color: '#64748b', font: { size: 11 } },
    },
    y: {
      grid:  { color: 'rgba(255,255,255,0.04)' },
      ticks: { color: '#64748b', font: { size: 11 } },
      beginAtZero: true,
    }
  }
};

// ── Monthly Trend Chart ───────────────────────────────────────
function initTrendChart(monthsData) {
  const ctx = document.getElementById('trendChart');
  if (!ctx || !monthsData) return;

  const labels    = monthsData.map(m => m.label);
  const lostData  = monthsData.map(m => m.lost);
  const foundData = monthsData.map(m => m.found);
  const recData   = monthsData.map(m => m.recovered);

  new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Lost',
          data: lostData,
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239,68,68,0.1)',
          borderWidth: 2.5,
          pointBackgroundColor: '#ef4444',
          pointRadius: 4,
          pointHoverRadius: 6,
          tension: 0.4,
          fill: true,
        },
        {
          label: 'Found',
          data: foundData,
          borderColor: '#10b981',
          backgroundColor: 'rgba(16,185,129,0.1)',
          borderWidth: 2.5,
          pointBackgroundColor: '#10b981',
          pointRadius: 4,
          pointHoverRadius: 6,
          tension: 0.4,
          fill: true,
        },
        {
          label: 'Recovered',
          data: recData,
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99,102,241,0.1)',
          borderWidth: 2.5,
          pointBackgroundColor: '#6366f1',
          pointRadius: 4,
          pointHoverRadius: 6,
          tension: 0.4,
          fill: true,
        }
      ]
    },
    options: {
      ...CHART_DEFAULTS,
      plugins: {
        ...CHART_DEFAULTS.plugins,
        legend: { ...CHART_DEFAULTS.plugins.legend, position: 'top' }
      }
    }
  });
}

// ── Category Doughnut Chart ───────────────────────────────────
function initCategoryChart(catData) {
  const ctx = document.getElementById('categoryChart');
  if (!ctx || !catData) return;

  const COLORS = ['#6366f1','#8b5cf6','#06b6d4','#10b981','#f59e0b','#ef4444','#ec4899','#14b8a6'];

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: catData.map(c => c[0] || 'Other'),
      datasets: [{
        data: catData.map(c => c[1]),
        backgroundColor: COLORS.map(c => c + 'cc'),
        borderColor:     COLORS,
        borderWidth: 2,
        hoverBorderWidth: 3,
        hoverOffset: 6,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '68%',
      plugins: {
        legend: {
          position: 'right',
          labels: {
            color: '#94a3b8',
            font: { family: 'Inter', size: 11 },
            padding: 12,
            usePointStyle: true,
            pointStyleWidth: 8,
          }
        },
        tooltip: CHART_DEFAULTS.plugins.tooltip,
      }
    }
  });
}

// ── Horizontal Bar Chart (Top Categories) ────────────────────
function initTopCatsChart(topCats) {
  const ctx = document.getElementById('topCatsChart');
  if (!ctx || !topCats) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: topCats.map(c => c[0]),
      datasets: [{
        label: 'Recovered',
        data: topCats.map(c => c[1]),
        backgroundColor: 'rgba(16,185,129,0.7)',
        borderColor: '#10b981',
        borderWidth: 2,
        borderRadius: 6,
      }]
    },
    options: {
      ...CHART_DEFAULTS,
      indexAxis: 'y',
      plugins: {
        ...CHART_DEFAULTS.plugins,
        legend: { display: false }
      },
      scales: {
        x: { ...CHART_DEFAULTS.scales.x },
        y: {
          grid: { display: false },
          ticks: { color: '#94a3b8', font: { size: 12 } }
        }
      }
    }
  });
}

// ── Analytics Monthly Bar Chart ───────────────────────────────
function initAnalyticsChart(monthlyData) {
  const ctx = document.getElementById('analyticsChart');
  if (!ctx || !monthlyData) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: monthlyData.map(m => m.label),
      datasets: [
        {
          label: 'Lost',
          data: monthlyData.map(m => m.lost),
          backgroundColor: 'rgba(239,68,68,0.7)',
          borderColor: '#ef4444', borderWidth: 1, borderRadius: 4,
        },
        {
          label: 'Found',
          data: monthlyData.map(m => m.found),
          backgroundColor: 'rgba(16,185,129,0.7)',
          borderColor: '#10b981', borderWidth: 1, borderRadius: 4,
        },
        {
          label: 'Recovered',
          data: monthlyData.map(m => m.recovered),
          backgroundColor: 'rgba(99,102,241,0.7)',
          borderColor: '#6366f1', borderWidth: 1, borderRadius: 4,
        }
      ]
    },
    options: {
      ...CHART_DEFAULTS,
      plugins: { ...CHART_DEFAULTS.plugins, legend: { ...CHART_DEFAULTS.plugins.legend, position: 'top' } }
    }
  });
}

// ── Drag-and-Drop Widget Layout ───────────────────────────────
const WIDGET_ORDER_KEY = 'lf_widget_order';

function initWidgetDrag() {
  const grid = document.getElementById('widgetGrid');
  if (!grid || typeof Sortable === 'undefined') return;

  // Restore saved order
  const saved = localStorage.getItem(WIDGET_ORDER_KEY);
  if (saved) {
    try {
      const order = JSON.parse(saved);
      const children = [...grid.children];
      order.forEach(id => {
        const el = grid.querySelector(`[data-widget="${id}"]`);
        if (el) grid.appendChild(el);
      });
    } catch (e) {}
  }

  Sortable.create(grid, {
    animation: 200,
    ghostClass: 'drag-ghost',
    chosenClass: 'drag-chosen',
    handle: '.card-header',
    onEnd: () => {
      const order = [...grid.children].map(el => el.getAttribute('data-widget'));
      localStorage.setItem(WIDGET_ORDER_KEY, JSON.stringify(order));
    }
  });

  // Add drag cursor to headers
  grid.querySelectorAll('.card-header').forEach(h => {
    h.style.cursor = 'grab';
  });
}

// ── Live Activity Feed Polling ────────────────────────────────
let feedInterval = null;
let lastFeedCount = 0;

async function updateActivityFeed() {
  const feedEl = document.getElementById('liveFeed');
  if (!feedEl) return;

  try {
    const res  = await fetch('/api/feed');
    const feed = await res.json();

    if (feed.length !== lastFeedCount) {
      lastFeedCount = feed.length;
      feedEl.innerHTML = feed.slice(0, 10).map(item => `
        <div class="feed-item">
          <div class="feed-dot"></div>
          <div class="feed-content">
            <div class="feed-action">${escHtml(item.action)}</div>
            <div class="feed-details">${escHtml(item.details || '')}</div>
          </div>
          <div class="feed-time">${relativeTime ? relativeTime(item.timestamp) : item.timestamp}</div>
        </div>
      `).join('');
    }
  } catch (e) {}
}

function escHtml(str) {
  return (str || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function startFeedPolling(ms = 15000) {
  updateActivityFeed();
  feedInterval = setInterval(updateActivityFeed, ms);
}

// ── Widget Collapse Toggle ────────────────────────────────────
function initWidgetCollapse() {
  document.querySelectorAll('.widget-collapse-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const body = btn.closest('.glass-card')?.querySelector('.card-body');
      if (!body) return;
      const isCollapsed = body.style.display === 'none';
      body.style.display = isCollapsed ? '' : 'none';
      btn.innerHTML = isCollapsed
        ? '<i class="fas fa-chevron-up"></i>'
        : '<i class="fas fa-chevron-down"></i>';
    });
  });
}

// ── Init Dashboard ────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initWidgetDrag();
  initWidgetCollapse();
  startFeedPolling(15000);

  // Charts are initialized via inline scripts in the template
  // (so data can be passed from Python)
});
