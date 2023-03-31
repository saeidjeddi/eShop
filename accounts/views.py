from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms
import random
from utils import send_otp_code
from .models import OtpCod, User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
# Create your views here.


class UserRegisterView(View):
    form_class = forms.UserRegisterForm
    templates_name = 'accounts/user_register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.templates_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCod.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registration'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],

            }
            messages.success(request, 'کد تایید ارسال شد.', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.templates_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = forms.VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify_code.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration']
        code_instance = OtpCod.objects.get(phone_number=user_session['phone_number'])

        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                user = User.objects.creat_user(user_session['phone_number'], user_session['username'], user_session['email'], user_session['full_name'],
                                        user_session['password'])

                code_instance.delete()
                login(request, user)
                messages.success(request, 'ثبت نام با موفقیت انجام شد .', 'success')
                return redirect('home:index')
            else:
                messages.error(request, 'کد وارده صحیح نمیباشد .', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:index')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'از حساب خارج شدید', 'success')
        return redirect('home:index')


class LoginView(View):
    form_class = forms.UserLoginForm
    template_name = 'accounts/user_login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد حساب شدید', 'info')
                return redirect('home:index')
            messages.error(request, 'خطا در ورود', 'warning')
        return render(request, self.template_name, {'form': form})
