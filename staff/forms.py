from django import forms
from .models import *
from crm.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Q

def is_code(value):
    if len(value) != 10 or not str(value).isnumeric():
        raise ValidationError('کد ملی صحیح نمی‌باشد!')
    
def is_mobile(value):
    if not str(value).isnumeric() or len(value) !=11 or str(value)[0] != '0':
        raise ValidationError('شماره موبایل صحیح نمی‌باشد!')
    
def is_phone(value):
    if not str(value).isnumeric() or len(value) !=11 or str(value)[0] != '0':
        raise ValidationError('شماره تلفن صحیح نمی‌باشد!')
    
def is_ncode(value):
    if len(value) != 10 or not str(value).isnumeric():
        raise ValidationError("شناسه ملی صحیح نمی‌باشد.")
    
def is_postal(value):
    if len(value) != 10 or not str(value).isnumeric():
        raise ValidationError('کد پستی صحیح نمی‌باشد!')
    
def is_positive(value):
    if not str(value).isnumeric():
        raise ValidationError('لطفاً فقط عدد وارد کنید!')
    if str(value).isnumeric():
        if int(value) < 1:
            raise ValidationError('عدد باید بزرگتر از صفر باشد!')
        
def is_discount(value):
    if not str(value).isnumeric():
        raise ValidationError('لطفاً فقط عدد وارد کنید!')
    if str(value).isnumeric():
        if int(value) < 0:
            raise ValidationError('کمترین مقدار می‌تواند عدد صفر باشد!')
        
    
class CustomerAddForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False), widget=forms.Select(attrs={'class':'form-control'}), label='کاربر')
    code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}), label="کد ملی", validators=[is_code])
    ncode = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class':'form-control'}), label="شناسه ملی", validators=[is_ncode])
    mobile = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'form-control'}), label="شماره همراه", validators=[is_mobile])
    phone = forms.CharField(max_length=11, required=False, widget=forms.TextInput(attrs={'class':'form-control'}), label="شماره ثابت", validators=[is_phone])
    fax = forms.CharField(max_length=11, required=False, widget=forms.TextInput(attrs={'class':'form-control'}), label="شماره فکس", validators=[is_phone])
    postalcode = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class':'form-control'}), label="کد پستی", validators=[is_postal])

    class Meta:
        model = CustomerModel
        fields = (
                  'user',
                  'state',
                  'is_active',
                  'firstname',
                  'lastname',
                  'fathername',
                  'code',
                  'ceoname',
                  'company',
                  'ncode',
                  'mobile',
                  'phone',
                  'fax',
                  'email',
                  'postalcode',
                  'address',
                  )
        widgets = {
            'state': forms.Select(attrs={'class':'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class':'form-control', 'style': 'float:right', "checked":True}),
            'firstname': forms.TextInput(attrs={'class':'form-control'}),
            'lastname': forms.TextInput(attrs={'class':'form-control'}),
            'fathername': forms.TextInput(attrs={'class':'form-control'}),
            'ceoname': forms.TextInput(attrs={'class':'form-control'}),
            'company': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'address': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }


class DocumentForm(forms.Form):
    file = forms.FileField(label='مدرک')


class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':2}), label="توضیحات", required=False)


class RequestAcceptForm(forms.Form):
    area = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="متراژ", validators=[is_positive])
    discount = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="تخفیف", required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':2}), label="توضیحات", required=False)


class InvoiceForm(forms.ModelForm):
    area = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="متراژ", validators=[is_positive])
    discount = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="تخفیف", required=True, validators=[is_discount], empty_value="0")


    class Meta:
        model = InvoiceModel
        fields = (
            'is_active',
            'customer',
            'exhibition',
            'area',
            'discount',
            'description',
        )
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class':'form-control', 'checked':True}),
            'customer': forms.Select(attrs={'class':'form-control'}),
            'exhibition': forms.Select(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }