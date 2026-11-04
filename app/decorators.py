"""Authorization decorators."""

from __future__ import annotations

from functools import wraps

from flask import abort
from flask_login import current_user


def superadmin_required(view):  # noqa: ANN001, ANN201
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_superadmin:
            abort(403)
        return view(*args, **kwargs)

    return wrapper
