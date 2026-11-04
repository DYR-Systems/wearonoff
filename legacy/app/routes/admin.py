"""CMS administration routes (login protected)."""

from __future__ import annotations

from typing import Any

from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from app.decorators import superadmin_required
from app.extensions import db
from app.forms import (
    BrandForm,
    MediaEditForm,
    MediaUploadForm,
    PageForm,
    ProfileForm,
    ProjectForm,
    SettingsForm,
    UserForm,
)
from app.models import Brand, ContactMessage, Media, Page, Project, SiteSettings, User
from app.services.media import delete_image, delete_media, process_image, save_media
from app.utils import clean, unique_slug

bp = Blueprint("admin", __name__, url_prefix="/admin")

FILE_FIELDS = {"logo", "favicon", "hero", "cover", "gallery", "files", "submit", "csrf_token"}


@bp.before_request
@login_required
def require_login():
    return None


@bp.context_processor
def inject_admin_globals() -> dict[str, object]:
    unread = 0
    if current_user.is_authenticated:
        unread = ContactMessage.query.filter_by(is_read=False).count()
    return {"unread_messages": unread}


def _replace_image(field, current: str | None) -> str | None:
    """Store an uploaded image, replacing (and deleting) the previous one."""
    if field is None or not getattr(field, "data", None):
        return current
    saved = process_image(field.data)
    if current and current != saved.filename:
        delete_image(current)
    return saved.filename


def _store_gallery(files, *, owner_field: str, owner_id: int) -> int:
    """Persist a list of gallery uploads attached to an owner. Returns count."""
    saved_count = 0
    start = (
        db.session.query(db.func.coalesce(db.func.max(Media.sort_order), 0))
        .filter(getattr(Media, owner_field) == owner_id)
        .scalar()
        or 0
    )
    for index, file_storage in enumerate(files or [], start=1):
        if not file_storage or not file_storage.filename:
            continue
        extra: dict[str, Any] = {owner_field: owner_id}
        save_media(
            file_storage,
            uploaded_by_id=current_user.id,
            sort_order=start + index,
            **extra,
        )
        saved_count += 1
    return saved_count


# --------------------------------------------------------------------------- #
# Dashboard
# --------------------------------------------------------------------------- #
@bp.route("/")
def dashboard():
    stats = {
        "brands": Brand.query.count(),
        "projects": Project.query.count(),
        "pages": Page.query.count(),
        "media": Media.query.count(),
        "unread_messages": ContactMessage.query.filter_by(is_read=False).count(),
    }
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_messages=recent_messages,
        recent_projects=recent_projects,
    )


# --------------------------------------------------------------------------- #
# Brands
# --------------------------------------------------------------------------- #
@bp.route("/marcas")
def brands():
    items = Brand.query.order_by(Brand.sort_order, Brand.name).all()
    return render_template("admin/brands/list.html", brands=items)


@bp.route("/marcas/nueva", methods=["GET", "POST"])
def brand_create():
    form = BrandForm()
    if form.validate_on_submit():
        brand = Brand()
        brand.name = clean(form.name.data)
        brand.slug = unique_slug(Brand, form.slug.data or brand.name)
        _assign_brand_fields(brand, form)
        db.session.add(brand)
        db.session.flush()
        _store_gallery(form.gallery.data, owner_field="brand_id", owner_id=brand.id)
        db.session.commit()
        flash("Marca creada.", "success")
        return redirect(url_for("admin.brands"))
    return render_template("admin/brands/form.html", form=form, brand=None)


@bp.route("/marcas/<int:brand_id>/editar", methods=["GET", "POST"])
def brand_edit(brand_id: int):
    brand = db.session.get(Brand, brand_id) or abort(404)
    form = BrandForm(obj=brand)
    if form.validate_on_submit():
        brand.name = clean(form.name.data)
        brand.slug = unique_slug(Brand, form.slug.data or brand.name, current_id=brand.id)
        _assign_brand_fields(brand, form)
        _store_gallery(form.gallery.data, owner_field="brand_id", owner_id=brand.id)
        db.session.commit()
        flash("Marca actualizada.", "success")
        return redirect(url_for("admin.brands"))
    return render_template("admin/brands/form.html", form=form, brand=brand)


@bp.route("/marcas/<int:brand_id>/eliminar", methods=["POST"])
def brand_delete(brand_id: int):
    brand = db.session.get(Brand, brand_id) or abort(404)
    for media in list(brand.gallery):
        delete_media(media)
    delete_image(brand.logo_filename)
    delete_image(brand.cover_filename)
    db.session.delete(brand)
    db.session.commit()
    flash("Marca eliminada.", "success")
    return redirect(url_for("admin.brands"))


@bp.route("/marcas/<int:brand_id>/galeria/<int:media_id>/eliminar", methods=["POST"])
def brand_gallery_delete(brand_id: int, media_id: int):
    media = db.session.get(Media, media_id) or abort(404)
    if media.brand_id != brand_id:
        abort(404)
    delete_media(media)
    db.session.commit()
    flash("Imagen eliminada.", "success")
    return redirect(url_for("admin.brand_edit", brand_id=brand_id))


def _assign_brand_fields(brand: Brand, form: BrandForm) -> None:
    brand.domain = (form.domain.data or "").strip()
    brand.tagline = (form.tagline.data or "").strip()
    brand.short_description = (form.short_description.data or "").strip()
    brand.description = form.description.data or ""
    brand.primary_color = (form.primary_color.data or "").strip()
    brand.website_url = (form.website_url.data or "").strip()
    brand.store_url = (form.store_url.data or "").strip()
    brand.is_store = bool(form.is_store.data)
    brand.is_published = bool(form.is_published.data)
    brand.is_featured = bool(form.is_featured.data)
    brand.sort_order = form.sort_order.data or 0
    brand.meta_title = (form.meta_title.data or "").strip()
    brand.meta_description = (form.meta_description.data or "").strip()
    brand.logo_filename = _replace_image(form.logo, brand.logo_filename)
    brand.cover_filename = _replace_image(form.cover, brand.cover_filename)


# --------------------------------------------------------------------------- #
# Projects
# --------------------------------------------------------------------------- #
@bp.route("/portafolio")
def projects():
    items = Project.query.order_by(Project.sort_order, Project.created_at.desc()).all()
    return render_template("admin/projects/list.html", projects=items)


@bp.route("/portafolio/nuevo", methods=["GET", "POST"])
def project_create():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project()
        project.title = clean(form.title.data)
        project.slug = unique_slug(Project, form.slug.data or project.title)
        _assign_project_fields(project, form)
        db.session.add(project)
        db.session.flush()
        _store_gallery(form.gallery.data, owner_field="project_id", owner_id=project.id)
        db.session.commit()
        flash("Proyecto creado.", "success")
        return redirect(url_for("admin.projects"))
    return render_template("admin/projects/form.html", form=form, project=None)


@bp.route("/portafolio/<int:project_id>/editar", methods=["GET", "POST"])
def project_edit(project_id: int):
    project = db.session.get(Project, project_id) or abort(404)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.title = clean(form.title.data)
        project.slug = unique_slug(Project, form.slug.data or project.title, current_id=project.id)
        _assign_project_fields(project, form)
        _store_gallery(form.gallery.data, owner_field="project_id", owner_id=project.id)
        db.session.commit()
        flash("Proyecto actualizado.", "success")
        return redirect(url_for("admin.projects"))
    return render_template("admin/projects/form.html", form=form, project=project)


@bp.route("/portafolio/<int:project_id>/eliminar", methods=["POST"])
def project_delete(project_id: int):
    project = db.session.get(Project, project_id) or abort(404)
    for media in list(project.gallery):
        delete_media(media)
    delete_image(project.cover_filename)
    db.session.delete(project)
    db.session.commit()
    flash("Proyecto eliminado.", "success")
    return redirect(url_for("admin.projects"))


@bp.route("/portafolio/<int:project_id>/galeria/<int:media_id>/eliminar", methods=["POST"])
def project_gallery_delete(project_id: int, media_id: int):
    media = db.session.get(Media, media_id) or abort(404)
    if media.project_id != project_id:
        abort(404)
    delete_media(media)
    db.session.commit()
    flash("Imagen eliminada.", "success")
    return redirect(url_for("admin.project_edit", project_id=project_id))


def _assign_project_fields(project: Project, form: ProjectForm) -> None:
    project.brand_id = form.brand_id.data or None
    project.client = (form.client.data or "").strip()
    project.category = (form.category.data or "").strip()
    project.year = (form.year.data or "").strip()
    project.summary = (form.summary.data or "").strip()
    project.description = form.description.data or ""
    project.project_url = (form.project_url.data or "").strip()
    project.is_published = bool(form.is_published.data)
    project.is_featured = bool(form.is_featured.data)
    project.sort_order = form.sort_order.data or 0
    project.meta_title = (form.meta_title.data or "").strip()
    project.meta_description = (form.meta_description.data or "").strip()
    project.cover_filename = _replace_image(form.cover, project.cover_filename)


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #
@bp.route("/paginas")
def pages():
    items = Page.query.order_by(Page.sort_order, Page.title).all()
    return render_template("admin/pages/list.html", pages=items)


@bp.route("/paginas/nueva", methods=["GET", "POST"])
def page_create():
    form = PageForm()
    if form.validate_on_submit():
        page = Page()
        page.title = clean(form.title.data)
        page.slug = unique_slug(Page, form.slug.data or page.title)
        _assign_page_fields(page, form)
        db.session.add(page)
        db.session.flush()
        _store_gallery(form.gallery.data, owner_field="page_id", owner_id=page.id)
        db.session.commit()
        flash("Pagina creada.", "success")
        return redirect(url_for("admin.pages"))
    return render_template("admin/pages/form.html", form=form, page=None)


@bp.route("/paginas/<int:page_id>/editar", methods=["GET", "POST"])
def page_edit(page_id: int):
    page = db.session.get(Page, page_id) or abort(404)
    form = PageForm(obj=page)
    if form.validate_on_submit():
        page.title = clean(form.title.data)
        page.slug = unique_slug(Page, form.slug.data or page.title, current_id=page.id)
        _assign_page_fields(page, form)
        _store_gallery(form.gallery.data, owner_field="page_id", owner_id=page.id)
        db.session.commit()
        flash("Pagina actualizada.", "success")
        return redirect(url_for("admin.pages"))
    return render_template("admin/pages/form.html", form=form, page=page)


@bp.route("/paginas/<int:page_id>/eliminar", methods=["POST"])
def page_delete(page_id: int):
    page = db.session.get(Page, page_id) or abort(404)
    for media in list(page.gallery):
        delete_media(media)
    delete_image(page.cover_filename)
    db.session.delete(page)
    db.session.commit()
    flash("Pagina eliminada.", "success")
    return redirect(url_for("admin.pages"))


@bp.route("/paginas/<int:page_id>/galeria/<int:media_id>/eliminar", methods=["POST"])
def page_gallery_delete(page_id: int, media_id: int):
    media = db.session.get(Media, media_id) or abort(404)
    if media.page_id != page_id:
        abort(404)
    delete_media(media)
    db.session.commit()
    flash("Imagen eliminada.", "success")
    return redirect(url_for("admin.page_edit", page_id=page_id))


def _assign_page_fields(page: Page, form: PageForm) -> None:
    page.body = form.body.data or ""
    page.is_published = bool(form.is_published.data)
    page.show_in_nav = bool(form.show_in_nav.data)
    page.sort_order = form.sort_order.data or 0
    page.meta_title = (form.meta_title.data or "").strip()
    page.meta_description = (form.meta_description.data or "").strip()
    page.cover_filename = _replace_image(form.cover, page.cover_filename)


# --------------------------------------------------------------------------- #
# Media library
# --------------------------------------------------------------------------- #
@bp.route("/media")
def media():
    page_number = request.args.get("page", 1, type=int)
    search = clean(request.args.get("q"))
    stmt = db.select(Media).order_by(Media.created_at.desc())
    if search:
        stmt = stmt.where(Media.original_filename.ilike(f"%{search}%"))
    pagination = db.paginate(stmt, page=page_number, per_page=24, error_out=False)
    form = MediaUploadForm()
    return render_template("admin/media/list.html", pagination=pagination, form=form, search=search)


@bp.route("/media/subir", methods=["POST"])
def media_upload():
    form = MediaUploadForm()
    if form.validate_on_submit():
        count = 0
        for file_storage in form.files.data or []:
            if not file_storage or not file_storage.filename:
                continue
            try:
                save_media(
                    file_storage,
                    alt_text=(form.alt_text.data or "").strip(),
                    caption=(form.caption.data or "").strip(),
                    uploaded_by_id=current_user.id,
                )
                count += 1
            except Exception as exc:  # noqa: BLE001
                flash(f"No se pudo subir {file_storage.filename}: {exc}", "danger")
        if count:
            db.session.commit()
            flash(f"{count} archivo(s) subido(s).", "success")
    else:
        flash("Selecciona al menos una imagen valida.", "danger")
    return redirect(url_for("admin.media"))


@bp.route("/media/subir-editor", methods=["POST"])
def media_upload_editor():
    """Endpoint used by the rich text editor to insert images."""
    file_storage = request.files.get("file")
    if file_storage is None or not file_storage.filename:
        return jsonify({"error": "No se recibio ningun archivo."}), 400
    try:
        media = save_media(file_storage, uploaded_by_id=current_user.id)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 400
    db.session.commit()
    return jsonify({"location": media.url})


@bp.route("/media/<int:media_id>/editar", methods=["GET", "POST"])
def media_edit(media_id: int):
    item = db.session.get(Media, media_id) or abort(404)
    form = MediaEditForm(obj=item)
    if form.validate_on_submit():
        item.alt_text = (form.alt_text.data or "").strip()
        item.caption = (form.caption.data or "").strip()
        db.session.commit()
        flash("Archivo actualizado.", "success")
        return redirect(url_for("admin.media"))
    return render_template("admin/media/form.html", form=form, item=item)


@bp.route("/media/<int:media_id>/eliminar", methods=["POST"])
def media_delete(media_id: int):
    item = db.session.get(Media, media_id) or abort(404)
    delete_media(item)
    db.session.commit()
    flash("Archivo eliminado.", "success")
    return redirect(url_for("admin.media"))


# --------------------------------------------------------------------------- #
# Contact messages
# --------------------------------------------------------------------------- #
@bp.route("/mensajes")
def messages():
    items = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/messages/list.html", messages=items)


@bp.route("/mensajes/<int:message_id>")
def message_detail(message_id: int):
    message = db.session.get(ContactMessage, message_id) or abort(404)
    if not message.is_read:
        message.is_read = True
        db.session.commit()
    return render_template("admin/messages/detail.html", message=message)


@bp.route("/mensajes/<int:message_id>/eliminar", methods=["POST"])
def message_delete(message_id: int):
    message = db.session.get(ContactMessage, message_id) or abort(404)
    db.session.delete(message)
    db.session.commit()
    flash("Mensaje eliminado.", "success")
    return redirect(url_for("admin.messages"))


# --------------------------------------------------------------------------- #
# Settings & profile
# --------------------------------------------------------------------------- #
@bp.route("/ajustes", methods=["GET", "POST"])
def settings():
    site = SiteSettings.get()
    form = SettingsForm(obj=site)
    if form.validate_on_submit():
        for field in form:
            if field.name in FILE_FIELDS:
                continue
            setattr(site, field.name, field.data)
        site.logo_filename = _replace_image(form.logo, site.logo_filename)
        site.favicon_filename = _replace_image(form.favicon, site.favicon_filename)
        site.hero_filename = _replace_image(form.hero, site.hero_filename)
        db.session.commit()
        flash("Ajustes guardados.", "success")
        return redirect(url_for("admin.settings"))
    return render_template("admin/settings.html", form=form, site=site)


@bp.route("/perfil", methods=["GET", "POST"])
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        email = clean(form.email.data).lower()
        existing = User.query.filter(User.email == email, User.id != current_user.id).first()
        if existing:
            flash("Ese correo ya esta en uso.", "danger")
        else:
            current_user.name = (form.name.data or "").strip()
            current_user.email = email
            if form.new_password.data:
                if not form.current_password.data or not current_user.check_password(
                    form.current_password.data
                ):
                    flash("La contrasena actual no es correcta.", "danger")
                    return render_template("admin/profile.html", form=form)
                current_user.set_password(form.new_password.data)
            db.session.commit()
            flash("Perfil actualizado.", "success")
            return redirect(url_for("admin.profile"))
    return render_template("admin/profile.html", form=form)


# --------------------------------------------------------------------------- #
# Users (superadmin only)
# --------------------------------------------------------------------------- #
@bp.route("/usuarios")
@superadmin_required
def users():
    items = User.query.order_by(User.name, User.email).all()
    return render_template("admin/users/list.html", users=items)


@bp.route("/usuarios/nuevo", methods=["GET", "POST"])
@superadmin_required
def user_create():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            name=(form.name.data or "").strip(),
            email=clean(form.email.data).lower(),
            is_superadmin=bool(form.is_superadmin.data),
            is_enabled=bool(form.is_enabled.data),
        )
        user.set_password(clean(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash("Usuario creado.", "success")
        return redirect(url_for("admin.users"))
    return render_template("admin/users/form.html", form=form, user=None)


@bp.route("/usuarios/<int:user_id>/editar", methods=["GET", "POST"])
@superadmin_required
def user_edit(user_id: int):
    user = db.session.get(User, user_id) or abort(404)
    form = UserForm(obj=user, user=user)
    if form.validate_on_submit():
        user.name = (form.name.data or "").strip()
        user.email = clean(form.email.data).lower()
        user.is_superadmin = bool(form.is_superadmin.data)
        user.is_enabled = bool(form.is_enabled.data)
        if form.password.data:
            user.set_password(clean(form.password.data))
        db.session.commit()
        flash("Usuario actualizado.", "success")
        return redirect(url_for("admin.users"))
    return render_template("admin/users/form.html", form=form, user=user)


@bp.route("/usuarios/<int:user_id>/eliminar", methods=["POST"])
@superadmin_required
def user_delete(user_id: int):
    user = db.session.get(User, user_id) or abort(404)
    if user.id == current_user.id:
        flash("No puedes eliminar tu propia cuenta.", "danger")
        return redirect(url_for("admin.users"))
    db.session.delete(user)
    db.session.commit()
    flash("Usuario eliminado.", "success")
    return redirect(url_for("admin.users"))
