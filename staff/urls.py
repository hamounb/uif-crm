from django.urls import path
from .views import *

app_name = 'staff'

urlpatterns = [
    path('', Test.as_view(), name='test'),
    path('customer/add/', CustomerAddView.as_view(), name='customer-add'),
    path('customer/change/<int:cid>/', CustomerChangeView.as_view(), name='customer-change'),
    path('customer/list/', CustomerListView.as_view(), name='customer-list'),
    path('request/list/', RequestListView.as_view(), name='request-list'),
    path('request/<int:rid>/', RequestDetailsView.as_view(), name='request-details'),
    path('invoice/add/', InvoiceAddView.as_view(), name='invoice-add'),
    path('invoice/list/', InvoiceListView.as_view(), name='invoice-list'),
    path('document/list/', DocumentsListView.as_view(), name='documents-list'),
    path('document/add/<int:id>/', DocumentsAddView.as_view(), name='documents-add'),
    path('document/del/<int:fid>/', DocumentsDelView.as_view(), name='documents-del'),
    ]