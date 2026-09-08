from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "accounts/login.html"


class AccountsLogoutView(LogoutView):
    next_page = "login"
