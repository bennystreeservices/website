/* Copyright and optional language preference. Both languages work without JS. */
(() => {
  document.querySelectorAll('[data-year]').forEach(el => {
    el.textContent = new Date().getFullYear();
  });

  const languageKey = 'bennys-language';
  const dismissalKey = 'bennys-language-prompt-dismissed';
  const currentLanguage = document.documentElement.lang.split('-')[0];
  const choices = document.querySelectorAll('[data-language-choice]');
  const languageSwitch = document.querySelector('.language-switch');
  const prompt = document.querySelector('.language-prompt');

  // Storage may be unavailable in private or restricted browsing modes.
  function readStorage(type, key) {
    try { return window[type].getItem(key); } catch { return null; }
  }
  function writeStorage(type, key, value) {
    try { window[type].setItem(key, value); } catch { /* Links still work. */ }
  }

  function preserveSection(link) {
    if (window.location.hash) {
      const target = new URL(link.href, window.location.href);
      target.hash = window.location.hash;
      link.href = target.href;
    }
  }

  choices.forEach(link => {
    preserveSection(link);
    link.addEventListener('click', () => {
      preserveSection(link);
      writeStorage('localStorage', languageKey, link.dataset.languageChoice);
    });
  });

  // Only an explicit past choice causes a redirect. Browser language alone
  // suggests Spanish without changing the page or interrupting the visitor.
  const savedLanguage = readStorage('localStorage', languageKey);
  if (languageSwitch && ['en', 'es'].includes(savedLanguage) && savedLanguage !== currentLanguage) {
    preserveSection(languageSwitch);
    window.location.replace(languageSwitch.href);
    return;
  }

  const preferredLanguage = (navigator.languages?.[0] || navigator.language || '').split('-')[0].toLowerCase();
  if (prompt && currentLanguage === 'en' && !savedLanguage && preferredLanguage === 'es' &&
      readStorage('sessionStorage', dismissalKey) !== 'yes') {
    prompt.hidden = false;
  }

  document.querySelector('[data-dismiss-language]')?.addEventListener('click', () => {
    if (prompt) prompt.hidden = true;
    writeStorage('sessionStorage', dismissalKey, 'yes');
    languageSwitch?.focus();
  });
})();
