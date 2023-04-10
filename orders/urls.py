from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:id>/', views.CartRemoveView.as_view(), name='cart_remove'),

    # re_path(r"cart/remove/(?P<id>[-\w]+)/", views.CartRemoveView.as_view(), name="cart_remove"),
    path('cart/create/', views.OrderCreatView.as_view(), name='order_create'),
    path('cart/detail/<int:id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('cart/remove/', views.RemoveOrderCart.as_view(), name='remove_order_cart'),
    path('pay/<int:id>/', views.OrderPayView.as_view(), name='pay'),
    path('verify/', views.OrderVerifyView.as_view(), name='verify'),
    path('apply/<int:id>', views.OrderApplyCoupanView.as_view(), name='apply'),
]
