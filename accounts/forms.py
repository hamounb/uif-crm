from django import forms
from django.core.exceptions import ValidationError
from .models import TokenModel

def is_code(value):
    if len(value) != 10 or not str(value).isnumeric():
        raise ValidationError('کد ملی صحیح نمی‌باشد!')
    
def is_mobile(value):
    if not str(value).isnumeric() or len(value) !=11 or str(value)[0] != '0':
        raise ValidationError('شماره موبایل صحیح نمی‌باشد!')

class SignUpForm(forms.Form):
    code = forms.CharField(
        max_length=10,
        validators=[is_code],
        widget=forms.TextInput(attrs={'class':'form-control', 'oninvalid':'this.setCustomValidity("Please Enter valid email")'}),
        label='کد ملی',
    )
    mobile = forms.CharField(
        max_length=11,
        validators=[is_mobile],
        widget=forms.TextInput(attrs={'class':'form-control'}),
        label='شماره موبایل',
    )

class LoginForm(forms.Form):
    code = forms.CharField(
        max_length=10,
        validators=[is_code],
        widget=forms.TextInput(attrs={'class':'form-control', 'title':'Please Enter valid email'}),
        label='کد ملی',
    )
    mobile = forms.CharField(
        max_length=11,
        validators=[is_mobile],
        widget=forms.TextInput(attrs={'class':'form-control'}),
        label='شماره موبایل',
    )

class TokenForm(forms.ModelForm):

    class Meta:
        model = TokenModel
        fields = (
            'otp',
        )
        widgets = {
            'otp': forms.TextInput(attrs={'class':'form-control'})
        }