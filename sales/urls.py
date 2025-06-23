from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('pos/', views.pos, name='pos'),
    path('process/', views.process_sale, name='process_sale'),
    path('receipt/<int:sale_id>/', views.print_receipt, name='print_receipt'),
    path('', views.sale_list, name='sale_list'),
    path('sale/<int:pk>/', views.sale_detail, name='sale_detail'),
]
