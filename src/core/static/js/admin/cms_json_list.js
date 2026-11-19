/**
 * Додати / прибрати рядки списків експертизи та карʼєри.
 */
(function () {
  "use strict";

  function closestList(node) {
    return node && node.closest ? node.closest("[data-cms-list]") : null;
  }

  function addRow(list) {
    var template = list.querySelector("[data-cms-list-template]");
    var rows = list.querySelector("[data-cms-list-rows]");
    if (!template || !rows || !template.content) return;
    var node = template.content.cloneNode(true);
    rows.appendChild(node);
    var input = rows.querySelector("[data-cms-list-row]:last-child input");
    if (input) input.focus();
  }

  function removeRow(button) {
    var row = button.closest("[data-cms-list-row]");
    if (!row) return;
    var list = closestList(row);
    var rows = list ? list.querySelectorAll("[data-cms-list-row]") : [];
    if (rows.length <= 1) {
      row.querySelectorAll("input").forEach(function (input) {
        input.value = "";
      });
      return;
    }
    row.remove();
  }

  document.addEventListener("click", function (event) {
    var add = event.target.closest("[data-cms-list-add]");
    if (add) {
      event.preventDefault();
      var list = closestList(add);
      if (list) addRow(list);
      return;
    }
    var remove = event.target.closest("[data-cms-list-remove]");
    if (remove) {
      event.preventDefault();
      removeRow(remove);
    }
  });
})();
