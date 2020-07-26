from django import forms
from .models import *


class UpdateSubscriptionDurationForm(forms.ModelForm):
    # sub_duration = forms.CharField()

    class Meta:
        model = SubscriptionType
        fields = ('sub_duration',)
