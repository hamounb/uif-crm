from django.shortcuts import render, redirect, get_object_or_404
from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.db import IntegrityError
from .models import *
from accounts.models import MobileModel
from .forms import *
from accounts.payamak import send_sms

# Create your views here.

class HelpView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request):
        return render(request, 'crm/help.html')


class IndexView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        customer = CustomerModel.objects.filter(user=user)
        mes = MessagesModel.objects.filter(Q(customer__user=user) & Q(is_active=True)).order_by('-created_date')
        invoices = InvoiceModel.objects.filter(Q(customer__user=user)).order_by('-created_date')
        context = {
            'mes':mes,
            'customer':customer,
            'invoices':invoices,
        }
        return render(request, 'crm/index.html', context)
    
class CustomerListView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        customer = CustomerModel.objects.filter(user=user).order_by('-created_date')
        if customer:
            return render(request, 'crm/customer-list.html', {'customer':customer})
        return redirect('crm:customer-add')

    
class CustomerAddView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        form = CustomerAddForm()
        return render(request, 'crm/customer-add.html', {'form':form})
    
    def post(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        mobile = get_object_or_404(MobileModel, user=user)
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
                    obj.code = user.username
                    obj.mobile = mobile.mobile
                    obj.user = user
                    obj.user_modified = user
                    obj.user_created = user
                    try:
                        obj.save()
                    except IntegrityError:
                        messages.error(request, f"نام تجاری مورد نظر قبلا توسط شما ثبت شده است!")
                        return render(request, 'crm/customer-add.html', {'form':form})
                    else:
                        messages.success(request, f"مشتری حقوقی {obj.company}، اطلاعات شما ثبت شد.")
                        send_sms(228007, f"{mobile}", [user.username, obj.company])
                        return redirect('crm:customer-change', id=obj.id)
            else:
                obj.code = user.username
                obj.mobile = mobile.mobile
                obj.ceoname = ''
                obj.ncode = ''
                obj.user = user
                obj.user_modified = user
                obj.user_created = user
                try:
                    obj.save()
                except IntegrityError:
                    messages.error(request, f"نام تجاری مورد نظر قبلا توسط شما ثبت شده است!")
                    return render(request, 'crm/customer-add.html', {'form':form})
                else:
                    messages.success(request, f"مشتری حقیقی {obj.company}، اطلاعات شما ثبت شد.")
                    send_sms(228007, str(mobile.mobile), [str(user.username), obj.company])
                    return redirect('crm:customer-change', id=obj.id)
        return render(request, 'crm/customer-add.html', {'form':form})


class CustomerChangeView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request, id):
        customer = get_object_or_404(CustomerModel, pk=id)
        form = CustomerAddForm(instance=customer)
        docs = DocumentsModel.objects.filter(customer=customer)
        form2 = DocumentForm()
        context = {
            'form':form,
            'customer':customer,
            'docs':docs,
            'form2':form2,
        }
        return render(request, 'crm/customer-change.html', context)
    
    def post(self, request, id):
        customer = get_object_or_404(CustomerModel, pk=id)
        user = get_object_or_404(User, pk=request.user.id)
        form = CustomerAddForm(request.POST, instance=customer)
        docs = DocumentsModel.objects.filter(customer=customer)
        form2 = DocumentForm()
        context = {
            'form':form,
            'customer':customer,
            'docs':docs,
            'form2':form2,
        }
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.state == "legal":
                if not obj.ncode:
                    messages.error(request, f"مشتری با نوع حقوقی باید دارای شناسه ملی باشد.", extra_tags='danger')
                    return render(request, 'crm/customer-change.html', context)
                elif not obj.ceoname:
                    messages.error(request, f"مشتری با نوع حقوقی باید دارای نام مدیرعامل باشد.", extra_tags='danger')
                    return render(request, 'crm/customer-change.html', context)
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
                return redirect('crm:customer-change', id=customer.pk)
        messages.error(request, f"ویرایش ثبت نشد، دوباره سعی کنید.", extra_tags='danger')
        return render(request, 'crm/customer-change.html', context)
    

class DocumentsAddView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def post(self, request, cid):
        user = get_object_or_404(User, pk=request.user.id)
        form = DocumentForm(request.POST, request.FILES)
        customer = get_object_or_404(CustomerModel, pk=cid)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = customer
            obj.user = user
            obj.user_created = user
            obj.user_modified = user
            obj.save()
            messages.success(request, f"مدرک شما با موفقیت بارگذاری شد!")
            return redirect('crm:customer-change', id=customer.pk)
        return redirect('crm:customer-change', id=customer.pk)
    

class DocumentsView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        docs = DocumentsModel.objects.filter(user=user).order_by('-created_date')
        form = DocumentForm()
        context = {
            'form':form,
            'docs':docs,
        }
        return render(request, 'crm/documents.html', context)
    

class RequestsListView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        req = RequestModel.objects.filter(user=user).order_by('-created_date')
        return render(request, 'crm/requests-list.html', {'req':req})


class RequestsAddView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        customer = CustomerModel.objects.filter(Q(user=user) & Q(is_active=True))
        form = RequestsForm()
        context = {
            'customer':customer,
            'form':form,
        }
        if customer:
            return render(request, 'crm/requests-add.html', context)
        messages.error(request, 'کابر گرامی شما پروفایل کاربری فعال ندارید!')
        return render(request, 'crm/requests-add.html', context)
    
    def post(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        customer = CustomerModel.objects.filter(Q(user=user) & Q(is_active=True))
        form = RequestsForm(request.POST)
        context = {
            'customer':customer,
            'form':form,
        }
        if customer:
            if form.is_valid():
                w = RequestModel.objects.filter(Q(customer=form.cleaned_data['customer']) & Q(exhibition=form.cleaned_data['exhibition']) & Q(state=RequestModel.STATE_WAIT))
                a = RequestModel.objects.filter(Q(customer=form.cleaned_data['customer']) & Q(exhibition=form.cleaned_data['exhibition']) & Q(state=RequestModel.STATE_ACCEPT))
                if w:
                    messages.warning(request, f"مشارکت کننده {form.cleaned_data['customer']}"
                                 f" درخواست شما برای نمایشگاه {form.cleaned_data['exhibition']} قبلا ثبت شده و در حال بررسی است.")
                    return render(request, 'crm/requests-add.html', context)
                elif a:
                    messages.warning(request, f"مشارکت کننده {form.cleaned_data['customer']}"
                                 f" قبلاً با درخواست شما برای نمایشگاه {form.cleaned_data['exhibition']} موافقت شده است و امکان ثبت دوباره ندارد.")
                    return render(request, 'crm/requests-add.html', context)
                else:
                    obj = form.save(commit=False)
                    obj.user = user
                    obj.created_user = user
                    obj.modified_user = user
                    obj.save()
                    messages.success(request, f"مشارکت کننده {form.cleaned_data['customer']}"
                                     f" درخواست شما برای نمایشگاه {form.cleaned_data['exhibition']} با متراژ {form.cleaned_data['area']} ثبت شد.")
                    return redirect('crm:request-list')
            return render(request, 'crm/requests-add.html', context)
        messages.error(request, 'کابر گرامی شما مشخصات کاربری فعال ندارید!', extra_tags='danger')
        return render(request, 'crm/requests-add.html', context)
    

class MessagesView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        mes = MessagesModel.objects.filter(customer__user=user).order_by('-created_date')
        return render(request, 'crm/messages.html', {'mes':mes})
    

class MessageDoneView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request, mid):
        mes = get_object_or_404(MessagesModel, pk=mid)
        mes.is_active = False
        mes.save()
        return redirect('crm:messages')
    

class InvoiceListView(LoginRequiredMixin, views.View):
    login_url = 'accounts:signin'

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        invoices = InvoiceModel.objects.filter(Q(customer__user=user)).order_by('-created_date')
        return render(request, 'crm/invoice-list.html', {'invoices':invoices})
    

