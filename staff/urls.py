from django.urls import path
from .views import *

app_name = 'staff'

urlpatterns = [
    path('', Test.as_view(), name='test'),
    path('customer/add/', CustomerAddView.as_view(), name='customer-add'),
    path('request/list/', RequestListView.as_view(), name='request-list'),
    path('invoice/add/', InvoiceAddView.as_view(), name='invoice-add'),
    path('invoice/list/', InvoiceListView.as_view(), name='invoice-list'),
    ]