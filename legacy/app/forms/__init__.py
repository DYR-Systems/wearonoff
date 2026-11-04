"""WTForms definitions."""

from app.forms.auth import LoginForm, ProfileForm, UserForm
from app.forms.contact import ContactForm
from app.forms.content import BrandForm, PageForm, ProjectForm, SettingsForm
from app.forms.media import MediaEditForm, MediaUploadForm

__all__ = [
    "BrandForm",
    "ContactForm",
    "LoginForm",
    "MediaEditForm",
    "MediaUploadForm",
    "PageForm",
    "ProfileForm",
    "ProjectForm",
    "SettingsForm",
    "UserForm",
]
