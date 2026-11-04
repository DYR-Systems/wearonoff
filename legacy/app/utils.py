"""Small, dependency-free helpers shared across the app."""

from __future__ import annotations

import re
import unicodedata

_SLUG_STRIP = re.compile(r"[^a-z0-9]+")
_SLUG_DASH = re.compile(r"-{2,}")


def clean(value: str | None) -> str:
    """Return a trimmed string, treating ``None`` as an empty string."""
    return (value or "").strip()


def slugify(value: str) -> str:
    """Turn an arbitrary string into a URL friendly slug.

    Accents are removed (``Marca Nino`` -> ``marca-nino``) so slugs remain
    portable across databases and hosting providers.
    """
    value = unicodedata.normalize("NFKD", value or "")
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower().strip()
    value = _SLUG_STRIP.sub("-", value)
    return _SLUG_DASH.sub("-", value).strip("-")


def unique_slug(model, value: str, *, current_id: int | None = None) -> str:  # noqa: ANN001
    """Return a slug unique for ``model`` appending ``-2``, ``-3``... if needed."""
    base = slugify(value) or "item"
    candidate = base
    counter = 1
    while True:
        query = model.query.filter(model.slug == candidate)
        if current_id is not None:
            query = query.filter(model.id != current_id)
        if query.first() is None:
            return candidate
        counter += 1
        candidate = f"{base}-{counter}"
