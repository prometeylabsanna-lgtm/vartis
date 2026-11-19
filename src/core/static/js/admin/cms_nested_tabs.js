(function () {
  function groupTabs() {
    var nav = document.querySelector(".tabs, .unfold-tabs, nav[role='tablist']");
    if (!nav || nav.dataset.cmsGrouped) {
      return;
    }
    var buttons = nav.querySelectorAll("a, button");
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
    var names = Object.keys(groups);
    if (!names.length) {
      return;
    }
    nav.dataset.cmsGrouped = "1";
    names.forEach(function (name) {
      groups[name].forEach(function (item) {
        item.btn.textContent = item.sub;
      });
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", groupTabs);
  } else {
    groupTabs();
  }
})();
