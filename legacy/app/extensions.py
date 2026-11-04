"""Shared Flask extension instances.

Kept in a dedicated module to avoid circular imports between the application
factory, models and blueprints.
"""

from __future__ import annotations

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = "auth.login"  # type: ignore[assignment]
login_manager.login_message = "Necesitas iniciar sesion para continuar."
login_manager.login_message_category = "warning"
