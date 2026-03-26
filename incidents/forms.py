from django import forms
from .models import Incident, IncidentLog
from accounts.models import CustomUser


# FORM FOR CREATING INCIDENT (user)
class IncidentCreateForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['title', 'description', 'priority']


# FORM FOR UPDATING INCIDENT (manager/analyst)
class IncidentUpdateForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['status', 'assigned_to', 'priority', 'description']

    # only analysts in dropdown
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = CustomUser.objects.filter(role__iexact='analyst')
class InvestigationNoteForm(forms.ModelForm):
    class Meta:
        model = IncidentLog
        fields = ["note"]
        widgets = {
            "note": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Write investigation notes...",
                "class": "form-control"
            })
        }
