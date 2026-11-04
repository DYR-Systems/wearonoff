"""Singleton row holding the global, editable site configuration."""

from __future__ import annotations

from flask import url_for

from app.extensions import db
from app.models.base import BaseModel


class SiteSettings(BaseModel):
    __tablename__ = "site_settings"

    id = db.Column(db.Integer, primary_key=True)

    # Identity
    site_name = db.Column(db.String(120), nullable=False, default="ON & OFF")
    tagline = db.Column(db.String(255), default="")
    meta_description = db.Column(db.String(320), default="")
    logo_filename = db.Column(db.String(255))
    favicon_filename = db.Column(db.String(255))

    # Hero
    hero_title = db.Column(db.String(255), default="")
    hero_subtitle = db.Column(db.Text, default="")
    hero_filename = db.Column(db.String(255))
    hero_cta_label = db.Column(db.String(80), default="")
    hero_cta_url = db.Column(db.String(255), default="")

    # About / corporate
    about_title = db.Column(db.String(255), default="")
    about_body = db.Column(db.Text, default="")
    mission = db.Column(db.Text, default="")
    vision = db.Column(db.Text, default="")

    # Contact
    contact_email = db.Column(db.String(255), default="")
    contact_phone = db.Column(db.String(80), default="")
    contact_whatsapp = db.Column(db.String(80), default="")
    address = db.Column(db.String(255), default="")

    # Social
    facebook_url = db.Column(db.String(255), default="")
    instagram_url = db.Column(db.String(255), default="")
    linkedin_url = db.Column(db.String(255), default="")
    tiktok_url = db.Column(db.String(255), default="")
    youtube_url = db.Column(db.String(255), default="")

    # Theme
    primary_color = db.Column(db.String(20), default="#0f0f10")
    accent_color = db.Column(db.String(20), default="#ff4d1c")
    footer_text = db.Column(db.Text, default="")

    @classmethod
    def get(cls) -> SiteSettings:
        """Return the single settings row, creating it on first use."""
        settings = db.session.get(cls, 1)
        if settings is None:
            settings = cls(id=1)
            db.session.add(settings)
            db.session.commit()
        return settings

    @staticmethod
    def _file_url(filename: str | None) -> str | None:
        if not filename:
            return None
        return url_for("public.uploaded_file", filename=filename)

    @property
    def logo_url(self) -> str | None:
        return self._file_url(self.logo_filename)

    @property
    def favicon_url(self) -> str | None:
        return self._file_url(self.favicon_filename)

    @property
    def hero_url(self) -> str | None:
        return self._file_url(self.hero_filename)

    @property
    def social_links(self) -> list[tuple[str, str]]:
        links = [
            ("Facebook", self.facebook_url),
            ("Instagram", self.instagram_url),
            ("LinkedIn", self.linkedin_url),
            ("TikTok", self.tiktok_url),
            ("YouTube", self.youtube_url),
        ]
        return [(label, url) for label, url in links if url]
