const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../script.js'), 'utf8');

function page({language = 'en', preferred = 'en-US', saved = null, dismissed = null, blocked = false, hash = ''} = {}) {
  const local = new Map(saved ? [['bennys-language', saved]] : []);
  const session = new Map(dismissed ? [['bennys-language-prompt-dismissed', dismissed]] : []);
  const listeners = {};
  const switchLink = {
    href: 'https://bennystreeservices.com/' + (language === 'en' ? 'es/contact.html' : 'contact.html'),
    dataset: {languageChoice: language === 'en' ? 'es' : 'en'},
    addEventListener(type, fn) { listeners.switch = fn; },
    focus() { this.focused = true; }
  };
  const promptLink = {...switchLink, addEventListener(type, fn) { listeners.prompt = fn; }};
  const prompt = language === 'en' ? {hidden: true} : null;
  const year = {};
  const dismiss = {addEventListener(type, fn) { listeners.dismiss = fn; }};
  const window = {location: {href: 'https://bennystreeservices.com/' + (language === 'es' ? 'es/' : '') + 'contact.html' + hash, hash,
    replace(url) { this.redirect = url; }}};
  for (const [name, store] of [['localStorage', local], ['sessionStorage', session]]) {
    Object.defineProperty(window, name, {get() {
      if (blocked) throw new Error('Storage blocked');
      return {getItem: key => store.get(key) ?? null, setItem: (key, value) => store.set(key, value)};
    }});
  }
  const document = {
    documentElement: {lang: language},
    querySelectorAll: selector => selector === '[data-year]' ? [year] : (prompt ? [switchLink, promptLink] : [switchLink]),
    querySelector: selector => ({'.language-switch': switchLink, '.language-prompt': prompt, '[data-dismiss-language]': prompt ? dismiss : null}[selector])
  };
  vm.runInNewContext(source, {document, window, navigator: {languages: [preferred], language: preferred}, URL, Date});
  return {local, session, window, prompt, year, switchLink, listeners};
}

test('Spanish browser gets an optional prompt without an automatic redirect', () => {
  const p = page({preferred: 'es-MX'});
  assert.equal(p.prompt.hidden, false);
  assert.equal(p.window.location.redirect, undefined);
});
test('English browser keeps a visible switch without a suggestion', () => {
  const p = page();
  assert.equal(p.prompt.hidden, true);
  assert.ok(p.switchLink.href.endsWith('es/contact.html'));
});
test('Spanish prompt can be dismissed for this session', () => {
  const p = page({preferred: 'es-US'});
  p.listeners.dismiss();
  assert.equal(p.prompt.hidden, true);
  assert.equal(p.session.get('bennys-language-prompt-dismissed'), 'yes');
  assert.equal(p.switchLink.focused, true);
  assert.equal(page({preferred: 'es-US', dismissed: 'yes'}).prompt.hidden, true);
});
test('A language choice persists and preserves the current section', () => {
  const p = page({hash: '#services'});
  p.listeners.switch();
  assert.equal(p.local.get('bennys-language'), 'es');
  assert.equal(p.switchLink.href, 'https://bennystreeservices.com/es/contact.html#services');
});
test('A saved Spanish choice reopens the equivalent Spanish page', () => {
  const p = page({saved: 'es', hash: '#about'});
  assert.equal(p.window.location.redirect, 'https://bennystreeservices.com/es/contact.html#about');
});
test('An explicit English choice overrides a Spanish browser preference', () => {
  assert.equal(page({saved: 'en', preferred: 'es-US'}).prompt.hidden, true);
  const p = page({language: 'es', saved: 'en'});
  assert.equal(p.window.location.redirect, 'https://bennystreeservices.com/contact.html');
});
test('Blocked browser storage never breaks contact links or language switching', () => {
  const p = page({preferred: 'es', blocked: true});
  assert.equal(p.prompt.hidden, false);
  assert.doesNotThrow(() => p.listeners.switch());
  assert.doesNotThrow(() => p.listeners.dismiss());
  assert.equal(p.prompt.hidden, true);
});
test('Spanish pages do not show a translation prompt', () => {
  const p = page({language: 'es', preferred: 'es-US'});
  assert.equal(p.prompt, null);
  assert.equal(p.switchLink.dataset.languageChoice, 'en');
  assert.equal(p.year.textContent, new Date().getFullYear());
});
