from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from inventory.models import Medicine
from sales.models import Sale
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
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
    class ExtendedUserCreationForm(UserCreationForm):
        email = forms.EmailField(required=True, label="Email")
        
        class Meta:
            model = User
            fields = ("username", "email", "password1", "password2")
        
        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already registered.")
            return email

    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, 'Registration successful! You can now login.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error during registration: {str(e)}')
        else:
            # Print form errors to console for debugging
            print("Form errors:", form.errors)
    else:
        form = ExtendedUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_view(request):
    # Force fresh data from database
    user = User.objects.get(pk=request.user.pk)
    
    # Debug: Verify we're getting fresh data
    print(f"\n[DEBUG] Profile View - Current User Data:")
    print(f"First: '{user.first_name}' | Last: '{user.last_name}' | Email: '{user.email}'")
    
    return render(request, 'registration/profile.html', {'user': user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        try:
            user = request.user
            new_email = request.POST.get('email', '').strip()
            
            # Debug: Show received form data
            print(f"\n[DEBUG] Edit Profile - Form Submission:")
            print(f"First: '{request.POST.get('first_name')}'")
            print(f"Last: '{request.POST.get('last_name')}'")
            print(f"Email: '{new_email}'")
            
            # Validate email format
            if '@' not in new_email or '.' not in new_email:
                raise ValidationError("Please enter a valid email address")
            
            # Check email uniqueness
            if new_email != user.email and User.objects.filter(email=new_email).exists():
                raise ValidationError("This email is already in use")
            
            # Update fields (convert empty strings to None)
            user.first_name = request.POST.get('first_name', '').strip() or None
            user.last_name = request.POST.get('last_name', '').strip() or None
            user.email = new_email
            
            # Debug: Before saving
            print(f"\n[DEBUG] Before Save - User State:")
            print(f"First: '{user.first_name}' | Last: '{user.last_name}' | Email: '{user.email}'")
            
            # Save with explicit field updates
            user.save(update_fields=['first_name', 'last_name', 'email'])
            
            # Debug: After saving
            print(f"\n[DEBUG] After Save - User State:")
            print(f"First: '{user.first_name}' | Last: '{user.last_name}' | Email: '{user.email}'")
            
            # Verify database state
            db_user = User.objects.get(pk=user.pk)
            print(f"\n[DEBUG] Database State:")
            print(f"First: '{db_user.first_name}' | Last: '{db_user.last_name}' | Email: '{db_user.email}'")
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            # Preserve form input on error
            return render(request, 'edit_profile.html', {
                'preserved_data': {
                    'first_name': request.POST.get('first_name'),
                    'last_name': request.POST.get('last_name'),
                    'email': request.POST.get('email')
                }
            })
    
    return render(request, 'registration/edit_profile.html')