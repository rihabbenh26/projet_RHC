from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Medicine, Category, StockMovement

@login_required
def medicine_list(request):
    """List all medicines"""
    medicines = Medicine.objects.all()
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        medicines = medicines.filter(
            Q(name__icontains=search) | 
            Q(generic_name__icontains=search) |
            Q(barcode__icontains=search)
        )
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        medicines = medicines.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(medicines, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search': search,
        'selected_category': category_id,
    }
    
    return render(request, 'inventory/medicine_list.html', context)

@login_required
def medicine_detail(request, pk):
    """Medicine detail view"""
    medicine = get_object_or_404(Medicine, pk=pk)
    movements = StockMovement.objects.filter(medicine=medicine)[:10]
    
    context = {
        'medicine': medicine,
        'movements': movements,
    }
    
    return render(request, 'inventory/medicine_detail.html', context)
