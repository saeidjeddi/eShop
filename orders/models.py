from django.db import models
# from accounts.models import User
# from django.conf import settings
from django.contrib.auth import get_user_model
from home.models import Product


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    paid = models.BooleanField(default=False, verbose_name='پرداخت شده ؟')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان سفارش')
    update = models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')
    trackingcode = models.PositiveIntegerField(default=0, verbose_name='کد پیگیری')

    class Meta:
        ordering = ('paid', '-update', '-created',)
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    def __str__(self):
        return f'{str(self.paid)}'

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


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

