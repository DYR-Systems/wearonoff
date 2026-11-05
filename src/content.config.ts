import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const ajustes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/ajustes' }),
  schema: z.object({
    anuncio_texto: z.string().default(''),
    anuncio_enlace: z.string().default('#colores'),
    anuncio_enlace_texto: z.string().default('Compra ahora'),
    hero_eyebrow: z.string().default(''),
    hero_titulo: z.string().default(''),
    hero_subtitulo: z.string().default(''),
    hero_imagen: z.string().default(''),
    hero_cta_primario_texto: z.string().default(''),
    hero_cta_primario_url: z.string().default('#'),
    hero_cta_secundario_texto: z.string().default(''),
    hero_cta_secundario_url: z.string().default('#'),
    colores_titulo: z.string().default('Compra por color'),
    colores_subtitulo: z.string().default(''),
    categorias_titulo: z.string().default('Por categoría'),
    categorias_subtitulo: z.string().default(''),
    productos_titulo: z.string().default('Los más vendidos'),
    productos_subtitulo: z.string().default(''),
    productos_cta_texto: z.string().default('Ver toda la colección'),
    productos_cta_url: z.string().default('#'),
    tela_eyebrow: z.string().default('Tecnología de la tela'),
    tela_titulo: z.string().default(''),
    tela_descripcion: z.string().default(''),
    tela_imagen: z.string().default(''),
    tela_bullets: z.array(z.object({ item: z.string() })).default([]),
    tela_cta_texto: z.string().default('Conoce la tela'),
    tela_cta_url: z.string().default('#productos'),
    equipo_titulo: z.string().default(''),
    equipo_descripcion: z.string().default(''),
    equipo_imagen: z.string().default(''),
    equipo_cta_texto: z.string().default('Comenzar'),
    equipo_cta_url: z.string().default('#'),
    redes_handle: z.string().default(''),
    redes_instagram: z.string().default('#'),
    redes_tiktok: z.string().default('#'),
    redes_youtube: z.string().default('#'),
    redes_pinterest: z.string().default('#'),
  }),
});

const colores = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/colores' }),
  schema: z.object({
    nombre: z.string(),
    codigo: z.string().default(''),
    hex: z.string(),
    orden: z.number().int().default(0),
  }),
});

const categorias = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/categorias' }),
  schema: z.object({
    nombre: z.string(),
    imagen: z.string().default(''),
    enlace: z.string().default('#productos'),
    orden: z.number().int().default(0),
  }),
});

const productos = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/productos' }),
  schema: z.object({
    nombre: z.string(),
    precio: z.string(),
    tallas: z.string().default(''),
    imagen: z.string().default(''),
    badge: z.string().default(''),
    badge_estilo: z.enum(['dark', 'light']).default('dark'),
    colores: z.array(z.object({ color: z.string() })).default([]),
    fotos_por_color: z
      .array(z.object({ codigo: z.string(), imagen: z.string() }))
      .default([]),
    orden: z.number().int().default(0),
  }),
});

export const collections = { ajustes, colores, categorias, productos };
