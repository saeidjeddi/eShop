from django.urls import path, re_path, include
from . import views


app_name = 'home'


bucket_urls = [

    path('', views.BucketHome.as_view(), name='bucket'),
    path('delete_obj/<str:key>', views.DeleteBucketView.as_view(), name='delete_obj'),
    # re_path(r'bucket_obj_delete/(?P<key>[-\w]+)', views.DeleteBucketView.as_view(), name='bucket_delete'),
    path('download_obj/<str:key>', views.DownloadBucketView.as_view(), name='download_obj'),
]

urlpatterns = [
    # path('category/<slug:category_slug>/', views.HomeView.as_view(), name='category'),
    re_path(r'category/(?P<slug>[-\w]+)/', views.HomeView.as_view(), name='category'),
    path('bucket/', include(bucket_urls)),
    # path('diteil/<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    re_path(r'diteil/(?P<id>[0-9]+)/(?P<slug>[-\w]+)', views.ProductDetailView.as_view(), name='product_detail'),
    path('', views.HomeView.as_view(), name='index'),
]
