from django.db import models
from extensions.jalali.utils import django_persianJalali_converter
from django.urls import reverse


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True, verbose_name='زیر مجموعه')
    is_sub = models.BooleanField(default=False, verbose_name='آیا زیر مجموعه میباشد ؟')
    name = models.CharField(max_length=255, verbose_name='نام')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name='اسلاگ')
    status = models.BooleanField(default=True, verbose_name='نمایش داده شود ؟')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان')

    def get_absolute_url(self):
        return reverse('home:category', args=[self.slug])

    class Meta:
        ordering = ('-created', 'name')
        verbose_name = "دسته بندی"
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products', verbose_name='دسته')
    name = models.CharField(max_length=255, verbose_name='نام')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name='اسلاگ')
    imag = models.ImageField(verbose_name='عکس')
    description = models.TextField(verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت') #models.DecimalField(max_digits=7, decimal_places=4)
    available = models.BooleanField(default=True, verbose_name='موجود')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی محصول')

    class Meta:
        ordering = ('-updated', '-created',)
        verbose_name = "محصول"
        verbose_name_plural = 'محصولات'

    def jalali(self):
        return django_persianJalali_converter(self.created)
    jalali.short_description = "زمان ارسال"

    def jalali_update(self):
        return django_persianJalali_converter(self.updated)
    jalali_update.short_description = "زمان آپدیت"

    def get_absolute_url(self):
        return reverse('home:product_detail', kwargs={'id': self.id, 'slug': self.slug})


    def __str__(self):
        return f'{self.name}'
