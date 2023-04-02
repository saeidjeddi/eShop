from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    # re_path(r"cart/remove/(?P<id>[-\w]+)/", views.CartRemoveView.as_view(), name="cart_remove"),
]
