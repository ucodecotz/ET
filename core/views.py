import string
from random import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import *
from .forms import *


class home(ListView):
    model = SubscriptionType
    template_name = 'home.html'


class sub_details(DetailView):
    model = SubscriptionType
    template_name = 'details.html'

    def get_context_data(self, **kwargs):
        context = super(sub_details, self).get_context_data()
        form_class = UpdateSubscriptionDurationForm
        context.update(
            {'update_sub_form': form_class}
        )
        return context


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def add_to_user_subscription(request, slug=None, ):
    sub_type = get_object_or_404(SubscriptionType, slug=slug)
    common_price = 2000
    subscribe, created = UserSubscriptions.objects.get_or_create(

        user_id=request.user,
        subscription_type=sub_type,
        active=False

    )
    invoice_qs = Invoice.objects.filter(user=request.user, payment_status=False)
    if invoice_qs.exists():
        invoice = invoice_qs[0]
        if invoice.subscriptions.filter(subscription_type__slug=sub_type.slug).exists():
            if request.method == "POST":
                form = UpdateSubscriptionDurationForm(request.POST)

                if form.is_valid():
                    _sub_unit_days = {
                        'D': 1.,
                        'W': 7.,
                        'M': 30.4368,  # http://en.wikipedia.org/wiki/Month#Julian_and_Gregorian_calendars
                        'Y': 365.2425,  # http://en.wikipedia.org/wiki/Year#Calendar_year
                    }

                    sub_duration = form.cleaned_data.get('sub_duration')
                    if sub_duration == 'D':
                        time_unit = 1
                        subscribe.end_date = subscribe.start_date + timedelta(days=time_unit)
                        subscribe.after_update_duration = sub_duration
                        subscribe.after_update_price = sub_type.get_price_before_subscriptions() * common_price
                        subscribe.save()
                        messages.info(request, f"Your invoce eas updated  to{sub_duration} .")
                        print(sub_duration)
                        return redirect('core:sub_details', slug=sub_type.slug)

                    elif sub_duration == 'W':
                        time_unit = 7
                        subscribe.after_update_duration = sub_duration
                        subscribe.end_date = subscribe.start_date + timedelta(days=time_unit)
                        subscribe.after_update_price = sub_type.get_price_before_subscriptions() * common_price
                        subscribe.save()
                        messages.info(request, "This item quantity was updated.")
                        print(sub_duration)
                        return redirect('core:sub_details', slug=sub_type.slug)
                    elif sub_duration == 'M':
                        time_unit = 30.4368
                        subscribe.after_update_price = sub_type.get_price_before_subscriptions() * common_price
                        subscribe.end_date = subscribe.start_date + timedelta(days=time_unit)
                        subscribe.after_update_duration = sub_duration
                        subscribe.save()
                        messages.info(request, f"Your invoce eas updated  to{sub_duration} .")
                        print(sub_duration)
                        return redirect('core:sub_details', slug=sub_type.slug)
                    elif sub_duration == 'Y':
                        time_unit = 365.2425
                        subscribe.after_update_price = sub_type.get_price_before_subscriptions() * common_price
                        subscribe.end_date = subscribe.start_date + timedelta(days=time_unit)
                        subscribe.after_update_duration = sub_duration
                        subscribe.save()
                        messages.info(request, f"Your invoce eas updated  to{sub_duration} .")
                        print(sub_duration)
                        return redirect('core:sub_details', slug=sub_type.slug)

                messages.info(request, f'This {sub_type.name} Plan was updated successfully')
                return redirect('core:sub_details', slug=sub_type.slug)

        else:
            invoice.subscriptions.add(subscribe)

            messages.success(request, f'thanks for subscribing to {sub_type.name}')
            return redirect('core:sub_details', slug=sub_type.slug)
    else:

        invoice = Invoice.objects.create(user=request.user, )
        invoice.subscriptions.add(subscribe)
        messages.success(request, f'thanks for subscribing to {sub_type.name}')
    return redirect('core:sub_details', slug=slug)
