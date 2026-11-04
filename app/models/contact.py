"""Messages sent through the public contact form."""

from __future__ import annotations

from app.extensions import db
from app.models.base import BaseModel


class ContactMessage(BaseModel):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(80), default="")
    company = db.Column(db.String(160), default="")
    subject = db.Column(db.String(255), default="")
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<ContactMessage {self.email}>"
