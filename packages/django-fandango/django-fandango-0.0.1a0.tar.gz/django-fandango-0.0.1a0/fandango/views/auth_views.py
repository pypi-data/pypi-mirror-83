from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import RedirectView

from fandango.forms.auth_forms import CustomPasswordResetForm, CustomResetPasswordForm, CustomSetPasswordForm
from fandango.views.base import BaseTemplateView


class PostLoginView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        # do something more useful?
        return reverse("index")


class LogoutView(BaseTemplateView):
    title = _("Logout")
    text = _("You have been logged out")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(self, request, *args, **kwargs)


class CustomLoginView(BaseTemplateView, LoginView):
    # can't do it like this:
    # extra_text = _('<a href="%s">Forgot password?</a>' % reverse_lazy("password_reset"))
    # ... end up getting this:
    # django.core.exceptions.ImproperlyConfigured: The included URLconf 'django_tango.urls' does not appear to have any
    # patterns in it. If you see valid patterns in the file then the issue is probably caused by a circular import.

    def get_extra_text(self):
        return _('<a href="%s">Forgot password?</a>' % reverse_lazy("password_reset"))


class PasswordResetBaseView(BaseTemplateView):
    title = _("Reset password")


class CustomPasswordResetView(PasswordResetBaseView, PasswordResetView):
    form_class = CustomPasswordResetForm


class CustomPasswordResetConfirmView(PasswordResetBaseView, PasswordResetConfirmView):
    form_class = CustomResetPasswordForm


class CustomPasswordResetCompleteView(PasswordResetBaseView):

    def get_extra_text(self):
        return _('The password reset is done<p><a href="%s">Login</a></p>' % reverse("login"))


def change_password(request):
    if request.method == 'POST':
        form = CustomSetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _("Your password was changed."))
            return redirect('change_password')
    else:
        form = CustomSetPasswordForm(request.user)

    context = {}
    context["form"] = form
    context["title"] = _("Change password")
    return render(request, 'website/base.html', context)
