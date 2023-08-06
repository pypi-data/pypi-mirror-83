from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm, AuthenticationForm
from django.forms import CharField
from django.utils.translation import ugettext as _

from fandango.forms.base import BaseForm


class BasePasswordForm(BaseForm):
    submit_text = _("Change password")


class CustomSetPasswordForm(BasePasswordForm, PasswordChangeForm):
    pass


class CustomPasswordResetForm(BasePasswordForm, PasswordResetForm):
    pass


class CustomResetPasswordForm(BasePasswordForm, SetPasswordForm):
    pass


class LoginForm(BaseForm, AuthenticationForm):
    submit_text = _("Login")
    username = CharField(label=_("Email or username"), max_length=150)
