"""Pytest fixtures shared by the test suite."""

from __future__ import annotations

import pytest

from app import create_app
from app.extensions import db as _db
from app.models import Brand, Project, SiteSettings, User


@pytest.fixture
def app():
    application = create_app("testing")
    with application.app_context():
        _db.create_all()

        settings = SiteSettings.get()
        settings.site_name = "ON & OFF"
        settings.hero_title = "Creamos marcas"

        admin = User(
            name="Admin",
            email="admin@test.com",
            is_superadmin=True,
            is_enabled=True,
        )
        admin.set_password("password123")

        brand = Brand(
            name="Scrubs",
            slug="scrubs",
            domain="scrubs.test",
            tagline="Uniformes medicos",
            is_published=True,
            is_featured=True,
        )
        project = Project(
            title="Identidad Scrubs",
            slug="identidad-scrubs",
            brand=brand,
            is_published=True,
        )
        _db.session.add_all([admin, brand, project])
        _db.session.commit()

        yield application

        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_client(client):
    response = client.post(
        "/admin/login",
        data={"email": "admin@test.com", "password": "password123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    return client
