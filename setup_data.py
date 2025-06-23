#!/usr/bin/env python
"""
Quick script to set up sample data for the pharmacy system
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy.settings')
django.setup()

from django.db import transaction
from inventory.models import Category, Supplier, Medicine
from datetime import date

def setup_sample_data():
    """Load sample data into the database"""
    
    with transaction.atomic():
        print("Loading sample data...")
        
        # Create categories
        categories_data = [
            ('Pain Relief', 'Medications for pain management'),
            ('Antibiotics', 'Antimicrobial medications'),
            ('Vitamins', 'Vitamin supplements'),
            ('Cold & Flu', 'Medications for cold and flu symptoms'),
            ('Digestive', 'Medications for digestive issues'),
        ]
        
        categories = {}
        for name, description in categories_data:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            categories[name] = category
            if created:
                print(f'✓ Created category: {name}')
        
        # Create suppliers
        suppliers_data = [
            ('MediSupply Co.', 'John Smith', '555-0101', 'john@medisupply.com', '123 Medical Ave, City, State'),
            ('PharmaDist Inc.', 'Jane Doe', '555-0102', 'jane@pharmadist.com', '456 Pharma St, City, State'),
            ('HealthCorp Ltd.', 'Bob Johnson', '555-0103', 'bob@healthcorp.com', '789 Health Blvd, City, State'),
        ]
        
        suppliers = {}
        for name, contact_person, phone, email, address in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                name=name,
                defaults={
                    'contact_person': contact_person,
                    'phone': phone,
                    'email': email,
                    'address': address
                }
            )
            suppliers[name] = supplier
            if created:
                print(f'✓ Created supplier: {name}')
        
        # Create medicines
        medicines_data = [
            ('Tylenol', 'Acetaminophen', 'tablet', '500mg', '123456789012', 8.99, 100, 20, date(2025, 12, 31), 'Pain reliever and fever reducer', 'Pain Relief', 'MediSupply Co.'),
            ('Advil', 'Ibuprofen', 'tablet', '200mg', '123456789013', 9.99, 75, 15, date(2025, 11, 30), 'Anti-inflammatory pain reliever', 'Pain Relief', 'MediSupply Co.'),
            ('Amoxicillin', 'Amoxicillin', 'capsule', '250mg', '123456789014', 15.99, 50, 10, date(2025, 10, 15), 'Antibiotic for bacterial infections', 'Antibiotics', 'PharmaDist Inc.'),
            ('Vitamin C', 'Ascorbic Acid', 'tablet', '1000mg', '123456789015', 12.99, 200, 30, date(2026, 6, 30), 'Immune system support', 'Vitamins', 'HealthCorp Ltd.'),
            ('Robitussin', 'Dextromethorphan', 'syrup', '15mg/5ml', '123456789016', 11.99, 60, 12, date(2025, 8, 20), 'Cough suppressant', 'Cold & Flu', 'PharmaDist Inc.'),
            ('Pepto-Bismol', 'Bismuth Subsalicylate', 'liquid', '262mg/15ml', '123456789017', 7.99, 40, 8, date(2025, 9, 15), 'Upset stomach relief', 'Digestive', 'HealthCorp Ltd.'),
            ('Aspirin', 'Acetylsalicylic Acid', 'tablet', '325mg', '123456789018', 6.99, 150, 25, date(2025, 7, 10), 'Pain reliever and blood thinner', 'Pain Relief', 'MediSupply Co.'),
            ('Multivitamin', 'Mixed Vitamins', 'tablet', 'Daily', '123456789019', 14.99, 80, 15, date(2026, 3, 20), 'Daily vitamin supplement', 'Vitamins', 'HealthCorp Ltd.'),
        ]
        
        for (name, generic_name, form, strength, barcode, price, quantity, 
             min_quantity, expiry_date, description, category_name, supplier_name) in medicines_data:
            
            medicine, created = Medicine.objects.get_or_create(
                name=name,
                defaults={
                    'generic_name': generic_name,
                    'form': form,
                    'strength': strength,
                    'barcode': barcode,
                    'price': price,
                    'quantity': quantity,
                    'min_quantity': min_quantity,
                    'expiry_date': expiry_date,
                    'description': description,
                    'category': categories[category_name],
                    'supplier': suppliers[supplier_name],
                }
            )
            if created:
                print(f'✓ Created medicine: {name}')
        
        print("\n🎉 Sample data loaded successfully!")
        print(f"📊 Created {len(categories)} categories")
        print(f"🏢 Created {len(suppliers)} suppliers") 
        print(f"💊 Created {len(medicines_data)} medicines")

if __name__ == '__main__':
    setup_sample_data()
