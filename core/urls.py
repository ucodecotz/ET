from django.urls import path
from .import views
app_name ='core'
urlpatterns = [
    path('',views.home.as_view(), name='homepage'),
    path('sub_details/<slug>', views.sub_details.as_view(), name= 'sub_details'),
    path('add_to_user_subscription/<slug>', views.add_to_user_subscription, name='add_to_user_subscription')
]
