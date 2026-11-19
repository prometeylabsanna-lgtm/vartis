(function () {
  function shortenLabels(nav) {
    var buttons = nav.querySelectorAll(":scope > a, :scope > button");
    var groups = {};
    buttons.forEach(function (btn) {
      var label = (btn.textContent || "").trim();
      var parts = label.split(" — ");
      if (parts.length < 2) {
        return;
      }
      var group = parts[0];
      var sub = parts.slice(1).join(" — ");
      groups[group] = groups[group] || [];
      groups[group].push({ btn: btn, sub: sub });
    });
    Object.keys(groups).forEach(function (name) {
      groups[name].forEach(function (item) {
        item.btn.textContent = item.sub;
      });
    });
  }

  function markTabNavs() {
    document.querySelectorAll("form nav.flex.flex-col.items-center").forEach(function (nav) {
      if (nav.querySelectorAll(":scope > a").length < 2) {
        return;
      }
      nav.setAttribute("data-cms-tabs", "1");
      if (!nav.dataset.cmsGrouped) {
        nav.dataset.cmsGrouped = "1";
        shortenLabels(nav);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", markTabNavs);
  } else {
    markTabNavs();
  }
})();
