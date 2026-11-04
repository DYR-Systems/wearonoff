"""Reusable model base class and mixins."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy.orm import relationship as _relationship

from app.extensions import db

# SQLAlchemy returns ``RelationshipProperty`` which is not assignable to the
# ``Mapped[...]`` annotation used for type checkers. Re-exporting it as ``Any``
# keeps the runtime call identical while letting the annotation drive typing.
relationship: Any = _relationship


def utcnow() -> datetime:
    return datetime.now(UTC)


class TimestampMixin:
    """Adds created/updated timestamps to a model."""

    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )


class BaseModel(db.Model, TimestampMixin):
    """Abstract base model.

    SQLAlchemy's declarative constructor is dynamic, so type checkers cannot
    infer that it accepts column keyword arguments. The ``TYPE_CHECKING``
    ``__init__`` restores that signature without affecting runtime behaviour.
    """

    __abstract__ = True
    # Relationships are annotated as ``Any`` for type checkers; this tells
    # SQLAlchemy to treat such annotations as legacy (non ``Mapped``) ones.
    __allow_unmapped__ = True

    if TYPE_CHECKING:

        def __init__(self, **kwargs: Any) -> None: ...
