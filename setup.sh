#!/bin/bash

# Pharmacy Management System Setup Script

echo "Setting up Pharmacy Management System..."

# Create virtual environment
python -m venv pharmacy_env

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source pharmacy_env/Scripts/activate
else
    source pharmacy_env/bin/activate
fi

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "Creating superuser..."
python manage.py createsuperuser

# Load initial data
echo "Loading initial data..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
from inventory.models import Category, Supplier, Medicine
from datetime import date

User = get_user_model()

# Create categories
categories = [
    ('Pain Relief', 'Medications for pain management'),
    ('Antibiotics', 'Antimicrobial medications'),
    ('Vitamins', 'Vitamin supplements'),
    ('Cold & Flu', 'Medications for cold and flu symptoms'),
    ('Digestive', 'Medications for digestive issues'),
]

for name, desc in categories:
    Category.objects.get_or_create(name=name, defaults={'description': desc})

# Create suppliers
suppliers = [
    ('MediSupply Co.', 'John Smith', '555-0101', 'john@medisupply.com', '123 Medical Ave'),
    ('PharmaDist Inc.', 'Jane Doe', '555-0102', 'jane@pharmadist.com', '456 Pharma St'),
    ('HealthCorp Ltd.', 'Bob Johnson', '555-0103', 'bob@healthcorp.com', '789 Health Blvd'),
]

for name, contact, phone, email, address in suppliers:
    Supplier.objects.get_or_create(
        name=name,
        defaults={
            'contact_person': contact,
            'phone': phone,
            'email': email,
            'address': address
        }
    )

print("Initial data loaded successfully!")
EOF

echo "Setup complete! Run 'python manage.py runserver' to start the application."
