from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F, Count
from django.db import transaction
from .models import Medicine, Category, Supplier, StockMovement
from .forms import MedicineForm, StockUpdateForm, CategoryForm, SupplierForm
from django.http import JsonResponse

@login_required
def medicine_list(request):
    """List all medicines with search and filtering"""
    medicines = Medicine.objects.select_related('category', 'supplier').all()
    
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

# @login_required
# def medicine_detail(request, pk):
#     """Medicine detail view"""
#     medicine = get_object_or_404(Medicine.objects.select_related('category', 'supplier'), pk=pk)
#     movements = StockMovement.objects.filter(medicine=medicine).select_related('user').order_by('-created_at')[:10]
    
#     context = {
#         'medicine': medicine,
#         'movements': movements,
#     }
#     return render(request, 'inventory/medicine_list.html', context)

@login_required
@permission_required('inventory.add_medicine', raise_exception=True)
def medicine_create(request):
    """Create new medicine"""
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            medicine = form.save()
            messages.success(request, f'Medicine "{medicine.name}" created successfully!')
            return redirect('inventory:medicine_list')  # Redirection vers la liste
    else:
        form = MedicineForm()
    
    context = {
        'form': form,
        'title': 'Add New Medicine'
    }
    return render(request, 'inventory/medicine_form.html', context)

@login_required
def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine.objects.select_related('category', 'supplier'), pk=pk)
    movements = StockMovement.objects.filter(medicine=medicine).select_related('user').order_by('-created_at')[:10]
    return render(request, 'inventory/medicine_detail.html', {
        'medicine': medicine,
        'movements': movements
    })
@login_required
@permission_required('inventory.change_medicine', raise_exception=True)
def medicine_update(request, pk):
    """Update existing medicine"""
    medicine = get_object_or_404(Medicine, pk=pk)
    
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES, instance=medicine)
        if form.is_valid():
            medicine = form.save()
            messages.success(request, f'Medicine "{medicine.name}" updated successfully!')
            return redirect('inventory:medicine_list')  # Redirection vers la liste
    else:
        form = MedicineForm(instance=medicine)
    
    context = {
        'form': form,
        'title': 'Edit Medicine',
        'medicine': medicine
    }
    return render(request, 'inventory/medicine_form.html', context)

@login_required
@permission_required('inventory.delete_medicine', raise_exception=True)
def medicine_delete(request, pk):
    """Delete medicine"""
    medicine = get_object_or_404(Medicine, pk=pk)
    
    if request.method == 'POST':
        medicine_name = medicine.name
        medicine.delete()
        messages.success(request, f'Medicine "{medicine_name}" deleted successfully!')
        return redirect('inventory:medicine_list')
    
    context = {'medicine': medicine}
    return render(request, 'inventory/medicine_confirm_delete.html', context)

@login_required
@permission_required('inventory.change_medicine', raise_exception=True)
def medicine_stock_update(request, pk):
    """Update medicine stock quantity"""
    medicine = get_object_or_404(Medicine, pk=pk)
    
    if request.method == 'POST':
        form = StockUpdateForm(request.POST)
        if form.is_valid():
            movement_type = form.cleaned_data['movement_type']
            quantity = form.cleaned_data['quantity']
            reason = form.cleaned_data['reason']
            
            try:
                with transaction.atomic():
                    if movement_type == 'out' and quantity > medicine.quantity:
                        raise ValueError(f'Cannot deduct {quantity} items. Only {medicine.quantity} available.')
                    
                    medicine.update_stock(
                        movement_type=movement_type,
                        quantity=quantity,
                        user=request.user,
                        reason=reason
                    )
                    
                    messages.success(request, f'Stock for "{medicine.name}" updated successfully!')
                    return redirect('inventory:medicine_list')  # Redirection vers la liste
            
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = StockUpdateForm()
    
    context = {
        'medicine': medicine,
        'form': form,
        'title': 'Update Stock'
    }
    return render(request, 'inventory/stock_update_form.html', context)
@login_required
def category_list(request):
    """List all categories"""
    categories = Category.objects.annotate(medicine_count=Count('medicine')).order_by('name')
    return render(request, 'inventory/category_list.html', {'categories': categories})

@login_required
@permission_required('inventory.add_category', raise_exception=True)
def category_create(request):
    """Create new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('inventory:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'inventory/category_form.html', {
        'form': form,
        'title': 'Add New Category'
    })

@login_required
def category_update(request, pk):
    """Vue pour modifier une catégorie existante"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('inventory:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'inventory/category_form.html', {
        'form': form,
        'title': f'Edit Category: {category.name}'
    })

@login_required
def category_delete(request, pk):
    """Vue pour supprimer une catégorie"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        try:
            category_name = category.name
            category.delete()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Category deleted successfully!'})
            
            messages.success(request, f'Category "{category_name}" was deleted successfully!')
            return redirect('inventory:category_list')
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)}, status=500)
            
            messages.error(request, f'Error deleting category: {str(e)}')
            return redirect('inventory:category_list')
    
    # Si ce n'est pas une requête POST, afficher la page de confirmation
    return render(request, 'inventory/category_detail.html', {'category': category})


@login_required
def supplier_list(request):
    """List all suppliers"""
    suppliers = Supplier.objects.annotate(medicine_count=Count('medicine')).order_by('name')
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})

@login_required
@permission_required('inventory.add_supplier', raise_exception=True)
def supplier_create(request):
    """Create new supplier"""
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Supplier "{supplier.name}" created successfully!')
            return redirect('inventory:supplier_list')
    else:
        form = SupplierForm()
    
    return render(request, 'inventory/supplier_form.html', {
        'form': form,
        'title': 'Add New Supplier'
    })

@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully!')
            return redirect('inventory:supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'inventory/supplier_form.html', {'form': form, 'supplier': supplier})

@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier_name = supplier.name
        supplier.delete()
        messages.success(request, f'Supplier "{supplier_name}" was deleted successfully!')
        return redirect('inventory:supplier_list')
    
    # Si la méthode n'est pas POST, rediriger vers la liste
    return redirect('inventory:supplier_list')

@login_required
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier.objects.prefetch_related('medicine_set'), pk=pk)
    return render(request, 'inventory/supplier_detail.html', {'supplier': supplier})