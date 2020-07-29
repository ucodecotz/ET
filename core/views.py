import string
from random import random
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from rest_framework import viewsets, request
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from .forms import *

"""
Here are project endpoint
"""


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class Sub_priceViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPrice.objects.all()
    serializer_class = Sub_priceSerializer


class SubscriptionTypeViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer


class UserSubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = UserSubscriptions.objects.all()
    serializer_class = SubscriptionTypeSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class CombinationViewSet(viewsets.ModelViewSet):
    queryset = Combinations.objects.all()
    serializer_class = PaymentsSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = PaymentsSerializer



"""
Normal function for the project
"""


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


class InvoiceView(View):
    def get(self, *args, **kwargs):
        invoice = Invoice.objects.filter(user=self.request.user,
                                         is_paid=False)
        provider = ServiceProvider.objects.all()
        context = {
            'invoice': invoice,
            'provider': provider,

        }
        return render(self.request, 'invoice.html', context)

    def post(self, *args, **kwargs):
        pass


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def add_to_user_subscription(request, slug=None, ):
    try:
        sub_type = get_object_or_404(SubscriptionType, slug=slug)

        subscribe, created = UserSubscriptions.objects.get_or_create(

            user_id=request.user,
            subscription_type=sub_type,
            is_active=False

        )
        invoice_qs = Invoice.objects.filter(user=request.user, is_paid=False)

        if invoice_qs.exists():
            invoice = invoice_qs[0]
            if invoice.subscriptions.filter(subscription_type__slug=sub_type.slug).exists():
                if request.method == "POST":
                    form = UpdateSubscriptionDurationForm(request.POST)
                    subscribe.number_subscription_made += 1

                    if form.is_valid():

                        sub_duration = form.cleaned_data.get('sub_duration')
                        if sub_duration == 'D':
                            time_unit = 1
                            subscribe.end_date = subscribe.start_date + timedelta(days=time_unit)
                            subscribe.after_update_duration = sub_duration
                            # subscribe.after_update_price = sub_type.get_price_before_subscriptions() * common_price
                            subscribe.save()
                            messages.info(request, f"Your invoce eas updated  to {sub_duration} .")
                            print(sub_duration)
                            return redirect('core:invoice')

                        elif sub_duration == 'W':
                            time_unit = 7
                            subscribe.after_update_duration = sub_duration
                            subscribe.end_date = subscribe.start_date + timedelta(days=time_unit)
                            # subscribe.after_update_price = sub_type.get_price_before_subscriptions() * common_price
                            subscribe.save()
                            messages.info(request, f"Your invoce eas updated  to {sub_duration} .")
                            print(sub_duration)
                            return redirect('core:invoice')
                        elif sub_duration == 'M':
                            time_unit = 30.4368
                            subscribe.end_date = subscribe.start_date + timedelta(days=time_unit)
                            # subscribe.after_update_price = sub_type.get_price_before_subscriptions() * common_price
                            subscribe.after_update_duration = sub_duration
                            subscribe.save()
                            messages.info(request, f"Your invoce eas updated  to{sub_duration} .")
                            print(sub_duration)
                            return redirect('core:invoice')
                        elif sub_duration == 'Y':
                            time_unit = 365.2425
                            subscribe.end_date = subscribe.start_date + timedelta(days=time_unit)
                            subscribe.after_update_duration = sub_duration
                            subscribe.save()
                            messages.info(request, f"Your invoce eas updated  to{sub_duration} .")
                            print(sub_duration)

                            return redirect('core:invoice')

                    messages.info(request, f'This {sub_type.name} Plan was updated successfully')
                    return redirect('core:sub_details', slug=sub_type.slug)

            else:
                invoice.subscriptions.add(subscribe)
                messages.success(request, f'thanks for subscribing to {sub_type.name}')
                return redirect('core:sub_details', slug=sub_type.slug)
        else:
            user = request.user
            invoice = Invoice.objects.create(
                user=request.user,

            )
            invoice.subscriptions.add(subscribe)
            messages.success(request, f'Thanks for subscribing to {sub_type.name}')
            return redirect('core:sub_details', slug=sub_type.slug)
    except ObjectDoesNotExist:
        messages.error(request, 'Object not found')
        return redirect('core:sub_details', slug=slug)
    messages.warning(request, 'Subscription already exists')
    return redirect('core:sub_details', slug=slug)


def Select_provider(request, pk=None):
    try:
        provider = get_object_or_404(ServiceProvider, pk=pk)
        invoice = Invoice.objects.filter(user=request.user, is_paid=False)
        if invoice.exists():
            customer_invoice = invoice[0]
            customer_invoice.service_provider_id = provider
            customer_invoice.save()
            messages.success(request, f'Payment Options was added successfully ,Continue to payment as {provider.name}')
            return redirect('core:paymentForm')
        else:
            messages.success(request, 'Tou have no Invoice for now')
            return redirect('core:invoice')

    except ObjectDoesNotExist:
        messages.success(request, ' Something wrong happened , please contact the support')
        return redirect('core:invoice')


class PaymentForm(View):
    def get(self, args, **kwargs):
        return render(self.request, 'payment.html',
                      context={
                          'invoice': Invoice.objects.filter(user=self.request.user, is_paid=False)

                      })

    def post(self, *args, **kwargs):
        # insert payment logic here
        try:
            invoices = Invoice.objects.get(
                user=self.request.user,
                is_paid=False)

            '''
            # TODO  payment getaway api
            '''

            # subscriptions = UserSubscriptions.objects.get(
            #     user_id=self.request.user,
            #     is_active=False,
            #
            # ).first()
            payments = Payments()
            payments.amount = invoices.get_total()
            payments.user = self.request.user
            # TODO
            """
            i have generated normal ref_key for now but this should come from server_provider
            
            """
            payments.reference_id_from_ISP = create_ref_code()
            payments.success_type = 'Payments descriptions heare'
            payments.save()

            sub_user = invoices.subscriptions.all()
            sub_user.update(is_paid=True, is_active=True, payment=payments)
            for sub in sub_user:
                sub.save()

            # update the invoice to paid
            invoices.payments = payments
            invoices.is_paid = True
            invoices.save()
            # again show the subscriber is active for this time
            # subscriptions.payment = payments
            # subscriptions.save()

        except ObjectDoesNotExist:
            raise Http404('Requested user not found.')

        messages.success(self.request, 'Thanks for making payments')
        return redirect('core:homepage')
