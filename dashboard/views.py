from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from checkout.models import Order
from dashboard.models import Dashboard

# Create your views here.

@login_required
def dashboard(request):
    if not request.user.is_superuser:
        profile = get_object_or_404(Dashboard, user=request.user.id)
        orders = profile.orders.all()
    
    template = 'dashboard/profile.html'
    context = {
        'orders': orders,
    }
    return render(request, template, context)