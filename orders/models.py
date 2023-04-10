from django.db import models
# from accounts.models import User
# from django.conf import settings
from django.contrib.auth import get_user_model
from home.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    paid = models.BooleanField(default=False, verbose_name='پرداخت شده ؟')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان سفارش')
    update = models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')
    trackingcode = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='کد پیگیری')
    discount = models.PositiveIntegerField(blank=True, null=True, default=0)

    class Meta:
        ordering = ('paid', '-update', '-created',)
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    def __str__(self):
        return f'{str(self.paid)}'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item_product', verbose_name='محصول')
    price = models.IntegerField(verbose_name='قیمت')
    quantity = models.IntegerField(default=1, verbose_name='تعداد')

    class Meta:
        ordering = ('price', 'quantity',)
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return str(self.order)

    def get_cost(self):
        return self.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True, verbose_name='کد تخفیف')
    valid_from = models.DateTimeField(verbose_name='شروع زمان تخفیف')
    valid_to = models.DateTimeField(verbose_name='پایان زمان تخفیف')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='درصد تخفیف')
    active = models.BooleanField(default=False, verbose_name='فعال')

    class Meta:
        ordering = ('-valid_to', 'active')
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد های تخفیف'

    def __str__(self):
        return self.code


