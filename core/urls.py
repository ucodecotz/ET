from django.urls import path, include
from rest_framework import routers
from . import views
from .views import *

router = routers.DefaultRouter()
router.register(r'users_api', UserViewSet)
router.register(r'users_profile_api', UserProfileViewSet)
router.register(r'subscription_type_api', SubscriptionTypeViewSet)
router.register(r'user_subscriptions_api', UserSubscriptionsViewSet)
router.register(r'invoice_view_set_api', InvoiceViewSet)
router.register(r'service_provider_api', ServiceProviderViewSet)
router.register(r'payments_api', PaymentsViewSet)
router.register(r'combination_api', CombinationViewSet)
router.register(r'subject_api', SubjectViewSet)
router.register(r'subscription_price_api',Sub_priceViewSet)

app_name = 'core'
urlpatterns = [

    #     End points

    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('home/', views.home.as_view(), name='homepage'),
    path('sub_details/<slug>', views.sub_details.as_view(), name='sub_details'),
    path('add_to_user_subscription/<slug>', views.add_to_user_subscription, name='add_to_user_subscription'),
    path('invoce/', views.InvoiceView.as_view(), name='invoice'),
    path('select_provider/<pk>', views.Select_provider, name='select_provider'),
    path('paymentForm/', views.PaymentForm.as_view(), name='paymentForm'),



]
