"""Application configuration.

Values are read from environment variables (see .env.example) with sensible
defaults so the project runs out of the box in development.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.pool import StaticPool

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"

load_dotenv(BASE_DIR / ".env")


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _normalize_database_url(url: str) -> str:
    """SQLAlchemy 2.x no longer accepts the legacy 'postgres://' scheme."""
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    SQLALCHEMY_DATABASE_URI = _normalize_database_url(
        os.environ.get("DATABASE_URL", f"sqlite:///{INSTANCE_DIR / 'onoff.db'}")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS: dict[str, object] = {
        "pool_pre_ping": True,
    }

    # Uploads
    UPLOAD_FOLDER = Path(os.environ.get("UPLOAD_FOLDER", INSTANCE_DIR / "uploads"))
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "avif", "svg"}
    IMAGE_MAX_DIMENSION = 2400
    THUMBNAIL_SIZE = (600, 600)
    THUMBNAIL_QUALITY = 82

    # Auth
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _as_bool(os.environ.get("SESSION_COOKIE_SECURE"), False)
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    WTF_CSRF_TIME_LIMIT = None

    # Branding fallbacks used before the CMS has been configured
    DEFAULT_SITE_NAME = os.environ.get("SITE_NAME", "ON & OFF")

    @staticmethod
    def init_app(app) -> None:  # noqa: ANN001
        Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
        INSTANCE_DIR.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "poolclass": StaticPool,
        "connect_args": {"check_same_thread": False},
    }
    UPLOAD_FOLDER = Path(tempfile.mkdtemp(prefix="onoff-test-uploads-"))


class ProductionConfig(Config):
    DEBUG = False


CONFIGS = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(name: str | None = None) -> type[Config]:
    name = name or os.environ.get("FLASK_ENV", "development")
    return CONFIGS.get(name, DevelopmentConfig)
