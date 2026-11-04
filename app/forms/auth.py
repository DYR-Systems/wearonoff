"""Authentication and account forms."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField, validators


class LoginForm(FlaskForm):
    email = EmailField(
        "Correo electronico",
        validators=[validators.DataRequired(), validators.Email()],
    )
    password = PasswordField(
        "Contrasena",
        validators=[validators.DataRequired()],
    )
    remember = BooleanField("Recordarme")
    submit = SubmitField("Entrar")


class ProfileForm(FlaskForm):
    name = StringField("Nombre", validators=[validators.Optional(), validators.Length(max=120)])
    email = EmailField(
        "Correo electronico",
        validators=[validators.DataRequired(), validators.Email()],
    )
    current_password = PasswordField("Contrasena actual", validators=[validators.Optional()])
    new_password = PasswordField(
        "Nueva contrasena",
        validators=[validators.Optional(), validators.Length(min=8)],
    )
    confirm_password = PasswordField("Confirmar contrasena", validators=[validators.Optional()])
    submit = SubmitField("Guardar cambios")

    def validate_new_password(self, field) -> None:  # noqa: ANN001
        if field.data and field.data != (self.confirm_password.data or ""):
            raise validators.ValidationError("Las contrasenas no coinciden.")


class UserForm(FlaskForm):
    name = StringField("Nombre", validators=[validators.Optional(), validators.Length(max=120)])
    email = EmailField(
        "Correo electronico",
        validators=[validators.DataRequired(), validators.Email()],
    )
    password = PasswordField(
        "Contrasena",
        validators=[validators.Optional(), validators.Length(min=8)],
        description="Dejar vacio para conservar la actual al editar.",
    )
    is_superadmin = BooleanField("Superadmin")
    is_enabled = BooleanField("Activo", default=True)
    submit = SubmitField("Guardar")

    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def validate_email(self, field) -> None:  # noqa: ANN001
        from app.models import User

        existing = User.query.filter(User.email == field.data.lower().strip()).first()
        if existing and (self.user is None or existing.id != self.user.id):
            raise validators.ValidationError("Ya existe un usuario con ese correo.")

    def validate_password(self, field) -> None:  # noqa: ANN001
        if self.user is None and not field.data:
            raise validators.ValidationError("La contrasena es obligatoria.")
