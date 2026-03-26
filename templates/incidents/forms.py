from django import forms
from .models import Incident
from accounts.models import CustomUser


class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['title', 'description', 'priority']   # ✅ FIXED

    # Keep this for update form later if needed
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only modify if field exists (safe check)
        if 'assigned_to' in self.fields:
            self.fields['assigned_to'].queryset = CustomUser.objects.filter(
                role__iexact='analyst'
            )

