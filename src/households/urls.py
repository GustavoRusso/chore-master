from django.urls import path

from src.households import views

urlpatterns = [
    path("", views.HomeGateView.as_view(), name="home"),
    path("households/create/", views.CreateHouseholdView.as_view(), name="household_create"),
    path("household/", views.HouseholdHomeView.as_view(), name="household_home"),
]
