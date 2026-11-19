(function () {
  'use strict';

  var COOKIE = 'vartis_cookie_consent';

  function hasConsent() {
    return document.cookie.split(';').some(function (part) {
      return part.trim().indexOf(COOKIE + '=1') === 0;
    });
  }

  function setConsent() {
    var secure = window.location.protocol === 'https:' ? '; Secure' : '';
    document.cookie = COOKIE + '=1; Max-Age=31536000; Path=/; SameSite=Lax' + secure;
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

  if (hasConsent()) {
    loadGtm();
    return;
  }

  var banner = document.querySelector('[data-cookie-banner]');
  if (!banner) return;
  var accept = banner.querySelector('[data-action="accept-cookies"]');
  if (!accept) return;
  accept.addEventListener('click', function () {
    setConsent();
    loadGtm();
    banner.hidden = true;
  });
})();
