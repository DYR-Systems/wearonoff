"""Media library forms."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators

from app.forms.fields import MultipleFileField


class MediaUploadForm(FlaskForm):
    files = MultipleFileField("Imagenes")
    alt_text = StringField(
        "Texto alternativo",
        validators=[validators.Optional(), validators.Length(max=255)],
    )
    caption = StringField(
        "Pie de foto",
        validators=[validators.Optional(), validators.Length(max=500)],
    )
    submit = SubmitField("Subir")


class MediaEditForm(FlaskForm):
    alt_text = StringField(
        "Texto alternativo",
        validators=[validators.Optional(), validators.Length(max=255)],
    )
    caption = TextAreaField(
        "Pie de foto",
        validators=[validators.Optional(), validators.Length(max=500)],
    )
    submit = SubmitField("Guardar")
