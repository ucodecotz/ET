from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = '__all__'


class UserSubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscriptions
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = '__all__'


class CombinationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combinations
        fields = '__all__'


class SubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class Sub_priceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPrice
        fields = '__all__'
