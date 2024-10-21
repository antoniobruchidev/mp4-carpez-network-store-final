from django.shortcuts import render

# Create your views here.


def home(request):
    """view for index page"""
    
    print(request.user.id)
    return render(request, 'home/home.html')