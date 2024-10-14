from django.shortcuts import render

# Create your views here.


def home(request):
    """view for index page"""
    return render(request, 'home/home.html')