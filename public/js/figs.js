(function () {
  var openBtn = document.querySelector("[data-figs-open]");
  var closeBtn = document.querySelector("[data-figs-close]");
  var drawer = document.querySelector("[data-figs-drawer]");

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

(function () {
  var dataEl = document.getElementById("figs-products-data");
  var modal = document.getElementById("figs-product-modal");

  if (!dataEl || !modal) return;

  var products = [];
  try {
    products = JSON.parse(dataEl.textContent || "[]");
  } catch (error) {
    return;
  }

  var productsById = {};
  var colorsByCode = {};
  products.forEach(function (product) {
    productsById[product.id] = product;
    product.colores.forEach(function (color) {
      if (color.codigo) colorsByCode[color.codigo.toLowerCase()] = color;
    });
  });

  var cards = Array.prototype.slice.call(
    document.querySelectorAll(".figs-product[data-product-id]")
  );
  cards.forEach(function (card) {
    var image = card.querySelector(".figs-product__media img");
    if (image && !image.getAttribute("data-default-src")) {
      image.setAttribute("data-default-src", image.getAttribute("src"));
    }
  });
  var colorLinks = Array.prototype.slice.call(
    document.querySelectorAll(".figs-color[data-color]")
  );
  var filterBar = document.getElementById("figs-color-filter");
  var filterName = document.getElementById("figs-filter-name");
  var filterSwatch = document.getElementById("figs-filter-swatch");
  var filterClear = document.getElementById("figs-filter-clear");

  var panel = modal.querySelector(".figs-modal__panel");
  var closeButton = modal.querySelector(".figs-modal__close");
  var modalImage = document.getElementById("figs-modal-img");
  var modalBadge = document.getElementById("figs-modal-badge");
  var modalTitle = document.getElementById("figs-modal-title");
  var modalPrice = document.getElementById("figs-modal-price");
  var modalColors = document.getElementById("figs-modal-colors");
  var modalColorLabel = document.getElementById("figs-modal-color-label");
  var modalSizes = document.getElementById("figs-modal-sizes");
  var modalQty = document.getElementById("figs-modal-qty");
  var modalError = document.getElementById("figs-modal-error");
  var modalCta = document.getElementById("figs-modal-cta");
  var modalPhotoNote = document.getElementById("figs-modal-photo-note");

  if (
    !panel ||
    !closeButton ||
    !modalImage ||
    !modalColors ||
    !modalSizes ||
    !modalQty ||
    !modalError ||
    !modalCta
  ) {
    return;
  }

  var activeColor = "";
  var currentProduct = null;
  var selectedColor = "";
  var selectedSize = "";
  var lastFocused = null;

  function normalize(value) {
    return (value || "").toLowerCase();
  }

  function colorLabel(color) {
    if (!color) return "";
    if (color.nombre) {
      return color.nombre + (color.codigo ? " (" + color.codigo + ")" : "");
    }
    return color.codigo || color.hex || "";
  }

  function colorPhoto(product, color) {
    if (!product) return "";
    if (!color || !color.codigo) return product.imagen;
    var photos = product.fotosPorColor || {};
    return photos[normalize(color.codigo)] || product.imagen;
  }

  function preloadPhotos(product) {
    var photos = product && product.fotosPorColor;
    if (!photos) return;
    Object.keys(photos).forEach(function (code) {
      var image = new Image();
      image.src = photos[code];
    });
  }

  function setFilter(hex, code, name, shouldScroll, preserveProduct) {
    activeColor = normalize(hex);
    cards.forEach(function (card) {
      var cardColors = (card.getAttribute("data-colores") || "").split(/\s+/);
      var matches = !activeColor || cardColors.indexOf(activeColor) !== -1;
      card.hidden = !matches;

      var image = card.querySelector(".figs-product__media img");
      if (!image) return;
      var defaultSrc =
        image.getAttribute("data-default-src") || image.getAttribute("src");
      var product = productsById[card.getAttribute("data-product-id")];
      if (!product) return;
      var color = activeColor
        ? product.colores.find(function (item) {
            return normalize(item.hex) === activeColor;
          })
        : null;
      var nextSrc = color ? colorPhoto(product, color) : defaultSrc;
      if (image.getAttribute("src") !== nextSrc) {
        image.setAttribute("src", nextSrc);
      }
    });

    colorLinks.forEach(function (link) {
      var isActive =
        !!activeColor &&
        normalize(link.getAttribute("data-color")) === activeColor;
      link.classList.toggle("is-active", isActive);
    });

    if (filterBar) {
      if (activeColor) {
        filterBar.hidden = false;
        if (filterName) {
          filterName.textContent = name
            ? name + (code ? " (" + code + ")" : "")
            : code || "";
        }
        if (filterSwatch) filterSwatch.style.setProperty("--c", hex);
      } else {
        filterBar.hidden = true;
      }
    }

    var url = new URL(window.location.href);
    if (code) url.searchParams.set("color", code);
    else url.searchParams.delete("color");
    if (!preserveProduct) {
      url.searchParams.delete("product");
      url.searchParams.delete("size");
    }
    history.replaceState(null, "", url.pathname + url.search + url.hash);

    if (shouldScroll) {
      var section = document.getElementById("productos");
      if (section) section.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  colorLinks.forEach(function (link) {
    link.addEventListener("click", function (event) {
      event.preventDefault();
      setFilter(
        link.getAttribute("data-color"),
        link.getAttribute("data-code"),
        link.getAttribute("data-name"),
        true,
        false
      );
    });
  });

  if (filterClear) {
    filterClear.addEventListener("click", function () {
      setFilter("", "", "", false, false);
    });
  }

  function updateColor() {
    Array.prototype.forEach.call(modalColors.children, function (button) {
      var isSelected =
        normalize(button.style.getPropertyValue("--c")) === normalize(selectedColor);
      button.classList.toggle("is-selected", isSelected);
      button.setAttribute("aria-pressed", isSelected ? "true" : "false");
    });

    if (currentProduct) {
      var color = currentProduct.colores.find(function (item) {
        return normalize(item.hex) === normalize(selectedColor);
      });
      if (modalColorLabel) modalColorLabel.textContent = colorLabel(color);

      var photo = colorPhoto(currentProduct, color);
      if (photo && modalImage.getAttribute("src") !== photo) {
        modalImage.setAttribute("src", photo);
      }
      modalImage.alt =
        currentProduct.nombre + (color ? " - " + colorLabel(color) : "");

      if (modalPhotoNote) {
        var hasCustomPhoto = !!(
          color &&
          color.codigo &&
          currentProduct.fotosPorColor &&
          currentProduct.fotosPorColor[normalize(color.codigo)]
        );
        modalPhotoNote.hidden = !color || hasCustomPhoto;
      }
    }
  }

  function updateSize() {
    Array.prototype.forEach.call(modalSizes.children, function (button) {
      var isSelected = button.getAttribute("data-size") === selectedSize;
      button.classList.toggle("is-selected", isSelected);
      button.setAttribute("aria-pressed", isSelected ? "true" : "false");
    });
  }

  function openModal(productId, colorHex, size) {
    var product = productsById[productId];
    if (!product) return;

    currentProduct = product;
    selectedSize = "";
    selectedColor = "";

    var requestedColor = normalize(colorHex);
    var colorMatch = product.colores.find(function (color) {
      return normalize(color.hex) === requestedColor;
    });
    if (!colorMatch && activeColor) {
      colorMatch = product.colores.find(function (color) {
        return normalize(color.hex) === activeColor;
      });
    }
    selectedColor = colorMatch
      ? colorMatch.hex
      : product.colores[0]
        ? product.colores[0].hex
        : "";

    modalImage.setAttribute("src", product.imagen);
    modalImage.alt = product.nombre;
    preloadPhotos(product);
    modalTitle.textContent = product.nombre;
    modalPrice.textContent = product.precio;

    if (product.badge) {
      modalBadge.textContent = product.badge;
      modalBadge.hidden = false;
    } else {
      modalBadge.hidden = true;
    }

    modalColors.innerHTML = "";
    product.colores.forEach(function (color) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "figs-modal__color";
      button.style.setProperty("--c", color.hex);
      button.title = colorLabel(color);
      button.setAttribute("aria-label", colorLabel(color));
      button.setAttribute("aria-pressed", "false");
      button.addEventListener("click", function () {
        selectedColor = color.hex;
        updateColor();
      });
      modalColors.appendChild(button);
    });

    modalSizes.innerHTML = "";
    product.tallas.forEach(function (talla) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "figs-modal__size";
      button.textContent = talla;
      button.setAttribute("data-size", talla);
      button.setAttribute("aria-pressed", "false");
      button.addEventListener("click", function () {
        selectedSize = talla;
        modalError.hidden = true;
        updateSize();
      });
      modalSizes.appendChild(button);
    });

    if (size) {
      var wantedSize = String(size).toUpperCase();
      var sizeMatch = product.tallas.find(function (talla) {
        return talla.toUpperCase() === wantedSize;
      });
      if (sizeMatch) selectedSize = sizeMatch;
    }

    modalQty.value = "1";
    modalError.hidden = true;
    updateColor();
    updateSize();

    lastFocused = document.activeElement;
    modal.hidden = false;
    document.body.classList.add("figs-modal-open");
    closeButton.focus();
  }

  function closeModal() {
    if (modal.hidden) return;
    modal.hidden = true;
    document.body.classList.remove("figs-modal-open");
    if (lastFocused && typeof lastFocused.focus === "function") {
      lastFocused.focus();
    }
  }

  Array.prototype.forEach.call(
    document.querySelectorAll(
      ".figs-product__open, .figs-product__options, .figs-product__dot"
    ),
    function (button) {
      button.addEventListener("click", function (event) {
        event.preventDefault();
        openModal(
          button.getAttribute("data-product-id"),
          button.getAttribute("data-color"),
          ""
        );
      });
    }
  );

  Array.prototype.forEach.call(
    document.querySelectorAll(".figs-product[data-product-id]"),
    function (card) {
      card.addEventListener("click", function (event) {
        if (event.target.closest("button, a")) return;
        openModal(card.getAttribute("data-product-id"), "", "");
      });
    }
  );

  Array.prototype.forEach.call(
    modal.querySelectorAll("[data-modal-close]"),
    function (element) {
      element.addEventListener("click", closeModal);
    }
  );

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !modal.hidden) closeModal();
  });

  panel.addEventListener("keydown", function (event) {
    if (event.key !== "Tab") return;

    var focusable = panel.querySelectorAll(
      'button:not([disabled]), input:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])'
    );
    if (!focusable.length) return;

    var first = focusable[0];
    var last = focusable[focusable.length - 1];

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  modalCta.addEventListener("click", function () {
    if (!currentProduct) return;

    if (!selectedSize) {
      modalError.hidden = false;
      var firstSize = modalSizes.querySelector(".figs-modal__size");
      if (firstSize) firstSize.focus();
      return;
    }

    var color = currentProduct.colores.find(function (item) {
      return normalize(item.hex) === normalize(selectedColor);
    });
    var quantity = parseInt(modalQty.value, 10);
    if (!quantity || quantity < 1) {
      quantity = 1;
      modalQty.value = "1";
    }

    var detailColor = colorLabel(color) || selectedColor;
    var subject =
      "Cotización: " +
      currentProduct.nombre +
      " - " +
      detailColor +
      " - " +
      selectedSize;
    var body =
      "Hola, quiero cotizar:\n\n" +
      "Producto: " +
      currentProduct.nombre +
      "\nColor: " +
      detailColor +
      "\nTalla: " +
      selectedSize +
      "\nCantidad: " +
      quantity +
      "\n\nGracias.";

    window.location.href =
      "mailto:hola@wearonoff.com?subject=" +
      encodeURIComponent(subject) +
      "&body=" +
      encodeURIComponent(body);
  });

  var initialParams = new URLSearchParams(window.location.search);
  var initialCode = initialParams.get("color");
  var initialProductId = initialParams.get("product");

  if (initialCode) {
    var initialLink = colorLinks.find(function (link) {
      return normalize(link.getAttribute("data-code")) === normalize(initialCode);
    });
    if (initialLink) {
      setFilter(
        initialLink.getAttribute("data-color"),
        initialLink.getAttribute("data-code"),
        initialLink.getAttribute("data-name"),
        !initialProductId,
        !!initialProductId
      );
    }
  }

  if (initialProductId && productsById[initialProductId]) {
    var initialColor = initialCode ? colorsByCode[normalize(initialCode)] : null;
    var initialHex = initialColor ? initialColor.hex : initialCode;
    openModal(initialProductId, initialHex || "", initialParams.get("size") || "");
  }
})();
