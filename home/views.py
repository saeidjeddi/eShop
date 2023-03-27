from django.shortcuts import render

# Create your views here.


def hone(request):
    return render(request, 'home/index.html', {})
