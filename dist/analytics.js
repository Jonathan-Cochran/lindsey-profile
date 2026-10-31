(() => {
  'use strict';

  const measurementId = document.currentScript?.dataset.measurementId;
  if (!/^G-[A-Z0-9]+$/.test(measurementId || '')) return;

  const storageKey = 'lindsey-analytics-choice-v1';
  const lifetime = 180 * 24 * 60 * 60 * 1000;
  const disableKey = `ga-disable-${measurementId}`;
  const production = location.protocol === 'https:' &&
    ['lindseycochran.com', 'www.lindseycochran.com'].includes(location.hostname);
  const school = document.documentElement.dataset.school || 'default';
  const pagePath = school === 'default' ? '/' : `/${school}/`;
  const banner = document.querySelector('[data-analytics-banner]');
  let started = false;
  let choice = readChoice();

  window[disableKey] = true;

  function readChoice() {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey));
      if (saved && ['accepted', 'declined'].includes(saved.choice) &&
          Number.isFinite(saved.expires) && saved.expires > Date.now()) return saved.choice;
    } catch { /* Storage can be unavailable; consent then lasts for this page only. */ }
    return null;
  }

  function updateControls() {
    if (banner) banner.hidden = choice !== null;
    document.querySelectorAll('[data-analytics-controls]').forEach(el => { el.hidden = false; });
    document.querySelectorAll('[data-analytics-status]').forEach(el => {
      el.textContent = !production ? 'Analytics is disabled in this preview.' :
        choice === 'accepted' ? 'Analytics is allowed in this browser.' :
        choice === 'declined' ? 'Analytics is declined in this browser.' : 'Analytics is off until you allow it.';
    });
    document.querySelectorAll('[data-analytics-choice]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.analyticsChoice === choice));
    });
  }

  function clearAnalyticsCookies() {
    const domains = ['', location.hostname, '.lindseycochran.com'];
    for (const cookie of document.cookie.split(';')) {
      const name = cookie.trim().split('=')[0];
      if (!/^_ga(?:_|$)/.test(name)) continue;
      for (const domain of domains) {
        document.cookie = `${name}=; Max-Age=0; Path=/; SameSite=Lax${domain ? `; Domain=${domain}` : ''}`;
      }
    }
  }

  function stopAnalytics() {
    window[disableKey] = true;
    clearAnalyticsCookies();
    // Unload Google's running code after withdrawal, without sending a denied-consent ping.
    if (started) location.reload();
  }

  function startAnalytics() {
    if (started || choice !== 'accepted' || !production) return;
    started = true;
    window[disableKey] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {
      analytics_storage: 'denied', ad_storage: 'denied',
      ad_user_data: 'denied', ad_personalization: 'denied'
    });
    window.gtag('js', new Date());
    window.gtag('consent', 'update', { analytics_storage: 'granted' });
    // Drop arbitrary query strings, fragments, referrers, and unrecognized URL paths.
    window.gtag('set', {
      page_location: `https://lindseycochran.com${pagePath}`,
      page_referrer: '',
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
    window.gtag('config', measurementId, {
      send_page_view: false,
      cookie_expires: lifetime / 1000,
      cookie_update: false
    });
    track('page_view');
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
    script.referrerPolicy = 'no-referrer';
    document.head.append(script);
  }

  function track(name, parameters = {}) {
    if (choice !== 'accepted' || !started || window[disableKey]) return;
    window.gtag('event', name, { school, ...parameters, send_to: measurementId });
  }

  function saveChoice(nextChoice) {
    choice = nextChoice;
    try {
      localStorage.setItem(storageKey, JSON.stringify({ choice, expires: Date.now() + lifetime }));
    } catch { /* The current page still honors the visitor's choice. */ }
    updateControls();
    if (choice === 'accepted') startAnalytics();
    else stopAnalytics();
  }

  document.addEventListener('click', event => {
    const button = event.target.closest('[data-analytics-choice]');
    if (button) {
      saveChoice(button.dataset.analyticsChoice);
      return;
    }
    if (event.target.closest('#print-profile')) {
      track('resume_print_click');
      return;
    }
    const link = event.target.closest('a[href]');
    if (!link) return;
    const href = link.getAttribute('href');
    if (href === '#privacy') {
      document.querySelector('#privacy').open = true;
      return;
    }
    // Only fixed, descriptive labels reach GA; never transmit hrefs or link text.
    if (href.startsWith('mailto:')) track('recruiting_contact_click');
    else if (href === '/lindsey-cochran-recruiting.pdf') track('resume_download');
    else if (link.classList.contains('video-card')) {
      const race = link.dataset.raceEvent;
      if (['1600m', '800m'].includes(race)) track('race_video_click', { race });
    } else if (link.classList.contains('instagram-link')) track('instagram_click');
    else {
      let url;
      try { url = new URL(href, location.href); } catch { return; }
      const providers = {
        'www.athletic.net': 'athletic_net',
        'oh.milesplit.com': 'milesplit',
        'pa.milesplit.com': 'milesplit',
        'ohsaaweb.blob.core.windows.net': 'ohsaa',
        'www.dispatch.com': 'sports_awards',
        'runcruit.com': 'runcruit'
      };
      const provider = providers[url.hostname];
      if (provider) track('evidence_link_click', { provider });
    }
  });

  window.addEventListener('storage', event => {
    if (event.key !== storageKey && event.key !== null) return;
    choice = readChoice();
    updateControls();
    if (choice === 'accepted') startAnalytics();
    else stopAnalytics();
  });

  updateControls();
  if (choice === 'accepted') startAnalytics();
  else clearAnalyticsCookies();
})();
