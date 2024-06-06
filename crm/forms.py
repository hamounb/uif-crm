from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

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


class CustomerAddForm(forms.ModelForm):
    ncode = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class':'form-control'}), label="شناسه ملی شرکت/سازمان", validators=[is_ncode])
    phone = forms.CharField(max_length=11, required=False, widget=forms.TextInput(attrs={'class':'form-control'}), label="شماره ثابت", validators=[is_phone])
    fax = forms.CharField(max_length=11, required=False, widget=forms.TextInput(attrs={'class':'form-control'}), label="شماره فکس", validators=[is_phone])
    postalcode = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class':'form-control'}), label="کد پستی", validators=[is_postal])

    class Meta:
        model = CustomerModel
        fields = (
                  'state',
                  'firstname',
                  'lastname',
                  'fathername',
                  'ceoname',
                  'company',
                  'ncode',
                  'phone',
                  'fax',
                  'email',
                  'postalcode',
                  'address',
                  )
        widgets = {
            'state': forms.Select(attrs={'class':'form-control'}),
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
            'file',
        )
        widgets = {
            'file': forms.FileInput(attrs={'value':'dd'}),
        }


class RequestsForm(forms.ModelForm):
    exhibition = forms.ModelChoiceField(
        queryset = ExhibitionModel.objects.filter(is_active=True),
        widget =forms.Select(attrs={'class':'form-control'}),
        required=True,
        label = 'عنوان نمایشگاه'
    )

    class Meta:
        model = RequestModel
        fields = (
            'customer',
            'exhibition',
            'area',
            'rules',
        )
        widgets = {
            'customer': forms.Select(attrs={'class':'form-control', 'required':True}),
            'area': forms.NumberInput(attrs={'class':'form-control'}),
            'rules': forms.CheckboxInput(attrs={'required':True})
        }