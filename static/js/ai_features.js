/* ═══════════════════════════════════════════════════════════════
   ai_features.js — Client-side AI: Duplicate Detection,
   Auto-tagging, Recovery Probability, Smart Summary, Sentiment
   ═══════════════════════════════════════════════════════════════ */

// ── Levenshtein Distance ──────────────────────────────────────
function levenshtein(a, b) {
  a = a.toLowerCase(); b = b.toLowerCase();
  const m = a.length, n = b.length;
  const dp = Array.from({length:m+1}, (_,i) => Array.from({length:n+1}, (_,j) => i===0?j:j===0?i:0));
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = a[i-1] === b[j-1]
        ? dp[i-1][j-1]
        : 1 + Math.min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]);
    }
  }
  return dp[m][n];
}

function similarity(a, b) {
  if (!a || !b) return 0;
  const maxLen = Math.max(a.length, b.length);
  if (maxLen === 0) return 1;
  return 1 - levenshtein(a, b) / maxLen;
}

// ── AI Duplicate Detection ────────────────────────────────────
const DUPLICATE_THRESHOLD = 0.72;

async function checkDuplicates(description, category, location) {
  try {
    const res   = await fetch('/api/items');
    const items = await res.json();
    const dupes = items.filter(item => {
      const descSim = similarity(description, item.description);
      const catMatch = category && item.category && category === item.category;
      const locSim  = similarity(location, item.location);
      return descSim > DUPLICATE_THRESHOLD || (catMatch && locSim > 0.6 && descSim > 0.5);
    }).slice(0, 3);
    return dupes;
  } catch (e) { return []; }
}

// ── Auto-Tagging ──────────────────────────────────────────────
const STOP_WORDS = new Set([
  'a','an','the','and','or','but','in','on','at','to','for','of','with',
  'is','are','was','were','i','my','it','this','that','its','found','lost',
  'near','by','from','have','has','been','be','their','they','some','not',
  'also','but','can','will','had','did','do','does','get','got','she','he',
  'we','you','your','our','his','her','they','them','who','which','what'
]);

const CATEGORY_KEYWORDS = {
  'Electronics':  ['phone','mobile','laptop','tablet','earphones','charger','camera','watch','smartwatch','headphones','earbuds','cable','power','bank','keyboard','mouse'],
  'Wallet':       ['wallet','purse','bag','card','cash','money','holder','billfold','pocket'],
  'ID Cards':     ['id','card','identity','license','pass','student','employee','aadhar','pan','voter'],
  'Keys':         ['key','keys','keychain','lock','remote'],
  'Books':        ['book','notebook','textbook','notes','diary','pen','pencil','stationery'],
  'Clothing':     ['jacket','shirt','sweater','cap','hat','shoes','belt','scarf','gloves','bag','backpack'],
  'Jewellery':    ['ring','chain','necklace','bracelet','earring','bangle','locket','gold','silver'],
  'Documents':    ['document','certificate','passport','file','paper','report','mark','sheet'],
  'Glasses':      ['glasses','spectacles','specs','sunglasses','lens'],
  'Umbrella':     ['umbrella','umbrella','rain'],
  'Food':         ['lunch','tiffin','box','bottle','flask','container'],
};

function autoTag(itemName, description) {
  const text = `${itemName} ${description}`.toLowerCase();
  const words = text.split(/\W+/).filter(w => w.length > 2 && !STOP_WORDS.has(w));
  const tagSet = new Set();

  // Add unique words
  words.forEach(w => { if (w.length > 3) tagSet.add(w); });

  // Category-based tags
  for (const [cat, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
    if (keywords.some(k => text.includes(k))) {
      tagSet.add(cat.toLowerCase());
    }
  }

  // Color detection
  ['black','white','red','blue','green','yellow','brown','grey','gray','silver','gold','pink','purple','orange'].forEach(c => {
    if (text.includes(c)) tagSet.add(c);
  });

  // Material detection
  ['leather','plastic','metal','fabric','cotton','glass','wood','rubber','silk'].forEach(m => {
    if (text.includes(m)) tagSet.add(m);
  });

  return [...tagSet].slice(0, 8);
}

// ── Recovery Probability ──────────────────────────────────────
const CATEGORY_BASE_PROB = {
  'Electronics':  0.55,
  'Wallet':       0.65,
  'ID Cards':     0.75,
  'Keys':         0.70,
  'Books':        0.60,
  'Clothing':     0.45,
  'Jewellery':    0.50,
  'Documents':    0.70,
  'Glasses':      0.55,
  'Umbrella':     0.40,
  'Food':         0.30,
  'Other':        0.50,
};

const LOCATION_BONUS = {
  'library':        0.10,
  'canteen':        0.05,
  'classroom':      0.10,
  'lab':            0.08,
  'office':         0.12,
  'hostel':         0.07,
  'playground':     0.02,
  'parking':        0.03,
  'gate':           0.05,
  'reception':      0.12,
};

function calcRecoveryProb(category, location, daysAgo = 0) {
  let prob = CATEGORY_BASE_PROB[category] || 0.50;

  // Location bonus
  const loc = (location || '').toLowerCase();
  for (const [loc_key, bonus] of Object.entries(LOCATION_BONUS)) {
    if (loc.includes(loc_key)) { prob += bonus; break; }
  }

  // Time penalty
  if (daysAgo <= 1)       prob *= 1.0;
  else if (daysAgo <= 3)  prob *= 0.92;
  else if (daysAgo <= 7)  prob *= 0.82;
  else if (daysAgo <= 14) prob *= 0.68;
  else if (daysAgo <= 30) prob *= 0.52;
  else                    prob *= 0.35;

  // Clamp
  prob = Math.max(0.05, Math.min(0.97, prob));
  return Math.round(prob * 100);
}

function updateProbMeter(percent) {
  const valueEl = document.getElementById('probValue');
  const fillEl  = document.getElementById('probFill');
  const labelEl = document.getElementById('probLabel');
  if (!valueEl) return;

  valueEl.textContent = `${percent}%`;
  fillEl.style.width  = `${percent}%`;

  // Color fill
  if (percent >= 70) {
    fillEl.style.background = 'linear-gradient(90deg,#10b981,#059669)';
    if (labelEl) labelEl.textContent = 'High chance of recovery!';
  } else if (percent >= 45) {
    fillEl.style.background = 'linear-gradient(90deg,#f59e0b,#d97706)';
    if (labelEl) labelEl.textContent = 'Moderate recovery chance';
  } else {
    fillEl.style.background = 'linear-gradient(90deg,#ef4444,#dc2626)';
    if (labelEl) labelEl.textContent = 'Low recovery probability';
  }
}

// ── AI Summary Generator ──────────────────────────────────────
function generateSummary(itemName, description, category, location, type) {
  const action = type === 'Lost' ? 'lost' : 'found';
  const place  = location ? `near ${location}` : 'on campus';
  const cat    = category && category !== 'Other' ? ` (${category})` : '';
  const name   = itemName || description.split(' ').slice(0, 4).join(' ');

  const templates = [
    `${name}${cat} ${action} ${place}. ${description.slice(0, 80)}${description.length > 80 ? '…' : ''}`,
    `A ${name.toLowerCase()}${cat} was ${action} ${place}. ${description.slice(0, 60)}${description.length > 60 ? '…' : ''}`,
    `${type}: ${name}${cat} — found ${place}. Contact for details.`,
  ];
  return templates[Math.floor(Math.random() * templates.length)];
}

// ── Sentiment / Spam Detection ────────────────────────────────
const SPAM_KEYWORDS = ['buy','sell','offer','discount','click','link','http','www','deal','promo','free money','make money'];
const FRAUD_KEYWORDS = ['police','complaint','legal','lawsuit','sue','reward money','ransom','pay me'];

function detectSentiment(text) {
  const lower = text.toLowerCase();
  const spamScore   = SPAM_KEYWORDS.filter(k => lower.includes(k)).length;
  const fraudScore  = FRAUD_KEYWORDS.filter(k => lower.includes(k)).length;
  if (fraudScore >= 2)  return { type:'danger',  msg:'⚠️ Suspicious content detected — possible fraud.' };
  if (spamScore  >= 2)  return { type:'warning', msg:'⚠️ This description looks like spam.' };
  return null;
}

// ── Form Integration ──────────────────────────────────────────
async function handleFormAI(formEl, type) {
  const itemName   = formEl.querySelector('[name="item_name"]')?.value || '';
  const description= formEl.querySelector('[name="description"]')?.value || '';
  const location   = formEl.querySelector('[name="location"]')?.value || '';
  const category   = formEl.querySelector('[name="category"]')?.value || 'Other';

  // Sentiment check
  const sentiment = detectSentiment(`${itemName} ${description}`);
  if (sentiment) {
    showToast('Content Check', sentiment.msg, sentiment.type, 6000);
    if (sentiment.type === 'danger') return false; // block submission
  }

  // Generate and display tags
  const tags = autoTag(itemName, description);
  const tagsInput = formEl.querySelector('[name="tags"]');
  if (tagsInput) tagsInput.value = tags.join(',');
  displayTags(tags);

  // Duplicate check
  const dupes = await checkDuplicates(description, category, location);
  if (dupes.length > 0) {
    showDuplicateModal(dupes, formEl);
    return false; // pause form until user confirms
  }

  // Recovery probability (for lost items)
  if (type === 'Lost') {
    const prob = calcRecoveryProb(category, location, 0);
    updateProbMeter(prob);
    showToast('Recovery Probability', `Estimated recovery chance: ${prob}%`,
      prob >= 70 ? 'success' : prob >= 45 ? 'warning' : 'danger', 5000);
  }

  return true;
}

function displayTags(tags) {
  const container = document.getElementById('tagPreview');
  if (!container || tags.length === 0) return;
  container.innerHTML = `
    <div class="fs-12 text-muted-c mb-16" style="margin-bottom:6px">
      <i class="fas fa-tags" style="color:var(--primary-light)"></i> Auto-generated tags:
    </div>
    <div class="tags-list">
      ${tags.map(t => `<span class="tag tag-primary">${t}</span>`).join('')}
    </div>
  `;
  container.style.display = 'block';
}

function showDuplicateModal(dupes, formEl) {
  const modal = document.getElementById('duplicateModal');
  if (!modal) { formEl.submit(); return; }

  const list = document.getElementById('dupeList');
  if (list) {
    list.innerHTML = dupes.map(d => `
      <div style="padding:8px 0; border-bottom:1px solid var(--border); font-size:13px">
        <span class="tag ${d.type==='Lost'?'tag-danger':'tag-success'}" style="margin-right:6px">${d.type}</span>
        <strong>${d.item_name || 'Item'}</strong>
        <span style="color:var(--text-muted); margin-left:6px">— ${(d.description||'').slice(0,50)}…</span>
        <a href="/item/${d.id}" target="_blank" style="margin-left:8px; font-size:11px">View →</a>
      </div>
    `).join('');
  }

  modal.classList.add('active');

  document.getElementById('dupeConfirm')?.addEventListener('click', () => {
    modal.classList.remove('active');
    formEl.submit();
  }, {once: true});

  document.getElementById('dupeCancel')?.addEventListener('click', () => {
    modal.classList.remove('active');
  }, {once: true});
}

// ── Live probability update on input change ───────────────────
function bindProbabilityUpdates() {
  const catSel = document.querySelector('[name="category"]');
  const locIn  = document.querySelector('[name="location"]');
  const updateProb = () => {
    const cat = catSel?.value || 'Other';
    const loc = locIn?.value  || '';
    const prob = calcRecoveryProb(cat, loc, 0);
    updateProbMeter(prob);
  };
  catSel?.addEventListener('change', updateProb);
  locIn?.addEventListener('input',   updateProb);
  updateProb();
}

document.addEventListener('DOMContentLoaded', () => {
  bindProbabilityUpdates();
});
