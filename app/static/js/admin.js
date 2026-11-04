(function () {
  var csrfMeta = document.querySelector('meta[name="csrf-token"]');
  var csrfToken = csrfMeta ? csrfMeta.getAttribute("content") : "";
  var uploadUrl = document.body.getAttribute("data-upload-url") || "";

  function initEditors() {
    if (typeof window.tinymce === "undefined") return;
    window.tinymce.init({
      selector: "textarea.rich",
      height: 440,
      menubar: false,
      branding: false,
      promotion: false,
      plugins: "lists link image table code fullscreen autoresize",
      toolbar:
        "undo redo | blocks | bold italic underline | bullist numlist | link image table | code fullscreen",
      content_style:
        "body{font-family:Inter,-apple-system,Segoe UI,Roboto,sans-serif;font-size:15px;line-height:1.6}",
      convert_urls: false,
      images_upload_handler: function (blobInfo) {
        return new Promise(function (resolve, reject) {
          var data = new FormData();
          data.append("file", blobInfo.blob(), blobInfo.filename());
          fetch(uploadUrl, {
            method: "POST",
            body: data,
            headers: { "X-CSRFToken": csrfToken },
          })
            .then(function (response) {
              return response.json().then(function (json) {
                return { ok: response.ok, json: json };
              });
            })
            .then(function (result) {
              if (result.ok && result.json.location) {
                resolve(result.json.location);
              } else {
                reject(result.json.error || "No se pudo subir la imagen");
              }
            })
            .catch(function () {
              reject("No se pudo subir la imagen");
            });
        });
      },
    });
  }

  function initConfirms() {
    document.querySelectorAll("form[data-confirm]").forEach(function (form) {
      form.addEventListener("submit", function (event) {
        if (!window.confirm(form.getAttribute("data-confirm"))) {
          event.preventDefault();
        }
      });
    });
  }

  function initCopyButtons() {
    document.querySelectorAll("[data-copy]").forEach(function (button) {
      button.addEventListener("click", function () {
        var value = button.getAttribute("data-copy") || "";
        var full = new URL(value, window.location.origin).href;
        var done = function () {
          var original = button.textContent;
          button.textContent = "Copiado";
          window.setTimeout(function () {
            button.textContent = original;
          }, 1400);
        };
        if (navigator.clipboard) {
          navigator.clipboard.writeText(full).then(done);
        } else {
          window.prompt("Copia la URL", full);
        }
      });
    });
  }

  function init() {
    initEditors();
    initConfirms();
    initCopyButtons();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
