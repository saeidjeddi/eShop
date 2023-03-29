from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'username', 'email', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('password dont mach')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='برای تغییر گذرواژه  <a href=\"../password/\"> به این لینک بروید . </a>',
        label='گذرواژه',

    )

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login', 'username')


class UserRegisterForm(forms.Form):
    email = forms.EmailField(label='ایمیل')
    username = forms.CharField(max_length=255, label='نام کاربری')
    full_name = forms.CharField(max_length=250, label='نام کامل')
    phone_number = forms.CharField(max_length=11, label='شماره موبایل')
    password = forms.CharField(widget=forms.PasswordInput, label='گذرواژه')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('کاربر با این ایمیل قبلا ثبت نام شده')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number__iexact=phone_number).exists():
            raise ValidationError('کاربر با این شماره قبلا ثبت نام شده')
        return phone_number

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('کاربر با این نام کاربری قبلا ثبت نام شده')
        return username


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(label='کد')
