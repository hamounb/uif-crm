from django.urls import path
from .views import *

app_name = 'crm'

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('customer/add/', CustomerAddView.as_view(), name='customer-add'),
    path('documents/', DocumentsView.as_view(), name='documents'),
    ]