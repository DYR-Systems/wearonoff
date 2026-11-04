"""Image upload pipeline: validation, resizing, thumbnails and storage.

Files are written under ``UPLOAD_FOLDER`` using a date based layout::

    instance/uploads/2026/09/<uuid>.jpg
    instance/uploads/thumbs/2026/09/<uuid>.jpg

The public URL is served by :func:`app.routes.public.uploaded_file`.
"""

from __future__ import annotations

import mimetypes
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from flask import current_app
from PIL import Image, ImageOps, UnidentifiedImageError
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.media import Media

RASTER_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".bmp", ".tiff"}
VECTOR_FORMATS = {".svg"}


class UploadError(Exception):
    """Raised when an uploaded file is missing or not a valid image."""


@dataclass
class SavedImage:
    filename: str
    thumbnail_filename: str
    width: int
    height: int
    size: int
    mime_type: str


def _extension(filename: str) -> str:
    return Path(filename or "").suffix.lower()


def allowed_image(filename: str) -> bool:
    ext = _extension(filename).lstrip(".")
    return ext in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def _upload_root() -> Path:
    root = Path(current_app.config["UPLOAD_FOLDER"])
    root.mkdir(parents=True, exist_ok=True)
    return root


def _relative_dir() -> Path:
    now = datetime.now(UTC)
    return Path(f"{now.year:04d}") / f"{now.month:02d}"


def _absolute(relative: str) -> Path:
    root = _upload_root().resolve()
    path = (root / relative).resolve()
    if root not in path.parents and path != root:
        raise UploadError("Ruta de archivo invalida.")
    return path


def _guess_mime(filename: str) -> str:
    return mimetypes.guess_type(filename)[0] or "application/octet-stream"


def _write_bytes(relative: str, data: bytes) -> int:
    path = _absolute(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return len(data)


def _guess_extension(file_storage: FileStorage) -> str:
    original = secure_filename(file_storage.filename or "")
    ext = _extension(original)
    if ext:
        return ext
    if file_storage.mimetype:
        guessed = mimetypes.guess_extension(file_storage.mimetype)
        if guessed:
            return guessed
    return ".bin"


def _raster_filename(file_storage: FileStorage) -> str:
    ext = _guess_extension(file_storage)
    stem = uuid.uuid4().hex
    return f"{stem}{ext}"


def process_image(file_storage: FileStorage) -> SavedImage:
    """Validate, normalise and persist an uploaded image."""
    if file_storage is None or not file_storage.filename:
        raise UploadError("No se recibio ningun archivo.")

    original_name = secure_filename(file_storage.filename)
    if not allowed_image(original_name):
        raise UploadError(f"Formato no permitido: {original_name}")

    ext = _guess_extension(file_storage)
    relative_dir = _relative_dir()
    filename = _raster_filename(file_storage)
    relative = str(relative_dir / filename)

    if ext in VECTOR_FORMATS:
        # SVG cannot be rasterised with Pillow; keep it untouched.
        file_storage.stream.seek(0)
        data = file_storage.stream.read()
        size = _write_bytes(relative, data)
        return SavedImage(
            filename=relative,
            thumbnail_filename=relative,
            width=0,
            height=0,
            size=size,
            mime_type="image/svg+xml",
        )

    if ext not in RASTER_FORMATS:
        raise UploadError(f"Formato no permitido: {original_name}")

    try:
        file_storage.stream.seek(0)
        image = Image.open(file_storage.stream)
        image.load()
    except (UnidentifiedImageError, OSError) as exc:
        raise UploadError("El archivo no es una imagen valida.") from exc

    if getattr(image, "is_animated", False):
        # Preserve animated GIF/WebP: store the original bytes untouched.
        file_storage.stream.seek(0)
        data = file_storage.stream.read()
        size = _write_bytes(relative, data)
        return SavedImage(
            filename=relative,
            thumbnail_filename=relative,
            width=image.width,
            height=image.height,
            size=size,
            mime_type=_guess_mime(original_name),
        )

    image = ImageOps.exif_transpose(image)

    max_dimension = int(current_app.config["IMAGE_MAX_DIMENSION"])
    if max(image.size) > max_dimension:
        image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

    save_kwargs: dict[str, Any] = {"optimize": True}
    if ext in {".jpg", ".jpeg"}:
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")
        save_kwargs["quality"] = 88
        save_kwargs["progressive"] = True
    elif ext == ".png":
        if image.mode not in ("RGB", "RGBA", "L", "LA", "P"):
            image = image.convert("RGBA")
    elif ext == ".webp":
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
        save_kwargs["quality"] = 85

    path = _absolute(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, **save_kwargs)
    size = path.stat().st_size

    thumb_rel = str(Path("thumbs") / relative_dir / filename)
    thumbnail = image.copy()
    thumbnail.thumbnail(
        tuple(current_app.config["THUMBNAIL_SIZE"]),
        Image.Resampling.LANCZOS,
    )
    thumb_path = _absolute(thumb_rel)
    thumb_path.parent.mkdir(parents=True, exist_ok=True)
    if thumb_rel.lower().endswith((".jpg", ".jpeg")):
        thumb_kwargs: dict[str, Any] = {
            "quality": current_app.config["THUMBNAIL_QUALITY"],
            "optimize": True,
        }
    else:
        thumb_kwargs = {"optimize": True}
    if thumb_path.suffix.lower() in {".jpg", ".jpeg"} and thumbnail.mode not in ("RGB", "L"):
        thumbnail = thumbnail.convert("RGB")
    thumbnail.save(thumb_path, **thumb_kwargs)

    return SavedImage(
        filename=relative,
        thumbnail_filename=thumb_rel,
        width=image.width,
        height=image.height,
        size=size,
        mime_type=_guess_mime(original_name),
    )


def save_media(
    file_storage: FileStorage,
    *,
    alt_text: str = "",
    caption: str = "",
    uploaded_by_id: int | None = None,
    brand_id: int | None = None,
    project_id: int | None = None,
    page_id: int | None = None,
    sort_order: int = 0,
) -> Media:
    """Process an upload and store it as a :class:`Media` row."""
    saved = process_image(file_storage)
    media = Media(
        filename=saved.filename,
        thumbnail_filename=saved.thumbnail_filename,
        original_filename=secure_filename(file_storage.filename or ""),
        alt_text=alt_text,
        caption=caption,
        mime_type=saved.mime_type,
        size=saved.size,
        width=saved.width,
        height=saved.height,
        uploaded_by_id=uploaded_by_id,
        brand_id=brand_id,
        project_id=project_id,
        page_id=page_id,
        sort_order=sort_order,
    )
    db.session.add(media)
    return media


def _delete_relative(relative: str | None) -> None:
    if not relative:
        return
    try:
        path = _absolute(relative)
    except UploadError:
        return
    if path.is_file():
        path.unlink(missing_ok=True)


def delete_media(media: Media) -> None:
    """Remove a media row and its stored files."""
    _delete_relative(media.filename)
    if media.thumbnail_filename and media.thumbnail_filename != media.filename:
        _delete_relative(media.thumbnail_filename)
    db.session.delete(media)


def delete_image(filename: str | None, *, thumbnail: str | None = None) -> None:
    """Delete a stored image (and optional thumbnail) by relative path."""
    _delete_relative(filename)
    if thumbnail and thumbnail != filename:
        _delete_relative(thumbnail)
