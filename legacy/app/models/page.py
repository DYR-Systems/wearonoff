"""Free-form content pages creatable from the CMS."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import url_for
from sqlalchemy.orm import Mapped

from app.extensions import db
from app.models.base import BaseModel, relationship

if TYPE_CHECKING:
    from app.models.media import Media


class Page(BaseModel):
    __tablename__ = "pages"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    body = db.Column(db.Text, default="")
    cover_filename = db.Column(db.String(255))

    is_published = db.Column(db.Boolean, default=True, nullable=False)
    show_in_nav = db.Column(db.Boolean, default=False, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)

    meta_title = db.Column(db.String(255), default="")
    meta_description = db.Column(db.String(320), default="")

    gallery: Mapped[list[Media]] = relationship(
        "Media",
        backref=db.backref("page", lazy="joined"),
        lazy="select",
        cascade="all, delete-orphan",
        order_by="Media.sort_order",
    )

    @property
    def url(self) -> str:
        return url_for("public.page_detail", slug=self.slug)

    @property
    def cover_url(self) -> str | None:
        if not self.cover_filename:
            return None
        return url_for("public.uploaded_file", filename=self.cover_filename)

    def __repr__(self) -> str:
        return f"<Page {self.slug}>"
