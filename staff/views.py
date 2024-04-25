from django.shortcuts import render, redirect, get_object_or_404
from django import views
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.contrib import messages

# Create your views here.

class Test(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = ['crm.add_customermodel', 'crm.add_requestmodel']
    permission_denied_message = "hp"

    def get(self, request):
        return render(request, 'staff/test.html')
    

class CustomerListView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request):
        customer = CustomerModel.objects.all().order_by('-created_date')
        return render(request, 'staff/customer-list.html', {'customer':customer})
    

class CustomerAddView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request):
        form = CustomerAddForm()
        return render(request, 'staff/customer-add.html', {'form':form})
    
    def post(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        form = CustomerAddForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.state == "legal":
                if not obj.ncode:
                    messages.error(request, f"مشتری با نوع حقوقی باید دارای شناسه ملی باشد.", extra_tags='danger')
                    return render(request, 'staff/customer-add.html', {'form':form})
                elif not obj.ceoname:
                    messages.error(request, f"مشتری با نوع حقوقی باید دارای نام مدیرعامل باشد.", extra_tags='danger')
                    return render(request, 'staff/customer-add.html', {'form':form})
                else:
                    obj.user_modified = user
                    obj.user_created = user
                    obj.save()
                    messages.success(request, f"مشتری حقوقی با نام تجاری {obj.company} با موفقیت ثبت شد.")
                    return redirect('staff:customer-change', id=obj.id)
            else:
                obj.ceoname = ''
                obj.ncode = ''
                obj.user = user
                obj.user_modified = user
                obj.user_created = user
                obj.save()
                messages.success(request, f"مشتری حقیقی با نام تجاری {obj.company} با موفقیت ثبت شد.")
                return redirect('staff:customer-change', id=obj.id)
        return render(request, 'staff/customer-add.html', {'form':form})
    

class CustomerChangeView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request, id):
        customer = get_object_or_404(CustomerModel, pk=id)
        form = CustomerAddForm(instance=customer)
        docs = DocumentsModel.objects.filter(customer=customer)
        form2 = DocumentForm()
        context = {
            'form':form,
            'form2':form2,
            'customer':customer,
            'docs':docs,
        }
        return render(request, 'staff/customer-change.html', context)
    
    def post(self, request, id):
        customer = get_object_or_404(CustomerModel, pk=id)
        user = get_object_or_404(User, pk=request.user.id)
        form = CustomerAddForm(request.POST, instance=customer)
        form2 = DocumentForm()
        context = {
            'form':form,
            'form2':form2,
            'customer':customer,
        }
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.state == "legal":
                if not obj.ncode:
                    messages.error(request, f"مشارکت کننده با نوع حقوقی باید دارای شناسه ملی باشد.", extra_tags='danger')
                    return render(request, 'staff/customer-change.html', {'form':form, 'form2':form2})
                elif not obj.ceoname:
                    messages.error(request, f"مشارکت کننده با نوع حقوقی باید دارای نام مدیرعامل باشد.", extra_tags='danger')
                    return render(request, 'staff/customer-change.html', {'form':form, 'form2':form2})
                else:
                    obj.user_modified = user
                    obj.save()
                    messages.success(request, f"اطلاعات {obj.company} بروزرسانی شد.")
                    return redirect('staff:customer-change', id=customer.pk)
            else:
                obj.ceoname = ''
                obj.ncode = ''
                obj.user_modified = user
                obj.save()
                messages.success(request, f"اطلاعات {obj.company} بروزرسانی شد.")
                return redirect('staff:customer-change', id=customer.pk)
        return render(request, 'staff/customer-change.html', context)
    

class DocumentsAddView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def post(self, request, id):
        user = get_object_or_404(User, pk=request.user.id)
        customer = get_object_or_404(CustomerModel, pk=id)
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.customer = customer
            obj.save()
            messages.success(request, f"مدرک شما با موفقیت بارگذاری شد!")
            return redirect('staff:customer-change', id=customer.pk)
        return redirect('staff:customer-change', id=customer.pk)
    

class RequestListView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request):
        req = RequestModel.objects.all().order_by('-created_date')
        return render(request, 'staff/requests-list.html', {'req':req})