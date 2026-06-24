/* ═══════════════════════════════════════════════════════════════
   main.js — Global Utilities: Theme, Sidebar, Toast, Animations
   ═══════════════════════════════════════════════════════════════ */

// ── Theme Toggle ─────────────────────────────────────────────
const THEME_KEY = 'lf_theme';

function initTheme() {
  const saved = localStorage.getItem('theme') || localStorage.getItem(THEME_KEY) || 'light';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeIcon(saved);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next    = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  localStorage.setItem(THEME_KEY, next);
  updateThemeIcon(next);
  showToast('Theme Changed', `Switched to ${next} mode`, next === 'dark' ? 'info' : 'warning');
}

function updateThemeIcon(theme) {
  const icon = document.getElementById('themeIcon');
  if (icon) {
    icon.className = theme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
  }
}

// ── Sidebar ───────────────────────────────────────────────────
function toggleSidebar() {
  const sidebar  = document.getElementById('sidebar');
  const overlay  = document.getElementById('sidebarOverlay');
  if (!sidebar) return;
  sidebar.classList.toggle('open');
  overlay.classList.toggle('show');
  document.body.style.overflow = sidebar.classList.contains('open') ? 'hidden' : '';
}

// ── Toast Notifications ───────────────────────────────────────
const TOAST_ICONS = {
  success: 'fa-check-circle',
  danger:  'fa-exclamation-circle',
  warning: 'fa-exclamation-triangle',
  info:    'fa-info-circle',
};

function showToast(title, message, type = 'info', duration = 4000) {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <div class="toast-icon"><i class="fas ${TOAST_ICONS[type] || 'fa-info-circle'}"></i></div>
    <div class="toast-body">
      <div class="toast-title">${title}</div>
      <div class="toast-msg">${message}</div>
    </div>
    <button class="toast-close" onclick="dismissToast(this.parentElement)">×</button>
  `;
  container.appendChild(toast);

  setTimeout(() => dismissToast(toast), duration);
}

function dismissToast(toast) {
  if (!toast || !toast.parentElement) return;
  toast.classList.add('leaving');
  setTimeout(() => toast.remove(), 300);
}

// ── FAB ───────────────────────────────────────────────────────
function toggleFab() {
  const fab  = document.getElementById('fabMain');
  const menu = document.getElementById('fabMenu');
  if (!fab || !menu) return;
  fab.classList.toggle('open');
  menu.classList.toggle('open');
}

// Close FAB when clicking outside
document.addEventListener('click', (e) => {
  const container = document.querySelector('.fab-container');
  if (container && !container.contains(e.target)) {
    document.getElementById('fabMain')?.classList.remove('open');
    document.getElementById('fabMenu')?.classList.remove('open');
  }
});

// ── Scroll Reveal ─────────────────────────────────────────────
function initReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}

// ── Active Nav Link ───────────────────────────────────────────
function setActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && path === href) {
      link.classList.add('active');
    } else if (href && href !== '/' && path.startsWith(href)) {
      link.classList.add('active');
    }
  });
}

// ── Counter Animation ─────────────────────────────────────────
function animateCounters() {
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = parseInt(el.getAttribute('data-count'), 10);
    const duration = 1200;
    const step  = target / (duration / 16);
    let current = 0;
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = Math.round(current).toLocaleString();
      if (current >= target) clearInterval(timer);
    }, 16);
  });
}

// ── Relative Time ─────────────────────────────────────────────
function relativeTime(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now  = new Date();
  const diff = now - date;
  const secs = Math.floor(diff / 1000);
  const mins = Math.floor(secs / 60);
  const hrs  = Math.floor(mins / 60);
  const days = Math.floor(hrs / 24);
  if (days > 30)  return date.toLocaleDateString();
  if (days > 0)   return `${days}d ago`;
  if (hrs > 0)    return `${hrs}h ago`;
  if (mins > 0)   return `${mins}m ago`;
  return 'just now';
}

// Apply relative times to all .rel-time elements
function applyRelativeTimes() {
  document.querySelectorAll('[data-time]').forEach(el => {
    el.textContent = relativeTime(el.getAttribute('data-time'));
    el.title = el.getAttribute('data-time');
  });
}

// ── Flash Auto-dismiss ────────────────────────────────────────
function autoDismissFlash() {
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    }, 5000);
  });
}

// ── Image Preview ─────────────────────────────────────────────
function previewImage(event, previewId = 'preview') {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    const preview = document.getElementById(previewId);
    if (preview) {
      preview.src = reader.result;
      preview.style.display = 'block';
      preview.parentElement.querySelector('i')?.remove();
      preview.parentElement.querySelector('span')?.remove();
    }
  };
  reader.readAsDataURL(file);
}

// ── Confirm Delete ────────────────────────────────────────────
function confirmDelete(formEl, msg = 'Are you sure you want to delete this item?') {
  if (confirm(msg)) formEl.submit();
  return false;
}

// ── Notification btn ──────────────────────────────────────────
function initNotifications() {
  const btn = document.getElementById('notificationsBtn');
  if (!btn) return;
  btn.addEventListener('click', () => {
    showToast('Notifications', 'No new notifications at this time.', 'info');
  });
}

// ── Real-time Stats Polling ───────────────────────────────────
let statsInterval = null;

function startStatsPolling(intervalMs = 30000) {
  updateLiveStats();
  statsInterval = setInterval(updateLiveStats, intervalMs);
}

async function updateLiveStats() {
  try {
    const res  = await fetch('/api/stats');
    const data = await res.json();
    Object.keys(data).forEach(key => {
      const el = document.querySelector(`[data-stat="${key}"]`);
      if (el) el.textContent = data[key].toLocaleString();
    });
  } catch (e) { /* silent fail */ }
}

// ── DOMContentLoaded Init ─────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  setActiveNav();
  initReveal();
  applyRelativeTimes();
  autoDismissFlash();
  animateCounters();
  initNotifications();

  // Convert flash messages to toasts
  document.querySelectorAll('.flash').forEach(flash => {
    const type = flash.classList.contains('flash-success') ? 'success'
               : flash.classList.contains('flash-danger')  ? 'danger'
               : flash.classList.contains('flash-warning') ? 'warning' : 'info';
    const text = flash.textContent.trim().replace(/[×✕]/g, '').trim();
    if (text) showToast(type.charAt(0).toUpperCase() + type.slice(1), text, type);
  });

  // Keyboard shortcut: / to focus search
  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT'
                      && document.activeElement.tagName !== 'TEXTAREA') {
      e.preventDefault();
      document.getElementById('searchInput')?.focus();
    }
    if (e.key === 'Escape') {
      document.getElementById('sidebar')?.classList.remove('open');
      document.getElementById('sidebarOverlay')?.classList.remove('show');
    }
  });

  // Start live stats polling
  startStatsPolling(30000);
});
