"""Public contact form."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, TextAreaField, validators


class ContactForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[validators.DataRequired(), validators.Length(max=160)],
    )
    email = EmailField(
        "Correo electronico",
        validators=[validators.DataRequired(), validators.Email()],
    )
    phone = StringField("Telefono", validators=[validators.Optional(), validators.Length(max=80)])
    company = StringField("Empresa", validators=[validators.Optional(), validators.Length(max=160)])
    subject = StringField("Asunto", validators=[validators.Optional(), validators.Length(max=255)])
    message = TextAreaField(
        "Mensaje",
        validators=[validators.DataRequired(), validators.Length(min=5, max=5000)],
    )
    submit = SubmitField("Enviar mensaje")
