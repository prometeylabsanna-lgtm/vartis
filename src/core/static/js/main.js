(function () {
  'use strict';

  document.body.addEventListener('htmx:beforeSwap', function (e) {
    var s = e.detail.xhr.status;
    if (s === 400 || s === 422) {
      e.detail.shouldSwap = true;
      e.detail.isError = false;
    }
  });

  document.body.addEventListener('htmx:configRequest', function (e) {
    var csrf = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrf) {
      e.detail.headers['X-CSRFToken'] = csrf.value;
    }
  });

  var header = document.getElementById('site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  var burger = document.querySelector('[data-action="toggle-menu"]');
  var mobileNav = document.getElementById('mobile-nav');
  var lockScrollY = 0;

  function lockBodyScroll(on) {
    if (on) {
      if (document.body.classList.contains('modal-open') ||
          document.body.classList.contains('nav-open')) {
        return;
      }
      lockScrollY = window.scrollY || window.pageYOffset || 0;
      document.body.style.top = '-' + lockScrollY + 'px';
      return;
    }
    if (document.body.classList.contains('modal-open') ||
        document.body.classList.contains('nav-open')) {
      return;
    }
    document.body.style.top = '';
    window.scrollTo(0, lockScrollY);
  }

  function setMenu(open) {
    if (!burger || !mobileNav) return;
    if (open) lockBodyScroll(true);
    burger.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    mobileNav.classList.toggle('is-open', open);
    mobileNav.setAttribute('aria-hidden', open ? 'false' : 'true');
    document.body.classList.toggle('nav-open', open);
    if (!open) lockBodyScroll(false);
  }
  if (burger) {
    burger.addEventListener('click', function () {
      setMenu(!mobileNav.classList.contains('is-open'));
    });
  }
  document.querySelectorAll('[data-action="close-menu"]').forEach(function (el) {
    el.addEventListener('click', function () { setMenu(false); });
  });

  var svcWrap = document.querySelector('[data-svc]');
  if (svcWrap) {
    var svcBtn = svcWrap.querySelector('[data-action="toggle-svc"]');
    var svcTimer;
    function setSvc(open) {
      svcWrap.classList.toggle('is-open', open);
      if (svcBtn) svcBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    svcWrap.addEventListener('mouseenter', function () {
      clearTimeout(svcTimer);
      setSvc(true);
    });
    svcWrap.addEventListener('mouseleave', function () {
      clearTimeout(svcTimer);
      svcTimer = setTimeout(function () { setSvc(false); }, 150);
    });
    if (svcBtn) {
      svcBtn.addEventListener('click', function () {
        setSvc(!svcWrap.classList.contains('is-open'));
      });
    }
  }

  var modal = document.getElementById('lead-modal');
  var modalPanel = document.getElementById('modal-panel');
  var modalPanelInitial = modalPanel ? modalPanel.innerHTML : '';
  function setModal(open) {
    if (!modal) return;
    if (open && modalPanel && modalPanelInitial && !modalPanel.querySelector('form')) {
      modalPanel.innerHTML = modalPanelInitial;
      if (window.htmx) window.htmx.process(modalPanel);
    }
    if (open) lockBodyScroll(true);
    modal.classList.toggle('is-open', open);
    modal.setAttribute('aria-hidden', open ? 'false' : 'true');
    document.body.classList.toggle('modal-open', open);
    if (!open) lockBodyScroll(false);
  }
  document.querySelectorAll('[data-action="open-form"]').forEach(function (el) {
    el.addEventListener('click', function () {
      setMenu(false);
      setModal(true);
    });
  });
  document.querySelectorAll('[data-action="close-form"]').forEach(function (el) {
    el.addEventListener('click', function () { setModal(false); });
  });
  if (modal) {
    modal.addEventListener('click', function (e) {
      if (e.target === modal) setModal(false);
    });
  }

  document.querySelectorAll('[data-action="share-copy"]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var url = btn.getAttribute('data-url') || window.location.href;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () {
          btn.textContent = 'Скопійовано';
          setTimeout(function () { btn.textContent = 'Скопіювати посилання'; }, 1800);
        });
      }
    });
  });

  document.querySelectorAll('[data-action="toggle-faq"]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.faq-item');
      if (!item) return;
      var panel = item.querySelector('.faq-item__panel');
      var open = item.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (panel) {
        if (open) panel.removeAttribute('hidden');
        else panel.setAttribute('hidden', '');
      }
    });
  });

  var photoLb = document.getElementById('photo-lb');
  var photoImg = document.getElementById('photo-lb-img');
  var photoCap = document.getElementById('photo-lb-caption');
  function setPhotoLb(open, src, title) {
    if (!photoLb) return;
    if (open && photoImg) {
      lockBodyScroll(true);
      photoImg.src = src || '';
      photoImg.alt = title || '';
      if (photoCap) photoCap.textContent = title || '';
      photoLb.removeAttribute('hidden');
      photoLb.classList.add('is-open');
      photoLb.setAttribute('aria-hidden', 'false');
      document.body.classList.add('modal-open');
    } else {
      photoLb.classList.remove('is-open');
      photoLb.setAttribute('hidden', '');
      photoLb.setAttribute('aria-hidden', 'true');
      if (photoImg) photoImg.removeAttribute('src');
      document.body.classList.remove('modal-open');
      lockBodyScroll(false);
    }
  }
  document.querySelectorAll('[data-action="zoom-photo"]').forEach(function (el) {
    el.addEventListener('click', function () {
      setPhotoLb(true, el.getAttribute('data-src'), el.getAttribute('data-title'));
    });
  });
  document.querySelectorAll('[data-action="close-photo"]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.stopPropagation();
      setPhotoLb(false);
    });
  });
  if (photoLb) {
    photoLb.addEventListener('click', function (e) {
      if (e.target === photoLb) setPhotoLb(false);
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      setModal(false);
      setMenu(false);
      setPhotoLb(false);
      if (svcWrap) svcWrap.classList.remove('is-open');
    }
  });
})();
