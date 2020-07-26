from django.contrib import admin
from .models import *


# Register your models here.

class SubTyeAdmin(admin.ModelAdmin):
    list_display = ('title', 'label', 'category', 'slug')
    list_filter = ("title",)
    search_fields = ['title', 'category']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(UserProfile)
admin.site.register(SubscriptionType)
admin.site.register(UserSubscriptions)
admin.site.register(Invoice)
admin.site.register(Payments)
admin.site.register(Payment_response)
admin.site.register(Combinations)
admin.site.register(Subject)
admin.site.register(ServiceProvider)
admin.site.register(SubscriptionPrice)
