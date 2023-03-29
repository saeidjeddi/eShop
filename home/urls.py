from django.urls import path, re_path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('bucket/', views.BucketHome.as_view(), name='bucket'),
    path('bucket_obj_delete/<key>', views.DeleteBucketView.as_view(), name='bucket_delete'),
    # re_path(r'bucket_obj_delete/(?P<key>[-\w]+)', views.DeleteBucketView.as_view(), name='bucket_delete'),
    # path('diteil/<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    re_path(r'diteil/(?P<id>[0-9]+)/(?P<slug>[-\w]+)', views.ProductDetailView.as_view(), name='product_detail'),
]
