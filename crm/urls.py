from django.urls import path
from .views import *

app_name = 'crm'

urlpatterns = [
    path('documents/', DocumentsView.as_view(), name='documents')
    ]