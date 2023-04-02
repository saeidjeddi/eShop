from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CortAddForm


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


