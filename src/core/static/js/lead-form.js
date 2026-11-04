(function () {
  'use strict';

  var NAME_RE = /^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ'ʼ’\-\s]{2,120}$/;
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  var MSG = {
    required: "Поле обов'язкове для заповнення",
    name: "Ім'я може містити лише літери, пробіл, дефіс або апостроф",
    phone: 'Введіть номер у форматі +380XXXXXXXXX або 0XXXXXXXXX',
    email: 'Введіть коректну електронну пошту',
    consent: 'Потрібна згода на обробку даних',
  };

  function digitsOnly(value) {
    return String(value || '').replace(/\D/g, '');
  }

  function isUaPhone(value) {
    var d = digitsOnly(value);
    return (d.indexOf('380') === 0 && d.length === 12) ||
      (d.charAt(0) === '0' && d.length === 10);
  }

  function fieldWrap(input) {
    return input.closest('.lead-form__label') ||
      input.closest('.lead-form__consent') ||
      input.parentElement;
  }

  function errorEl(input) {
    var wrap = fieldWrap(input);
    if (!wrap) return null;
    var el = wrap.querySelector('.lead-form__error');
    if (el) return el;
    if (input.getAttribute('data-validate') === 'consent') {
      var form = input.closest('.lead-form');
      return form ? form.querySelector('[data-error-for="consent"]') : null;
    }
    return null;
  }

  function setError(input, message) {
    input.classList.add('is-invalid');
    input.setAttribute('aria-invalid', 'true');
    var el = errorEl(input);
    if (el) el.textContent = message || '';
  }

  function clearError(input) {
    input.classList.remove('is-invalid');
    input.removeAttribute('aria-invalid');
    var el = errorEl(input);
    if (el) el.textContent = '';
  }

  function validateField(input) {
    var type = input.getAttribute('data-validate');
    if (!type) return true;

    if (type === 'consent') {
      if (!input.checked) {
        setError(input, MSG.consent);
        return false;
      }
      clearError(input);
      return true;
    }

    var value = (input.value || '').trim();
    if (!value) {
      setError(input, MSG.required);
      return false;
    }

    if (type === 'name') {
      var name = value.replace(/\s+/g, ' ');
      if (name.length < 2 || !NAME_RE.test(name)) {
        setError(input, name.length < 2 ? MSG.required : MSG.name);
        return false;
      }
    }

    if (type === 'phone' && !isUaPhone(value)) {
      setError(input, MSG.phone);
      return false;
    }

    if (type === 'email' && !EMAIL_RE.test(value)) {
      setError(input, MSG.email);
      return false;
    }

    clearError(input);
    return true;
  }

  function validateForm(form) {
    var ok = true;
    var firstInvalid = null;
    form.querySelectorAll('[data-validate]').forEach(function (input) {
      if (!validateField(input)) {
        ok = false;
        if (!firstInvalid) firstInvalid = input;
      }
    });
    if (firstInvalid) {
      try { firstInvalid.focus(); } catch (e) { /* iOS Safari */ }
    }
    return ok;
  }

  function onSubmit(e) {
    var form = e.target;
    if (!form || !form.classList || !form.classList.contains('lead-form')) return;
    if (!validateForm(form)) {
      e.preventDefault();
      e.stopPropagation();
      if (typeof e.stopImmediatePropagation === 'function') {
        e.stopImmediatePropagation();
      }
      return;
    }
    var btn = form.querySelector('[type="submit"]');
    if (btn) {
      if (btn.getAttribute('aria-busy') === 'true') {
        e.preventDefault();
        e.stopPropagation();
        return;
      }
      btn.setAttribute('aria-busy', 'true');
      btn.disabled = true;
    }
  }

  document.addEventListener('submit', onSubmit, true);

  document.body.addEventListener('htmx:afterRequest', function (e) {
    var form = e.target;
    if (!form || !form.classList || !form.classList.contains('lead-form')) return;
    if (e.detail && e.detail.successful) return;
    var btn = form.querySelector('[type="submit"]');
    if (!btn) return;
    btn.disabled = false;
    btn.removeAttribute('aria-busy');
  });

  document.addEventListener('blur', function (e) {
    var input = e.target;
    if (!input || !input.getAttribute || !input.getAttribute('data-validate')) return;
    if (!input.closest('.lead-form')) return;
    validateField(input);
  }, true);

  document.addEventListener('input', function (e) {
    var input = e.target;
    if (!input || !input.classList || !input.classList.contains('is-invalid')) return;
    if (!input.closest('.lead-form')) return;
    validateField(input);
  }, true);

  document.addEventListener('change', function (e) {
    var input = e.target;
    if (!input || input.getAttribute('data-validate') !== 'consent') return;
    if (!input.closest('.lead-form')) return;
    validateField(input);
  }, true);
})();
