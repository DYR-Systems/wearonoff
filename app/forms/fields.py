"""Custom WTForms fields."""

from __future__ import annotations

from typing import Any

from flask import request
from wtforms import MultipleFileField as _MultipleFileField
from wtforms.validators import Optional


class MultipleFileField(_MultipleFileField):
    """A ``MultipleFileField`` that is forgiving about empty submissions.

    WTForms' default validates the field even when no file was selected; this
    variant treats an empty selection as "no data" so it can be marked optional.
    """

    def __init__(self, label: str = "", validators: Any = None, **kwargs) -> None:
        super().__init__(label, validators=validators or [Optional()], **kwargs)

    def process_formdata(self, valuelist) -> None:  # noqa: ANN001
        if request is not None and request.files:
            self.data = [f for f in request.files.getlist(self.name) if f and f.filename]
        else:
            self.data = []
