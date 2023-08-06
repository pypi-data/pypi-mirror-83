from django.conf.urls.static import static
from django.urls import path

from fandango.conf.settings import print_at_startup
from fandango.forms.auth_forms import LoginForm
from fandango.views.auth_views import CustomLoginView, PostLoginView, LogoutView, change_password, \
    CustomPasswordResetView, PasswordResetBaseView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
from fandango.views.json_views import JSONSuggestView
from fandango.views.views import GenericListView, GenericModelCreateView, GenericModelUpdateView
from django.utils.translation import ugettext as _
from django.conf import settings

urlpatterns = [
    #######################################
    # auth/login
    #######################################
    path('login/', CustomLoginView.as_view(authentication_form=LoginForm, title=_("Login")), name="login"),
    path('post-login/', PostLoginView.as_view(), name="post_login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    # password
    path('password/', change_password, name="change_password"),
    path('password/reset/', CustomPasswordResetView.as_view(), name="password_reset"),
    path('password/reset/done/', PasswordResetBaseView.as_view(extra_text="Instructions on how to reset the password "
                                                                          "has been sent to your email-address."),
         name="password_reset_done"),
    path('password/reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password/reset/complete/', CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    #######################################
    # list view(s)
    #######################################
    path('list/<model_name>/', GenericListView.as_view(), name='list_view'),

    #######################################
    # generic model create/update views
    #######################################
    path('create/<model_name>/', GenericModelCreateView.as_view(), name='create_model'),
    path('update/<model_name>/<int:id>', GenericModelUpdateView.as_view(), name='update_model'),

    #######################################
    # hxr-views
    #######################################
    path('json/<model_name>/', JSONSuggestView.as_view(), name='json_suggest'),
]

if settings.DEBUG:
    # add media ... if it's debug
    urlpatterns += static(getattr(settings, "MEDIA_URL", None), document_root=getattr(settings, "MEDIA_ROOT", None))

if print_at_startup():
    from fandango import bootstrap
