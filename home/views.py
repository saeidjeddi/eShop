from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from . import models
from . import tasks
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import IsAdminUsrMixin

# Create your views here.


class HomeView(View):
    def get(self, request, slug=None):
        products = models.Product.objects.filter(available=True)
        sercher1 = models.Product.objects.filter(available=True).order_by('?')[:3]
        categories = models.Category.objects.filter(status=True, is_sub=False)
        if slug:
            category = get_object_or_404(models.Category, slug=slug)
            products = products.filter(category=category)
        return render(request, 'home/index.html', {'products': products, 'sercher1': sercher1, 'categories': categories})


class ProductDetailView(View):
    def get(self, request, id, slug):
        product = get_object_or_404(models.Product, id=id, slug=slug)
        return render(request, 'home/product_detail.html', {'product': product})


class BucketHome(LoginRequiredMixin,IsAdminUsrMixin, View):
    template_name = 'home/bucket.html'

    def get(self, request):
        objects = tasks.all_bucket_task()
        return render(request, self.template_name, {'objects': objects})


class DeleteBucketView(LoginRequiredMixin,IsAdminUsrMixin, View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'فایل حذف شد', 'info')
        return redirect('home:bucket')


class DownloadBucketView(LoginRequiredMixin,IsAdminUsrMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'فایل دانلود شد', 'primary')
        return redirect('home:bucket')


