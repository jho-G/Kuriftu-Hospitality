from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import SiteLoginForm
from .web_views import dashboard_view, signup_view

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path(
        "login/",
        LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=SiteLoginForm,
            redirect_authenticated_user=True,
            extra_context={"nav_active": "account"},
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page=getattr(settings, "LOGOUT_REDIRECT_URL", "/") or "/"),
        name="logout",
    ),
    path("dashboard/", dashboard_view, name="dashboard"),
]
