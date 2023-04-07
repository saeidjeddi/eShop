from django.contrib import admin
from .models import Order, OrderItem




class OrderInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'update', 'paid')
    list_filter = ('paid',)
    inlines = (OrderInline,)
