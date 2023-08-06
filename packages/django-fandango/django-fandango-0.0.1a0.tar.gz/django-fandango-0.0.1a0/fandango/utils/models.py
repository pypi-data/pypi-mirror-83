import django
from django.apps import apps
from django.db.models import Q
from django.urls import reverse


def get_editable_by_name(model_name):
    for model in get_editable_models():
        split = model._meta.model_name.split(".")
        if split[0] == model_name:
            return model

    return None


def get_editable_models_dict():
    models = []
    for model in get_editable_models():
        models.append(get_model_dict(model))
    return models


def get_model_dict(model):
    model_dict = dict()
    model_dict["meta"] = model._meta
    if hasattr(model._meta, "create_url"):
        model_dict["create_url"] = model._meta.create_url
    else:
        model_dict["create_url"] = reverse("create_model", args=[model._meta.model_name])

    return model_dict


def get_editable_models():
    models = []
    for model in django.apps.apps.get_models():
        if hasattr(model._meta, "visible_fields"):
            models.append(model)
    models.sort(key=lambda x: x._meta.model_name, reverse=True)
    return models


def search_model(model, fields, query):
    qr = None
    for field in fields:
        q = Q(**{"%s__icontains" % field: query})
        if qr:
            qr = qr | q
        else:
            qr = q

        return model.objects.filter(qr).order_by("id")
