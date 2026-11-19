(function () {
  function iconData() {
    var node = document.getElementById("cms-icon-data");
    if (!node) {
      return {};
    }
    try {
      return JSON.parse(node.textContent || "{}");
    } catch (error) {
      return {};
    }
  }

  document.addEventListener("change", function (event) {
    var input = event.target;
    if (!input.matches || !input.matches("[data-cms-image] input[type=file]")) {
      return;
    }
    var box = input.closest("[data-cms-image]");
    var file = input.files && input.files[0];
    if (!box || !file) {
      return;
    }
    var url = URL.createObjectURL(file);
    box.querySelectorAll("[data-cms-preview]").forEach(function (node) {
      if (node.tagName === "IMG") {
        node.src = url;
      } else {
        node.style.backgroundImage = "url('" + url + "')";
      }
      node.hidden = false;
    });
  });

  document.addEventListener("input", function (event) {
    var input = event.target;
    var box = input.closest && input.closest("[data-cms-icon]");
    if (!box || input.tagName !== "INPUT") {
      return;
    }
    var data = iconData()[input.value];
    var pic = box.querySelector(".cms-icon__pic");
    if (!data) {
      if (pic) {
        pic.hidden = true;
      }
      return;
    }
    if (!pic) {
      pic = document.createElement("span");
      pic.className = "cms-icon__pic";
      box.insertBefore(pic, box.firstChild);
    }
    pic.hidden = false;
    pic.innerHTML =
      '<svg width="28" height="28" viewBox="' +
      data.viewBox +
      '" fill="none" aria-hidden="true">' +
      data.body +
      "</svg>";
  });
})();
