let currentLang = 'ru';
let stats = { checked: 0, found: 0, notfound: 0, limit: 0 };
let loaderInterval = null;
let currentFilter = 'all';

function setButtonText(stateClass, text) {
    const p = document.querySelector(`.${stateClass} p`);
    if (!p) return;
    p.innerHTML = '';
    [...text].forEach((char, index) => {
        const span = document.createElement('span');
        span.style.setProperty('--i', index + 1);
        span.innerText = char === ' ' ? '\u00A0' : char;
        p.appendChild(span);
    });
}

function updateButtonLanguages() {
    setButtonText('state--default', translations[currentLang].btnScan);
    setButtonText('state--sent', translations[currentLang].btnSent);
}

function updateLoaderText() {
    const text = translations[currentLang].loaderText;
    document.querySelectorAll('.loader .text span').forEach(span => {
        span.innerText = text;
    });
}

function handleEmailInput(val) {
    const badgeEl = document.getElementById('domain-badge');
    if (!badgeEl) return;
    
    const email = val.trim();
    if (!email.includes('@')) {
        badgeEl.classList.add('hidden');
        return;
    }
    
    const parts = email.split('@');
    if (parts.length < 2 || !parts[1]) {
        badgeEl.classList.add('hidden');
        return;
    }
    
    const domain = parts[1].toLowerCase();
    let label = '';
    let iconClass = 'fa-solid fa-globe';

    if (domain.includes('gmail.com')) {
        label = 'Google Mail';
        iconClass = 'fa-brands fa-google text-red-400';
    } else if (domain.includes('yandex') || domain.includes('ya.ru')) {
        label = 'Yandex';
        iconClass = 'fa-solid fa-envelope text-red-500';
    } else if (domain.includes('mail.ru') || domain.includes('inbox.ru') || domain.includes('bk.ru')) {
        label = 'Mail.ru';
        iconClass = 'fa-solid fa-at text-blue-400';
    } else if (domain.includes('outlook') || domain.includes('hotmail') || domain.includes('live.com')) {
        label = 'Microsoft';
        iconClass = 'fa-brands fa-microsoft text-sky-400';
    } else if (domain.includes('proton')) {
        label = 'Proton Mail';
        iconClass = 'fa-solid fa-shield-halved text-purple-400';
    } else if (domain.includes('icloud') || domain.includes('me.com')) {
        label = 'Apple iCloud';
        iconClass = 'fa-brands fa-apple text-zinc-300';
    } else if (domain.length > 3) {
        label = domain;
        iconClass = 'fa-solid fa-globe text-indigo-400';
    }

    if (label) {
        badgeEl.innerHTML = `<i class="${iconClass} text-xs mr-1.5"></i> <span>${label}</span>`;
        badgeEl.classList.remove('hidden');
    } else {
        badgeEl.classList.add('hidden');
    }
}

function showToast(message) {
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toast-message');
    if (!toast || !toastMsg) return;

    toastMsg.innerText = message;
    toast.classList.remove('translate-y-20', 'opacity-0', 'pointer-events-none');
    toast.classList.add('translate-y-0', 'opacity-100');

    setTimeout(() => {
        toast.classList.remove('translate-y-0', 'opacity-100');
        toast.classList.add('translate-y-20', 'opacity-0', 'pointer-events-none');
    }, 3000);
}

function filterResults(type) {
    currentFilter = type;
    const cards = document.querySelectorAll('.cyber-card');
    const searchInput = document.getElementById('search-cards-input');
    const searchVal = searchInput ? searchInput.value.toLowerCase().trim() : '';

    const tabs = document.querySelectorAll('.filter-tab');
    if (tabs.length > 0) {
        tabs.forEach(tab => {
            tab.className = "filter-tab px-3.5 py-1.5 text-xs font-bold rounded-xl bg-zinc-900 border border-zinc-800 text-zinc-400 hover:border-zinc-700 transition-all duration-200";
        });

        const targetId = type === 'not found' ? 'filter-btn-notfound' : `filter-btn-${type}`;
        const activeTab = document.getElementById(targetId);
        if (activeTab) {
            if (type === 'all') activeTab.className = "filter-tab px-3.5 py-1.5 text-xs font-bold rounded-xl bg-indigo-600 text-white transition-all duration-200";
            else if (type === 'EXISTS') activeTab.className = "filter-tab px-3.5 py-1.5 text-xs font-bold rounded-xl bg-emerald-600 text-white transition-all duration-200";
            else if (type === 'not found') activeTab.className = "filter-tab px-3.5 py-1.5 text-xs font-bold rounded-xl bg-zinc-700 text-white transition-all duration-200";
            else if (type === 'LIMIT') activeTab.className = "filter-tab px-3.5 py-1.5 text-xs font-bold rounded-xl bg-amber-600 text-white transition-all duration-200";
        }
    }

    cards.forEach(card => {
        const cardStatus = (card.getAttribute('data-status') || '').trim();
        const cardName = (card.getAttribute('data-name') || '').toLowerCase().trim();
        
        const matchesFilter = (type === 'all') || (cardStatus === type);
        const matchesSearch = !searchVal || cardName.includes(searchVal);

        if (matchesFilter && matchesSearch) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function searchCards() {
    filterResults(currentFilter);
}

function switchLanguage(lang) {
    currentLang = lang;
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) {
            if (el.tagName === 'INPUT') {
                el.placeholder = translations[lang][key];
            } else {
                el.innerHTML = translations[lang][key];
            }
        }
    });
    
    const ruBtn = document.getElementById('btn-ru');
    const enBtn = document.getElementById('btn-en');
    if (lang === 'ru') {
        ruBtn.className = "px-3.5 py-1.5 text-xs font-black rounded-lg bg-indigo-600 text-white transition-all duration-300";
        enBtn.className = "px-3.5 py-1.5 text-xs font-black rounded-lg bg-transparent text-zinc-500 hover:bg-zinc-900 hover:text-zinc-300 transition-all duration-300";
    } else {
        enBtn.className = "px-3.5 py-1.5 text-xs font-black rounded-lg bg-indigo-600 text-white transition-all duration-300";
        ruBtn.className = "px-3.5 py-1.5 text-xs font-black rounded-lg bg-transparent text-zinc-500 hover:bg-zinc-900 hover:text-zinc-300 transition-all duration-300";
    }
    
    document.querySelectorAll('[data-card-status]').forEach(el => {
        const status = el.getAttribute('data-card-status');
        if (status === 'EXISTS') el.innerHTML = translations[lang].statusExists;
        if (status === 'not found') el.innerHTML = translations[lang].statusNotFound;
        if (status === 'LIMIT') el.innerHTML = translations[lang].statusLimit;
        if (status === 'ERROR') el.innerHTML = translations[lang].statusError;
    });

    const bannerTitle = document.getElementById('no-accounts-title');
    const bannerText = document.getElementById('no-accounts-text');
    if (bannerTitle) bannerTitle.innerText = translations[currentLang].noAccountsBannerTitle;
    if (bannerText) bannerText.innerText = translations[currentLang].noAccountsBannerText;

    updateButtonLanguages();
    updateLoaderText();
}

function updateTheme(val) {
    const p = val / 100;
    
    const bgR = Math.round(214 * (1 - p));
    const bgG = Math.round(210 * (1 - p));
    const bgB = Math.round(196 * (1 - p));
    document.documentElement.style.setProperty('--bg-color', `rgb(${bgR}, ${bgG}, ${bgB})`);
    
    const textR = Math.round(15 + (244 - 15) * p);
    const textG = Math.round(15 + (244 - 15) * p);
    const textB = Math.round(17 + (245 - 17) * p);
    document.documentElement.style.setProperty('--text-color', `rgb(${textR}, ${textG}, ${textB})`);
    
    const cardR = Math.round(250 * (1 - p) + 9 * p);
    const cardG = Math.round(248 * (1 - p) + 9 * p);
    const cardB = Math.round(242 * (1 - p) + 11 * p);
    const cardAlpha = 0.9 * (1 - p) + 0.6 * p;
    document.documentElement.style.setProperty('--card-bg', `rgba(${cardR}, ${cardG}, ${cardB}, ${cardAlpha})`);
    
    const borderR = Math.round(212 * (1 - p) + 39 * p);
    const borderG = Math.round(208 * (1 - p) + 39 * p);
    const borderB = Math.round(196 * (1 - p) + 42 * p);
    const borderAlpha = 0.8 * (1 - p) + 0.8 * p;
    document.documentElement.style.setProperty('--border-color', `rgba(${borderR}, ${borderG}, ${borderB}, ${borderAlpha})`);
    
    const slider = document.getElementById('theme-slider');
    if (p > 0.5) {
        slider.style.setProperty('--thumb-color', 'rgb(196, 201, 209)');
        slider.style.setProperty('--thumb-glow', 'rgba(196, 201, 209, 0.8)');
        document.body.classList.remove('light-theme');
        document.documentElement.style.setProperty('--sky-day-opacity', '0');
        document.documentElement.style.setProperty('--sky-night-opacity', '1');
        document.documentElement.style.setProperty('--cloud-translate-x', '-50px');
    } else {
        slider.style.setProperty('--thumb-color', 'rgb(236, 202, 47)');
        slider.style.setProperty('--thumb-glow', 'rgba(236, 202, 47, 0.8)');
        document.body.classList.add('light-theme');
        document.documentElement.style.setProperty('--sky-day-opacity', '1');
        document.documentElement.style.setProperty('--sky-night-opacity', '0');
        document.documentElement.style.setProperty('--cloud-translate-x', '0px');
    }
}

function downloadResults() {
    const cards = document.querySelectorAll('.cyber-card');
    let content = 'Holehe OSINT Scan Report\nTarget: ' + document.getElementById('email-input').value + '\n\n';
    let foundCount = 0;
    
    cards.forEach(card => {
        const name = card.getAttribute('data-name');
        const statusBadge = card.querySelector('[data-card-status]');
        const status = statusBadge ? statusBadge.getAttribute('data-card-status') : '';
        const domain = card.querySelector('p').innerText.trim();
        
        if (status === 'EXISTS') {
            content += `[+] ${name} | ${domain}\n`;
            foundCount++;
        }
    });
    
    if (foundCount === 0) {
        content += 'No accounts found.\n';
    }
    
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `holehe_report_${document.getElementById('email-input').value}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function downloadResultsJson() {
    const cards = document.querySelectorAll('.cyber-card');
    let results = [];
    
    cards.forEach(card => {
        const name = card.getAttribute('data-name');
        const status = card.getAttribute('data-status');
        const domain = card.querySelector('p').innerText.trim();
        results.push({ name, status, domain });
    });
    
    const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `holehe_report_${document.getElementById('email-input').value}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function copyFoundResults() {
    const cards = document.querySelectorAll('.cyber-card[data-status="EXISTS"]');
    if (cards.length === 0) return;
    
    let text = `Holehe OSINT Target: ${document.getElementById('email-input').value}\nFound Accounts:\n`;
    cards.forEach(card => {
        const name = card.getAttribute('data-name');
        const domain = card.querySelector('p').innerText.trim();
        text += `[+] ${name} | ${domain}\n`;
    });
    
    navigator.clipboard.writeText(text).then(() => {
        showToast(translations[currentLang].copiedToast);
    });
}

function startScan() {
    const email = document.getElementById('email-input').value.trim();
    if (!email) return;

    const grid = document.getElementById('results-grid');
    if (grid) grid.innerHTML = '';

    const existingBanner = document.getElementById('no-accounts-banner');
    if (existingBanner) existingBanner.remove();

    const dlBtn = document.getElementById('download-btn');
    if (dlBtn) dlBtn.classList.add('hidden');

    const dlJsonBtn = document.getElementById('download-json-btn');
    if (dlJsonBtn) dlJsonBtn.classList.add('hidden');

    const copyBtn = document.getElementById('copy-btn');
    if (copyBtn) copyBtn.classList.add('hidden');

    const controls = document.getElementById('results-controls');
    if (controls) controls.classList.add('hidden');

    const statsSec = document.getElementById('stats-section');
    if (statsSec) statsSec.classList.add('hidden');

    const loadContainer = document.getElementById('loading-container');
    if (loadContainer) loadContainer.classList.remove('hidden');

    stats = { checked: 0, found: 0, notfound: 0, limit: 0 };
    document.getElementById('stat-checked').innerText = '0';
    document.getElementById('stat-found').innerText = '0';
    document.getElementById('stat-notfound').innerText = '0';
    document.getElementById('stat-limit').innerText = '0';

    const btn = document.getElementById('scan-btn');
    if (btn) btn.disabled = true;

    let stageIndex = 0;
    
    clearInterval(loaderInterval);
    loaderInterval = setInterval(() => {
        const stages = [
            translations[currentLang].loaderStage1,
            translations[currentLang].loaderStage2,
            translations[currentLang].loaderStage3,
            translations[currentLang].loaderStage4,
            translations[currentLang].loaderStage5
        ];
        const checked = stats.checked;
        stageIndex = (stageIndex + 1) % stages.length;
        const statusEl = document.getElementById('loader-status');
        if (statusEl) statusEl.innerText = `[${checked} / 52] ${stages[stageIndex]}`;
    }, 2500);

    const eventSource = new EventSource(`/api/scan?email=${encodeURIComponent(email)}`);

    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        if (data.type === 'info') {
            let msg = data.message;
            if (msg.includes('Checking if domain')) {
                msg = translations[currentLang].statusCheckingDomain;
            } else if (msg.includes('TARGET:')) {
                msg = translations[currentLang].statusScanStart;
            }
            const statusEl = document.getElementById('loader-status');
            if (statusEl) statusEl.innerText = `[${stats.checked} / 52] ${msg}`;
        }

        if (data.type === 'progress') {
            const statsSec = document.getElementById('stats-section');
            if (statsSec) statsSec.classList.remove('hidden');

            const controls = document.getElementById('results-controls');
            if (controls) controls.classList.remove('hidden');

            stats.checked++;
            document.getElementById('stat-checked').innerText = stats.checked;

            let bgClass = '';
            let textClass = '';
            let badge = '';

            if (data.status === 'EXISTS') {
                stats.found++;
                document.getElementById('stat-found').innerText = stats.found;
                bgClass = 'border-emerald-500/20 hover:border-emerald-500/60 hover:shadow-[0_0_20px_rgba(16,185,129,0.15)]';
                textClass = 'text-emerald-500';
                badge = `<span class="px-2 py-1 text-[11px] font-bold rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1.5">
                            <span class="relative flex h-2 w-2">
                                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                                <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                            </span>
                            <span data-card-status="EXISTS">${translations[currentLang].statusExists}</span>
                         </span>`;
            } else if (data.status === 'not found') {
                stats.notfound++;
                document.getElementById('stat-notfound').innerText = stats.notfound;
                bgClass = 'border-zinc-900 hover:border-zinc-700 hover:shadow-[0_0_20px_rgba(255,255,255,0.05)]';
                textClass = 'text-zinc-500';
                badge = `<span class="px-2 py-1 text-[11px] font-bold rounded-lg bg-zinc-900 text-zinc-400 border border-zinc-800 flex items-center gap-1.5">
                            <span class="inline-flex rounded-full h-2 w-2 bg-zinc-600"></span>
                            <span data-card-status="not found">${translations[currentLang].statusNotFound}</span>
                         </span>`;
            } else {
                stats.limit++;
                document.getElementById('stat-limit').innerText = stats.limit;
                bgClass = 'border-amber-500/20 hover:border-amber-500/60 hover:shadow-[0_0_20px_rgba(245,158,11,0.15)]';
                textClass = 'text-amber-500';
                badge = `<span class="px-2 py-1 text-[11px] font-bold rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20 flex items-center gap-1.5">
                            <span class="relative flex h-2 w-2">
                                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
                                <span class="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
                            </span>
                            <span data-card-status="LIMIT">${translations[currentLang].statusLimit}</span>
                         </span>`;
            }

            const card = document.createElement('div');
            card.className = `cyber-card p-5 rounded-2xl border ${bgClass}`;
            card.setAttribute('data-status', data.status);
            card.setAttribute('data-name', data.name);
            card.innerHTML = `
                <div class="flex items-center justify-between mb-3">
                    <h3 class="text-base font-extrabold text-zinc-100 tracking-tight">${data.name}</h3>
                    ${badge}
                </div>
                <p class="text-xs ${textClass} break-all font-mono">
                    <i class="fa-solid fa-link mr-1 opacity-70"></i> ${data.domain}
                </p>
            `;
            if (grid) grid.appendChild(card);
            filterResults(currentFilter);
        }

        if (data.type === 'done') {
            clearInterval(loaderInterval);
            eventSource.close();
            if (btn) btn.disabled = false;
            
            const loadContainer = document.getElementById('loading-container');
            if (loadContainer) loadContainer.classList.add('hidden');

            if (stats.checked === 0) {
                const statusEl = document.getElementById('loader-status');
                if (statusEl) statusEl.innerText = translations[currentLang].errorScriptOrEmail;
                if (loadContainer) loadContainer.classList.remove('hidden');
            } else if (stats.found === 0) {
                const banner = document.createElement('div');
                banner.id = 'no-accounts-banner';
                banner.className = 'w-full bg-zinc-950 border border-zinc-800 p-6 rounded-2xl mb-6 flex flex-col items-center justify-center text-center';
                banner.innerHTML = `
                    <div class="w-12 h-12 rounded-full bg-amber-500/10 border border-amber-500/20 flex items-center gap-1 justify-center text-amber-400 mb-3 text-lg">
                        <i class="fa-solid fa-triangle-exclamation"></i>
                    </div>
                    <h4 id="no-accounts-title" class="text-base font-bold text-zinc-100">${translations[currentLang].noAccountsBannerTitle}</h4>
                    <p id="no-accounts-text" class="text-xs text-zinc-400 max-w-md mt-1 font-mono">${translations[currentLang].noAccountsBannerText}</p>
                `;
                if (grid && grid.parentNode) grid.parentNode.insertBefore(banner, grid);
            }

            if (stats.found > 0) {
                const dlBtn = document.getElementById('download-btn');
                if (dlBtn) dlBtn.classList.remove('hidden');

                const dlJsonBtn = document.getElementById('download-json-btn');
                if (dlJsonBtn) dlJsonBtn.classList.remove('hidden');

                const copyBtn = document.getElementById('copy-btn');
                if (copyBtn) copyBtn.classList.remove('hidden');
            }
        }
    };

    eventSource.onerror = function() {
        clearInterval(loaderInterval);
        eventSource.close();
        if (btn) btn.disabled = false;
        const statusEl = document.getElementById('loader-status');
        if (statusEl) statusEl.innerText = translations[currentLang].errorServerConnection;
    };
}

document.addEventListener('DOMContentLoaded', () => {
    updateButtonLanguages();
    updateLoaderText();
});