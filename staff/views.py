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

    def get(self, request):
        return render(request, 'staff/test.html')
    

class HomeView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request):
        customer = CustomerModel.objects.filter(is_active=False).order_by('-created_date')
        req = RequestModel.objects.filter(state=RequestModel.STATE_WAIT).order_by('-created_date')
        exhibition = ExhibitionModel.objects.filter(is_active=True)
        context = {
            'customer':customer,
            'exhibition':exhibition,
            'req':req,
        }
        return render(request, 'staff/home.html', context)
    

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
                    code = form.cleaned_data.get('code')
                    mobile = form.cleaned_data.get('mobile')
                    try:
                        cus = User.objects.get(username=code)
                    except User.DoesNotExist:
                        new = User(username=code)
                        new.set_password(mobile)
                        new.save()
                        obj.user = new
                        obj.user_modified = user
                        obj.user_created = user
                        obj.save()
                        messages.success(request, f"مشتری حقوقی با نام تجاری {obj.company} با موفقیت ثبت شد.")
                        return redirect('staff:customer-change', cid=obj.id)
                    obj.user = cus
                    obj.user_modified = user
                    obj.user_created = user
                    obj.save()
                    messages.success(request, f"مشتری حقوقی با نام تجاری {obj.company} با موفقیت ثبت شد.")
                    return redirect('staff:customer-change', cid=obj.id)
            else:
                code = form.cleaned_data.get('code')
                mobile = form.cleaned_data.get('mobile')
                try:
                    cus = User.objects.get(username=code)
                except User.DoesNotExist:
                    new = User(username=code)
                    new.set_password(mobile)
                    new.save()
                    obj.user = new
                    obj.ceoname = ''
                    obj.ncode = ''
                    obj.user_modified = user
                    obj.user_created = user
                    obj.save()
                    messages.success(request, f"مشتری حقیقی با نام تجاری {obj.company} با موفقیت ثبت شد.")
                    return redirect('staff:customer-change', cid=obj.pk)
                obj.user = cus
                obj.ceoname = ''
                obj.ncode = ''
                obj.user_modified = user
                obj.user_created = user
                obj.save()
                messages.success(request, f"مشتری حقیقی با نام تجاری {obj.company} با موفقیت ثبت شد.")
                return redirect('staff:customer-change', cid=obj.pk)
        return render(request, 'staff/customer-add.html', {'form':form})
    

class CustomerChangeView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request, cid):
        customer = get_object_or_404(CustomerModel, pk=cid)
        form = CustomerChangeForm(instance=customer)
        docs = DocumentsModel.objects.filter(customer=customer).order_by('-created_date')
        form2 = DocumentForm()
        context = {
            'form':form,
            'form2':form2,
            'customer':customer,
            'docs':docs,
        }
        return render(request, 'staff/customer-change.html', context)
    
    def post(self, request, cid):
        customer = get_object_or_404(CustomerModel, pk=cid)
        user = get_object_or_404(User, pk=request.user.id)
        form = CustomerChangeForm(request.POST, instance=customer)
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
                    return redirect('staff:customer-change', cid=customer.pk)
                elif not obj.ceoname:
                    messages.error(request, f"مشارکت کننده با نوع حقوقی باید دارای نام مدیرعامل باشد.", extra_tags='danger')
                    return redirect('staff:customer-change', cid=customer.pk)
                else:
                    obj.user_modified = user
                    obj.save()
                    messages.success(request, f"اطلاعات {obj.company} بروزرسانی شد.")
                    return render(request, 'staff/customer-change.html', context)
            else:
                obj.ceoname = ''
                obj.ncode = ''
                obj.user_modified = user
                obj.save()
                messages.success(request, f"اطلاعات {obj.company} بروزرسانی شد.")
                return render(request, 'staff/customer-change.html', context)
        return render(request, 'staff/customer-change.html', context)
    

class DocumentsAddView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def post(self, request, id):
        user = get_object_or_404(User, pk=request.user.id)
        customer = get_object_or_404(CustomerModel, pk=id)
        form2 = DocumentForm(request.POST, request.FILES)
        if form2.is_valid():
            file = form2.cleaned_data['file']
            obj = DocumentsModel(
                is_active = True,
                state = DocumentsModel.STATE_ACCEPT,
                file = file,
                user = customer.user,
                user_created = user,
                user_modified = user,
                customer = customer,
            )
            obj.save()
            messages.success(request, f"مدرک شما با موفقیت بارگذاری شد!")
            return redirect('staff:customer-change', cid=customer.pk)
        return redirect('staff:customer-change', cid=customer.pk)
    

class DocumentsDelView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request, fid):
        file = get_object_or_404(DocumentsModel, pk=fid)
        file.file.delete(save=True)
        file.delete()
        ref = request.META.get('HTTP_REFERER')
        messages.success(request, "مدرک انتخابی شما با موفقیت حذف شد.")
        return redirect(ref)
    

class DocumentsAcceptView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request, fid):
        file = get_object_or_404(DocumentsModel, pk=fid)
        file.state = DocumentsModel.STATE_ACCEPT
        file.save()
        ref = request.META.get('HTTP_REFERER')
        messages.success(request, f"مدرک مشارکت کننده با نام تجاری {file.customer.company} با موفقیت تایید شد.")
        return redirect(ref)
    

class DocumentsDenyView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request, fid):
        file = get_object_or_404(DocumentsModel, pk=fid)
        file.state = DocumentsModel.STATE_DENY
        file.save()
        ref = request.META.get('HTTP_REFERER')
        messages.warning(request, f"مدرک مشارکت کننده با نام تجاری {file.customer.company} به حالت تعلیق تغییر یافت!")
        return redirect(ref)



class DocumentsListView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request):
        doc = DocumentsModel.objects.filter(Q(state=DocumentsModel.STATE_WAIT) | Q(state=DocumentsModel.STATE_DENY)).order_by('-created_date')
        return render(request, 'staff/documents-list.html', {'doc':doc})
    

class RequestListView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request):
        req = RequestModel.objects.all().order_by('-created_date')
        return render(request, 'staff/request-list.html', {'req':req})
    

class RequestDetailsView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request, rid):
        req = get_object_or_404(RequestModel, pk=rid)
        mes = MessagesModel.objects.filter(customer=req.customer)
        form = MessageForm()
        form2 = RequestAcceptForm()
        context = {
            'req':req,
            'mes':mes,
            'form':form,
            'form2':form2,
        }
        return render(request, 'staff/request-details.html', context)
    
    def post(self, request, rid):
        req = get_object_or_404(RequestModel, pk=rid)
        mes = MessagesModel.objects.filter(customer=req.customer)
        form = MessageForm(request.POST)
        form2 = RequestAcceptForm(request.POST)
        context = {
            'req':req,
            'mes':mes,
            'form':form,
            'form':form2,
        }
        if form.is_valid() and 'btn1' in request.POST:
            text = form.cleaned_data.get('text')
            mes = MessagesModel()
            mes.text = text
            mes.is_active = True
            mes.customer = req.customer
            mes.save()
            req.state = req.STATE_DENY
            req.save()
            messages.success(request, 'پیغام شما با موفقیت ارسال شد.')
            return render(request, 'staff/request-details.html', context)
        if form2.is_valid() and 'btn2' in request.POST:
            area = form2.cleaned_data.get('area')
            discount = form2.cleaned_data.get('discount')
            description = form2.cleaned_data.get('description')
            total = int(req.exhibition.price) * int(area) + int(int(req.exhibition.price) * int(area) * int(req.exhibition.value_added) / 100)
            invoice = InvoiceModel(
                is_active=True,
                user=req.user,
                customer=req.customer,
                exhibition=req.exhibition,
                price=req.exhibition.price,
                area=area,
                value_added=req.exhibition.value_added,
                discount=discount,
                total_price=total,
                description=description,
            )
            invoice.save()
            req.state = req.STATE_ACCEPT
            req.save()
            messages.success(request, f'موافقت شما با درخواست {req.customer.company} برای نمایشگاه {req.exhibition.title} به متراژ {area} ثبت شد.')
            return render(request, 'staff/request-details.html', context)
        messages.error(request, 'درخواست عملیات شما با خطا مواجه شد!', extra_tags="danger")
        return redirect('staff:request-details', rid=req.pk)
    

class InvoiceAddView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request):
        form = InvoiceForm()
        return render(request, 'staff/invoice-add.html', {'form':form})
    
    def post(self, request):
        form = InvoiceForm(request.POST)
        user = get_object_or_404(User, pk=request.user.id)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = CustomerModel.objects.get(company=form.cleaned_data.get('customer')).user
            obj.price = ExhibitionModel.objects.get(pk=form.cleaned_data['exhibition'].id).price
            obj.value_added = ExhibitionModel.objects.get(pk=form.cleaned_data['exhibition'].id).value_added
            total = int(ExhibitionModel.objects.get(pk=form.cleaned_data['exhibition'].id).price) * int(form.cleaned_data.get('area'))
            amount = int(total + (total * int(ExhibitionModel.objects.get(pk=form.cleaned_data['exhibition'].id).value_added) / 100))
            obj.total_price = float(amount - int(amount * int(form.cleaned_data.get('discount')) / 100))
            obj.user_created = user
            obj.save()
            messages.success(request, f'فاکتور برای مشارکت کننده نمایشگاه {obj.exhibition} با نام تجاری {obj.customer.company} با موفقیت ثبت شد.')
            return render(request, 'staff/invoice-add.html', {'form':form})
        return render(request, 'staff/invoice-add.html', {'form':form})
    

class InvoiceListView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request):
        invoices = InvoiceModel.objects.all().order_by('-created_date')
        return render(request, 'staff/invoice-list.html', {'invoices':invoices})
    

class InvoiceDetailsView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request, iid):
        invoice = get_object_or_404(InvoiceModel, pk=iid)
        return render(request, 'staff/invoice-details.html', {'invoice':invoice})
    

class ExhibitionAddView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request):
        form = ExhibitionForm()
        return render(request, 'staff/exhibition-add.html', {'form':form})
    
    def post(self, request):
        form = ExhibitionForm(request.POST)
        user = get_object_or_404(User, pk=request.user.id)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_created = user
            obj.user_modified = user
            obj.price = float(form.cleaned_data.get('price'))
            obj.save()
            messages.success(request, f"عنوان جدید {obj.title} با موفقیت ثبت شد.")
            return redirect('staff:exhibition-add')
        return render(request, 'staff/exhibition-add.html', {'form':form})
    

class ExhibitionListView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request):
        exh = ExhibitionModel.objects.all().order_by('-created_date')
        return render(request, 'staff/exhibition-list.html', {'exh':exh})
    

class ExhibitionDetailsView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request, eid):
        cus = InvoiceModel.objects.filter(Q(is_active=True) & Q(exhibition=eid))
        return render(request, 'staff/exhibition-details.html', {'cus':cus})


class MessagesListView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request):
        mes = MessagesModel.objects.all().order_by('-created_date')
        form = MessageAddForm()
        return render(request, 'staff/messages-list.html', {'mes':mes, 'form':form})
    

class MessageAddView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def post(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        form = MessageAddForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_created = user
            obj.user_modified = user
            obj.is_active = True
            obj.save()
            messages.success(request, f"پیغام شما برای مشارکت کننده {obj.customer.company} ({obj.customer.firstname} {obj.customer.firstname}) با موفقیت ارسال شد.")
            return redirect('staff:message-list')
        messages.warning(request, "خطا در انجام عملیات رخ داده است، لطفا دوباره سعی کنید!")
        return redirect('staff:message-list')
    

class MessageChangeView(PermissionRequiredMixin, views.View):
    login_url = 'accounts:signin'
    permission_required = []

    def get(self, request, mid):
        mes = get_object_or_404(MessagesModel, pk=mid)
        form = MessageForm(initial={'text':mes.text})
        context = {
            'mes':mes,
            'form':form,
        }
        return render(request, 'staff/message-change.html', context)
    
    def post(self, request, mid):
        user = get_object_or_404(User, pk=request.user.id)
        mes = get_object_or_404(MessagesModel, pk=mid)
        form = MessageForm(request.POST)
        context = {
            'mes':mes,
            'form':form,
        }
        if form.is_valid():
            text = form.cleaned_data.get('text')
            old = MessageChangeModel()
            old.text = mes.text
            old.user_modified = mes.user_modified
            old.modified_date = mes.modified_date
            old.message = mes
            old.save()
            messages.success(request, f"پیغام شما برای مشارکت کننده {mes.customer.company} با موفقیت ویرایش شد.")
            mes.user_modified = user
            mes.text = text
            mes.save()
            return redirect('staff:message-list')
        return render(request, 'staff/message-change.html', context)