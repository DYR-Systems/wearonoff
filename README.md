# WearOnOff — Sitio estático

Sitio estático de **Scrubs (WearOnOff)** construido con [Astro](https://astro.build/) y administrado con [Decap CMS](https://decapcms.org/).

## Desarrollo

```bash
npm install
npm run dev
# http://localhost:4321
```

Para probar el administrador en local:

```bash
npx decap-server
npm run dev
# http://localhost:4321/cms
```

## Producción

```bash
npm run build
npm run preview
```

El resultado se genera en `dist/`.

## Contenido

El contenido vive en `src/content/` y se edita desde `/cms`:

- `ajustes/general.md`: textos, imágenes y enlaces de la página de inicio.
- `colores/*.md`: círculos de "Compra por color".
- `categorias/*.md`: tarjetas de categorías.
- `productos/*.md`: productos destacados.

Las imágenes subidas se guardan en `public/images/`.

## Admin (Decap CMS)

- URL: `/cms`
- Configuración: `public/cms/config.yml`
- Repo: `DYR-Systems/wearonoff`
- OAuth: `https://dyr-wearonoff-oauth-backend.onrender.com`

Cada cambio del admin crea un commit en la rama `main`. Render reconstruye el sitio automáticamente.

Para usar el botón "Deploy a Producción" del admin, reemplaza `REEMPLAZA_CON_TU_DEPLOY_HOOK` en `public/cms/index.html` con el Deploy Hook de tu servicio en Render.

## Despliegue en Render

- Tipo: **Static Site**
- Build Command: `npm install && npm run build`
- Publish Directory: `dist`

El archivo `render.yaml` ya contiene esta configuración.

## Dominio

En Render → Settings → Custom Domains agrega `wearonoff.com` y `www.wearonoff.com`. Luego en Squarespace (DNS) crea:

- `@` → `A` → `216.24.57.1`
- `www` → `CNAME` → `tu-servicio.onrender.com`

## Código anterior

La versión Flask original se conserva en `legacy/`.
