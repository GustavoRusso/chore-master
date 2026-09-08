from django.urls import path

from src.accounts import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.AccountsLogoutView.as_view(), name="logout"),
]
