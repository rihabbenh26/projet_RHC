from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.medicine_list, name='medicine_list'),
    path('medicine/<int:pk>/', views.medicine_detail, name='medicine_detail'),
]
