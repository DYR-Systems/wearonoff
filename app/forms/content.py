"""Forms for brands, projects, pages and global settings."""

from __future__ import annotations

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
    validators,
)

from app.forms.fields import MultipleFileField
from app.models import Brand

IMAGE_RULES = FileAllowed(
    ["png", "jpg", "jpeg", "gif", "webp", "avif", "svg"],
    "Solo se permiten imagenes.",
)


class BrandForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[validators.DataRequired(), validators.Length(max=160)],
    )
    slug = StringField(
        "Slug (URL)",
        validators=[
            validators.Optional(),
            validators.Length(max=180),
            validators.Regexp(
                r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
                message="Solo minusculas, numeros y guiones.",
            ),
        ],
        description="Dejar vacio para generarlo desde el nombre.",
    )
    domain = StringField(
        "Dominio",
        validators=[validators.Optional(), validators.Length(max=255)],
        description="Ej: scrubs.wearonoff.com",
    )
    tagline = StringField("Tagline", validators=[validators.Optional(), validators.Length(max=255)])
    short_description = TextAreaField(
        "Descripcion corta",
        validators=[validators.Optional(), validators.Length(max=500)],
    )
    description = TextAreaField(
        "Descripcion completa",
        validators=[validators.Optional()],
        render_kw={"class": "rich", "rows": 12},
    )

    logo = FileField("Logo", validators=[IMAGE_RULES])
    cover = FileField("Imagen de portada", validators=[IMAGE_RULES])
    gallery = MultipleFileField("Galeria (varias imagenes)")

    primary_color = StringField(
        "Color de marca",
        validators=[validators.Optional(), validators.Length(max=20)],
        description="Hexadecimal, ej: #ff4d1c",
        render_kw={"type": "color"},
    )

    website_url = StringField("Sitio web", validators=[validators.Optional(), validators.URL()])
    store_url = StringField("Tienda online", validators=[validators.Optional(), validators.URL()])
    is_store = BooleanField("Es una tienda")

    is_published = BooleanField("Publicada", default=True)
    is_featured = BooleanField("Destacar en inicio")
    sort_order = IntegerField("Orden", default=0)

    meta_title = StringField(
        "Meta titulo", validators=[validators.Optional(), validators.Length(max=255)]
    )
    meta_description = TextAreaField(
        "Meta descripcion",
        validators=[validators.Optional(), validators.Length(max=320)],
    )
    submit = SubmitField("Guardar marca")


class ProjectForm(FlaskForm):
    title = StringField(
        "Titulo",
        validators=[validators.DataRequired(), validators.Length(max=200)],
    )
    slug = StringField(
        "Slug (URL)",
        validators=[
            validators.Optional(),
            validators.Length(max=220),
            validators.Regexp(
                r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
                message="Solo minusculas, numeros y guiones.",
            ),
        ],
        description="Dejar vacio para generarlo desde el titulo.",
    )
    brand_id = SelectField("Marca", coerce=int, validators=[validators.Optional()])
    client = StringField("Cliente", validators=[validators.Optional(), validators.Length(max=160)])
    category = StringField(
        "Categoria", validators=[validators.Optional(), validators.Length(max=120)]
    )
    year = StringField("Ano", validators=[validators.Optional(), validators.Length(max=10)])
    summary = TextAreaField(
        "Resumen", validators=[validators.Optional(), validators.Length(max=500)]
    )
    description = TextAreaField(
        "Descripcion",
        validators=[validators.Optional()],
        render_kw={"class": "rich", "rows": 12},
    )
    cover = FileField("Imagen de portada", validators=[IMAGE_RULES])
    gallery = MultipleFileField("Galeria (varias imagenes)")
    project_url = StringField(
        "Enlace externo", validators=[validators.Optional(), validators.URL()]
    )

    is_published = BooleanField("Publicado", default=True)
    is_featured = BooleanField("Destacar en inicio")
    sort_order = IntegerField("Orden", default=0)

    meta_title = StringField(
        "Meta titulo", validators=[validators.Optional(), validators.Length(max=255)]
    )
    meta_description = TextAreaField(
        "Meta descripcion",
        validators=[validators.Optional(), validators.Length(max=320)],
    )
    submit = SubmitField("Guardar proyecto")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.brand_id.choices = [(0, "Sin marca")] + [
            (b.id, b.name) for b in Brand.query.order_by(Brand.name).all()
        ]


class PageForm(FlaskForm):
    title = StringField(
        "Titulo",
        validators=[validators.DataRequired(), validators.Length(max=200)],
    )
    slug = StringField(
        "Slug (URL)",
        validators=[
            validators.Optional(),
            validators.Length(max=220),
            validators.Regexp(
                r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
                message="Solo minusculas, numeros y guiones.",
            ),
        ],
        description="Dejar vacio para generarlo desde el titulo.",
    )
    body = TextAreaField(
        "Contenido",
        validators=[validators.Optional()],
        render_kw={"class": "rich", "rows": 14},
    )
    cover = FileField("Imagen de portada", validators=[IMAGE_RULES])
    gallery = MultipleFileField("Galeria (varias imagenes)")

    is_published = BooleanField("Publicada", default=True)
    show_in_nav = BooleanField("Mostrar en el menu")
    sort_order = IntegerField("Orden", default=0)

    meta_title = StringField(
        "Meta titulo", validators=[validators.Optional(), validators.Length(max=255)]
    )
    meta_description = TextAreaField(
        "Meta descripcion",
        validators=[validators.Optional(), validators.Length(max=320)],
    )
    submit = SubmitField("Guardar pagina")


class SettingsForm(FlaskForm):
    site_name = StringField(
        "Nombre del sitio", validators=[validators.DataRequired(), validators.Length(max=120)]
    )
    tagline = StringField("Tagline", validators=[validators.Optional(), validators.Length(max=255)])
    meta_description = TextAreaField(
        "Meta descripcion",
        validators=[validators.Optional(), validators.Length(max=320)],
    )
    logo = FileField("Logo", validators=[IMAGE_RULES])
    favicon = FileField("Favicon", validators=[IMAGE_RULES])

    hero_title = StringField(
        "Titulo del hero", validators=[validators.Optional(), validators.Length(max=255)]
    )
    hero_subtitle = TextAreaField("Subtitulo del hero", validators=[validators.Optional()])
    hero = FileField("Imagen del hero", validators=[IMAGE_RULES])
    hero_cta_label = StringField(
        "Texto del boton", validators=[validators.Optional(), validators.Length(max=80)]
    )
    hero_cta_url = StringField("Enlace del boton", validators=[validators.Optional()])

    about_title = StringField(
        "Titulo 'Nosotros'", validators=[validators.Optional(), validators.Length(max=255)]
    )
    about_body = TextAreaField(
        "Texto 'Nosotros'",
        validators=[validators.Optional()],
        render_kw={"class": "rich", "rows": 12},
    )
    mission = TextAreaField("Mision", validators=[validators.Optional()], render_kw={"rows": 4})
    vision = TextAreaField("Vision", validators=[validators.Optional()], render_kw={"rows": 4})

    contact_email = StringField(
        "Email de contacto", validators=[validators.Optional(), validators.Email()]
    )
    contact_phone = StringField(
        "Telefono", validators=[validators.Optional(), validators.Length(max=80)]
    )
    contact_whatsapp = StringField(
        "WhatsApp", validators=[validators.Optional(), validators.Length(max=80)]
    )
    address = StringField(
        "Direccion", validators=[validators.Optional(), validators.Length(max=255)]
    )

    facebook_url = StringField("Facebook", validators=[validators.Optional(), validators.URL()])
    instagram_url = StringField("Instagram", validators=[validators.Optional(), validators.URL()])
    linkedin_url = StringField("LinkedIn", validators=[validators.Optional(), validators.URL()])
    tiktok_url = StringField("TikTok", validators=[validators.Optional(), validators.URL()])
    youtube_url = StringField("YouTube", validators=[validators.Optional(), validators.URL()])

    primary_color = StringField(
        "Color primario",
        validators=[validators.Optional(), validators.Length(max=20)],
        render_kw={"type": "color"},
    )
    accent_color = StringField(
        "Color de acento",
        validators=[validators.Optional(), validators.Length(max=20)],
        render_kw={"type": "color"},
    )
    footer_text = TextAreaField("Texto del footer", validators=[validators.Optional()])
    submit = SubmitField("Guardar ajustes")
