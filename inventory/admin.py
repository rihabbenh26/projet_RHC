from django.contrib import admin
from .models import Category, Supplier, Medicine, StockMovement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email')
    search_fields = ('name', 'contact_person')

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'is_low_stock')
    list_filter = ('category', 'form', 'supplier')
    search_fields = ('name', 'generic_name', 'barcode')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'movement_type', 'quantity', 'user', 'created_at')
    list_filter = ('movement_type', 'created_at')
    readonly_fields = ('created_at',)
