from django.shortcuts import render, redirect, get_object_or_404
from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.

class IndexView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request):
        return render(request, 'crm/index.html')
    
# class CustomerView(LoginRequiredMixin, views.View):
#     login_url = 'accounts:signin'

#     def get(self, request):
#         user = get_object_or_404(User, pk=request.user.id)
#         customer = CustomerModel.objects.filter(user=user)
#         if customer:

    
class CustomerAddView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        form = CustomerAddForm()
        return render(request, 'crm/customer-add.html', {'form':form})
    
    def post(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        form = CustomerAddForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.state == "legal":
                if not obj.ncode:
                    messages.error(request, f"مشتری با نوع حقوقی باید دارای شناسه ملی باشد.", extra_tags='danger')
                    return render(request, 'crm/customer-add.html', {'form':form})
                elif not obj.ceoname:
                    messages.error(request, f"مشتری با نوع حقوقی باید دارای نام مدیرعامل باشد.", extra_tags='danger')
                    return render(request, 'crm/customer-add.html', {'form':form})
                else:
                    obj.user = user
                    obj.user_modified = user
                    obj.user_created = user
                    obj.save()
                    messages.success(request, f"مشتری حقوقی {obj.company} اطلاعات شما ثبت شد.")
                    return render(request, 'crm/message.html', {'form':form})
            else:
                obj.ceoname = ''
                obj.ncode = ''
                obj.user = user
                obj.user_modified = user
                obj.user_created = user
                obj.save()
                messages.success(request, f"مشتری حقیقی {obj.company} اطلاعات شما ثبت شد.")
                return render(request, 'crm/message.html')
        return render(request, 'crm/customer-add.html', {'form':form})

class CustomerChangeView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request, id):
        customer = get_object_or_404(CustomerModel, pk=id)
        form = CustomerAddForm(instance=customer)
        return render(request, 'crm/customer-change.html', {'form':form})
    
    def post(self, request, id):
        customer = get_object_or_404(CustomerModel, pk=id)
        user = get_object_or_404(User, pk=request.user.id)
        form = CustomerAddForm(request.POST, instance=customer)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.state == "legal":
                if not obj.ncode:
                    messages.error(request, f"مشتری با نوع حقوقی باید دارای شناسه ملی باشد.", extra_tags='danger')
                    return render(request, 'crm/customer-change.html', {'form':form})
                elif not obj.ceoname:
                    messages.error(request, f"مشتری با نوع حقوقی باید دارای نام مدیرعامل باشد.", extra_tags='danger')
                    return render(request, 'crm/customer-change.html', {'form':form})
                else:
                    obj.user_modified = user
                    obj.save()
                    messages.success(request, f"اطلاعات {obj.company} بروزرسانی شد.")
                    return redirect('crm:customer-change', id=customer.pk)
            else:
                obj.ceoname = ''
                obj.ncode = ''
                obj.user_modified = user
                obj.save()
                messages.success(request, f"اطلاعات {obj.company} بروزرسانی شد.")
                return render(request, 'crm/message.html')
        return render(request, 'crm/customer-change.html', {'form':form})
    
class DocumentsView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        customer = CustomerModel.objects.filter(user=user)
        docs = DocumentsModel.objects.filter(user=user).order_by('-created_date')
        form = DocumentForm()
        context = {
            'customer':customer,
            'form':form,
            'docs':docs,
        }
        return render(request, 'crm/documents.html', context)
        
class RequestsView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        customer = CustomerModel.objects.filter(Q(user=user) & Q(is_active=True))
        if customer:
            form = RequestsForm()
            context = {
                'customer':customer,
                'form':form,
            }
            return render(request, 'crm/requests.html', context)
        messages.error(request, 'کابر گرامی شما مشخصات کاربری فعال ندارید!', extra_tags='danger')
        return render(request, 'crm/message.html')
    
    def post(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        customer = CustomerModel.objects.filter(Q(user=user) & Q(is_active=True))
        if customer:
            form = RequestsForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = user
                obj.created_user = user
                obj.modified_user = user
                obj.save()
                messages.success(request, f"مشارکت کننده {form.cleaned_data['customer']}"
                                 f" درخواست شما برای نمایشگاه {form.cleaned_data['exhibition']} با متراژ {form.cleaned_data['area']} ثبت شد.")
                return redirect('crm:customer-change', id=customer.pk)
            context = {
                'customer':customer,
                'form':form,
            }
            return render(request, 'crm/requests.html', context)
        messages.error(request, 'کابر گرامی شما مشخصات کاربری فعال ندارید!', extra_tags='danger')
        return render(request, 'crm/message.html')