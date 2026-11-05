(function () {
  var openBtn = document.querySelector("[data-wearonoff-open]");
  var closeBtn = document.querySelector("[data-wearonoff-close]");
  var drawer = document.querySelector("[data-wearonoff-drawer]");

  if (!drawer) return;

  function setOpen(open) {
    drawer.classList.toggle("is-open", open);
    document.body.style.overflow = open ? "hidden" : "";
    if (openBtn) openBtn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  if (openBtn) {
    openBtn.addEventListener("click", function () {
      setOpen(true);
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener("click", function () {
      setOpen(false);
    });
  }

  drawer.addEventListener("click", function (event) {
    if (event.target === drawer) setOpen(false);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") setOpen(false);
  });
})();
