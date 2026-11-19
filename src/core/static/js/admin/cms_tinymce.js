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

  function isDark() {
    return document.documentElement.classList.contains("dark");
  }

  function editorContentStyle(article) {
    var dark = isDark();
    var color = dark ? "#f4efe6" : "#12263a";
    var bg = dark ? "#0b1626" : "#ffffff";
    var css =
      "body{font-family:Roboto,-apple-system,'Segoe UI',Arial,sans-serif;" +
      "font-size:15px;line-height:1.55;color:" + color + ";background:" + bg + ";}" +
      "p{margin:0 0 0.75em;}p:last-child{margin-bottom:0;}" +
      "ul,ol{margin:0 0 0.75em;padding-left:1.25em;}" +
      "a{color:#b58b4a;}";
    if (article) {
      css +=
        "h2{font-size:1.35em;font-weight:700;margin:1em 0 0.45em;color:" + color + ";}" +
        "blockquote.art-note{border:1.5px solid #b58b4a;border-radius:24px;" +
        "padding:16px 20px;margin:0.85em 0;}";
    }
    return css;
  }

  function paintEditor(editor) {
    var body = editor.getBody && editor.getBody();
    if (!body) return;
    var dark = isDark();
    var color = dark ? "#f4efe6" : "#12263a";
    var bg = dark ? "#0b1626" : "#ffffff";
    body.style.color = color;
    body.style.backgroundColor = bg;
    var doc = editor.getDoc && editor.getDoc();
    if (!doc) return;
    if (doc.documentElement) {
      doc.documentElement.style.backgroundColor = bg;
    }
    var style = doc.getElementById("cms-theme-contrast");
    if (!style) {
      style = doc.createElement("style");
      style.id = "cms-theme-contrast";
      (doc.head || doc.documentElement).appendChild(style);
    }
    style.textContent =
      "html,body,body.mce-content-body{color:" + color + ";background:" + bg + ";}";
  }

  function eachEditor(fn) {
    if (!window.tinymce) return;
    var list = typeof window.tinymce.get === "function" ? window.tinymce.get() : null;
    if (Array.isArray(list) && list.length) {
      list.forEach(fn);
      return;
    }
    if (window.tinymce.activeEditor) {
      fn(window.tinymce.activeEditor);
    }
  }

  function paintAllEditors() {
    eachEditor(paintEditor);
  }

  var VALID_BASE =
    "p[style],br,strong/b,em/i,u,ul,ol,li,a[href|target|rel|title],span[style]";

  function bindSave(editor) {
    editor.on("init", function () {
      paintEditor(editor);
    });
    editor.on("change keyup", function () {
      editor.save();
    });
  }

  function registerArticleTools(editor) {
    editor.on("PreInit", function () {
      editor.formatter.register("artnote", {
        block: "blockquote",
        classes: "art-note",
        wrapper: true,
      });
    });
    editor.ui.registry.addToggleButton("cmsheading", {
      text: "Заголовок",
      tooltip: "Заголовок",
      onAction: function () {
        var heading = editor.formatter.match("h2");
        editor.execCommand("FormatBlock", false, heading ? "p" : "h2");
      },
      onSetup: function (api) {
        function sync() {
          api.setActive(!!editor.formatter.match("h2"));
        }
        editor.on("NodeChange", sync);
        return function () {
          editor.off("NodeChange", sync);
        };
      },
    });
    editor.ui.registry.addToggleButton("cmsframe", {
      text: "Рамка",
      tooltip: "Рамка для виділеного блоку",
      onAction: function () {
        editor.formatter.toggle("artnote");
      },
      onSetup: function (api) {
        function sync() {
          api.setActive(!!editor.formatter.match("artnote"));
        }
        editor.on("NodeChange", sync);
        return function () {
          editor.off("NodeChange", sync);
        };
      },
    });
  }

  function baseConfig() {
    return {
      menubar: false,
      branding: false,
      promotion: false,
      toolbar_mode: "wrap",
      plugins: "lists link autolink",
      font_family_formats:
        "Roboto=Roboto, -apple-system, Segoe UI, Arial, sans-serif;" +
        "Arial=Arial, Helvetica, sans-serif;" +
        "Georgia=Georgia, serif;" +
        "Times New Roman='Times New Roman', Times, serif;" +
        "Courier New='Courier New', Courier, monospace",
      font_size_formats: "12px 14px 16px 18px 20px 24px 28px",
      color_map: [
        "#12263a", "Текст",
        "#ffffff", "Білий",
        "#b58b4a", "Золото",
        "#d4b072", "Світле золото",
        "#5a6270", "Сірий",
        "#d64545", "Червоний",
        "#f4e6c3", "Підсвітка",
        "#0b1626", "Темний",
      ],
      color_default_foreground: "#12263a",
      color_default_background: "#f4e6c3",
      forced_root_block: "p",
      convert_urls: false,
      link_default_target: "_blank",
      link_assume_external_targets: true,
      content_css:
        "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700&display=swap",
    };
  }

  function init() {
    if (!window.tinymce) return;
    if (!document.querySelectorAll("textarea.cms-tinymce").length) return;
    prepareTextareas();
    if (document.documentElement.getAttribute(INIT_FLAG) === "1") return;
    document.documentElement.setAttribute(INIT_FLAG, "1");
    var shared = baseConfig();
    window.tinymce.init(
      Object.assign({}, shared, {
        selector: "textarea.cms-tinymce:not(.cms-tinymce--article)",
        height: 380,
        toolbar:
          "undo redo | fontsize | bold italic underline | " +
          "forecolor backcolor | bullist numlist | link unlink | removeformat",
        valid_elements: VALID_BASE,
        content_style: editorContentStyle(false),
        setup: bindSave,
      })
    );
    if (document.querySelector("textarea.cms-tinymce--article")) {
      window.tinymce.init(
        Object.assign({}, shared, {
          selector: "textarea.cms-tinymce.cms-tinymce--article",
          height: 520,
          toolbar:
            "undo redo | cmsheading cmsframe | fontsize | bold italic underline | " +
            "forecolor backcolor | bullist numlist | link unlink | removeformat",
          valid_elements: VALID_BASE + ",h2,h3,blockquote[class]",
          content_style: editorContentStyle(true),
          setup: function (editor) {
            registerArticleTools(editor);
            bindSave(editor);
          },
        })
      );
    }
    var html = document.documentElement;
    if (window.MutationObserver && !html.getAttribute("data-cms-tinymce-theme")) {
      html.setAttribute("data-cms-tinymce-theme", "1");
      new MutationObserver(paintAllEditors).observe(html, {
        attributes: true,
        attributeFilter: ["class"],
      });
    }
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
