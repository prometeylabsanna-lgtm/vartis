/**
 * TinyMCE для textarea.cms-tinymce в адмінці.
 */
(function () {
  "use strict";

  var INIT_FLAG = "data-cms-tinymce-ready";
  var HAS_TAG = /<[a-z][\s\S]*>/i;

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function plainToHtml(raw) {
    var text = String(raw || "")
      .replace(/\r\n/g, "\n")
      .replace(/\r/g, "\n")
      .trim();
    if (!text) return "";
    if (HAS_TAG.test(text)) return text;
    return text
      .split(/\n\s*\n/)
      .map(function (b) {
        return b.replace(/\n+/g, " ").trim();
      })
      .filter(Boolean)
      .map(function (b) {
        return "<p>" + escapeHtml(b) + "</p>";
      })
      .join("");
  }

  function prepareTextareas() {
    document.querySelectorAll("textarea.cms-tinymce").forEach(function (ta) {
      if (ta.getAttribute("data-cms-plain-converted") === "1") return;
      ta.value = plainToHtml(ta.value);
      ta.setAttribute("data-cms-plain-converted", "1");
    });
  }

  function init() {
    if (!window.tinymce) return;
    if (!document.querySelectorAll("textarea.cms-tinymce").length) return;
    prepareTextareas();
    if (document.documentElement.getAttribute(INIT_FLAG) === "1") return;
    document.documentElement.setAttribute(INIT_FLAG, "1");
    window.tinymce.init({
      selector: "textarea.cms-tinymce",
      menubar: false,
      branding: false,
      promotion: false,
      height: 360,
      plugins: "lists link autolink",
      toolbar: "bold italic | bullist numlist | link | removeformat",
      valid_elements: "p,br,strong/b,em/i,ul,ol,li,a[href|target|rel|title]",
      forced_root_block: "p",
      convert_urls: false,
      content_style:
        "body{font-family:system-ui,-apple-system,sans-serif;font-size:15px;line-height:1.55;}" +
        "p{margin:0 0 0.75em;}p:last-child{margin-bottom:0;}",
      setup: function (editor) {
        editor.on("change keyup", function () {
          editor.save();
        });
      },
    });
  }

  function beforeSubmit() {
    if (window.tinymce) window.tinymce.triggerSave();
  }

  function onReady() {
    init();
    document.querySelectorAll("form").forEach(function (form) {
      form.addEventListener("submit", beforeSubmit);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
})();
