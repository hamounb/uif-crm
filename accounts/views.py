from django.shortcuts import render, redirect, get_object_or_404
from django import views
from .forms import *
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import TokenModel
from django.core.exceptions import ObjectDoesNotExist

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
            tk = TokenModel(user=new)
            tk.save()
            tk.generate()
            tk.save()
            request.session['un'] = code
            request.session['mo'] = mobile
            return redirect('accounts:verify', code=code)
        else:
            return render(request, 'accounts/signup.html', {'form':form})
        
class SignInView(views.View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('crm:index')
        form = LoginForm()
        return render(request, 'accounts/signin.html', {'form':form})
    
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('crm:index')
        form = LoginForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            mobile = form.cleaned_data.get('mobile')
            try:
                user = User.objects.get(username=code)
            except User.DoesNotExist:
                messages.error(request, 'حساب کاربری با این کد ملی وجود ندارد، لطفا ابتدا حساب کاربری ایجاد کنید!')
                return render(request, 'accounts/signin.html', {'form':form})
            auser = authenticate(username=code, password=mobile)
            if auser is not None:
                login(request, user)
                return redirect('crm:index')
            elif not user.is_active:
                try:
                    tk = TokenModel.objects.get(user=user)
                except TokenModel.DoesNotExist:
                    tk = TokenModel(user=user)
                    tk.generate()
                    tk.save()
                    request.session['un'] = code
                    request.session['mo'] = mobile
                    return redirect('accounts:verify', code=user.username)
                tk.generate()
                tk.save()
                request.session['un'] = code
                request.session['mo'] = mobile
                return redirect('accounts:verify', code=user.username)
            else:
                messages.error(request, 'شماره موبایل اشتباه است!')
                return render(request, 'accounts/signin.html', {'form':form})
        else:
            return render(request, 'accounts/signin.html', {'form':form})
        

class MobileVerifyView(views.View):

    def get(self, request, code):
        user = get_object_or_404(User, username=code)
        if not user.is_active:
            form = TokenForm()
            return render(request, 'accounts/token.html', {'form':form})
        return redirect('accounts:signin')
    
    def post(self, request, code):
        user = get_object_or_404(User, username=code)
        print(user)
        if not user.is_active:
            form = TokenForm(request.POST)
            try:
                tk = TokenModel.objects.get(user=user)
            except ObjectDoesNotExist:
                return redirect('accounts:re-mobile')
            if form.is_valid():
                otp = form.cleaned_data['otp']
                mobile = request.session.get('mo')
                if tk.otp == otp:
                    us = authenticate(username=code, password=mobile)
                    if us is not None:
                        user.is_active = True
                        user.save()
                        login(request, user)
                        del request.session['mo']
                        del request.session['un']
                        return redirect('crm:index')
                    else:
                        return redirect('accounts:re-mobile')
                else:
                    messages.error(request, 'رمز یکبارمصرف اشتباه است!', extra_tags='danger')
                    return render(request, 'accounts/token.html', {'form':form})
            else:
                return render(request, 'accounts/token.html', {'form':form})
        else:
            return redirect('crm:index')
        

class ChangeMobileView(views.View):

    def get(self, request, code):
        user = get_object_or_404(User, username=code)
        if not user.is_active:
            form = ChangeMobileForm()
            return render(request, 'accounts/change-mobile.html', {'form':form})
        return redirect('accounts:signin')
    
    def post(self, request, code):
        user = get_object_or_404(User, username=code)
        if not user.is_active:
            form = ChangeMobileForm(request.POST)
            if form.is_valid():
                mobile = form.cleaned_data.get('mobile')
                user.set_password(mobile)
                tk = TokenModel(user=user)
                tk.save()
                tk.generate()
                tk.save()
                request.session['mo'] = mobile
                return redirect('accounts:verify', code=code)
            return render(request, 'accounts/change-mobile.html', {'form':form})
        return redirect('accounts:signin')