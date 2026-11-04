"""Authentication routes for the CMS."""

from __future__ import annotations

from urllib.parse import urlsplit

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app.forms import LoginForm
from app.models import User
from app.utils import clean

bp = Blueprint("auth", __name__, url_prefix="/admin")


def _safe_next(target: str | None) -> str:
    if not target:
        return url_for("admin.dashboard")
    parts = urlsplit(target)
    if parts.netloc or parts.scheme:
        return url_for("admin.dashboard")
    return target


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == clean(form.email.data).lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash("Credenciales incorrectas.", "danger")
        elif not user.is_enabled:
            flash("Tu cuenta esta desactivada.", "danger")
        else:
            login_user(user, remember=form.remember.data)
            user.touch_login()
            from app.extensions import db

            db.session.commit()
            flash(f"Bienvenido, {user.name or user.email}.", "success")
            return redirect(_safe_next(request.args.get("next")))
    return render_template("admin/login.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash("Sesion cerrada.", "success")
    return redirect(url_for("public.index"))
