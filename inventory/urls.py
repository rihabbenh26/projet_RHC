from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.medicine_list, name='medicine_list'),
    path('medicine/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('medicine/add/', views.medicine_create, name='medicine_create'),
    path('medicine/<int:pk>/edit/', views.medicine_update, name='medicine_update'),
    path('medicine/<int:pk>/delete/', views.medicine_delete, name='medicine_delete'),
    path('medicine/<int:pk>/stock-update/', views.medicine_stock_update, name='medicine_stock_update'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    # Suppliers
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
    path('suppliers/<int:pk>/', views.supplier_detail, name='supplier_detail'),
]