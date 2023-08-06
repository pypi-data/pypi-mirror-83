from django.urls import reverse
from django.utils.translation import ugettext as _
from django_tables2 import SingleTableView, RequestConfig, tables

from fandango.forms.forms import GenericModelSearchForm
from fandango.views.base import GenericModelView, BaseCreateUpdateView, BaseCreateView, BaseUpdateView


def get_default_table(model):
    table_class = tables.table_factory(model, fields=model._meta.visible_fields + ["get_add_link"])
    table_class._meta.attrs["class"] = "table table-striped table-responsive table-hover w-100 d-block d-md-table"
    return table_class


class GenericListView(GenericModelView, SingleTableView):
    paginate_by = 25
    template_name = "website/list_view.html"

    def get_table_class(self):
        return get_default_table()

    def get_table(self, **kwargs):
        table = super().get_table(**kwargs)
        return RequestConfig(self.request, paginate=self.get_table_pagination(table)).configure(table)

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Models.search(self.model, self.model._meta.search_fields, query)

        return self.model.objects.all().order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.model._meta, "search_fields"):
            context["form"] = GenericModelSearchForm(self.request, model=self.model)
        return context


class GenericModelCreateUpdateView(GenericModelView, BaseCreateUpdateView):

    def get_success_url(self):
        return reverse("list_view", args=[self.model._meta.model_name])


class GenericModelCreateView(GenericModelCreateUpdateView, BaseCreateView):

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        self.heading = _("Create") + " " + self.model._meta.verbose_name
        return response


class GenericModelUpdateView(GenericModelCreateUpdateView, BaseUpdateView):

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        self.heading = _("Create") + " " + self.model._meta.verbose_name
        return response
