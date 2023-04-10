from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CortAddForm, CouponForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Coupon
import requests
import json
import datetime
from django.contrib import messages



class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=id)
        form = CortAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product, cd['quantity'])
        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderCreatView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        cart.clear()
        return redirect('orders:order_detail', order.id)


class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponForm

    def get(self, request, id):
        order = get_object_or_404(Order, id=id)
        return render(request, 'orders/order.html', {'order': order, 'form': self.form_class})


class RemoveOrderCart(LoginRequiredMixin, View):
    def get(self, request):
        Cart(request).clear()

        return redirect('orders:cart')


MERCHANT = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
CallbackURL = 'http://127.0.0.1:8000/orders/verify/'


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, id):
        order = Order.objects.get(id=id)
        request.session['order_pay'] = {
            'order_id': order.id,
        }
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.get_total_price(),
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user.phone_number, "email": request.user.email}
        }
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        t_authority = request.GET['Authority']
        t_status = request.GET.get('Status')
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.get_total_price(),
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.paid = True
                    order.trackingcode = int(req.json()['data']['ref_id'])
                    order.save()
                    return HttpResponse('Transaction success.\nRefID: ' + str(req.json()['data']['ref_id']))
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(req.json()['data']['message']))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(req.json()['data']['message']))

        else:
            return HttpResponse('معامله انجام نشد یا توسط کاربر لغو شد')


class OrderApplyCoupanView(LoginRequiredMixin, View):
    form_class = CouponForm

    def post(self, request, id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'کد تخفیف اشتباه یا قبلا استفاده شده هست', 'danger')
                return redirect('orders:order_detail', id)
            order = Order.objects.get(id=id)
            order.discount = coupon.discount
            order.save()
        return redirect('orders:order_detail', id)


