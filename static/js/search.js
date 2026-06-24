/* ═══════════════════════════════════════════════════════════════
   search.js — Smart Search: Suggestions, Voice, Recent, Typo Fix
   ═══════════════════════════════════════════════════════════════ */

const RECENT_KEY   = 'lf_recent_searches';
const MAX_RECENT   = 8;

// ── Recent Searches ───────────────────────────────────────────
function getRecentSearches() {
  try { return JSON.parse(localStorage.getItem(RECENT_KEY)) || []; }
  catch { return []; }
}

function addRecentSearch(q) {
  if (!q.trim()) return;
  let recent = getRecentSearches().filter(r => r !== q);
  recent.unshift(q);
  recent = recent.slice(0, MAX_RECENT);
  localStorage.setItem(RECENT_KEY, JSON.stringify(recent));
}

function clearRecentSearches() {
  localStorage.removeItem(RECENT_KEY);
}

// ── Search Dropdown ───────────────────────────────────────────
let searchTimeout = null;

async function handleSearchInput(input, dropdown) {
  const q = input.value.trim();
  clearTimeout(searchTimeout);

  if (q.length < 2) {
    showRecentSearches(dropdown, input);
    return;
  }

  searchTimeout = setTimeout(async () => {
    dropdown.style.display = 'block';
    dropdown.innerHTML = `<div style="padding:12px;text-align:center;color:var(--text-muted);font-size:12px"><i class="fas fa-spinner fa-spin"></i> Searching…</div>`;

    try {
      const res     = await fetch(`/api/items/search?q=${encodeURIComponent(q)}`);
      const results = await res.json();

      if (results.length === 0) {
        dropdown.innerHTML = `
          <div style="padding:12px 16px;color:var(--text-muted);font-size:12px;text-align:center">
            <i class="fas fa-search" style="margin-right:6px"></i>No results for "<strong>${escHtml(q)}</strong>"
          </div>`;
      } else {
        dropdown.innerHTML = results.map(r => `
          <a href="/item/${r.id}" class="search-result-item" onclick="addRecentSearch('${escAttr(q)}')">
            <span class="ri-type ${r.type==='Lost'?'tag-danger':'tag-success'}">${r.type}</span>
            <div style="flex:1;min-width:0">
              <div style="font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
                ${highlight(r.item_name || r.description?.slice(0,40) || 'Item', q)}
              </div>
              <div style="font-size:11px;color:var(--text-muted)">
                <i class="fas fa-map-marker-alt" style="margin-right:3px"></i>${escHtml(r.location || '')}
              </div>
            </div>
            <span class="tag ${r.status==='Active'?'tag-info':r.status==='Recovered'?'tag-success':'tag-warning'}" style="font-size:10px">${r.status}</span>
          </a>
        `).join('');

        // Add "View all results" link
        dropdown.innerHTML += `
          <a href="/view?q=${encodeURIComponent(q)}" onclick="addRecentSearch('${escAttr(q)}')"
             style="display:block;padding:10px 14px;font-size:12px;font-weight:600;color:var(--primary-light);text-align:center;border-top:1px solid var(--border)">
            View all results for "${escHtml(q)}" <i class="fas fa-arrow-right"></i>
          </a>`;
      }
    } catch (e) {
      dropdown.innerHTML = `<div style="padding:12px;color:var(--text-muted);font-size:12px;text-align:center">Search unavailable</div>`;
    }
  }, 300);
}

function showRecentSearches(dropdown, input) {
  const recent = getRecentSearches();
  if (recent.length === 0) {
    dropdown.style.display = 'none';
    return;
  }
  dropdown.style.display = 'block';
  dropdown.innerHTML = `
    <div style="padding:8px 12px;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--text-muted);display:flex;justify-content:space-between">
      Recent Searches
      <button onclick="clearRecentSearches();this.closest('.search-dropdown').style.display='none'"
              style="background:none;border:none;color:var(--primary-light);cursor:pointer;font-size:10px;font-weight:600">Clear</button>
    </div>
    ${recent.map(r => `
      <div class="search-result-item" onclick="document.getElementById('searchInput').value='${escAttr(r)}';handleSearchInput(document.getElementById('searchInput'),document.getElementById('searchDropdown'))">
        <i class="fas fa-clock" style="color:var(--text-muted);font-size:11px"></i>
        <span style="font-size:13px;color:var(--text-secondary)">${escHtml(r)}</span>
      </div>
    `).join('')}
    <div style="padding:8px 12px;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--text-muted)">Trending</div>
    ${['Wallet','Phone','Keys','ID Card','Laptop'].map(t => `
      <div class="search-result-item" onclick="document.getElementById('searchInput').value='${t}';handleSearchInput(document.getElementById('searchInput'),document.getElementById('searchDropdown'))">
        <i class="fas fa-fire" style="color:var(--warning);font-size:11px"></i>
        <span style="font-size:13px;color:var(--text-secondary)">${t}</span>
      </div>
    `).join('')}
  `;
}

function highlight(text, query) {
  if (!text || !query) return escHtml(text || '');
  const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')})`, 'gi');
  return escHtml(text).replace(regex, '<mark style="background:var(--primary-glow);color:var(--primary-light);border-radius:2px;padding:0 2px">$1</mark>');
}

function escHtml(str) {
  return (str || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function escAttr(str) {
  return (str || '').replace(/'/g,"\\'").replace(/"/g,'&quot;');
}

// ── Voice Search ──────────────────────────────────────────────
let recognition = null;

function initVoiceSearch(inputEl, btnEl) {
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    if (btnEl) {
      btnEl.title = 'Voice search not supported';
      btnEl.style.opacity = '0.4';
      btnEl.style.cursor  = 'not-allowed';
    }
    return;
  }

  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SR();
  recognition.lang = 'en-IN';
  recognition.continuous = false;
  recognition.interimResults = true;

  recognition.onstart = () => {
    if (btnEl) btnEl.classList.add('listening');
    if (inputEl) inputEl.placeholder = '🎤 Listening…';
    showToast('Voice Search', 'Listening… speak now!', 'info', 3000);
  };

  recognition.onresult = (e) => {
    const transcript = Array.from(e.results).map(r => r[0].transcript).join('');
    if (inputEl) {
      inputEl.value = transcript;
      const dropdown = document.getElementById('searchDropdown');
      if (dropdown) handleSearchInput(inputEl, dropdown);
    }
  };

  recognition.onerror = () => {
    if (btnEl) btnEl.classList.remove('listening');
    if (inputEl) inputEl.placeholder = 'Search items…';
    showToast('Voice Search', 'Could not understand. Try again.', 'warning');
  };

  recognition.onend = () => {
    if (btnEl) btnEl.classList.remove('listening');
    if (inputEl) inputEl.placeholder = 'Search items…';
    // Submit if we got a query
    if (inputEl?.value.trim()) addRecentSearch(inputEl.value.trim());
  };

  if (btnEl) {
    btnEl.addEventListener('click', () => {
      if (btnEl.classList.contains('listening')) {
        recognition.stop();
      } else {
        recognition.start();
      }
    });
  }
}

// ── Filter page search with voice ────────────────────────────
function initFilterSearch() {
  const input  = document.getElementById('filterSearch');
  const voiceBtn = document.getElementById('voiceSearchBtn');
  if (!input) return;

  // Debounced live filter
  let filterTimeout = null;
  input.addEventListener('input', () => {
    clearTimeout(filterTimeout);
    filterTimeout = setTimeout(() => filterItemCards(input.value), 200);
  });

  if (voiceBtn) initVoiceSearch(input, voiceBtn);
}

function filterItemCards(q) {
  const cards = document.querySelectorAll('.item-card[data-search]');
  const lower = q.toLowerCase();
  let visible = 0;
  cards.forEach(card => {
    const text = (card.getAttribute('data-search') || '').toLowerCase();
    const show = !lower || text.includes(lower);
    card.closest('.item-col')?.style.setProperty('display', show ? '' : 'none');
    if (show) visible++;
  });

  const emptyEl = document.getElementById('itemsEmpty');
  if (emptyEl) emptyEl.style.display = visible === 0 ? '' : 'none';
}

// ── Navbar global search ──────────────────────────────────────
function initNavSearch() {
  const input    = document.getElementById('searchInput');
  const dropdown = document.getElementById('searchDropdown');
  if (!input || !dropdown) return;

  input.addEventListener('input', () => handleSearchInput(input, dropdown));
  input.addEventListener('focus', () => {
    if (input.value.length < 2) showRecentSearches(dropdown, input);
    else dropdown.style.display = 'block';
  });

  // Close dropdown when clicking outside
  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.style.display = 'none';
    }
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && input.value.trim()) {
      addRecentSearch(input.value.trim());
      window.location.href = `/view?q=${encodeURIComponent(input.value.trim())}`;
    }
    if (e.key === 'Escape') {
      dropdown.style.display = 'none';
      input.blur();
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initNavSearch();
  initFilterSearch();
});
