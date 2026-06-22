const API_URL = `${window.location.origin}/api/check`;
const IDENTITY_API_URL = `${window.location.origin}/api/products/identity-check`;

let selectedFiles = { barcode: null, screenshot: null };
let currentAnalysisMethod = 'text';

function initializeEventHandlers() {
  // View switching (logo, brand name, back button)
  document.querySelectorAll('[data-view]').forEach(el => {
    el.addEventListener('click', e => {
      e.preventDefault();
      const view = el.dataset.view;
      if (view === 'results') {
        showResults();
      } else {
        const homePage = document.getElementById('home-page');
        const isAlreadyHome = homePage && homePage.classList.contains('active');
        showHome();
        if (isAlreadyHome) {
          const mainInput = document.getElementById('input-main-val');
          if (mainInput) {
            mainInput.value = '';
            mainInput.placeholder = "Tempel tautan produk, nama klinik, atau komposisi bahan...";
            mainInput.focus();
          }
          const statusEl = document.getElementById('status-main');
          if (statusEl) statusEl.innerText = '';
          const resultCard = document.getElementById('identity-result');
          if (resultCard) resultCard.hidden = true;
        }
      }
    });
  });

  // Mobile Menu Drawer Triggers
  const btnOpenMenu = document.getElementById('btn-open-mobile-menu');
  const btnCloseMenu = document.getElementById('btn-close-mobile-menu');
  const mobileMenu = document.getElementById('mobile-menu');

  if (btnOpenMenu && mobileMenu) {
    btnOpenMenu.addEventListener('click', () => {
      mobileMenu.classList.remove('translate-x-full');
      mobileMenu.classList.add('translate-x-0');
    });
  }

  if (btnCloseMenu && mobileMenu) {
    btnCloseMenu.addEventListener('click', () => {
      mobileMenu.classList.remove('translate-x-0');
      mobileMenu.classList.add('translate-x-full');
    });
  }

  // Close mobile menu on clicking any link
  if (mobileMenu) {
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('translate-x-0');
        mobileMenu.classList.add('translate-x-full');
      });
    });
  }

  // Handle smooth scroll for page sections, switching to home page if necessary
  const navLinks = document.querySelectorAll('nav.waras-nav div.hidden a');
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    const targetId = anchor.getAttribute('href');
    if (targetId === '#' || !targetId.startsWith('#')) return;
    
    anchor.addEventListener('click', e => {
      e.preventDefault();
      showHome(); // Ensure home page is active first
      
      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        // Wait a small bit for layout to settle in case view just switched
        setTimeout(() => {
          targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 50);
      }
    });
  });

  // Intersection Observer for auto-updating active navbar links on scroll
  if (typeof IntersectionObserver !== 'undefined') {
    const observerOptions = {
      root: null,
      rootMargin: '-20% 0px -60% 0px',
      threshold: 0
    };

    const observer = new IntersectionObserver(entries => {
      // Only process observer if home page is active
      const homePage = document.getElementById('home-page');
      if (!homePage || !homePage.classList.contains('active')) return;

      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          const correspondingLink = document.querySelector(`nav.waras-nav div.hidden a[href="#${id}"]`);
          
          if (correspondingLink) {
            navLinks.forEach(link => {
              link.className = "text-on-surface-variant hover:text-primary transition-colors font-label-md text-label-md uppercase";
            });
            correspondingLink.className = "text-primary font-bold border-b-2 border-primary pb-1 font-label-md text-label-md uppercase";
          } else if (id === 'home-page') {
            // Check if we are scrolled near the top/hero, then highlight "Cek Keamanan"
            const scrollY = window.scrollY;
            if (scrollY < 300) {
              navLinks.forEach(link => {
                link.className = "text-on-surface-variant hover:text-primary transition-colors font-label-md text-label-md uppercase";
              });
              const checkLink = document.querySelector('nav.waras-nav div.hidden a[data-view="home"]');
              if (checkLink) {
                checkLink.className = "text-primary font-bold border-b-2 border-primary pb-1 font-label-md text-label-md uppercase";
              }
            }
          }
        }
      });
    }, observerOptions);

    const sectionsToObserve = [
      document.getElementById('how-it-works'),
      document.getElementById('what-we-check'),
      document.getElementById('home-page')
    ];
    sectionsToObserve.forEach(sec => {
      if (sec) observer.observe(sec);
    });

    // Also update on manual scroll top
    window.addEventListener('scroll', () => {
      const homePage = document.getElementById('home-page');
      if (homePage && homePage.classList.contains('active') && window.scrollY < 100) {
        navLinks.forEach(link => {
          link.className = "text-on-surface-variant hover:text-primary transition-colors font-label-md text-label-md uppercase";
        });
        const checkLink = document.querySelector('nav.waras-nav div.hidden a[data-view="home"]');
        if (checkLink) {
          checkLink.className = "text-primary font-bold border-b-2 border-primary pb-1 font-label-md text-label-md uppercase";
        }
      }
    });
  }

  // Action Buttons underneath search
  const btnActionLink = document.getElementById('btn-action-link');
  const btnActionBarcode = document.getElementById('btn-action-barcode');
  const btnActionImage = document.getElementById('btn-action-image');
  const mainInput = document.getElementById('input-main-val');

  if (btnActionLink && mainInput) {
    btnActionLink.addEventListener('click', () => {
      showDevelopmentPopup();
    });
  }

  if (btnActionBarcode) {
    btnActionBarcode.addEventListener('click', () => {
      const fileInput = document.getElementById('input-barcode-file');
      if (fileInput) fileInput.click();
    });
  }

  if (btnActionImage) {
    btnActionImage.addEventListener('click', () => {
      const fileInput = document.getElementById('input-screenshot-file');
      if (fileInput) fileInput.click();
    });
  }

  // File Inputs
  const barcodeFileInput = document.getElementById('input-barcode-file');
  if (barcodeFileInput) {
    barcodeFileInput.addEventListener('change', () => {
      if (barcodeFileInput.files && barcodeFileInput.files[0]) {
        handleFileSelect('barcode', barcodeFileInput.files[0]);
      }
    });
  }

  const screenshotFileInput = document.getElementById('input-screenshot-file');
  if (screenshotFileInput) {
    screenshotFileInput.addEventListener('change', () => {
      if (screenshotFileInput.files && screenshotFileInput.files[0]) {
        handleFileSelect('screenshot', screenshotFileInput.files[0]);
      }
    });
  }

  // Analyze Button click & Enter key
  const btnAnalyze = document.getElementById('btn-main-analyze');
  if (btnAnalyze) {
    btnAnalyze.addEventListener('click', () => analyzeMainInput());
  }

  if (mainInput) {
    mainInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        analyzeMainInput();
      }
    });
  }

  // Demo buttons
  const demoBpomBtn = document.getElementById('demo-bpom');
  const demoOverclaimBtn = document.getElementById('demo-overclaim');
  const demoShopeeBtn = document.getElementById('demo-shopee');

  if (demoBpomBtn) {
    demoBpomBtn.addEventListener('click', () => runDemo('bpom'));
  }
  if (demoOverclaimBtn) {
    demoOverclaimBtn.addEventListener('click', () => runDemo('overclaim'));
  }
  if (demoShopeeBtn) {
    demoShopeeBtn.addEventListener('click', () => runDemo('shopee'));
  }

  // Tour guide triggers
  const btnStartTour = document.getElementById('btn-start-tour');
  const btnStartTourMobile = document.getElementById('btn-start-tour-mobile');
  const btnStartResultTour = document.getElementById('btn-start-result-tour');

  if (btnStartTour) {
    btnStartTour.addEventListener('click', () => startTour('home'));
  }
  if (btnStartTourMobile) {
    btnStartTourMobile.addEventListener('click', () => {
      const mobileMenu = document.getElementById('mobile-menu');
      if (mobileMenu) {
        mobileMenu.classList.remove('translate-x-0');
        mobileMenu.classList.add('translate-x-full');
      }
      startTour('home');
    });
  }
  if (btnStartResultTour) {
    btnStartResultTour.addEventListener('click', () => startTour('result'));
  }

  // Auto-start panduan interaktif saat pertama kali user mengakses website di sesi baru
  const hasSeenTour = sessionStorage.getItem('hasSeenOnboardingTour');
  if (!hasSeenTour) {
    setTimeout(() => {
      startTour('home');
      // Tandai agar tidak muncul terus-menerus di halaman refresh tab yang sama
      sessionStorage.setItem('hasSeenOnboardingTour', 'true');
    }, 1000); // Jeda 1 detik agar transisi loading awal halaman selesai dengan mulus
  }
}

// Handler for file selection
function handleFileSelect(method, file) {
  selectedFiles[method] = file;
  const statusEl = document.getElementById('status-main');
  if (statusEl) {
    statusEl.innerText = `File terpilih: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    statusEl.className = 'status-message mt-4 text-center text-sm is-success text-primary';
  }

  // Trigger check immediately
  checkProductFile(method, file);
}

// Smart auto-detection for text input
function analyzeMainInput() {
  // If user triggers manually, reset the isDemoActive flag
  window.isDemoActive = false;

  const mainInput = document.getElementById('input-main-val');
  if (!mainInput) return;

  const val = mainInput.value.trim();
  const statusEl = document.getElementById('status-main');
  const resultCard = document.getElementById('identity-result');

  if (statusEl) {
    statusEl.innerText = '';
    statusEl.className = 'status-message mt-4 text-center text-sm';
  }
  if (resultCard) {
    resultCard.hidden = true;
  }

  if (!val) {
    if (statusEl) {
      statusEl.innerText = 'Masukkan input terlebih dahulu (Tautan, Teks Klaim, atau nama produk).';
      statusEl.className = 'status-message mt-4 text-center text-sm is-error text-error';
    }
    return;
  }

  // Regex to check if it's a URL
  const isUrl = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/.test(val);

  if (isUrl) {
    checkProductLink(val);
  } else {
    // Check if it's a BPOM registration number (e.g. POM TR123456789, NA18200100001, etc.)
    const bpomRegex = /^(POM\s+)?(TR|QD|QI|SD|SI|SL|NA|NB|NC|ND|NE|DKL|DKP|DKS|GKL|GKP|GKS)\s*\d{7,11}[A-Z\d]*$/i;
    const isBpom = bpomRegex.test(val);

    // Heuristics for claims: common Indonesian verbs/adjectives/nouns indicating medical claims or diseases
    const claimIndicatorRegex = /\b(sembuh|menyembuhkan|penyembuhan|sembuhin|mengobati|pengobatan|obatin|mencegah|pencegahan|meredakan|peredaan|redain|mengatasi|ampuh|mujarab|manjur|khasiat|manfaat|aman|seketika|instan|permanen|absolut|terbukti|kanker|stroke|diabetes|kencing manis|tumor|jantung|ginjal|katarak|lumpuh|menurunkan|menaikkan|menghilangkan|mematikan|membunuh|bebas|alami)\b/i;
    const isClaim = val.length >= 35 || claimIndicatorRegex.test(val);

    if (isBpom || (!isClaim && val.length < 35)) {
      // Small query without claim keywords or a BPOM code: run identity verification
      checkProductIdentity(val);
    } else {
      // Longer paragraph or a query containing claim keywords: run claim analysis
      checkProductText(val);
    }
  }
}

// 1. Check Product Link (marketplace link)
async function checkProductLink(urlVal) {
  showDevelopmentPopup();
}

async function checkProductLinkDisabled(urlVal) {
  currentAnalysisMethod = 'link';
  showLoading('Sedang membaca informasi produk...');

  let payload = new FormData();
  payload.append('type', 'link');
  payload.append('url', urlVal);

  try {
    const response = await fetch(API_URL, { method: 'POST', body: payload });
    if (!response.ok) throw new Error('Gagal menghubungi server.');
    const result = await response.json();
    if (result.status === 'success') {
      displayResults(result);
    } else {
      showStatusMsg('status-main', 'Error: ' + result.message, true);
    }
  } catch (err) {
    console.error(err);
    showStatusMsg('status-main', 'Gagal menghubungkan ke backend. Pastikan server Flask berjalan di http://localhost:5000', true);
  } finally {
    hideLoading();
  }
}

// 2. Check Product File (barcode or screenshot)
async function checkProductFile(method, file) {
  currentAnalysisMethod = method;
  showLoading(method === 'barcode' ? 'Sedang membaca barcode produk...' : 'Sedang membaca teks pada gambar...');

  let payload = new FormData();
  payload.append('type', method);
  payload.append('image', file);

  try {
    const response = await fetch(API_URL, { method: 'POST', body: payload });
    if (!response.ok) throw new Error('Gagal menghubungi server.');
    const result = await response.json();
    if (result.status === 'success') {
      displayResults(result);
    } else {
      showStatusMsg('status-main', 'Error: ' + result.message, true);
    }
  } catch (err) {
    console.error(err);
    showStatusMsg('status-main', 'Gagal menghubungkan ke backend. Pastikan server Flask berjalan di http://localhost:5000', true);
  } finally {
    hideLoading();
  }
}

// 3. Check Product Text (claim paragraph)
async function checkProductText(textVal) {
  currentAnalysisMethod = 'text';
  showLoading('Sedang menganalisis klaim...');

  let payload = new FormData();
  payload.append('type', 'text');
  payload.append('text', textVal);

  try {
    const response = await fetch(API_URL, { method: 'POST', body: payload });
    if (!response.ok) throw new Error('Gagal menghubungi server.');
    const result = await response.json();
    if (result.status === 'success') {
      displayResults(result);
    } else {
      showStatusMsg('status-main', 'Error: ' + result.message, true);
    }
  } catch (err) {
    console.error(err);
    showStatusMsg('status-main', 'Gagal menghubungkan ke backend. Pastikan server Flask berjalan di http://localhost:5000', true);
  } finally {
    hideLoading();
  }
}

// 4. Check Product Identity (BPOM / name lookup)
async function checkProductIdentity(queryVal) {
  showLoading('Sedang memeriksa identitas produk...');
  const resultCard = document.getElementById('identity-result');
  if (resultCard) resultCard.hidden = true;

  try {
    const response = await fetch(IDENTITY_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: queryVal })
    });
    if (!response.ok) throw new Error('Server error');
    const data = await response.json();
    displayIdentityResult(data);
  } catch (err) {
    console.error(err);
    showStatusMsg('status-main', 'Data identitas belum dapat diperiksa. Layanan sumber data sedang tidak tersedia.', true);
  } finally {
    hideLoading();
  }
}

// Helper to update status message
function showStatusMsg(id, msg, isError) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = msg;
  el.className = 'status-message mt-4 text-center text-sm ' + (isError ? 'text-error is-error' : 'text-primary is-success');
}

// Switch between Home and Results
function showHome() {
  document.getElementById('home-page').classList.add('active');
  document.getElementById('results-page').classList.remove('active');
}

function showResults() {
  document.getElementById('home-page').classList.remove('active');
  document.getElementById('results-page').classList.add('active');
  window.scrollTo(0, 0);
}

// Loading overlay helpers
function showLoading(text) {
  const overlay = document.getElementById('loading-overlay');
  const loadingText = document.getElementById('loading-text');
  if (loadingText) loadingText.innerText = text;
  if (overlay) {
    overlay.style.display = 'flex';
    overlay.setAttribute('aria-hidden', 'false');
  }
}

function hideLoading() {
  const overlay = document.getElementById('loading-overlay');
  if (overlay) {
    overlay.style.display = 'none';
    overlay.setAttribute('aria-hidden', 'true');
  }
}

// Display Identity Result in Card
function displayIdentityResult(data) {
  const container = document.getElementById('identity-result');
  const header = document.getElementById('identity-result-header');
  const body = document.getElementById('identity-result-body');
  const footer = document.getElementById('identity-result-footer');

  if (!container || !header || !body || !footer) return;

  container.hidden = false;

  if (data.status === 'found') {
    const p = data.product;
    header.innerHTML = `<div class="identity-status is-found">✓ Produk ditemukan</div>`;
    body.innerHTML = `<table>
      <tr><td>Nama produk</td><td>${p.product_name || '-'}</td></tr>
      <tr><td>Nomor registrasi</td><td>${p.registration_number || '-'}</td></tr>
      <tr><td>Kategori produk</td><td>${p.product_category || '-'}</td></tr>
      <tr><td>Produsen</td><td>${p.manufacturer || '-'}</td></tr>
      <tr><td>Bahan aktif</td><td>${p.ingredient || '-'}</td></tr>
      <tr><td>Status kecocokan</td><td><span class="identity-match-status ${data.match === 'full' ? 'match-full' : 'match-partial'}">${data.match === 'full' ? 'Sesuai' : 'Cocok sebagian'}</span></td></tr>
    </table>`;
    footer.innerHTML = `<p class="text-xs text-on-surface-variant mt-2">Produk terdaftar di database BPOM. Ingin memeriksa kebenaran klaim iklannya?</p>
      <button class="bg-primary text-on-primary px-5 py-2 rounded-full text-xs font-semibold mt-3 hover:bg-primary/90 transition-colors" type="button" id="btn-identity-to-claim">Periksa klaim produk ini</button>`;
    
    setTimeout(() => {
      const btn = document.getElementById('btn-identity-to-claim');
      if (btn) {
        btn.addEventListener('click', () => {
          checkProductText(p.product_name);
        });
      }
    }, 50);
  } else if (data.status === 'partial') {
    const p = data.product;
    header.innerHTML = `<div class="identity-status is-partial">⚠ Cocok Sebagian</div>`;
    body.innerHTML = `<p class="text-xs text-on-surface-variant">Nomor registrasi cocok, namun nama atau produsen yang diinput berbeda. Detail database:</p>
      <table>
        <tr><td>Nama produk</td><td>${p.product_name || '-'}</td></tr>
        <tr><td>Nomor registrasi</td><td>${p.registration_number || '-'}</td></tr>
        <tr><td>Produsen</td><td>${p.manufacturer || '-'}</td></tr>
      </table>`;
    footer.innerHTML = `<p class="text-xs text-on-surface-variant mt-2">Pastikan ejaan dan nomor registrasi sesuai kemasan asli.</p>`;
  } else {
    header.innerHTML = `<div class="identity-status is-not-found">✗ Produk Tidak Ditemukan</div>`;
    body.innerHTML = `<p class="text-sm text-on-surface-variant">Nomor registrasi atau nama produk tidak ditemukan dalam database BPOM WARAS.ID.</p>`;
    footer.innerHTML = `<p class="text-xs text-on-surface-variant mt-2">Coba masukkan ejaan lain, atau gunakan fitur foto barcode jika tersedia.</p>`;
  }
}

// Display Claim Analysis Results
function displayResults(result) {
  const safety = result.consumer_safety_score || { final_score: 50 };
  const score = safety.final_score;
  const vDetails = result.verdict_details || {};

  let statusText = 'RISIKO SEDANG', statusColor = '#9a5b00';
  if (score >= 81) { statusText = 'RISIKO RENDAH'; statusColor = '#168464'; }
  else if (score < 31) { statusText = 'RISIKO TINGGI'; statusColor = '#b3261e'; }

  const statusTag = document.getElementById('result-status-tag');
  if (statusTag) {
    statusTag.innerText = statusText;
    statusTag.style.color = statusColor;
  }

  const titleEl = document.getElementById('result-product-title');
  if (titleEl) titleEl.innerText = vDetails.product_name || "Hasil Pemeriksaan Produk";

  const scoreEl = document.getElementById('result-verdict-score');
  if (scoreEl) scoreEl.innerText = `${score} / 100`;

  // Update Safety Meter SVG dynamically
  const needle = document.getElementById('safety-meter-needle');
  const meterFill = document.getElementById('safety-meter-fill');
  if (needle && meterFill) {
    // angle goes from 180 (for score 0) to 0 (for score 100)
    const angle = 180 - (score * 1.8);
    const rad = angle * Math.PI / 180;
    
    // needle length is 35
    const nx = 50 + 35 * Math.cos(rad);
    const ny = 50 - 35 * Math.sin(rad);
    needle.setAttribute('x2', nx.toFixed(2));
    needle.setAttribute('y2', ny.toFixed(2));
    needle.style.color = statusColor;
    
    // fill path length is 40
    const fx = 50 + 40 * Math.cos(rad);
    const fy = 50 - 40 * Math.sin(rad);
    meterFill.setAttribute('d', `M 10 50 A 40 40 0 0 1 ${fx.toFixed(2)} ${fy.toFixed(2)}`);
    meterFill.style.color = statusColor;
  }

  // Reasons list
  const reasonsC = document.getElementById('result-score-reasons-list');
  if (reasonsC) {
    reasonsC.innerHTML = '';
    if (safety.reasons && safety.reasons.length > 0) {
      const ul = document.createElement('ul');
      ul.className = 'space-y-sm';
      safety.reasons.slice(0, 5).forEach(r => {
        const li = document.createElement('li');
        li.className = 'flex items-start gap-xs';
        
        let icon = 'check_circle';
        let iconClass = 'text-primary';
        let textClass = 'text-on-surface';
        
        if (r.icon === 'close' || r.icon === 'error' || r.icon === 'warning') {
          icon = 'cancel';
          iconClass = 'text-error';
          textClass = 'text-on-surface';
        } else if (r.icon === 'info') {
          icon = 'info';
          iconClass = 'text-outline';
          textClass = 'text-on-surface-variant';
        }
        
        li.innerHTML = `
          <span class="material-symbols-outlined ${iconClass} text-xl flex-shrink-0">${icon}</span>
          <span class="font-body-md text-body-md ${textClass}">${r.text}</span>
        `;
        ul.appendChild(li);
      });
      reasonsC.appendChild(ul);
    } else {
      reasonsC.innerHTML = `<div class="empty-note">Tidak ada detail alasan.</div>`;
    }
  }

  // Evidence list
  const claim = result.claim_analysis || {};
  const evidenceC = document.getElementById('result-evidence-container');
  if (evidenceC) {
    evidenceC.innerHTML = '';
    let sourceText = 'Teks Input';
    if (currentAnalysisMethod === 'screenshot') sourceText = 'Gambar Iklan';
    else if (currentAnalysisMethod === 'barcode') sourceText = 'Barcode Kemasan';
    else if (currentAnalysisMethod === 'link') sourceText = 'Link Deskripsi Marketplace';

    if (claim.trigger_sentences && claim.trigger_sentences.length > 0) {
      claim.trigger_sentences.forEach(s => {
        const d = document.createElement('div');
        d.className = 'bg-surface-variant rounded-xl p-md border-l-4 border-primary mb-4';
        d.innerHTML = `
          <h3 class="font-label-md text-label-md text-on-surface-variant uppercase mb-2">Teks Promosi Terdeteksi</h3>
          <blockquote class="font-body-lg text-body-lg text-on-surface italic mb-4">
            "${s}"
          </blockquote>
          <div class="font-caption text-caption text-on-surface-variant mb-2">Sumber: <span class="font-bold text-primary">${sourceText}</span></div>
          <div class="mt-md pt-md border-t border-outline-variant">
            <h3 class="font-label-md text-label-md text-on-surface-variant uppercase mb-2">Analisis Medis WARAS.ID</h3>
            <p class="font-body-md text-body-md text-on-surface">
              Sistem mendeteksi klaim ini sebagai klaim yang berlebihan atau membutuhkan pembuktian klinis lebih lanjut berdasarkan database literatur ilmiah WARAS.ID.
            </p>
          </div>
        `;
        evidenceC.appendChild(d);
      });
    } else if (claim.trigger_words && claim.trigger_words.length > 0) {
      const d = document.createElement('div');
      d.className = 'bg-surface-variant rounded-xl p-md border-l-4 border-primary mb-4';
      d.innerHTML = `
        <h3 class="font-label-md text-label-md text-on-surface-variant uppercase mb-2">Kata Kunci Klaim Terdeteksi</h3>
        <blockquote class="font-body-lg text-body-lg text-on-surface italic mb-4">
          "${claim.trigger_words.join(', ')}"
        </blockquote>
        <div class="font-caption text-caption text-on-surface-variant mb-2">Sumber: <span class="font-bold text-primary">${sourceText}</span></div>
        <div class="mt-md pt-md border-t border-outline-variant">
          <h3 class="font-label-md text-label-md text-on-surface-variant uppercase mb-2">Analisis Medis WARAS.ID</h3>
          <p class="font-body-md text-body-md text-on-surface">
            Terdapat beberapa kata sensitif yang berpotensi melebih-lebihkan khasiat produk di atas standar medis.
          </p>
        </div>
      `;
      evidenceC.appendChild(d);
    } else {
      evidenceC.innerHTML = `<div class="bg-surface-container p-md rounded-xl text-center font-body-md text-on-surface-variant">Tidak ditemukan klaim berlebihan yang signifikan dari teks/gambar.</div>`;
    }
  }

  // Product Profile table
  const profile = result.product_profile;
  const profileFields = {
    'prof-name': profile ? profile.product_name : null,
    'prof-reg': profile ? profile.registration_number : null,
    'prof-bpom-interpretation': profile ? profile.bpom_interpretation : null,
    'prof-mfr': profile ? profile.manufacturer : null,
    'prof-cat': profile ? profile.product_category : null,
    'prof-golongan': profile ? profile.therapeutic_group : null,
    'prof-atc': profile ? profile.atc_code : null,
    'prof-ingredient': profile ? profile.ingredient : null
  };

  for (const [id, value] of Object.entries(profileFields)) {
    const el = document.getElementById(id);
    if (el) el.innerText = value || "-";
  }

  // Layman / Drug Category indications
  const drugFunc = result.drug_function || { layman_category: "Kategori Terapi Umum", indications: [] };
  const laymanCatEl = document.getElementById('layman-cat');
  if (laymanCatEl) laymanCatEl.innerText = drugFunc.layman_category;

  const laymanList = document.getElementById('layman-indications-list');
  if (laymanList) {
    laymanList.innerHTML = '';
    if (drugFunc.indications && drugFunc.indications.length > 0) {
      drugFunc.indications.forEach(ind => {
        const li = document.createElement('li');
        li.innerText = ind;
        laymanList.appendChild(li);
      });
    } else {
      const li = document.createElement('li');
      li.innerText = "Digunakan sesuai petunjuk dokter atau indikasi umum pada kemasan produk.";
      laymanList.appendChild(li);
    }
  }

  // WHO ATC standard dosage (DDD)
  const ddd = result.ddd_dosage || {};
  const dddValEl = document.getElementById('ddd-val');
  if (dddValEl) dddValEl.innerText = ddd.ddd || "-";

  const dddUomEl = document.getElementById('ddd-uom');
  if (dddUomEl) dddUomEl.innerText = ddd.uom || "";

  const dddRouteEl = document.getElementById('ddd-route-std');
  if (dddRouteEl) dddRouteEl.innerText = ddd.administration_route || "-";

  const dddMediaEl = document.getElementById('ddd-media-penggunaan');
  if (dddMediaEl) dddMediaEl.innerText = ddd.media_penggunaan || "-";

  const dddDiscEl = document.getElementById('ddd-disclaimer');
  if (dddDiscEl) dddDiscEl.innerText = ddd.disclaimer || "";

  // OpenFDA adverse events
  const fda = result.openfda_safety_insight || {};
  const ingredientEl = document.getElementById('ae-ingredient-queried');
  if (ingredientEl) ingredientEl.innerText = fda.ingredient_queried || "-";

  const reactionsC = document.getElementById('ae-reactions-list');
  if (reactionsC) {
    reactionsC.innerHTML = '';
    if (fda.side_effects && fda.side_effects.length > 0) {
      fda.side_effects.forEach(item => {
        const li = document.createElement('li');
        li.className = 'bg-error-container text-on-error-container px-4 py-2 rounded-lg font-body-md text-body-md flex items-center gap-2';
        let term = item.term.toUpperCase();
        const translations = {
          'FATIGUE': 'Kelelahan (Fatigue)', 'NAUSEA': 'Mual (Nausea)', 'DIARRHOEA': 'Diare (Diarrhoea)',
          'DIARRHEA': 'Diare (Diarrhea)', 'HEADACHE': 'Sakit Kepala (Headache)', 'DIZZINESS': 'Pusing (Dizziness)',
          'DRUG INEFFECTIVE': 'Obat Tidak Efektif (Drug Ineffective)', 'OFF LABEL USE': 'Penggunaan Off-label (Off Label Use)'
        };
        if (translations[term]) term = translations[term];
        li.innerHTML = `<span class="material-symbols-outlined text-sm">warning</span> <span><strong>${term}</strong> (${item.count.toLocaleString()} laporan)</span>`;
        reactionsC.appendChild(li);
      });
    } else {
      reactionsC.innerHTML = `<li class="bg-surface-container text-on-surface px-4 py-2 rounded-lg font-body-md text-body-md">Tidak ditemukan informasi efek samping yang relevan.</li>`;
    }
  }

  // System Recommendations
  const recC = document.getElementById('verdict-recommendation');
  if (recC) {
    if (score >= 81) recC.innerText = "Produk ini terdaftar secara resmi di BPOM, memiliki klaim promosi yang wajar (sesuai indikasi), dan memiliki profil keamanan yang baik. Silakan gunakan sesuai dosis referensi.";
    else if (score >= 61) recC.innerText = "Produk terdaftar di BPOM namun iklan/klaim mungkin mengandung sedikit hiperbola atau memiliki laporan efek samping yang cukup tinggi di OpenFDA. Gunakan dengan wajar dan perhatikan dosis referensi.";
    else if (score >= 31) recC.innerText = "Perhatian! Produk mungkin belum terdaftar di BPOM, memiliki klaim medis berlebihan yang tidak sesuai kategori terapinya, atau mengandung efek samping serius. Konsultasikan dengan dokter sebelum digunakan.";
    else recC.innerText = "Sangat Berisiko! Iklan produk ini menggunakan klaim medis berlebihan (Overclaim Tinggi) untuk penyakit berat, atau produk tidak terdaftar dengan tingkat laporan kejadian berbahaya yang sangat tinggi. Sangat direkomendasikan untuk menghindari produk ini.";
  }

  // Dynamic Safety Tips based on Category
  const tipsList = document.getElementById('result-safety-tips');
  if (tipsList) {
    tipsList.innerHTML = '';
    const category = (profile ? profile.product_category : "") || "";
    const catLower = category.toLowerCase();
    
    let tips = [];
    if (catLower.includes("kosmetik") || catLower.includes("cosmetic") || catLower.includes("skin") || catLower.includes("wajah") || catLower.includes("kecantikan")) {
      tips = [
        "Lakukan patch test (uji tempel) di kulit belakang telinga atau lengan bagian dalam selama 24 jam sebelum pemakaian pertama.",
        "Gunakan tabir surya (sunscreen) minimal SPF 30 di pagi/siang hari, terutama jika produk mengandung zat eksfoliasi aktif.",
        "Hentikan penggunaan segera jika timbul sensasi terbakar, gatal ekstrem, bengkak, atau kemerahan luar biasa."
      ];
    } else if (catLower.includes("suplemen") || catLower.includes("supplement") || catLower.includes("traditional") || catLower.includes("jamu") || catLower.includes("herbal")) {
      tips = [
        "Konsumsi setelah makan untuk menghindari potensi iritasi lambung, kecuali jika terdapat petunjuk khusus pada kemasan.",
        "Patuhi dosis harian yang dianjurkan resmi. Jangan mengonsumsi berlebihan hanya untuk mempercepat efek khasiat.",
        "Konsultasikan dengan dokter jika Anda sedang hamil, menyusui, atau memiliki penyakit penyerta sebelum mengonsumsi."
      ];
    } else {
      // Obat / General medicine
      tips = [
        "Pahami aturan pakai, dosis standar, efek samping, dan kontraindikasi obat yang tertera pada brosur kemasan resmi.",
        "Jangan meminum obat ini bersamaan dengan alkohol atau obat sejenis lainnya tanpa petunjuk dokter untuk mencegah efek toksik.",
        "Simpan obat di tempat kering, sejuk (di bawah suhu 30°C), terhindar dari cahaya langsung, dan jauhkan dari anak-anak."
      ];
    }

    tips.forEach(tip => {
      const li = document.createElement('li');
      li.innerText = tip;
      tipsList.appendChild(li);
    });
  }

  const overallDiscEl = document.getElementById('overall-disclaimer');
  if (overallDiscEl) {
    overallDiscEl.innerText = result.disclaimer || "WARAS-ID adalah platform analisis keselamatan konsumen bertenaga AI. Seluruh analisis bersifat informatif dan tidak menggantikan nasihat medis profesional.";
  }

  // Technical Details (Accordion fields)
  const aiSummaryEl = document.getElementById('result-ai-summary');
  if (aiSummaryEl) aiSummaryEl.innerText = result.ai_executive_summary || "Tidak ada ringkasan otomatis.";

  const nlpLabel = claim.label || "tidak overclaim";
  const confPct = ((claim.confidence || 1.0) * 100).toFixed(1);
  const modelLabel = document.getElementById('result-model-label');
  if (modelLabel) {
    modelLabel.innerText = nlpLabel.toUpperCase();
    let labelColor = '#168464'; // green
    if (nlpLabel === 'overclaim tinggi' || nlpLabel === 'overclaim') labelColor = '#b3261e'; // red
    else if (nlpLabel === 'overclaim sedang' || nlpLabel === 'ambiguous') labelColor = '#9a5b00'; // amber
    modelLabel.style.color = labelColor;

    const bar = document.getElementById('result-model-confidence-bar');
    if (bar) {
      bar.style.backgroundColor = labelColor;
      bar.style.width = `${confPct}%`;
    }
  }

  const confEl = document.getElementById('result-model-confidence');
  if (confEl) confEl.innerText = `${confPct}%`;

  const twC = document.getElementById('detected-trigger-words');
  if (twC) {
    if (claim.trigger_words && claim.trigger_words.length > 0) {
      twC.innerText = claim.trigger_words.join(', ');
      twC.style.color = '#b3261e';
    } else {
      twC.innerText = 'Tidak ditemukan';
      twC.style.color = '#62625d';
    }
  }

  // Medical Consistency fields
  const consistency = result.medical_consistency || {};
  const cBadge = document.getElementById('consistency-score-badge');
  if (cBadge) {
    cBadge.innerText = `${consistency.score || 0} / 100`;
    let cColor = consistency.score >= 80 ? '#168464' : consistency.score >= 50 ? '#9a5b00' : '#b3261e';
    cBadge.style.color = cColor;
  }

  const cExplEl = document.getElementById('consistency-explanation');
  if (cExplEl) cExplEl.innerText = consistency.explanation || "-";

  const crC = document.getElementById('consistency-reasons-list');
  if (crC) {
    crC.innerHTML = '';
    if (consistency.reasons && consistency.reasons.length > 0) {
      consistency.reasons.forEach(r => {
        const div = document.createElement('div');
        div.className = 'flex items-center gap-xs text-xs';
        const icon = r.icon === 'check' ? 'check_circle' : 'cancel';
        const iconClass = r.icon === 'check' ? 'text-primary' : 'text-error';
        div.innerHTML = `<span class="material-symbols-outlined ${iconClass} text-sm flex-shrink-0">${icon}</span> <span class="text-on-surface">${r.text}</span>`;
        crC.appendChild(div);
      });
    } else {
      crC.innerHTML = `<div class="empty-note empty-note--small">Tidak ada detail.</div>`;
    }
  }

  // OpenFDA Counts
  const totalReportsEl = document.getElementById('ae-total-reports');
  if (totalReportsEl) totalReportsEl.innerText = (fda.total_reports || 0).toLocaleString();

  const seriousReportsEl = document.getElementById('ae-serious-reports');
  if (seriousReportsEl) seriousReportsEl.innerText = (fda.serious_reports || 0).toLocaleString();

  const fdaDiscEl = document.getElementById('fda-disclaimer');
  if (fdaDiscEl) fdaDiscEl.innerText = fda.disclaimer || "Laporan kejadian efek samping.";

  // Raw OCR Text
  const ocrC = document.getElementById('result-ocr-text');
  if (ocrC) {
    const et = result.extracted_text;
    ocrC.innerText = (et && et.trim ? et.trim() : et) || '(Tidak ada teks yang terdeteksi)';
  }

  // Breakdown Safety Scores
  const bpomScoreEl = document.getElementById('score-bpom');
  if (bpomScoreEl) bpomScoreEl.innerText = `${safety.bpom_score || 0}%`;

  const consistencyScoreEl = document.getElementById('score-consistency');
  if (consistencyScoreEl) consistencyScoreEl.innerText = `${safety.consistency_score || 0}%`;

  const nlpScoreEl = document.getElementById('score-nlp');
  if (nlpScoreEl) nlpScoreEl.innerText = `${safety.claim_score || 0}%`;

  const fdaScoreEl = document.getElementById('score-fda');
  if (fdaScoreEl) fdaScoreEl.innerText = `${safety.adverse_event_score || 0}%`;

  showResults();

  // If this analysis was triggered by the demo, automatically start the results page guide
  if (window.isDemoActive) {
    window.isDemoActive = false;
    wasDemoTour = true;
    setTimeout(() => {
      startTour('result');
    }, 400);
  }
}

// Typewriter effect for demo buttons
let typingTimeoutId = null;
function typeWriter(text, inputEl, callback) {
  if (typingTimeoutId) {
    clearTimeout(typingTimeoutId);
  }
  inputEl.value = '';
  
  // Wait for page switch/repaint before scrolling and focusing
  setTimeout(() => {
    inputEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    inputEl.focus();
  }, 150);

  let i = 0;
  function type() {
    if (i < text.length) {
      inputEl.value += text.charAt(i);
      inputEl.focus();
      
      // Keep cursor at the end of the text
      const pos = i + 1;
      inputEl.setSelectionRange(pos, pos);
      
      // Scroll horizontally to keep the typed word in view
      inputEl.scrollLeft = inputEl.scrollWidth;

      i++;
      typingTimeoutId = setTimeout(type, 40);
    } else {
      typingTimeoutId = null;
      if (callback) callback();
    }
  }
  
  // Start typing after scroll is initiated
  setTimeout(type, 200);
}

// Demo runner function
function runDemo(type) {
  const mainInput = document.getElementById('input-main-val');
  if (!mainInput) return;

  // Set isDemoActive to true so that results page tour triggers automatically
  window.isDemoActive = true;

  // Clear input and show home page first
  if (typeof showHome === 'function') {
    showHome();
  }

  let textVal = '';
  let actionCallback = null;

  if (type === 'bpom') {
    textVal = 'SD161548601';
    actionCallback = () => checkProductIdentity(textVal);
  } else if (type === 'overclaim') {
    textVal = 'Minyak herbal ajaib ini terbukti paling ampuh 100% sembuh total secara instan dari stroke dan diabetes tanpa efek samping!';
    actionCallback = () => checkProductText(textVal);
  } else if (type === 'shopee') {
    showDevelopmentPopup();
    return;
  }

  typeWriter(textVal, mainInput, actionCallback);
}

// Onboarding Tour logic
let tourCurrentStep = 0;
let tourSteps = [];
let tourActivePage = '';
let wasDemoTour = false;

const homeTourSteps = [
  {
    targetId: 'input-main-val',
    title: 'Kolom Pencarian Utama',
    text: 'Ketik nama produk (misal: "Vitamin B"), nomor registrasi BPOM, atau salin teks iklan promosi yang ingin dicek di sini (misal: "Diapet menyembuhkan kanker").'
  },
  {
    targetId: 'btn-action-link',
    title: 'Pindai Tautan Shopee',
    text: 'Klik di sini untuk menempel link produk Shopee. AI akan secara otomatis memindai deskripsi produk dari platform e-commerce tersebut.'
  },
  {
    targetId: 'btn-action-barcode',
    title: 'Unggah Barcode atau Gambar',
    text: 'Unggah foto barcode kemasan produk fisik atau screenshot promosi untuk memindai kode dan teks dengan OCR bertenaga AI.'
  },
  {
    targetId: 'demo-bpom',
    title: 'Preset Uji Coba Demo',
    text: 'Klik tombol demo ini untuk langsung melihat kehebatan sistem dalam mendeteksi legalitas, klaim iklan, dan efek samping secara instan.'
  }
];

const resultTourSteps = [
  {
    targetId: 'result-verdict-score',
    title: 'Skor Keselamatan Konsumen',
    text: 'Angka 0-100 ini dihitung secara proporsional berdasarkan registrasi BPOM, deteksi overclaim, konsistensi indikasi, dan data OpenFDA.'
  },
  {
    targetId: 'result-ai-summary',
    title: 'Ringkasan Eksekutif AI',
    text: 'AI merangkum secara cerdas tingkat bahaya, legalitas, serta kecocokan klaim produk dengan fungsi terapinya.'
  },
  {
    targetId: 'result-score-reasons-list',
    title: 'Faktor Skor Keamanan',
    text: 'Menampilkan poin-poin checklist detail yang memengaruhi skor keamanan (keabsahan BPOM, indikasi overclaim, atau kesesuaian kategori terapi).'
  },
  {
    targetId: 'prof-bpom-interpretation',
    title: 'Profil Resmi BPOM',
    text: 'Menampilkan detail produsen dan interpretasi kode abreviasi BPOM secara transparan.'
  },
  {
    targetId: 'ddd-route-std',
    title: 'Dosis Standar WHO',
    text: 'Menunjukkan standar takaran harian (Defined Daily Dose) dan rute pemakaian aman sesuai panduan resmi WHO.'
  },
  {
    targetId: 'result-evidence-container',
    title: 'Deteksi & Bukti Overclaim',
    text: 'Bagian ini memaparkan kutipan kalimat promosi yang dideteksi oleh AI sebagai klaim berlebihan (overclaim), lengkap dengan analisis kebenaran medisnya.'
  },
  {
    targetId: 'ae-reactions-list-container',
    title: 'Potensi Efek Samping Global',
    text: 'Daftar efek samping yang paling sering dilaporkan pasien di seluruh dunia berdasarkan database OpenFDA.'
  }
];

function startTour(page) {
  const tempWasDemo = wasDemoTour;
  endTour();
  wasDemoTour = tempWasDemo;

  tourActivePage = page;
  tourSteps = page === 'home' ? homeTourSteps : resultTourSteps;
  tourCurrentStep = 0;

  if (page === 'home') {
    showHome();
  } else {
    const resultsPage = document.getElementById('results-page');
    if (!resultsPage || !resultsPage.classList.contains('active')) {
      alert('Jalankan analisis produk terlebih dahulu untuk melihat panduan hasil.');
      return;
    }
  }

  const overlay = document.createElement('div');
  overlay.id = 'tour-overlay';
  overlay.className = 'tour-overlay';
  
  const spotlight = document.createElement('div');
  spotlight.id = 'tour-spotlight';
  spotlight.className = 'tour-spotlight';
  
  const tooltip = document.createElement('div');
  tooltip.id = 'tour-tooltip';
  tooltip.className = 'tour-tooltip';
  
  overlay.appendChild(spotlight);
  overlay.appendChild(tooltip);
  document.body.appendChild(overlay);

  // Attach event listeners for real-time positioning on scroll/resize
  window.addEventListener('scroll', updateTourPosition, { passive: true });
  window.addEventListener('resize', updateTourPosition, { passive: true });

  renderTourStep();
}

function updateTourPosition() {
  const overlay = document.getElementById('tour-overlay');
  if (!overlay) return;

  const step = tourSteps[tourCurrentStep];
  const target = document.getElementById(step.targetId);
  const spotlight = document.getElementById('tour-spotlight');
  const tooltip = document.getElementById('tour-tooltip');

  if (!target || !spotlight || !tooltip) return;

  const rect = target.getBoundingClientRect();
  const padding = 8;
  spotlight.style.top = `${rect.top - padding}px`;
  spotlight.style.left = `${rect.left - padding}px`;
  spotlight.style.width = `${rect.width + padding * 2}px`;
  spotlight.style.height = `${rect.height + padding * 2}px`;

  const tooltipWidth = 340;
  const tooltipPadding = 16;
  let tooltipTop = rect.bottom + tooltipPadding;
  let tooltipLeft = rect.left + (rect.width / 2) - (tooltipWidth / 2);

  if (tooltipLeft < 10) tooltipLeft = 10;
  if (tooltipLeft + tooltipWidth > window.innerWidth - 10) {
    tooltipLeft = window.innerWidth - tooltipWidth - 10;
  }

  // If target is too low, place tooltip above it
  if (rect.bottom + tooltipPadding + 220 > window.innerHeight) {
    tooltipTop = rect.top - 230;
  }

  tooltip.style.top = `${tooltipTop}px`;
  tooltip.style.left = `${tooltipLeft}px`;
}

function renderTourStep() {
  const step = tourSteps[tourCurrentStep];
  const target = document.getElementById(step.targetId);

  if (!target) {
    if (tourCurrentStep < tourSteps.length - 1) {
      tourCurrentStep++;
      renderTourStep();
    } else {
      endTour(false);
    }
    return;
  }

  // Auto focus / scroll instantly to center the target element
  target.scrollIntoView({ behavior: 'auto', block: 'center' });

  // Instantly position the spotlight and tooltip
  updateTourPosition();

  // Populate content in tooltip
  const tooltip = document.getElementById('tour-tooltip');
  if (tooltip) {
    const isFirst = tourCurrentStep === 0;
    const isLast = tourCurrentStep === tourSteps.length - 1;

    tooltip.innerHTML = `
      <div class="tour-tooltip-title">${step.title}</div>
      <div class="tour-tooltip-body">${step.text}</div>
      <div class="tour-tooltip-footer">
        <span class="tour-counter">${tourCurrentStep + 1} dari ${tourSteps.length}</span>
        <div class="tour-btn-group">
          ${!isLast ? `<button class="tour-btn-skip" onclick="endTour(false)">Lewati</button>` : ''}
          ${!isFirst ? `<button class="tour-btn-prev" onclick="prevTourStep()">Kembali</button>` : ''}
          <button class="tour-btn-next" onclick="${isLast ? 'endTour(true)' : 'nextTourStep()'}">
            ${isLast ? 'Selesai' : 'Lanjut'}
          </button>
        </div>
      </div>
    `;
  }
}

function nextTourStep() {
  if (tourCurrentStep < tourSteps.length - 1) {
    tourCurrentStep++;
    renderTourStep();
  }
}

function prevTourStep() {
  if (tourCurrentStep > 0) {
    tourCurrentStep--;
    renderTourStep();
  }
}

function endTour(completed) {
  // Remove event listeners
  window.removeEventListener('scroll', updateTourPosition);
  window.removeEventListener('resize', updateTourPosition);

  const overlay = document.getElementById('tour-overlay');
  if (overlay) {
    overlay.remove();
  }

  // If this was a demo tour and they completed the last step, show the completion modal
  if (wasDemoTour && completed) {
    wasDemoTour = false;
    setTimeout(() => {
      showDemoCompletionModal();
    }, 300);
  } else {
    wasDemoTour = false;
  }
}

// Demo Completion Modal Helpers
function showDemoCompletionModal() {
  const existingModal = document.getElementById('demo-completion-modal');
  if (existingModal) existingModal.remove();

  const modal = document.createElement('div');
  modal.id = 'demo-completion-modal';
  modal.className = 'demo-modal-overlay';
  
  modal.innerHTML = `
    <div class="demo-modal-card">
      <svg class="demo-modal-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#00696b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M5.8 11.3 2 22l10.7-3.8M4 20l.5-.5M7 17l.5-.5M9 15l.5-.5M16 2a5 5 0 0 0-4 4v1h5a4 4 0 0 1 4 4v1a3 3 0 0 0 3-3V6a4 4 0 0 0-4-4Z"/>
        <path d="M11.3 8.3c.2-.7.7-1.3 1.4-1.6M14 5.5c.8 0 1.5.3 2 .8M19 10.5c0 .8-.3 1.5-.8 2"/>
      </svg>
      <h3 class="demo-modal-title">Demo Selesai!</h3>
      <p class="demo-modal-text">Anda telah melihat bagaimana Waras-ID menganalisis produk kesehatan. Apa yang ingin Anda lakukan selanjutnya?</p>
      <div class="demo-modal-buttons">
        <button class="demo-modal-btn-secondary" onclick="handleDemoAction('repeat')">Ulangi Demo</button>
        <button class="demo-modal-btn-primary" onclick="handleDemoAction('start')">AYO MULAI SEKARANG</button>
      </div>
    </div>
  `;
  document.body.appendChild(modal);

  setTimeout(() => {
    modal.classList.add('show');
  }, 50);
}

function handleDemoAction(action) {
  const modal = document.getElementById('demo-completion-modal');
  if (modal) {
    modal.classList.remove('show');
    setTimeout(() => modal.remove(), 300);
  }

  if (action === 'repeat') {
    runDemo('bpom');
  } else if (action === 'start') {
    showHome();
    const mainInput = document.getElementById('input-main-val');
    if (mainInput) {
      mainInput.value = '';
      mainInput.focus();
    }
  }
}

// Development Feature Pop-up Helpers
function showDevelopmentPopup() {
  const existingModal = document.getElementById('dev-feature-modal');
  if (existingModal) existingModal.remove();

  const modal = document.createElement('div');
  modal.id = 'dev-feature-modal';
  modal.className = 'demo-modal-overlay';
  
  modal.innerHTML = `
    <div class="demo-modal-card">
      <svg class="demo-modal-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
      </svg>
      <h3 class="demo-modal-title">Fitur Dalam Pengembangan</h3>
      <p class="demo-modal-text">Mohon maaf, fitur pemindaian tautan e-commerce (Shopee) saat ini masih dalam proses pengembangan dan penyempurnaan.</p>
      <div class="demo-modal-buttons">
        <button class="demo-modal-btn-primary" onclick="closeDevPopup()" style="background: #d97706; border: none; color: white;">Mengerti</button>
      </div>
    </div>
  `;
  document.body.appendChild(modal);

  setTimeout(() => {
    modal.classList.add('show');
  }, 50);
}

function closeDevPopup() {
  const modal = document.getElementById('dev-feature-modal');
  if (modal) {
    modal.classList.remove('show');
    setTimeout(() => modal.remove(), 300);
  }
}

// Bind to window to allow HTML onclick access
window.runDemo = runDemo;
window.startTour = startTour;
window.nextTourStep = nextTourStep;
window.prevTourStep = prevTourStep;
window.endTour = endTour;
window.handleDemoAction = handleDemoAction;
window.showDevelopmentPopup = showDevelopmentPopup;
window.closeDevPopup = closeDevPopup;

// Run on load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeEventHandlers);
} else {
  initializeEventHandlers();
}
