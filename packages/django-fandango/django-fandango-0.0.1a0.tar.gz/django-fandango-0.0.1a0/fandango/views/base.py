from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, UpdateView, TemplateView

from fandango.conf.settings import base_template
from fandango.forms import get_default_form_helper
from fandango.utils.models import get_editable_by_name, get_model_dict


class StaffRequiredView:

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class BaseView:
    title = None
    heading = None
    template_name = None
    extra_text = None
    template_name = base_template()

    def get_extra_text(self):
        return self.extra_text


class BaseTemplateView(BaseView, TemplateView):
    context_var = None


class GenericModelView:
    # set this so django doesn't crash with a ... "without the 'fields' attribute is prohibited."
    fields = ["id"]

    def dispatch(self, request, *args, **kwargs):
        model = get_editable_by_name(kwargs["model_name"])
        if model:
            self.model = model
        else:
            raise PermissionDenied()

        self.fields = self.model._meta.visible_fields
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # can't access _meta in them templates...
        context["model"] = get_model_dict(self.model)
        return context


class BaseCreateUpdateView(BaseView):
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        message = _("The %s was added" % self.model._meta.verbose_name)
        messages.add_message(self.request, messages.INFO, message)
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.helper = get_default_form_helper(self.submit_button_text)
        return form


class BaseCreateView(BaseCreateUpdateView, CreateView):
    model = None
    submit_button_text = _("Save")


class BaseUpdateView(BaseCreateUpdateView, UpdateView):
    model = None
    submit_button_text = _("Update")
