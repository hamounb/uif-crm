from django.urls import path
from .views import *

app_name = 'staff'

urlpatterns = [
    path('', Test.as_view(), name='test'),
    path('home/', HomeView.as_view(), name='home'),
    path('customer/list/', CustomerListView.as_view(), name='customer-list'),
    path('customer/add/', CustomerAddView.as_view(), name='customer-add'),
    path('customer/change/<int:cid>/', CustomerChangeView.as_view(), name='customer-change'),
    path('request/list/', RequestListView.as_view(), name='request-list'),
    path('request/<int:rid>/', RequestDetailsView.as_view(), name='request-details'),
    path('invoice/add/', InvoiceAddView.as_view(), name='invoice-add'),
    path('invoice/list/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoice/details/<int:iid>/', InvoiceDetailsView.as_view(), name='invoice-details'),
    path('document/list/', DocumentsListView.as_view(), name='documents-list'),
    path('document/add/<int:id>/', DocumentsAddView.as_view(), name='documents-add'),
    path('document/del/<int:fid>/', DocumentsDelView.as_view(), name='documents-del'),
    path('document/accept/<int:fid>/', DocumentsAcceptView.as_view(), name='documents-accept'),
    path('document/deny/<int:fid>/', DocumentsDenyView.as_view(), name='documents-deny'),
    path('message/list/', MessagesListView.as_view(), name='message-list'),
    path('exhibition/add/', ExhibitionAddView.as_view(), name='exhibition-add'),
    path('exhibition/list/', ExhibitionListView.as_view(), name='exhibition-list'),
    path('exhibition/details/<int:eid>/', ExhibitionDetailsView.as_view(), name='exhibition-details'),
    ]