from django import forms


class CreateHouseholdForm(forms.Form):
    name = forms.CharField(max_length=120, label="Household name")
