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
    after_update_price = models.PositiveIntegerField(null=True, blank=True,)

    after_update_duration = models.CharField(max_length=200, choices=_TIME_UNIT_CHOICES, default='M', null=True,
                                             blank=True)

    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=False, null=True, blank=True)
    # from payment_type to payment_status
    payment = models.ForeignKey('Payments', on_delete=models.SET_NULL, blank=True, null=True)

    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'subscription'

    def get_price_before_subscriptions(self):
        print(int(self.subscription_type.sub_price.sub_price_amount))
        return int(self.subscription_type.sub_price.sub_price_amount)

    # TODO: add  a function to  for manging sub_time

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


class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    invoice_title = models.CharField(max_length=200, null=True, blank=True)
    unique_code = models.CharField(max_length=200, null=True, blank=True)
    subscriptions = models.ManyToManyField(UserSubscriptions, blank=True)
    # payments method
    service_provider_id = models.ForeignKey('ServiceProvider', on_delete=models.CASCADE, null=True)
    payment_status = models.BooleanField(null=True, blank=True, default=False)
    created_on = models.DateTimeField(default=timezone.now)

    # TODO: we need to get total amount for all subcribed server
    # TODO: depending to the customer
    # subscription_price_id = models.ForeignKey('', )


class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    reference_id_from_ISP = models.CharField(max_length=50, null=True, blank=True)
    success_type = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Payments"

    def __str__(self):
        return self.user.username


class Payment_response(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invoice_id = models.ForeignKey('Invoice', on_delete=models.SET_NULL, null=True, blank=True)
    reference_id_from_ISP = models.CharField(max_length=50, null=True, blank=True)
    success_type = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Payments rResponse"

    def __str__(self):
        return self.user.username
