from django.urls import path
from .views import *

app_name = 'crm'

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('help/', HelpView.as_view(), name='help'),
    path('customer/add/', CustomerAddView.as_view(), name='customer-add'),
    path('customer/list/', CustomerListView.as_view(), name='customer-list'),
    path('customer/change/<int:id>/', CustomerChangeView.as_view(), name='customer-change'),
    path('documents/', DocumentsView.as_view(), name='documents'),
    path('documents/add/<int:cid>/', DocumentsAddView.as_view(), name='documents-add'),
    path('requests/add/', RequestsAddView.as_view(), name='request-add'),
    path('requests/list/', RequestsListView.as_view(), name='request-list'),
    path('messages/', MessagesView.as_view(), name='messages'),
    path('messages/<int:mid>/', MessageDoneView.as_view(), name='message-done'),
    path('invoices/list/', InvoiceListView.as_view(), name='invoice-list'),
    ]