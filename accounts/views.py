from django.shortcuts import render
from django import views
from .forms import *
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

class SignUpView(views.View):
    
    def get(self, request):
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form':form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            mobile = form.cleaned_data.get('mobile')
            new = User(username=code)
            new.set_password(mobile)
            new.is_active = False
            try:
                new.save()
            except IntegrityError as e:
                e = 'قبلا با این کد ملی حساب کاربری ایجاد شده است!'
                return render(request, 'accounts/signup.html', {'form':form, 'message':e})
        else:
            return render(request, 'accounts/signup.html', {'form':form})
        
class SignInView(views.View):

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'accounts/test.html')
        form = LoginForm()
        return render(request, 'accounts/signin.html', {'form':form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            mobile = form.cleaned_data.get('mobile')
            try:
                user = User.objects.get(username=code)
            except User.DoesNotExist:
                messages.error(request, 'حساب کاربری با این کد ملی وجود ندارد، لطفا ابتدا حساب کاربری ایجاد کنید!')
                return render(request, 'accounts/signin.html', {'form':form})
            else:
                user = authenticate(username=code, password=mobile)
                if user is not None:
                    login(request, user)
                    messages.info(request, 'yes')
                    return render(request, 'accounts/signin.html', {'form':form})
                else:
                    messages.info(request, 'no')
                    return render(request, 'accounts/signin.html', {'form':form})
        else:
            return render(request, 'accounts/signin.html', {'form':form})