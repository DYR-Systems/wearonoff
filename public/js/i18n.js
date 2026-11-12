(function () {
  var STORAGE_KEY = "wearonoff_lang";
  var DEFAULT_LANG = "es";
  var current = DEFAULT_LANG;

  var translations = {
    // Navegación y accesibilidad
    "Tienda": "Shop",
    "Mujeres": "Women",
    "Hombres": "Men",
    "Colores": "Colors",
    "Nuestra historia": "Our Story",
    "Pedidos grupales": "Group Orders",
    "Compra ahora": "Shop now",
    "Abrir menú": "Open menu",
    "Cerrar menú": "Close menu",
    "Buscar": "Search",
    "Mi cuenta": "My account",
    "Abrir carrito": "Open cart",
    "Cerrar carrito": "Close cart",
    "Cerrar": "Close",
    "Principal": "Main",
    "Móvil": "Mobile",
    "Idioma": "Language",

    // Barra de anuncio y home
    "Envío gratis en pedidos superiores a ₡35.000 · Devoluciones gratuitas":
      "Free shipping on orders over ₡35,000 · Free returns",
    "Indumentaria médica de lujo": "Luxury Medical Apparel",
    "ACTIVA TU ESENCIA.": "BE ON. BE YOU.",
    "Prendas profesionales, diseño contemporáneo, comodidad y funcionalidad, para acompañar a quienes dedican su trabajo a cuidar de los demás.":
      "Professional garments with contemporary design, comfort and functionality, to accompany those who dedicate their work to caring for others.",
    "Comprar mujer": "Shop women",
    "Comprar hombre": "Shop men",
    "Colores exclusivos": "Signature Colors",
    "Colores disponibles en stock para entrega inmediata.":
      "Colors available in stock for immediate delivery.",
    "La colección": "The Collection",
    "Uniformes y conjuntos disponibles en stock para entrega inmediata.":
      "Uniforms and sets available in stock for immediate delivery.",
    "En stock": "In Stock",
    "Nuevos ingresos disponibles para entrega inmediata.":
      "New arrivals available for immediate delivery.",
    "Ver todo": "Shop all",
    "Composición y cuidados": "Composition and care",
    "Tela y detalles": "Fabric & Details",
    "Una mezcla pensada para acompañarte en cada turno: suave al tacto, con elasticidad y transpirabilidad para moverte sin límites.":
      "A blend designed to accompany you through every shift: soft to the touch, with stretch and breathability so you can move without limits.",
    "72% poliéster · 22% rayón · 6% elastano":
      "72% polyester · 22% rayon · 6% elastane",
    "Elástica, suave y transpirable": "Stretchy, soft and breathable",
    "Lavar a máquina a 30 °C · No usar blanqueador":
      "Machine wash at 30 °C · Do not bleach",
    "Secar a baja temperatura · Planchar a baja temperatura":
      "Tumble dry low · Iron low",
    "No lavar en seco": "Do not dry clean",
    "Ver productos": "View products",
    "Los equipos extraordinarios merecen uniformes extraordinarios. Facilitamos los pedidos grupales para clínicas y hospitales.":
      "Extraordinary teams deserve extraordinary uniforms. We make group orders easy for clinics and hospitals.",
    "Cotizar pedido": "Request a quote",
    "Somos ticos con una idea clara: la ropa de trabajo también puede ser cómoda, elegante y accesible. Nacimos para comercializar prendas de alta calidad a un precio más bajo, seleccionando cada pieza con cuidado para que te sientas bien dentro y fuera del turno. Creemos que vestir bien no debería ser un lujo, así que unimos comodidad, diseño y precios justos en cada prenda importada de calidad que traemos para vos.":
      "We are Costa Ricans with a clear idea: workwear can also be comfortable, elegant and accessible. We were born to offer high-quality garments at a lower price, carefully selecting each piece so you feel good inside and outside your shift. We believe dressing well should not be a luxury, so we combine comfort, design and fair prices in every quality imported garment we bring to you.",

    // Preguntas frecuentes
    "Preguntas frecuentes": "Frequently asked questions",
    "¿Hacen envíos a todo Costa Rica?": "Do you ship throughout Costa Rica?",
    "Sí. Entregamos de forma física en San José, Heredia y Pérez Zeledón, y enviamos a cualquier parte del país por Correos de Costa Rica. Además, el envío es gratis en pedidos superiores a ₡35.000.":
      "Yes. We deliver in person in San José, Heredia and Pérez Zeledón, and ship anywhere in the country through Correos de Costa Rica. Shipping is also free on orders over ₡35,000.",
    "¿Puedo cambiar o devolver una prenda?": "Can I exchange or return a garment?",
    "Sí. Aceptamos cambios y devoluciones de prendas sin uso y en buen estado. Escríbenos y coordinamos el proceso sin costo.":
      "Yes. We accept exchanges and returns of unused garments in good condition. Write to us and we will coordinate the process at no cost.",
    "¿Cómo elijo mi talla?": "How do I choose my size?",
    "Revisa nuestra guía de tallas o escríbenos con tus medidas y te ayudamos a encontrar la talla ideal. Por ahora manejamos tallas XS, S y M; estamos confeccionando más. Si no queda perfecta, la cambiamos.":
      "Check our size guide or send us your measurements and we will help you find the ideal size. We currently carry sizes XS, S and M; more are in the works. If it does not fit perfectly, we will exchange it.",
    "¿Cómo debo lavar mis prendas?": "How should I wash my garments?",
    "Lávalas a máquina a 30 °C, sin blanqueador, y sécalas y plánchalas a baja temperatura. No usar lavado en seco.":
      "Machine wash at 30 °C without bleach, and tumble dry and iron on low. Do not dry clean.",
    "¿Hacen pedidos para equipos, clínicas u hospitales?":
      "Do you take orders for teams, clinics or hospitals?",
    "Sí. Facilitamos pedidos grupales y personalización para equipos. Escríbenos a hola@wearonoff.com y te ayudamos con tu cotización.":
      "Yes. We make group orders and team customization easy. Write to us at hola@wearonoff.com and we will help you with your quote.",
    "¿Puedo personalizar mi uniforme?": "Can I customize my uniform?",
    "Sí. Podemos personalizar tus prendas con logos, nombres o detalles del equipo. Cuéntanos qué necesitas y lo hacemos realidad.":
      "Yes. We can customize your garments with logos, names or team details. Tell us what you need and we will make it happen.",
    "¿Cómo obtengo el descuento para estudiantes?":
      "How do I get the student discount?",
    "Si eres estudiante, escríbenos y te enviamos un cupón de descuento para tu compra.":
      "If you are a student, write to us and we will send you a discount coupon for your purchase.",
    "Descuento para estudiantes": "Student discount",
    "Si eres estudiante, escríbenos y obtén tu cupón de descuento.":
      "If you are a student, write to us and get your discount coupon.",
    "Solicitar mi cupón": "Request my coupon",
    "HECHO PARA LA SALUD · #WEARONOFF": "MADE FOR HEALTHCARE · #WEARONOFF",

    // Página de colección
    "Explora la colección completa de uniformes y conjuntos disponibles en stock. Cada diseño se puede cotizar en varias tallas y colores.":
      "Explore the full collection of uniforms and sets available in stock. Each design can be quoted in multiple sizes and colors.",
    "Filtrar por color": "Filter by color",
    "Toca un color para ver los diseños disponibles en ese color.":
      "Tap a color to see the designs available in that color.",
    "Todos los modelos en stock. Elige un diseño para ver sus colores, tallas y opciones de cotización.":
      "All models in stock. Choose a design to see its colors, sizes and quote options.",
    "¿Buscas otro diseño? Escríbenos": "Looking for another design? Contact us",
    "Volver al inicio": "Back to home",

    // Pie de página
    "Obtén ayuda": "Get help",
    "Centro de ayuda": "Help center",
    "Envío y entregas": "Shipping and delivery",
    "Devoluciones y cambios": "Returns and exchanges",
    "Contáctanos": "Contact us",
    "Nuestra empresa": "Our company",
    "Guías": "Guides",
    "Guía de tallas": "Size guide",
    "Cuidado de la prenda": "Garment care",
    "Materiales": "Materials",
    "Personaliza tu uniforme": "Customize your uniform",
    "Más información": "More information",
    "Todos los derechos reservados.": "All rights reserved.",

    // Carrito
    "Tu carrito": "Your cart",
    "Tu carrito está vacío. Agrega una prenda desde la colección.":
      "Your cart is empty. Add a garment from the collection.",
    "Los precios se confirman por WhatsApp. No se realiza ningún cobro en línea.":
      "Prices are confirmed via WhatsApp. No online payment is made.",
    "Cotizar por WhatsApp": "Request a quote via WhatsApp",
    "Vaciar carrito": "Empty cart",
    "Quitar": "Remove",
    "Quitar una unidad": "Remove one unit",
    "Agregar una unidad": "Add one unit",
    "Consultar precio": "Price upon request",
    "Color": "Color",
    "Color:": "Color:",
    "Talla": "Size",
    "Talla:": "Size:",
    "Tallas:": "Sizes:",
    "Cantidad": "Quantity",
    "Cantidad:": "Quantity:",

    // Modal de producto
    "Foto de referencia del color base.": "Reference photo of the base color.",
    "Selecciona una talla para continuar.": "Select a size to continue.",
    "Agregar al carrito": "Add to cart",
    "Agrega tus prendas y solicita la cotización por WhatsApp.":
      "Add your garments and request a quote via WhatsApp.",
    "Agotado.": "Sold out.",
    "Agotado para esta combinación.": "Sold out for this combination.",
    "No se pudo agregar al carrito.": "Could not add to cart.",
    "Selecciona color y talla.": "Select a color and size.",
    "No hay stock disponible para esta combinación.":
      "No stock available for this combination.",
    "Ver todos": "View all",
    "Ver opciones": "View options",

    // Productos, categorías y colores
    "Conjunto quirúrgico": "Surgical set",
    "Uniforme quirúrgico": "Surgical uniform",
    "Conjunto con chaqueta": "Set with jacket",
    "Conjuntos": "Sets",
    "Uniformes": "Uniforms",
    "Verde lima": "Lime green",
    "Azul petróleo": "Petrol blue",
    "Azul marino": "Navy blue",
    "Borgoña": "Burgundy",
    "Negro": "Black",
    "Café": "Brown",
    "Rosa salmón": "Salmon pink",
    "Azul cielo": "Sky blue",

    // Títulos de página
    "WEARONOFF — Indumentaria médica de lujo":
      "WEARONOFF — Luxury Medical Apparel",
    "Colección completa — WearOnOff": "Complete Collection — WearOnOff",
    "Indumentaria médica de diseño editorial para profesionales de la salud. Comodidad, calidad y estilo para cada turno.":
      "Editorial-design medical apparel for healthcare professionals. Comfort, quality and style for every shift.",

    // Mensajes generados por JavaScript
    "Hola, quiero cotizar:\n\n{lines}\n\nGracias.":
      "Hi, I would like a quote:\n\n{lines}\n\nThank you.",
    "{index}. {name} — Color: {color} — Talla: {size} — Cantidad: {qty}":
      "{index}. {name} — Color: {color} — Size: {size} — Quantity: {qty}",
    "Color: {color} · Talla: {size}": "Color: {color} · Size: {size}",
    "Stock total del diseño: {count} unidad(es)":
      "Total stock for this design: {count} unit(s)",
    "Disponible: {count} unidad(es)": "Available: {count} unit(s)",
    "Abrir carrito, {count} artículo(s)": "Open cart, {count} item(s)",
    "Solo hay {count} unidad(es) disponibles para esta combinación.":
      "Only {count} unit(s) available for this combination."
  };

  var patterns = [
    [/^(.+?) \(([A-Z]{1,3}\d{1,3})\)$/, function (match) {
      return translateText(match[1]) + " (" + match[2] + ")";
    }],
    [/^(\d+) en stock$/, function (match) {
      return match[1] + " in stock";
    }],
    [/^Tallas: (.+)$/, function (match) {
      return "Sizes: " + translateText(match[1]);
    }],
    [/^(\d+) diseños disponibles$/, function (match) {
      return match[1] + " designs available";
    }],
    [/^Abrir carrito, (\d+) artículo\(s\)$/, function (match) {
      return "Open cart, " + match[1] + " item(s)";
    }],
    [/^Stock total del diseño: (\d+) unidad\(es\)$/, function (match) {
      return "Total stock for this design: " + match[1] + " unit(s)";
    }],
    [/^Disponible: (\d+) unidad\(es\)$/, function (match) {
      return "Available: " + match[1] + " unit(s)";
    }],
    [/^Solo hay (\d+) unidad\(es\) disponibles para esta combinación\.$/, function (match) {
      return "Only " + match[1] + " unit(s) available for this combination.";
    }],
    [/^Ver opciones de (.+)$/, function (match) {
      return "View options for " + translateText(match[1]);
    }],
    [/^Ver (.+) en (.+)$/, function (match) {
      return "View " + translateText(match[1]) + " in " + translateText(match[2]);
    }],
    [/^Color: (.+) · Talla: (.+)$/, function (match) {
      return "Color: " + translateText(match[1]) + " · Size: " + translateText(match[2]);
    }],
    [/^Color: (.+)$/, function (match) {
      return "Color: " + translateText(match[1]);
    }],
    [/^(.+?) Todos los derechos reservados\.$/, function (match) {
      return match[1] + " All rights reserved.";
    }]
  ];

  var textOriginals = new WeakMap();
  var attributeOriginals = new WeakMap();

  var titleOriginal = document.title;
  var descriptionMeta = document.querySelector('meta[name="description"]');
  var descriptionOriginal = descriptionMeta
    ? descriptionMeta.getAttribute("content") || ""
    : "";

  function translateText(value) {
    if (value == null) return value;

    var raw = String(value);
    var trimmed = raw.trim();
    if (!trimmed) return raw;

    if (Object.prototype.hasOwnProperty.call(translations, trimmed)) {
      return raw.replace(trimmed, translations[trimmed]);
    }

    for (var i = 0; i < patterns.length; i += 1) {
      var match = trimmed.match(patterns[i][0]);
      if (match) {
        return raw.replace(trimmed, patterns[i][1](match));
      }
    }

    return raw;
  }

  function t(text, vars) {
    var source = text == null ? "" : String(text);
    var output = current === "en" ? translateText(source) : source;

    if (vars) {
      output = output.replace(/\{(\w+)\}/g, function (match, key) {
        return Object.prototype.hasOwnProperty.call(vars, key)
          ? String(vars[key])
          : match;
      });
    }

    return output;
  }

  function applyTextNode(node) {
    var value = node.nodeValue || "";
    if (!value.trim()) return;

    var original = textOriginals.get(node);
    if (original === undefined) {
      original = value;
      textOriginals.set(node, original);
    } else {
      var translated = translateText(original);
      if (value !== original && value !== translated) {
        original = value;
        textOriginals.set(node, original);
      }
    }

    var next = current === "en" ? translateText(original) : original;
    if (node.nodeValue !== next) node.nodeValue = next;
  }

  function applyAttribute(element, attribute) {
    if (!element.hasAttribute(attribute)) return;

    var store = attributeOriginals.get(element);
    if (!store) {
      store = {};
      attributeOriginals.set(element, store);
    }

    var value = element.getAttribute(attribute);
    var original = store[attribute];

    if (original === undefined) {
      original = value;
      store[attribute] = original;
    } else {
      var translated = translateText(original);
      if (value !== original && value !== translated) {
        original = value;
        store[attribute] = original;
      }
    }

    var next = current === "en" ? translateText(original) : original;
    if (value !== next) element.setAttribute(attribute, next);
  }

  function translateAttributes(root) {
    var attributes = ["title", "aria-label", "placeholder", "alt"];
    var elements = [];

    if (root.nodeType === 1) {
      elements.push(root);
      elements = elements.concat(
        Array.prototype.slice.call(
          root.querySelectorAll("[title], [aria-label], [placeholder], [alt]")
        )
      );
    } else if (root.querySelectorAll) {
      elements = Array.prototype.slice.call(
        root.querySelectorAll("[title], [aria-label], [placeholder], [alt]")
      );
    }

    elements.forEach(function (element) {
      attributes.forEach(function (attribute) {
        applyAttribute(element, attribute);
      });
    });
  }

  function translate(root) {
    if (!root) return;

    if (root.nodeType === 3) {
      applyTextNode(root);
      return;
    }

    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    var node = walker.nextNode();

    while (node) {
      var parent = node.parentNode;
      var tag = parent && parent.nodeType === 1 ? parent.tagName : "";
      if (tag !== "SCRIPT" && tag !== "STYLE" && tag !== "NOSCRIPT") {
        applyTextNode(node);
      }
      node = walker.nextNode();
    }

    translateAttributes(root);
  }

  function updateSwitcher() {
    Array.prototype.forEach.call(
      document.querySelectorAll("[data-lang]"),
      function (button) {
        var active = button.getAttribute("data-lang") === current;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-pressed", active ? "true" : "false");
      }
    );
  }

  function updateDocumentMeta() {
    document.title =
      current === "en" ? translateText(titleOriginal) : titleOriginal;

    if (descriptionMeta) {
      descriptionMeta.setAttribute(
        "content",
        current === "en"
          ? translateText(descriptionOriginal)
          : descriptionOriginal
      );
    }
  }

  function setLang(lang) {
    current = lang === "en" ? "en" : "es";

    try {
      localStorage.setItem(STORAGE_KEY, current);
    } catch (error) {
      // El idioma se mantiene solo en memoria.
    }

    document.documentElement.lang = current;
    updateSwitcher();
    updateDocumentMeta();
    translate(document.body);

    window.dispatchEvent(
      new CustomEvent("wearonoff:langchange", { detail: { lang: current } })
    );
  }

  Array.prototype.forEach.call(
    document.querySelectorAll("[data-lang]"),
    function (button) {
      button.addEventListener("click", function () {
        setLang(button.getAttribute("data-lang"));
      });
    }
  );

  var stored = DEFAULT_LANG;
  try {
    stored = localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG;
  } catch (error) {
    stored = DEFAULT_LANG;
  }
  if (stored !== "en") stored = DEFAULT_LANG;

  current = DEFAULT_LANG;
  translate(document.body);
  updateSwitcher();

  if (stored === "en") setLang("en");

  window.WearOnOffI18n = {
    getLang: function () {
      return current;
    },
    setLang: setLang,
    t: t,
    translate: translate
  };
})();
