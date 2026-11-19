(function () {
  'use strict';

  var COOKIE = 'vartis_cookie_consent';

  function cookieSuffix() {
    var secure = window.location.protocol === 'https:' ? '; Secure' : '';
    return '; Path=/; SameSite=Lax' + secure;
  }

  function hasConsent() {
    return document.cookie.split(';').some(function (part) {
      return part.trim().indexOf(COOKIE + '=1') === 0;
    });
  }

  function setConsent() {
    document.cookie = COOKIE + '=1; Max-Age=31536000' + cookieSuffix();
  }

  function clearConsent() {
    document.cookie = COOKIE + '=; Max-Age=0' + cookieSuffix();
  }

  function loadGtm() {
    var id = document.documentElement.getAttribute('data-gtm-id');
    if (!id || window.__vartisGtmLoaded) return;
    window.__vartisGtmLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(id);
    document.head.appendChild(script);
  }

  var banner = document.querySelector('[data-cookie-banner]');

  function showBanner() {
    if (!banner) return;
    banner.hidden = false;
    banner.removeAttribute('hidden');
  }

  function hideBanner() {
    if (!banner) return;
    banner.hidden = true;
  }

  if (hasConsent()) {
    hideBanner();
    loadGtm();
  } else {
    showBanner();
  }

  if (banner) {
    var accept = banner.querySelector('[data-action="accept-cookies"]');
    if (accept) {
      accept.addEventListener('click', function () {
        setConsent();
        loadGtm();
        hideBanner();
      });
    }
  }

  document.querySelectorAll('[data-action="reset-cookies"]').forEach(function (el) {
    el.addEventListener('click', function (event) {
      event.preventDefault();
      clearConsent();
      window.__vartisGtmLoaded = false;
      showBanner();
    });
  });
})();
