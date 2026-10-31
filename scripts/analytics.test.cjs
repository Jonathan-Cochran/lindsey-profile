const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');

const source = readFileSync(`${__dirname}/../dist/analytics.js`, 'utf8');
const key = 'lindsey-analytics-choice-v1';
const saved = choice => JSON.stringify({ choice, expires: Date.now() + 86400000 });

function browser({ stored, local = false, school, blockedStorage = false } = {}) {
  const listeners = {};
  const scripts = [];
  const cookieWrites = [];
  const storage = new Map(stored ? [[key, stored]] : []);
  const banner = { hidden: true };
  const status = {};
  const controls = {};
  const privacy = {};
  const location = {
    protocol: local ? 'http:' : 'https:',
    hostname: local ? '127.0.0.1' : 'lindseycochran.com',
    href: 'https://lindseycochran.com/private@example.com/?email=private@example.com#secret',
    reloads: 0,
    reload() { this.reloads++; }
  };
  const document = {
    currentScript: { dataset: { measurementId: 'G-P3HMCFQ70E' } },
    documentElement: { dataset: { school } },
    querySelector: selector => ({ '[data-analytics-banner]': banner, '#privacy': privacy })[selector],
    querySelectorAll: selector => ({ '[data-analytics-controls]': [controls], '[data-analytics-status]': [status] })[selector] || [],
    createElement: () => ({}),
    head: { append: script => scripts.push(script) },
    addEventListener: (name, listener) => { listeners[name] = listener; },
    get cookie() { return '_ga=old; _ga_P3HMCFQ70E=old; unrelated=keep'; },
    set cookie(value) { cookieWrites.push(value); }
  };
  const window = { addEventListener: (name, listener) => { listeners[name] = listener; } };
  const localStorage = {
    getItem(name) { if (blockedStorage) throw Error('blocked'); return storage.get(name) || null; },
    setItem(name, value) { if (blockedStorage) throw Error('blocked'); storage.set(name, value); }
  };
  vm.runInNewContext(source, { document, window, localStorage, location, URL });
  const click = target => listeners.click({ target });
  const choose = choice => {
    const button = { dataset: { analyticsChoice: choice } };
    click({ closest: selector => selector === '[data-analytics-choice]' ? button : null });
  };
  const link = (href, classes = [], dataset = {}) => {
    const anchor = { dataset, getAttribute: () => href, classList: { contains: name => classes.includes(name) } };
    click({ closest: selector => selector === 'a[href]' ? anchor : null });
  };
  const commands = () => JSON.parse(JSON.stringify(Array.from(window.dataLayer || [], args => Array.from(args))));
  const events = () => commands().filter(command => command[0] === 'event');
  return { banner, status, scripts, cookieWrites, storage, location, window, listeners, choose, link, commands, events, privacy };
}

test('no Google script or events before consent, or after declining', () => {
  const b = browser();
  assert.equal(b.banner.hidden, false);
  b.link('/lindsey-cochran-recruiting.pdf');
  assert.equal(b.events().length, 0);
  b.choose('declined');
  assert.equal(b.banner.hidden, true);
  assert.equal(b.scripts.length, 0);
  assert.equal(b.commands().length, 0);
  assert.equal(JSON.parse(b.storage.get(key)).choice, 'declined');
});

test('acceptance starts one pageview, with ads denied and URLs sanitized', () => {
  const b = browser();
  b.choose('accepted');
  b.choose('accepted');
  assert.equal(b.scripts.length, 1);
  assert.equal(b.scripts[0].src, 'https://www.googletagmanager.com/gtag/js?id=G-P3HMCFQ70E');
  assert.equal(b.events().filter(event => event[1] === 'page_view').length, 1);
  const defaults = b.commands().find(command => command[0] === 'consent' && command[1] === 'default')[2];
  assert.equal(defaults.ad_storage, 'denied');
  assert.equal(defaults.ad_user_data, 'denied');
  assert.equal(defaults.ad_personalization, 'denied');
  const config = b.commands().find(command => command[0] === 'set')[1];
  assert.equal(config.allow_google_signals, false);
  assert.equal(config.allow_ad_personalization_signals, false);
  assert.equal(config.page_location, 'https://lindseycochran.com/');
  assert.equal(config.page_referrer, '');
  assert.doesNotMatch(JSON.stringify(b.commands()), /private@|\?email=|#secret/);
});

test('recruiting clicks report categories without contact addresses or raw destinations', () => {
  const b = browser({ stored: saved('accepted'), school: 'bgsu' });
  b.link('mailto:private@example.com');
  b.link('/lindsey-cochran-recruiting.pdf');
  b.link('https://oh.milesplit.com/videos/embed/820055', ['video-card'], { raceEvent: '1600m' });
  b.link('https://www.athletic.net/result/example/?private=secret');
  b.link('https://www.instagram.com/private', ['instagram-link']);
  b.link('https://example.org/unrelated');
  assert.deepEqual(b.events().map(event => event[1]), [
    'page_view', 'recruiting_contact_click', 'resume_download', 'race_video_click', 'evidence_link_click', 'instagram_click'
  ]);
  assert.equal(b.events().find(event => event[1] === 'race_video_click')[2].race, '1600m');
  assert.equal(b.events().find(event => event[1] === 'evidence_link_click')[2].provider, 'athletic_net');
  assert.ok(b.events().every(event => event[2].school === 'bgsu'));
  assert.doesNotMatch(JSON.stringify(b.commands()), /private|mailto|820055|athletic\.net/);
  assert.equal(b.commands().find(command => command[0] === 'set')[1].page_location, 'https://lindseycochran.com/bgsu/');
});

test('withdrawal stops tracking, clears GA cookies only, and unloads the running tag', () => {
  const b = browser({ stored: saved('accepted') });
  const before = b.events().length;
  b.choose('declined');
  b.link('/lindsey-cochran-recruiting.pdf');
  assert.equal(b.window['ga-disable-G-P3HMCFQ70E'], true);
  assert.equal(b.events().length, before);
  assert.equal(b.location.reloads, 1);
  assert.equal(JSON.parse(b.storage.get(key)).choice, 'declined');
  assert.ok(b.cookieWrites.some(cookie => cookie.startsWith('_ga=')));
  assert.ok(b.cookieWrites.every(cookie => !cookie.includes('unrelated')));
});

test('returning declines and expired or malformed choices do not enable tracking', () => {
  for (const stored of [saved('declined'), '{broken', JSON.stringify({ choice: 'accepted', expires: Date.now() - 1 })]) {
    assert.equal(browser({ stored }).scripts.length, 0);
  }
  assert.equal(browser({ stored: saved('declined') }).banner.hidden, true);
  assert.equal(browser({ stored: '{broken' }).banner.hidden, false);
});

test('local previews never load Google even with consent', () => {
  const b = browser({ local: true });
  b.choose('accepted');
  assert.equal(b.scripts.length, 0);
  assert.equal(b.events().length, 0);
});

test('blocked storage still requires explicit consent and does not break the page', () => {
  const b = browser({ blockedStorage: true });
  assert.equal(b.scripts.length, 0);
  b.choose('accepted');
  assert.equal(b.scripts.length, 1);
});

test('revocation in another tab is honored and privacy details remain accessible', () => {
  const b = browser({ stored: saved('accepted') });
  b.link('#privacy');
  assert.equal(b.privacy.open, true);
  b.storage.set(key, saved('declined'));
  b.listeners.storage({ key });
  assert.equal(b.window['ga-disable-G-P3HMCFQ70E'], true);
  assert.equal(b.location.reloads, 1);
});
