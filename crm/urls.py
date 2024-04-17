from django.urls import path
from .views import *

app_name = 'crm'

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('customer/add/', CustomerAddView.as_view(), name='customer-add'),
    path('customer/change/<int:id>/', CustomerChangeView.as_view(), name='customer-change'),
    path('documents/add/<int:id>/', DocumentsAddView.as_view(), name='documents-add'),
    path('requests/add/', RequestsAddView.as_view(), name='request-add'),
    ]