from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from django.template.loader import render_to_string
from inventory.models import Medicine, StockMovement
from .models import Sale, SaleItem, Customer
import json

@login_required
def pos(request):
    """Point of Sale view"""
    medicines = Medicine.objects.filter(quantity__gt=0).order_by('name')
    return render(request, 'sales/pos.html', {'medicines': medicines})

@login_required
def process_sale(request):
    """Process a sale"""
    if request.method == 'POST':
        try:
            cart_data = json.loads(request.POST.get('cart', '[]'))
            payment_method = request.POST.get('payment_method', 'cash')
            
            if not cart_data:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Cart is empty'
                })
            
            # Create sale
            sale = Sale.objects.create(
                cashier=request.user,
                payment_method=payment_method
            )
            
            total = 0
            
            # Process each item
            for item in cart_data:
                medicine = get_object_or_404(Medicine, pk=item['id'])
                quantity = int(item['quantity'])
                
                # Check stock
                if medicine.quantity < quantity:
                    sale.delete()
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Insufficient stock for {medicine.name}'
                    })
                
                # Create sale item
                sale_item = SaleItem.objects.create(
                    sale=sale,
                    medicine=medicine,
                    quantity=quantity,
                    unit_price=medicine.price
                )
                
                total += sale_item.total_price
                
                # Update stock
                old_quantity = medicine.quantity
                medicine.quantity -= quantity
                medicine.save()
                
                # Record stock movement
                StockMovement.objects.create(
                    medicine=medicine,
                    movement_type='out',
                    quantity=quantity,
                    previous_quantity=old_quantity,
                    new_quantity=medicine.quantity,
                    reason=f'Sale {sale.sale_number}',
                    user=request.user
                )
            
            # Update sale total
            sale.total_amount = total
            sale.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Sale completed successfully',
                'sale_id': sale.sale_number,
                'total': float(total)
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error processing sale: {str(e)}'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def print_receipt(request, sale_id):
    """Generate printable receipt"""
    sale = get_object_or_404(Sale, pk=sale_id)
    
    context = {
        'sale': sale,
    }
    
    return render(request, 'sales/receipt_template.html', context)

@login_required
def sale_list(request):
    """List all sales"""
    sales = Sale.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(sales, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'sales/sale_list.html', {'page_obj': page_obj})

@login_required
def sale_detail(request, pk):
    """Sale detail view"""
    sale = get_object_or_404(Sale, pk=pk)
    items = sale.items.all()
    
    return render(request, 'sales/sale_detail.html', {
        'sale': sale,
        'items': items
    })
