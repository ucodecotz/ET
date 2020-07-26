import string
from random import random

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import *


class home(ListView):
    model = SubscriptionType
    template_name = 'home.html'


class sub_details(DetailView):
    model = SubscriptionType
    template_name = 'details.html'


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def add_to_user_subscription(request, slug=None):
    sub_type = get_object_or_404(SubscriptionType, slug=slug)
    subscribe, created = USerSubscriptions.objects.get_or_create(
        user_id=request.user,
        subscription_type=sub_type,
        active=False

    )
    invoice_qs = Invoice.objects.filter(user=request.user, payment_status=False)
    if invoice_qs.exists():
        invoice = invoice_qs[0]
        if invoice.subscriptions.filter(subscription_type__slug=sub_type.slug).exists():
            # ToDO add more functionality when the wantes to later customize the plan
            messages.info(request, f'This {sub_type.name} Plan was updated successfully')
        else:
            invoice.subscriptions.add(subscribe)
            
            messages.success(request, f'thanks for subscribing to {sub_type.name}')
            return redirect('core:sub_details', slug=sub_type.slug)
    else:

        invoice = Invoice.objects.create(user=request.user, )
        invoice.subscriptions.add(subscribe)
        messages.success(request, f'thanks for subscribing to {sub_type.name}')
    return redirect('core:sub_details', slug=slug)
