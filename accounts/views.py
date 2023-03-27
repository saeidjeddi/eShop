from django.shortcuts import render
from django.views.generic import View
from . import forms

# Create your views here.


class UserRegisterView(View):
    form_class = forms.UserRegisterForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/user_register.html', {'form': form})

    def post(self, request):
        pass
