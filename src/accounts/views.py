from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "accounts/login.html"


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/home.html"


class AccountsLogoutView(LogoutView):
    next_page = "login"
