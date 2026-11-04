"""Model package.

Importing every model here guarantees they are registered on the SQLAlchemy
metadata, which Flask-Migrate needs for ``autogenerate``.
"""

from app.models.base import utcnow
from app.models.brand import Brand
from app.models.contact import ContactMessage
from app.models.media import Media
from app.models.page import Page
from app.models.project import Project
from app.models.site_settings import SiteSettings
from app.models.user import User

__all__ = [
    "Brand",
    "ContactMessage",
    "Media",
    "Page",
    "Project",
    "SiteSettings",
    "User",
    "utcnow",
]
