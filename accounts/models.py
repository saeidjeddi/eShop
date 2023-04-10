from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from .manegers import UserManager
from extensions.jalali.utils import django_persianJalali_converter


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, verbose_name='نام کاربری')
    email = models.EmailField(max_length=255, unique=True, verbose_name='ایمیل')
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')
    full_name = models.CharField(max_length=255, verbose_name='نام کامل')
    is_active = models.BooleanField(default=True, verbose_name='کاربر فعال')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email', 'full_name']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'حساب'
        verbose_name_plural = 'حساب ها'


    @property
    def is_staff(self):
        return self.is_admin


class OtpCod(models.Model):
    phone_number = models.CharField(max_length=11, verbose_name='شماره تماس', unique=True)
    code = models.PositiveSmallIntegerField(verbose_name='کد تایید')
    created = models.DateTimeField(auto_now=True)

    def jalali(self):
        return django_persianJalali_converter(self.created)
    jalali.short_description = "زمان ارسال"

    class Meta:
        verbose_name = 'کد تایید'
        verbose_name_plural = 'کد تایید ارسال شده'

    def __str__(self):
        return f'{self.code} -> {self.phone_number}'
