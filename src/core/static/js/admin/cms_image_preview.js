(function () {
  document.addEventListener("change", function (event) {
    var input = event.target;
    if (!input.matches || !input.matches("[data-cms-image] input[type=file]")) {
      return;
    }
    var box = input.closest("[data-cms-image]");
    var img = box && box.querySelector("img");
    var file = input.files && input.files[0];
    if (!img || !file) {
      return;
    }
    img.src = URL.createObjectURL(file);
    img.hidden = false;
  });
})();
