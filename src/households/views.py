from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView, TemplateView

from src.households.forms import CreateHouseholdForm
from src.households.models import Household, Membership, household_for


class HomeGateView(LoginRequiredMixin, View):
    def get(self, request):
        if household_for(request.user) is not None:
            return redirect("household_home")
        return redirect("household_create")


class CreateHouseholdView(LoginRequiredMixin, FormView):
    template_name = "households/create.html"
    form_class = CreateHouseholdForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and household_for(request.user) is not None:
            return redirect("household_home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        household = Household.objects.create(name=form.cleaned_data["name"])
        Membership.objects.create(user=self.request.user, household=household)
        return redirect("household_home")


class HouseholdHomeView(LoginRequiredMixin, TemplateView):
    template_name = "households/home.html"

    def get(self, request, *args, **kwargs):
        if household_for(request.user) is None:
            return redirect("household_create")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        household = household_for(self.request.user)
        context["household"] = household
        context["members"] = [
            membership.user
            for membership in household.memberships.select_related("user").all()
        ]
        return context
