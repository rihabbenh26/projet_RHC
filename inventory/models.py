from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Medicine category"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Supplier(models.Model):
    """Medicine supplier"""
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Medicine(models.Model):
    """Medicine model"""
    
    FORM_CHOICES = [
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('cream', 'Cream'),
        ('drops', 'Drops'),
        ('liquid', 'Liquid'),
        ('lozenge', 'Lozenge'),
    ]
    
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    form = models.CharField(max_length=20, choices=FORM_CHOICES, default='tablet')
    strength = models.CharField(max_length=50, blank=True)
    barcode = models.CharField(max_length=50, unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    min_quantity = models.PositiveIntegerField(default=10)
    expiry_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='medicines/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.strength}"
    
    @property
    def is_low_stock(self):
        return self.quantity <= self.min_quantity
    
    @property
    def is_out_of_stock(self):
        return self.quantity == 0

    def update_stock(self, movement_type, quantity, user, reason=''):
        """Update medicine stock and create movement record"""
        previous_quantity = self.quantity

        if movement_type == 'in':
            self.quantity += quantity
        elif movement_type == 'out':
            self.quantity = max(0, self.quantity - quantity)
        elif movement_type == 'adjustment':
            self.quantity = max(0, quantity)

        self.save()

        # Create stock movement record
        StockMovement.objects.create(
            medicine=self,
            movement_type=movement_type,
            quantity=quantity,
            previous_quantity=previous_quantity,
            new_quantity=self.quantity,
            reason=reason,
            user=user
        )

class StockMovement(models.Model):
    """Track stock movements"""
    
    MOVEMENT_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
    ]
    
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    previous_quantity = models.PositiveIntegerField()
    new_quantity = models.PositiveIntegerField()
    reason = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.medicine.name} - {self.get_movement_type_display()}"