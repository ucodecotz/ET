import random
import string

from django.conf import settings
from django.contrib import auth
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.translation import ugettext as _, ungettext, ugettext_lazy

SUB_STATUS = (
    ('A', 'Active'),
    ('E', 'expired'),

    # TODO add add another

)

PAYMENT_STATUS = (
    ('p', 'Paid'),
    ('U', 'Unpaid'),
)

_TIME_UNIT_CHOICES = (
    ('D', ugettext_lazy('Day')),
    ('W', ugettext_lazy('Week')),
    ('M', ugettext_lazy('Month')),
    ('Y', ugettext_lazy('Year')),
)
_sub_unit_days = {
    'D': 1.,
    'W': 7.,
    'M': 30.4368,  # http://en.wikipedia.org/wiki/Month#Julian_and_Gregorian_calendars
    'Y': 365.2425,  # http://en.wikipedia.org/wiki/Year#Calendar_year
}


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_customer_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


class Combinations(models.Model):
    sub_type_id = models.ForeignKey('SubscriptionType', on_delete=models.CASCADE)
    combination_name = models.CharField(max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Combination'

    def __str__(self):
        return self.combination_name


class Subject(models.Model):
    combination_id = models.ManyToManyField(Combinations,
                                            blank=True)
    subject_name = models.CharField(max_length=50)
    create = models.DateTimeField(default=timezone.now)


# TODO: i dont suggest to have this table :
# TODO: coz we need to assign thr price to subscrtion type itself to remove redudant of tables


class SubscriptionPrice(models.Model):
    sub_price_code = models.CharField(max_length=200, null=True, blank=True)
    sub_price_amount = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Subscription Price'

    def __str__(self):
        return f' {str(self.sub_price_amount)}'


#  This is main table to handle our service
class SubscriptionType(models.Model):
    name = models.CharField(max_length=200, null=True, )
    sub_code = models.CharField(max_length=200, blank=True, null=True)
    # we need to add the user to subscription Group of user after subscription
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    sub_price = models.ForeignKey(SubscriptionPrice, null=True, blank=True, on_delete=models.CASCADE)
    sub_duration = models.CharField(max_length=200, choices=_TIME_UNIT_CHOICES, default='M', null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    #  slug is for making queries without using  "id"
    slug = models.SlugField(max_length=200, null=True)

    class Meta:
        verbose_name = 'Subscription Type'

    def __str__(self):
        return f" Subscribed to {str(self.name)}"

    def subscription_type_absolute_url(self):
        return reverse('core:sub_details', kwargs={
            'slug': self.slug
        })

    def get_add_to_user_subscription_url(self):
        return reverse('core:add_to_user_subscription', kwargs={'slug': self.slug})

    def get_price_before_subscriptions(self):
        print(int(self.sub_price.sub_price_amount))
        return int(self.sub_price.sub_price_amount)


#  this where all subscription are handled
class UserSubscriptions(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True, blank=True)
    subscription_type = models.ForeignKey(SubscriptionType,
                                          on_delete=models.CASCADE,
                                          null=True,
                                          blank=True)
    after_update_price = models.FloatField(null=True, blank=True, )

    after_update_duration = models.CharField(max_length=200, choices=_TIME_UNIT_CHOICES, default='M', null=True,
                                             blank=True)
    number_subscription_made = models.IntegerField(null=True, default=0)

    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    # from payment_type to payment_status
    payment = models.ForeignKey('Payments', on_delete=models.SET_NULL, blank=True, null=True)

    is_paid = models.BooleanField(default=False, )

    # TODO add timedelta here

    class Meta:
        verbose_name_plural = 'subscription'

    def get_price_before_subscriptions(self):
        return int(self.subscription_type.sub_price.sub_price_amount)

    def set_is_active(self):
        # we need to change the subscription  to active  if the payments is done

        self.is_active = True
        return self.is_active

    def set_is_paid(self):
        # we need to change the subscription by setting as is paid if the payments is done

        self.is_paid = True
        return self.is_paid

    def save(self, *args, **kwargs):
        charge_per_day = float(self.subscription_type.sub_price.sub_price_amount)

        if self.after_update_duration == 'M':
            self.after_update_price = charge_per_day * _sub_unit_days['M']
            self.end_date = self.start_date + timedelta(days=_sub_unit_days['M'])
            super(UserSubscriptions, self).save(*args, **kwargs)
        if self.after_update_duration == 'D':
            self.after_update_price = charge_per_day * _sub_unit_days['D']

            super(UserSubscriptions, self).save(*args, **kwargs)
        elif self.after_update_duration == 'W':
            self.after_update_price = charge_per_day * _sub_unit_days['W']
            super(UserSubscriptions, self).save(*args, **kwargs)

        elif self.after_update_duration == 'Y':
            self.after_update_price = charge_per_day * _sub_unit_days['Y']
            super(UserSubscriptions, self).save(*args, **kwargs)
        if self.payment is not None:
            self.is_active = self.set_is_active()
            self.payment_status = self.set_is_paid()
            super(UserSubscriptions, self).save(*args, **kwargs)

    # def get_final_price(self, *args, **kwargs):
    #     #  we can  a certain amount pay and
    #     #  sometimes try to times with the number of day the user has subscribed
    #     # TODO something to with final price hare afer subscripyion
    #     #  for now i can do this. not real what i wanted
    #     self.after_update_price = self.get_price_before_subscriptions()
    #     super(UserSubscriptions, self).get_final_price(**kwargs, *args)

    # TODO: add  expiration's function here
    # def subscription_expire(self):
    #     if self.end_date

    def __str__(self):
        return str(f"{self.user_id}'s subscription started on: {self.start_date}  and ends on{self.end_date} ")

    # TODO: add function to manage sub status after payments

    # TODO: we need function for handling thr total amount for subscriptions


class ServiceProvider(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='provider_image')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Service provider'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:select_provider', kwargs={'pk': self.pk})


def get_code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class Invoice(models.Model):
    INVOICE_STATUS = (
        ('P', 'pending invoice'),
        ('A', 'Approved')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    invoice_title = models.CharField(max_length=200, null=True, blank=True)
    invoice_code = models.CharField(max_length=200, null=True, blank=True)
    subscriptions = models.ManyToManyField(UserSubscriptions, blank=True)
    # payments method
    service_provider_id = models.ForeignKey('ServiceProvider', on_delete=models.CASCADE, null=True)
    payments = models.ForeignKey('Payments', on_delete=models.SET_NULL, null=True)
    is_paid = models.BooleanField(null=True, blank=True, default=False)

    created_on = models.DateTimeField(default=timezone.now)
    invoice_status = models.CharField( max_length=200,choices=INVOICE_STATUS, null=True)

    # TODO: we need to get total amount for all subcribed server
    # TODO: depending to the customer
    # subscription_price_id = models.ForeignKey('', )

    def __str__(self):
        return str(self.user.username)

    def get_invoice_status(self):
        if self.payments is not None:
            self.invoice_status = self.INVOICE_STATUS[1]
        else:
            self.invoice_status = self.INVOICE_STATUS[0]
        return self.invoice_status

    def get_total(self):
        total = 0
        number_of_subscribed_service = int(self.subscriptions.count())
        for sub_service in self.subscriptions.all():
            total += sub_service.after_update_price * number_of_subscribed_service
        # if self.coupon:
        #     total -= self.coupon.amount
        return total

    def save(self, *args, **kwargs):
        self.invoice_status = self.get_invoice_status()
        self.invoice_code = create_ref_code()
        self.invoice_title = f'The is an invoice for {str(self.user)}  subscription'
        super(Invoice, self).save(*args, **kwargs)


class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    reference_id_from_ISP = models.CharField(max_length=50, null=True, blank=True)
    success_type = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Payments"

    def __str__(self):
        return self.reference_id_from_ISP

# class Payment_response(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True)
#     reference_id_from_ISP = models.CharField(max_length=50, null=True, blank=True)
#     success_type = models.CharField(max_length=50, null=True, blank=True)
#
#     class Meta:
#         verbose_name_plural = "Payments rResponse"
#
#     def __str__(self):
#         return self.user.username

# try:
#     user = User.objects.get(username=username)
# except:
#     raise Http404('Requested user not found.')
