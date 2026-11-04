"""CMS authentication and CRUD tests."""


def test_admin_requires_login(client):
    response = client.get("/admin/")
    assert response.status_code == 302
    assert "/admin/login" in response.headers["Location"]


def test_login_with_bad_credentials(client):
    response = client.post(
        "/admin/login",
        data={"email": "admin@test.com", "password": "wrong"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"incorrectas" in response.data


def test_login_success(admin_client):
    response = admin_client.get("/admin/")
    assert response.status_code == 200


def test_create_brand(admin_client, app):
    from app.models import Brand

    response = admin_client.post(
        "/admin/marcas/nueva",
        data={"name": "Pets", "slug": "", "is_published": "y"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        brand = Brand.query.filter_by(slug="pets").first()
        assert brand is not None
        assert brand.name == "Pets"


def test_update_settings(admin_client, app):
    from app.models import SiteSettings

    response = admin_client.post(
        "/admin/ajustes",
        data={
            "site_name": "Nueva Empresa",
            "tagline": "Hola",
            "primary_color": "#111111",
            "accent_color": "#ff0000",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        assert SiteSettings.get().site_name == "Nueva Empresa"


def test_message_detail_marks_read(admin_client, app):
    from app.extensions import db
    from app.models import ContactMessage

    with app.app_context():
        message = ContactMessage(name="Luis", email="luis@example.com", message="Hola")
        db.session.add(message)
        db.session.commit()
        message_id = message.id

    response = admin_client.get(f"/admin/mensajes/{message_id}")
    assert response.status_code == 200
    with app.app_context():
        stored = db.session.get(ContactMessage, message_id)
        assert stored is not None
        assert stored.is_read is True
