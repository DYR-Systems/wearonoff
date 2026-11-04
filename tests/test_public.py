"""Public site smoke tests."""


def test_home_ok(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Scrubs" in response.data


def test_classic_home_ok(client):
    response = client.get("/inicio-clasico")
    assert response.status_code == 200
    assert b"ON &amp; OFF" in response.data or b"ON & OFF" in response.data


def test_brands_page_lists_brand(client):
    response = client.get("/marcas")
    assert response.status_code == 200
    assert b"Scrubs" in response.data


def test_brand_detail(client):
    response = client.get("/marcas/scrubs")
    assert response.status_code == 200
    assert b"Scrubs" in response.data


def test_project_detail(client):
    response = client.get("/portafolio/identidad-scrubs")
    assert response.status_code == 200


def test_about_and_contact(client):
    assert client.get("/nosotros").status_code == 200
    assert client.get("/contacto").status_code == 200


def test_contact_submission(client, app):
    from app.models import ContactMessage

    response = client.post(
        "/contacto",
        data={
            "name": "Ana",
            "email": "ana@example.com",
            "message": "Hola, quiero informacion.",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        assert ContactMessage.query.count() == 1


def test_unknown_page_returns_404(client):
    assert client.get("/marcas/no-existe").status_code == 404


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}
