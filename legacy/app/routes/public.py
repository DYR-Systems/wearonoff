"""Public facing routes: corporate site, brands, portfolio and pages."""

from __future__ import annotations

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

from app.extensions import db
from app.forms import ContactForm
from app.models import Brand, ContactMessage, Page, Project, SiteSettings
from app.utils import clean

bp = Blueprint("public", __name__)


def _published_brands():
    return Brand.query.filter_by(is_published=True).order_by(Brand.sort_order, Brand.name).all()


def _published_projects():
    return (
        Project.query.filter_by(is_published=True)
        .order_by(Project.sort_order, Project.created_at.desc())
        .all()
    )


def _brand_for_host() -> Brand | None:
    """Return the published brand whose domain matches the current host.

    This is what allows ``scrubs.wearonoff.com`` to render the Scrubs brand as
    its own landing page without deploying a separate application.
    """
    host = (request.host or "").split(":")[0].lower()
    if not host or host in {"localhost", "127.0.0.1"}:
        return None
    return Brand.query.filter(
        Brand.is_published.is_(True),
        db.func.lower(Brand.domain) == host,
    ).first()


@bp.route("/")
def index():
    brand = _brand_for_host()
    if brand is not None:
        template = (
            "public/scrubs_home.html" if brand.slug == "scrubs" else "public/brand_detail.html"
        )
        return render_template(template, brand=brand, brand_home=True)

    scrubs = Brand.query.filter_by(slug="scrubs", is_published=True).first()
    return render_template("public/scrubs_home.html", brand=scrubs, brand_home=True)


@bp.route("/inicio-clasico")
def classic_index():
    settings = SiteSettings.get()
    featured_brands = (
        Brand.query.filter_by(is_published=True, is_featured=True)
        .order_by(Brand.sort_order, Brand.name)
        .limit(6)
        .all()
    )
    if not featured_brands:
        featured_brands = _published_brands()[:6]

    featured_projects = (
        Project.query.filter_by(is_published=True, is_featured=True)
        .order_by(Project.sort_order, Project.created_at.desc())
        .limit(6)
        .all()
    )
    if not featured_projects:
        featured_projects = _published_projects()[:6]

    return render_template(
        "public/index.html",
        settings=settings,
        featured_brands=featured_brands,
        featured_projects=featured_projects,
    )


@bp.route("/marcas")
def brands():
    return render_template("public/brands.html", brands=_published_brands())


@bp.route("/marcas/<slug>")
def brand_detail(slug: str):
    brand = Brand.query.filter_by(slug=slug, is_published=True).first_or_404()
    projects = (
        Project.query.filter_by(brand_id=brand.id, is_published=True)
        .order_by(Project.sort_order, Project.created_at.desc())
        .all()
    )
    template = "public/scrubs_home.html" if brand.slug == "scrubs" else "public/brand_detail.html"
    return render_template(
        template,
        brand=brand,
        projects=projects,
        brand_home=False,
    )


@bp.route("/portafolio")
def projects():
    brand_slug = request.args.get("marca")
    query = Project.query.filter_by(is_published=True)
    current_brand = None
    if brand_slug:
        current_brand = Brand.query.filter_by(slug=brand_slug).first_or_404()
        query = query.filter_by(brand_id=current_brand.id)
    items = query.order_by(Project.sort_order, Project.created_at.desc()).all()
    return render_template(
        "public/projects.html",
        projects=items,
        brands=_published_brands(),
        current_brand=current_brand,
    )


@bp.route("/portafolio/<slug>")
def project_detail(slug: str):
    project = Project.query.filter_by(slug=slug, is_published=True).first_or_404()
    related = (
        Project.query.filter(
            Project.is_published.is_(True),
            Project.id != project.id,
            Project.brand_id == project.brand_id,
        )
        .order_by(Project.created_at.desc())
        .limit(3)
        .all()
        if project.brand_id
        else []
    )
    return render_template("public/project_detail.html", project=project, related=related)


@bp.route("/nosotros")
def about():
    return render_template("public/about.html", settings=SiteSettings.get())


@bp.route("/contacto", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            name=clean(form.name.data),
            email=clean(form.email.data).lower(),
            phone=(form.phone.data or "").strip(),
            company=(form.company.data or "").strip(),
            subject=(form.subject.data or "").strip(),
            message=clean(form.message.data),
        )
        db.session.add(message)
        db.session.commit()
        flash("Gracias por escribirnos. Te responderemos muy pronto.", "success")
        return redirect(url_for("public.contact"))
    return render_template("public/contact.html", form=form, settings=SiteSettings.get())


@bp.route("/p/<slug>")
def page_detail(slug: str):
    page = Page.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template("public/page.html", page=page)


@bp.route("/uploads/<path:filename>")
def uploaded_file(filename: str):
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        filename,
        max_age=60 * 60 * 24 * 30,
    )


@bp.route("/robots.txt")
def robots():
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin",
        f"Sitemap: {url_for('public.sitemap', _external=True)}",
        "",
    ]
    return current_app.response_class("\n".join(lines), mimetype="text/plain")


@bp.route("/sitemap.xml")
def sitemap():
    pages: list[str] = [
        url_for("public.index", _external=True),
        url_for("public.brands", _external=True),
        url_for("public.projects", _external=True),
        url_for("public.about", _external=True),
        url_for("public.contact", _external=True),
    ]
    pages += [
        url_for("public.brand_detail", slug=b.slug, _external=True) for b in _published_brands()
    ]
    pages += [
        url_for("public.project_detail", slug=p.slug, _external=True) for p in _published_projects()
    ]
    pages += [
        url_for("public.page_detail", slug=p.slug, _external=True)
        for p in Page.query.filter_by(is_published=True).all()
    ]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        xml += f"  <url><loc>{page}</loc></url>\n"
    xml += "</urlset>"
    return current_app.response_class(xml, mimetype="application/xml")


@bp.route("/health")
def health():
    return {"status": "ok"}


def not_found(_error):  # noqa: ANN001
    return render_template("errors/404.html"), 404


def server_error(_error):  # noqa: ANN001
    db.session.rollback()
    return render_template("errors/500.html"), 500
