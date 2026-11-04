/**
 * Лічильник символів для CMS-полів з data-max-chars / maxlength.
 */
(function () {
  "use strict";

  function plainLength(value) {
    var raw = String(value || "");
    if (/<[a-z][\s\S]*>/i.test(raw)) {
      var tmp = document.createElement("div");
      tmp.innerHTML = raw;
      raw = tmp.textContent || tmp.innerText || "";
    }
    return raw.length;
  }

  function ensureCounter(el) {
    var max = parseInt(el.getAttribute("data-max-chars") || el.getAttribute("maxlength") || "0", 10);
    if (!max) return null;
    var host = el.closest(".site-content-editor__field, .form-row, .fieldBox, .flex") || el.parentNode;
    if (!host) return null;
    var counter = host.querySelector(".cms-char-counter");
    if (!counter) {
      counter = document.createElement("div");
      counter.className = "cms-char-counter";
      counter.setAttribute("aria-live", "polite");
      host.appendChild(counter);
    }
    counter.setAttribute("data-max", String(max));
    return counter;
  }

  function update(el, counter) {
    if (!counter) return;
    var max = parseInt(counter.getAttribute("data-max") || "0", 10);
    var len = plainLength(el.value);
    counter.textContent = len + " / " + max;
    counter.classList.toggle("is-over", len > max);
    counter.classList.toggle("is-warn", len > Math.floor(max * 0.9) && len <= max);
  }

  function bindField(el) {
    if (el.getAttribute("data-cms-counter") === "1") return;
    var counter = ensureCounter(el);
    if (!counter) return;
    el.setAttribute("data-cms-counter", "1");
    var sync = function () {
      update(el, counter);
    };
    el.addEventListener("input", sync);
    el.addEventListener("change", sync);
    sync();
  }

  function bindTiny() {
    if (!window.tinymce || !window.tinymce.editors) return;
    window.tinymce.editors.forEach(function (ed) {
      if (!ed || ed.__cmsCounterBound) return;
      var ta = ed.targetElm || ed.getElement();
      if (!ta) return;
      var max = parseInt(ta.getAttribute("data-max-chars") || "0", 10);
      if (!max) return;
      var counter = ensureCounter(ta);
      if (!counter) return;
      ed.__cmsCounterBound = true;
      var sync = function () {
        var text = ed.getContent({ format: "text" }) || "";
        counter.textContent = text.length + " / " + max;
        counter.classList.toggle("is-over", text.length > max);
        counter.classList.toggle("is-warn", text.length > Math.floor(max * 0.9) && text.length <= max);
      };
      ed.on("keyup change SetContent Undo Redo", sync);
      sync();
    });
  }

  function scan() {
    document
      .querySelectorAll("input[data-max-chars], textarea[data-max-chars], input[maxlength], textarea[maxlength]")
      .forEach(bindField);
    bindTiny();
  }

  function onReady() {
    scan();
    if (window.tinymce && window.tinymce.on) {
      window.tinymce.on("AddEditor", function () {
        setTimeout(bindTiny, 120);
      });
    }
    document.addEventListener("htmx:afterSwap", scan);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
})();
