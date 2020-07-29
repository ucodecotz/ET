from django import forms
from .models import *


class UpdateSubscriptionDurationForm(forms.ModelForm):
    # sub_duration = forms.CharField()

    class Meta:
        model = SubscriptionType
        fields = ('sub_duration',)


class payments_form(forms.ModelForm):
    model = Payments
    fields = ('amount', 'reference_id_from_ISP')


class ServiceProviderForm(forms.ModelForm):
    model = ServiceProvider
    fields = ('name', 'image',)
