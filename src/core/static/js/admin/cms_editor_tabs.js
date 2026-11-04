/**
 * Вкладки Контент | SEO у CMS-редакторі.
 */
(function () {
  "use strict";

  function activate(root, name) {
    root.querySelectorAll("[data-cms-tab]").forEach(function (btn) {
      var on = btn.getAttribute("data-cms-tab") === name;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-selected", on ? "true" : "false");
    });
    root.querySelectorAll("[data-cms-panel]").forEach(function (panel) {
      var on = panel.getAttribute("data-cms-panel") === name;
      panel.hidden = !on;
    });
    try {
      window.sessionStorage.setItem(
        "cms-editor-tab:" + window.location.pathname,
        name
      );
    } catch (e) {}
  }

  function initForm(form) {
    if (!form || form.getAttribute("data-cms-tabs") !== "1") return;
    if (form.getAttribute("data-cms-tabs-ready") === "1") return;
    form.setAttribute("data-cms-tabs-ready", "1");

    var saved = "";
    try {
      saved =
        window.sessionStorage.getItem(
          "cms-editor-tab:" + window.location.pathname
        ) || "";
    } catch (e) {}
    if (saved === "seo" || saved === "content") {
      activate(form, saved);
    }

    form.querySelectorAll("[data-cms-tab]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        activate(form, btn.getAttribute("data-cms-tab"));
      });
    });
  }

  function scan() {
    document.querySelectorAll("form[data-cms-tabs='1']").forEach(initForm);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
  } else {
    scan();
  }
})();
