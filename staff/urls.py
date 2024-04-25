from django.urls import path
from .views import *

app_name = 'staff'

urlpatterns = [
    path('', Test.as_view(), name='test'),
    path('customer/add/', CustomerAddView.as_view(), name='customer-add'),
    ]