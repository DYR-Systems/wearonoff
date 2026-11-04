"""Child brands managed by the parent company."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import url_for
from sqlalchemy.orm import Mapped

from app.extensions import db
from app.models.base import BaseModel, relationship

if TYPE_CHECKING:
    from app.models.media import Media


class Brand(BaseModel):
    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False, index=True)
    domain = db.Column(db.String(255), default="")

    tagline = db.Column(db.String(255), default="")
    short_description = db.Column(db.Text, default="")
    description = db.Column(db.Text, default="")

    logo_filename = db.Column(db.String(255))
    cover_filename = db.Column(db.String(255))
    primary_color = db.Column(db.String(20), default="")

    website_url = db.Column(db.String(255), default="")
    store_url = db.Column(db.String(255), default="")
    is_store = db.Column(db.Boolean, default=False, nullable=False)

    is_published = db.Column(db.Boolean, default=True, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)

    meta_title = db.Column(db.String(255), default="")
    meta_description = db.Column(db.String(320), default="")

    # Media attached as a gallery (Media.brand_id == brand.id)
    gallery: Mapped[list[Media]] = relationship(
        "Media",
        backref=db.backref("brand", lazy="joined"),
        lazy="select",
        cascade="all, delete-orphan",
        order_by="Media.sort_order",
    )

    @property
    def url(self) -> str:
        return url_for("public.brand_detail", slug=self.slug)

    @property
    def logo_url(self) -> str | None:
        if not self.logo_filename:
            return None
        return url_for("public.uploaded_file", filename=self.logo_filename)

    @property
    def cover_url(self) -> str | None:
        if not self.cover_filename:
            return None
        return url_for("public.uploaded_file", filename=self.cover_filename)

    @property
    def initials(self) -> str:
        parts = [p for p in self.name.split() if p]
        return "".join(p[0] for p in parts[:2]).upper() or "?"

    @property
    def display_url(self) -> str:
        if self.store_url:
            return self.store_url
        if self.website_url:
            return self.website_url
        return self.url

    @property
    def is_external(self) -> bool:
        return bool(self.store_url or self.website_url)

    def __repr__(self) -> str:
        return f"<Brand {self.slug}>"
