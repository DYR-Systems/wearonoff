function wearonoffLocalize(root) {
  if (!root || !window.WearOnOffI18n) return;
  window.WearOnOffI18n.translate(root);
}

function wearonoffT(text, vars) {
  if (window.WearOnOffI18n && window.WearOnOffI18n.t) {
    return window.WearOnOffI18n.t(text, vars);
  }
  return text;
}

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

(function () {
  var dataEl = document.getElementById("wearonoff-products-data");
  var modal = document.getElementById("wearonoff-product-modal");

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
    document.querySelectorAll(".wearonoff-product[data-product-id]")
  );
  cards.forEach(function (card) {
    var image = card.querySelector(".wearonoff-product__media img");
    if (image && !image.getAttribute("data-default-src")) {
      image.setAttribute("data-default-src", image.getAttribute("src"));
    }
  });
  var colorLinks = Array.prototype.slice.call(
    document.querySelectorAll(".wearonoff-color[data-color]")
  );
  var filterBar = document.getElementById("wearonoff-color-filter");
  var filterName = document.getElementById("wearonoff-filter-name");
  var filterSwatch = document.getElementById("wearonoff-filter-swatch");
  var filterClear = document.getElementById("wearonoff-filter-clear");

  var panel = modal.querySelector(".wearonoff-modal__panel");
  var closeButton = modal.querySelector(".wearonoff-modal__close");
  var modalImage = document.getElementById("wearonoff-modal-img");
  var modalBadge = document.getElementById("wearonoff-modal-badge");
  var modalTitle = document.getElementById("wearonoff-modal-title");
  var modalPrice = document.getElementById("wearonoff-modal-price");
  var modalColors = document.getElementById("wearonoff-modal-colors");
  var modalColorLabel = document.getElementById("wearonoff-modal-color-label");
  var modalSizes = document.getElementById("wearonoff-modal-sizes");
  var modalQty = document.getElementById("wearonoff-modal-qty");
  var modalError = document.getElementById("wearonoff-modal-error");
  var modalCta = document.getElementById("wearonoff-modal-cta");
  var modalPhotoNote = document.getElementById("wearonoff-modal-photo-note");
  var modalStock = document.getElementById("wearonoff-modal-stock");

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
    return color.nombre || color.hex || "";
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

      var image = card.querySelector(".wearonoff-product__media img");
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
      wearonoffLocalize(filterBar);
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
      updateStock();
    }

    wearonoffLocalize(modal);
  }

  function variantStock(product, color, size) {
    if (!product || !color) return 0;
    var inventario = product.inventario || [];
    if (inventario.length) {
      var row = inventario.find(function (entry) {
        return (
          normalize(entry.codigo) === normalize(color.codigo) &&
          normalize(entry.talla) === normalize(size)
        );
      });
      return row ? Math.max(0, parseInt(row.stock, 10) || 0) : 0;
    }
    return Math.max(0, parseInt(product.stock, 10) || 0);
  }

  function updateStock() {
    if (!modalStock) return;
    if (!currentProduct) {
      modalStock.textContent = "";
      modalStock.classList.remove("is-out");
      return;
    }
    var color = currentProduct.colores.find(function (item) {
      return normalize(item.hex) === normalize(selectedColor);
    });
    if (!color) {
      modalStock.textContent = "";
      modalStock.classList.remove("is-out");
      return;
    }

    var hasInventory =
      Array.isArray(currentProduct.inventario) && currentProduct.inventario.length > 0;
    var total = hasInventory
      ? currentProduct.inventario.reduce(function (sum, row) {
          return sum + (parseInt(row.stock, 10) || 0);
        }, 0)
      : Math.max(0, parseInt(currentProduct.stock, 10) || 0);

    if (!hasInventory) {
      modalStock.textContent =
        total > 0
          ? "Stock total del diseño: " + total + " unidad(es)"
          : "Agotado.";
    } else if (selectedSize) {
      var quantity = variantStock(currentProduct, color, selectedSize);
      modalStock.textContent =
        quantity > 0
          ? "Disponible: " + quantity + " unidad(es)"
          : "Agotado para esta combinación.";
    } else {
      modalStock.textContent =
        total > 0
          ? "Stock total del diseño: " + total + " unidad(es)"
          : "Agotado.";
    }
    modalStock.classList.toggle(
      "is-out",
      hasInventory && selectedSize
        ? variantStock(currentProduct, color, selectedSize) <= 0
        : total <= 0
    );
    wearonoffLocalize(modal);
  }

  function updateSize() {
    Array.prototype.forEach.call(modalSizes.children, function (button) {
      var isSelected = button.getAttribute("data-size") === selectedSize;
      button.classList.toggle("is-selected", isSelected);
      button.setAttribute("aria-pressed", isSelected ? "true" : "false");
    });
    updateStock();
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
      button.className = "wearonoff-modal__color";
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
      button.className = "wearonoff-modal__size";
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
    wearonoffLocalize(modal);

    lastFocused = document.activeElement;
    modal.hidden = false;
    document.body.classList.add("wearonoff-modal-open");
    closeButton.focus();
  }

  function closeModal() {
    if (modal.hidden) return;
    modal.hidden = true;
    document.body.classList.remove("wearonoff-modal-open");
    if (lastFocused && typeof lastFocused.focus === "function") {
      lastFocused.focus();
    }
  }

  Array.prototype.forEach.call(
    document.querySelectorAll(
      ".wearonoff-product__open, .wearonoff-product__options, .wearonoff-product__dot"
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
    document.querySelectorAll(".wearonoff-product[data-product-id]"),
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
      modalError.textContent = "Selecciona una talla para continuar.";
      modalError.hidden = false;
      wearonoffLocalize(modalError);
      var firstSize = modalSizes.querySelector(".wearonoff-modal__size");
      if (firstSize) firstSize.focus();
      return;
    }

    var quantity = parseInt(modalQty.value, 10);
    if (!quantity || quantity < 1) {
      quantity = 1;
      modalQty.value = "1";
    }

    if (!window.WearOnOffCart) return;

    var result = window.WearOnOffCart.add(
      currentProduct.id,
      selectedColor,
      selectedSize,
      quantity
    );

    if (!result || !result.ok) {
      modalError.textContent =
        (result && result.message) || "No se pudo agregar al carrito.";
      modalError.hidden = false;
      wearonoffLocalize(modalError);
      return;
    }

    closeModal();
    window.WearOnOffCart.open();
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

(function () {
  var dataEl = document.getElementById("wearonoff-products-data");
  var cartRoot = document.getElementById("wearonoff-cart");
  if (!dataEl || !cartRoot) return;

  var products = [];
  try {
    products = JSON.parse(dataEl.textContent || "[]");
  } catch (error) {
    return;
  }

  var productsById = {};
  products.forEach(function (product) {
    productsById[product.id] = product;
  });

  var itemsEl = document.getElementById("wearonoff-cart-items");
  var emptyEl = document.getElementById("wearonoff-cart-empty");
  var whatsappEl = document.getElementById("wearonoff-cart-whatsapp");
  var clearEl = cartRoot.querySelector("[data-cart-clear]");
  var panel = cartRoot.querySelector(".wearonoff-cart__panel");
  if (!itemsEl || !emptyEl || !whatsappEl || !panel) return;

  var KEY = "wearonoff_cart_v1";
  var items = load();
  var lastFocused = null;

  function normalize(value) {
    return (value || "").toLowerCase();
  }

  function load() {
    try {
      var parsed = JSON.parse(localStorage.getItem(KEY) || "[]");
      return Array.isArray(parsed) ? parsed : [];
    } catch (error) {
      return [];
    }
  }

  function save() {
    try {
      localStorage.setItem(KEY, JSON.stringify(items));
    } catch (error) {
      return;
    }
    render();
  }

  function findProduct(productId) {
    return productsById[productId] || null;
  }

  function findColor(product, hex) {
    if (!product) return null;
    return (
      product.colores.find(function (color) {
        return normalize(color.hex) === normalize(hex);
      }) || null
    );
  }

  function findItem(key) {
    return (
      items.find(function (item) {
        return item.key === key;
      }) || null
    );
  }

  function lineKey(productId, colorHex, size) {
    return productId + "|" + normalize(colorHex) + "|" + size;
  }

  function hasInventory(product) {
    return Array.isArray(product.inventario) && product.inventario.length > 0;
  }

  function stockFor(product, color, size) {
    if (!product || !color) return 0;
    if (!hasInventory(product)) {
      return Math.max(0, parseInt(product.stock, 10) || 0);
    }
    var row = product.inventario.find(function (entry) {
      return (
        normalize(entry.codigo) === normalize(color.codigo) &&
        normalize(entry.talla) === normalize(size)
      );
    });
    return row ? Math.max(0, parseInt(row.stock, 10) || 0) : 0;
  }

  function lineCapacity(product, color, size, key) {
    if (hasInventory(product)) {
      return stockFor(product, color, size);
    }
    var totalStock = Math.max(0, parseInt(product.stock, 10) || 0);
    var otherQuantity = 0;
    items.forEach(function (item) {
      if (item.productId === product.id && item.key !== key) {
        otherQuantity += item.qty;
      }
    });
    return Math.max(0, totalStock - otherQuantity);
  }

  function validItem(item) {
    var product = findProduct(item.productId);
    var color = findColor(product, item.colorHex);
    return !!(
      product &&
      color &&
      item.size &&
      product.tallas.indexOf(item.size) !== -1 &&
      (product.colores.length === 0 || color)
    );
  }

  function sanitize() {
    items = items.filter(validItem);
  }

  function totalCount() {
    return items.reduce(function (total, item) {
      return total + item.qty;
    }, 0);
  }

  function updateHeader() {
    var count = totalCount();
    Array.prototype.forEach.call(
      document.querySelectorAll("[data-cart-count]"),
      function (element) {
        element.textContent = String(count);
      }
    );
    Array.prototype.forEach.call(
      document.querySelectorAll("[data-cart-open]"),
      function (element) {
        element.setAttribute(
          "aria-label",
          count > 0 ? "Abrir carrito, " + count + " artículo(s)" : "Abrir carrito"
        );
        wearonoffLocalize(element);
      }
    );
  }

  function buildWhatsappUrl() {
    var phone = String(cartRoot.getAttribute("data-whatsapp") || "50660658625").replace(
      /\D/g,
      ""
    );
    var lines = items.map(function (item, index) {
      return wearonoffT(
        "{index}. {name} — Color: {color} — Talla: {size} — Cantidad: {qty}",
        {
          index: index + 1,
          name: wearonoffT(item.nombre),
          color: wearonoffT(item.colorNombre),
          size: item.size,
          qty: item.qty,
        }
      );
    });
    var message = wearonoffT("Hola, quiero cotizar:\n\n{lines}\n\nGracias.", {
      lines: lines.join("\n"),
    });
    return "https://wa.me/" + phone + "?text=" + encodeURIComponent(message);
  }

  function render() {
    sanitize();
    itemsEl.innerHTML = "";
    emptyEl.hidden = items.length > 0;

    items.forEach(function (item) {
      var product = findProduct(item.productId);
      var color = findColor(product, item.colorHex);
      var max = lineCapacity(product, color, item.size, item.key);

      var article = document.createElement("article");
      article.className = "wearonoff-cart-item";
      article.setAttribute("data-cart-key", item.key);

      var image = document.createElement("img");
      image.src = item.imagen;
      image.alt = item.nombre;
      image.loading = "lazy";

      var content = document.createElement("div");
      content.className = "wearonoff-cart-item__content";

      var name = document.createElement("p");
      name.className = "wearonoff-cart-item__name";
      name.textContent = item.nombre;

      var meta = document.createElement("p");
      meta.className = "wearonoff-cart-item__meta";
      meta.textContent = "Color: " + item.colorNombre + " · Talla: " + item.size;

      var price = document.createElement("p");
      price.className = "wearonoff-cart-item__price";
      price.textContent = item.precio || "Consultar precio";

      var actions = document.createElement("div");
      actions.className = "wearonoff-cart-item__actions";

      var dec = document.createElement("button");
      dec.type = "button";
      dec.className = "wearonoff-cart-item__qty-btn";
      dec.setAttribute("data-cart-dec", "");
      dec.setAttribute("aria-label", "Quitar una unidad");
      dec.textContent = "−";

      var qty = document.createElement("span");
      qty.className = "wearonoff-cart-item__qty";
      qty.textContent = String(item.qty);

      var inc = document.createElement("button");
      inc.type = "button";
      inc.className = "wearonoff-cart-item__qty-btn";
      inc.setAttribute("data-cart-inc", "");
      inc.setAttribute("aria-label", "Agregar una unidad");
      inc.textContent = "+";
      inc.disabled = item.qty >= max;

      var remove = document.createElement("button");
      remove.type = "button";
      remove.className = "wearonoff-cart-item__remove";
      remove.setAttribute("data-cart-remove", "");
      remove.textContent = "Quitar";

      actions.appendChild(dec);
      actions.appendChild(qty);
      actions.appendChild(inc);
      actions.appendChild(remove);
      content.appendChild(name);
      content.appendChild(meta);
      content.appendChild(price);
      content.appendChild(actions);
      article.appendChild(image);
      article.appendChild(content);
      itemsEl.appendChild(article);
    });

    var count = totalCount();
    if (clearEl) clearEl.hidden = count === 0;
    whatsappEl.href = count > 0 ? buildWhatsappUrl() : "#";
    whatsappEl.setAttribute("aria-disabled", count > 0 ? "false" : "true");
    whatsappEl.classList.toggle("is-disabled", count === 0);
    updateHeader();
    wearonoffLocalize(itemsEl);
  }

  function add(productId, colorHex, size, quantity) {
    var product = findProduct(productId);
    var color = findColor(product, colorHex);
    if (!product || !color || !size) {
      return { ok: false, message: "Selecciona color y talla." };
    }

    var qty = Math.max(1, parseInt(quantity, 10) || 1);
    var key = lineKey(productId, color.hex, size);
    var existing = findItem(key);
    var max = lineCapacity(product, color, size, key);
    var current = existing ? existing.qty : 0;
    var desired = current + qty;

    if (max <= 0) {
      return {
        ok: false,
        message: "No hay stock disponible para esta combinación.",
      };
    }

    if (desired > max) {
      return {
        ok: false,
        message: "Solo hay " + max + " unidad(es) disponibles para esta combinación.",
      };
    }

    var image = (product.fotosPorColor || {})[normalize(color.codigo)] || product.imagen;
    if (existing) {
      existing.qty = desired;
    } else {
      items.push({
        key: key,
        productId: productId,
        nombre: product.nombre,
        imagen: image,
        colorHex: color.hex,
        colorNombre: color.nombre || color.hex,
        size: size,
        qty: qty,
        precio: product.precio,
      });
    }

    save();
    return { ok: true };
  }

  function setQty(key, nextQty) {
    var item = findItem(key);
    if (!item) return;
    var product = findProduct(item.productId);
    var color = findColor(product, item.colorHex);
    var max = lineCapacity(product, color, item.size, key);
    var qty = Math.max(1, parseInt(nextQty, 10) || 1);
    if (max <= 0) {
      removeItem(key);
      return;
    }
    item.qty = Math.min(qty, max);
    save();
  }

  function removeItem(key) {
    items = items.filter(function (item) {
      return item.key !== key;
    });
    save();
  }

  function clear() {
    items = [];
    save();
  }

  function open() {
    if (!cartRoot.hidden) return;
    lastFocused = document.activeElement;
    cartRoot.hidden = false;
    document.body.classList.add("wearonoff-cart-open");
    panel.focus();
  }

  function close() {
    if (cartRoot.hidden) return;
    cartRoot.hidden = true;
    document.body.classList.remove("wearonoff-cart-open");
    if (lastFocused && typeof lastFocused.focus === "function") lastFocused.focus();
  }

  Array.prototype.forEach.call(
    document.querySelectorAll("[data-cart-open]"),
    function (button) {
      button.addEventListener("click", open);
    }
  );

  Array.prototype.forEach.call(
    cartRoot.querySelectorAll("[data-cart-close]"),
    function (element) {
      element.addEventListener("click", close);
    }
  );

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !cartRoot.hidden) close();
  });

  itemsEl.addEventListener("click", function (event) {
    var action = event.target.closest("[data-cart-dec], [data-cart-inc], [data-cart-remove]");
    if (!action) return;
    var article = action.closest("[data-cart-key]");
    if (!article) return;
    var key = article.getAttribute("data-cart-key");
    var item = findItem(key);
    if (!item) return;

    if (action.hasAttribute("data-cart-remove")) {
      removeItem(key);
    } else if (action.hasAttribute("data-cart-inc")) {
      setQty(key, item.qty + 1);
    } else {
      setQty(key, item.qty - 1);
    }
  });

  if (clearEl) {
    clearEl.addEventListener("click", clear);
  }

  whatsappEl.addEventListener("click", function (event) {
    if (totalCount() === 0) event.preventDefault();
  });

  window.addEventListener("storage", function (event) {
    if (event.key !== KEY) return;
    items = load();
    render();
  });

  window.addEventListener("wearonoff:langchange", function () {
    render();
  });

  window.WearOnOffCart = {
    add: add,
    open: open,
    close: close,
  };

  sanitize();
  render();
})();
