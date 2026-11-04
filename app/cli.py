"""Custom ``flask`` CLI commands."""

from __future__ import annotations

import os

import click
from flask import Flask
from flask.cli import with_appcontext

from app.extensions import db
from app.models import Brand, Page, Project, SiteSettings, User


def register_cli(app: Flask) -> None:
    app.cli.add_command(init_db)
    app.cli.add_command(seed)
    app.cli.add_command(create_admin)
    app.cli.add_command(set_password)


@click.command("init-db")
@with_appcontext
def init_db() -> None:
    """Create all database tables (without migrations)."""
    db.create_all()
    click.echo("Base de datos inicializada.")


@click.command("seed")
@with_appcontext
def seed() -> None:
    """Create settings, an admin user and sample content for a fresh install."""
    db.create_all()

    SiteSettings.get()

    email = os.environ.get("ADMIN_EMAIL", "admin@wearonoff.com")
    password = os.environ.get("ADMIN_PASSWORD", "cambiame123")
    name = os.environ.get("ADMIN_NAME", "Administrador")

    admin = User.query.filter_by(email=email).first()
    if admin is None:
        admin = User(name=name, email=email, is_superadmin=True, is_enabled=True)
        admin.set_password(password)
        db.session.add(admin)
        click.echo(f"Superadmin creado: {email} / {password}")

    if Brand.query.count() == 0:
        scrubs = Brand(
            name="Scrubs",
            slug="scrubs",
            domain="scrubs.wearonoff.com",
            tagline="Uniformes medicos con estilo",
            short_description=(
                "Scrubs comodos, resistentes y con diseno para profesionales de la salud."
            ),
            description="<p>Scrubs es nuestra marca de uniformes medicos.</p>",
            website_url="https://scrubs.wearonoff.com",
            is_store=True,
            is_featured=True,
            sort_order=1,
        )
        pets = Brand(
            name="Pets",
            slug="pets",
            domain="pets.wearonoff.com",
            tagline="Accesorios para consentir a tu mascota",
            short_description="Juguetes, camas y accesorios para mascotas felices.",
            description="<p>Pets es la marca con la que acompanamos a las mascotas.</p>",
            website_url="https://pets.wearonoff.com",
            is_store=True,
            is_featured=True,
            sort_order=2,
        )
        db.session.add_all([scrubs, pets])
        db.session.flush()

        db.session.add_all(
            [
                Project(
                    title="Identidad de marca Scrubs",
                    slug="identidad-scrubs",
                    brand_id=scrubs.id,
                    category="Branding",
                    year="2025",
                    summary="Sistema visual completo para la linea de uniformes.",
                    description="<p>Disenamos la identidad y el packaging de la linea.</p>",
                    is_featured=True,
                    sort_order=1,
                ),
                Project(
                    title="Lanzamiento tienda Pets",
                    slug="lanzamiento-pets",
                    brand_id=pets.id,
                    category="E-commerce",
                    year="2025",
                    summary="Estrategia y montaje de la tienda en linea.",
                    description="<p>Construimos la experiencia de compra de la marca.</p>",
                    is_featured=True,
                    sort_order=2,
                ),
            ]
        )
        db.session.add(
            Page(
                title="Aviso de privacidad",
                slug="aviso-de-privacidad",
                body="<p>Este es un texto de ejemplo. Editalo desde el CMS.</p>",
                show_in_nav=False,
                sort_order=10,
            )
        )

    db.session.commit()
    click.echo("Datos de ejemplo listos.")


@click.command("create-admin")
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@click.option("--name", default="Administrador")
@with_appcontext
def create_admin(email: str, password: str, name: str) -> None:
    """Create (or promote) a superadmin account."""
    db.create_all()
    email = email.strip().lower()
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email=email, name=name, is_superadmin=True, is_enabled=True)
        db.session.add(user)
    else:
        user.is_superadmin = True
        user.is_enabled = True
    user.set_password(password)
    db.session.commit()
    click.echo(f"Superadmin listo: {email}")


@click.command("set-password")
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@with_appcontext
def set_password(email: str, password: str) -> None:
    """Change the password of an existing user."""
    user = User.query.filter_by(email=email.strip().lower()).first()
    if user is None:
        raise click.ClickException("No existe un usuario con ese correo.")
    user.set_password(password)
    db.session.commit()
    click.echo("Contrasena actualizada.")
