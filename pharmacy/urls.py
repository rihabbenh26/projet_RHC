"""
URL configuration for pharmacy project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('inventory/', include('inventory.urls')),
    path('sales/', include('sales.urls')),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
<<<<<<< HEAD
    path('register/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='register'),
   path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
=======
    path('register/', include('accounts.urls')),
    path('profile/', auth_views.LoginView.as_view(template_name='registration/profile.html'), name='profile'),
  
>>>>>>> f74a36dc7c234a12739c8ec447d15bba32dc096d
    path('accounts/', include('django.contrib.auth.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
