"""Application factory."""

from __future__ import annotations

from datetime import UTC, datetime

from flask import Flask, render_template

from app.config import get_config
from app.extensions import csrf, db, login_manager, migrate
from app.models import Page, SiteSettings, User


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    config_class.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.routes import admin, auth, public

    app.register_blueprint(public.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)

    _register_login(app)
    _register_context(app)
    _register_error_handlers(app)

    from app.cli import register_cli

    register_cli(app)

    return app


def _register_login(app: Flask) -> None:
    @login_manager.user_loader
    def load_user(user_id: str):  # noqa: ANN202
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None


def _register_context(app: Flask) -> None:
    @app.context_processor
    def inject_globals() -> dict[str, object]:
        try:
            site = SiteSettings.get()
            nav_pages = (
                Page.query.filter_by(is_published=True, show_in_nav=True)
                .order_by(Page.sort_order, Page.title)
                .all()
            )
        except Exception:  # noqa: BLE001 - database not initialised yet
            db.session.rollback()
            site = None
            nav_pages = []
        return {
            "site": site,
            "nav_pages": nav_pages,
            "current_year": datetime.now(UTC).year,
        }


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(403)
    def forbidden(_error):  # noqa: ANN001
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(_error):  # noqa: ANN001
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(_error):  # noqa: ANN001
        db.session.rollback()
        return render_template("errors/500.html"), 500
