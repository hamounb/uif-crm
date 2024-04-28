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
        
    
class CustomerAddForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False), widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Pick a state...'}), required=True, label='کاربر')
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
            'is_active': forms.CheckboxInput(attrs={'class':'form-control'}),
            'firstname': forms.TextInput(attrs={'class':'form-control'}),
            'lastname': forms.TextInput(attrs={'class':'form-control'}),
            'fathername': forms.TextInput(attrs={'class':'form-control'}),
            'ceoname': forms.TextInput(attrs={'class':'form-control'}),
            'company': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'address': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }


class DocumentForm(forms.ModelForm):

    class Meta:
        model = DocumentsModel
        fields = (
            'state',
            'is_active',
            'file',
        )
        widgets = {
            'state': forms.Select(attrs={'class':'form-control', 'disabled':True}),
            'is_active': forms.CheckboxInput(attrs={'class':'form-control', 'disabled':True}),
            'file': forms.FileInput(attrs={'value':'dd'})
        }


class MessageForm(forms.ModelForm):
    STATE_WAIT = 'wait'
    STATE_ACCEPT = 'accept'
    STATE_DENY = 'deny'
    STATE_CHOICES = (
        (STATE_WAIT, 'در انتظار بررسی'),
        (STATE_ACCEPT, 'قبول شده'),
        (STATE_DENY, 'رد شده')
    )
    state = forms.ChoiceField(choices=STATE_CHOICES, widget=forms.Select(attrs={'class':'form-control'}, choices=STATE_CHOICES))
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))


class InvoiceForm(forms.ModelForm):
    area = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="متراژ", validators=[is_positive])
    discount = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="تخفیف", required=False)


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
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
        }