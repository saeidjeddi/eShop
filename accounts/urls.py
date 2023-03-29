from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('register/verifycode/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
]

