(function () {
  'use strict';

  const measurementId = 'G-XKJC1CGVS0';
  const consentKey = 'emiralili_analytics_consent';

  function loadAnalytics() {
    if (window.__emirAnalyticsLoaded) return;
    window.__emirAnalyticsLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', measurementId, { anonymize_ip: true });

    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(measurementId);
    document.head.appendChild(script);
  }

  function saveChoice(choice) {
    try { localStorage.setItem(consentKey, choice); } catch (_) {}
    document.querySelector('.analytics-consent')?.remove();
    const preferences = document.querySelector('.analytics-preferences');
    if (preferences) preferences.hidden = false;
    if (choice === 'granted') loadAnalytics();
    if (choice === 'denied' && window.__emirAnalyticsLoaded) window.location.reload();
  }

  function showBanner() {
    if (document.querySelector('.analytics-consent')) return;
    const preferences = document.querySelector('.analytics-preferences');
    if (preferences) preferences.hidden = true;
    const banner = document.createElement('section');
    banner.className = 'analytics-consent';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Preferenze statistiche');
    banner.innerHTML = '<div><strong>Misurazione del traffico</strong><p>Con il tuo consenso utilizziamo Google Analytics per capire quali contenuti vengono letti e migliorare il sito. Il rifiuto non limita la navigazione. <a href="/privacy-cookie.html">Privacy e cookie</a>.</p></div><div class="analytics-consent-actions"><button type="button" data-consent="denied">Rifiuta</button><button type="button" class="primary" data-consent="granted">Accetta</button></div>';
    banner.querySelectorAll('[data-consent]').forEach(function (button) {
      button.addEventListener('click', function () { saveChoice(button.dataset.consent); });
    });
    document.body.appendChild(banner);
  }

  function addPreferencesControl() {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'analytics-preferences';
    button.textContent = 'Preferenze cookie';
    button.addEventListener('click', showBanner);
    document.body.appendChild(button);
  }

  function init() {
    const stylesheet = document.createElement('link');
    stylesheet.rel = 'stylesheet';
    stylesheet.href = '/analytics.css?v=1';
    document.head.appendChild(stylesheet);

    let choice = null;
    try { choice = localStorage.getItem(consentKey); } catch (_) {}
    if (choice === 'granted') loadAnalytics();
    if (choice !== 'granted' && choice !== 'denied') showBanner();
    addPreferencesControl();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
