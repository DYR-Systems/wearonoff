"""Uploaded files. Acts as a small reusable media library."""

from __future__ import annotations

from flask import url_for

from app.extensions import db
from app.models.base import BaseModel


class Media(BaseModel):
    __tablename__ = "media"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    thumbnail_filename = db.Column(db.String(255))
    original_filename = db.Column(db.String(255))
    alt_text = db.Column(db.String(255), default="")
    caption = db.Column(db.String(500), default="")
    mime_type = db.Column(db.String(100))
    size = db.Column(db.Integer, default=0)
    width = db.Column(db.Integer, default=0)
    height = db.Column(db.Integer, default=0)
    sort_order = db.Column(db.Integer, default=0, nullable=False)

    # Optional ownership. A file may belong to a brand gallery, a project
    # gallery or a page gallery (or to none of them = standalone library file).
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id", ondelete="CASCADE"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"))
    page_id = db.Column(db.Integer, db.ForeignKey("pages.id", ondelete="CASCADE"))
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))

    @property
    def url(self) -> str:
        return url_for("public.uploaded_file", filename=self.filename)

    @property
    def thumbnail_url(self) -> str:
        return url_for(
            "public.uploaded_file",
            filename=self.thumbnail_filename or self.filename,
        )

    @property
    def extension(self) -> str:
        return (self.filename or "").rsplit(".", 1)[-1].lower()

    @property
    def is_image(self) -> bool:
        return (self.mime_type or "").startswith("image/")
