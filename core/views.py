from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from inventory.models import Medicine
from sales.models import Sale
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

@login_required
def dashboard(request):
    """Main dashboard view"""
    
    # Get statistics
    total_medicines = Medicine.objects.count()
    low_stock_count = Medicine.objects.filter(quantity__lte=10).count()
    out_of_stock_count = Medicine.objects.filter(quantity=0).count()
    
    # Sales statistics
    today = datetime.now().date()
    today_sales = Sale.objects.filter(created_at__date=today)
    today_revenue = today_sales.aggregate(total=Sum('total_amount'))['total'] or 0
    today_sales_count = today_sales.count()
    
    # Recent sales
    recent_sales = Sale.objects.order_by('-created_at')[:5]
    
    # Low stock items
    low_stock_items = Medicine.objects.filter(quantity__lte=10).order_by('quantity')[:5]
    
    context = {
        'total_medicines': total_medicines,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'today_revenue': today_revenue,
        'today_sales_count': today_sales_count,
        'recent_sales': recent_sales,
        'low_stock_items': low_stock_items,
    }
    
    return render(request, 'core/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
