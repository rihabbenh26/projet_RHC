#!/usr/bin/env python
"""
Load sample data for pharmacy system with XAMPP MySQL
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

def load_sample_data():
    """Load sample data into MySQL database"""
    
    try:
        with transaction.atomic():
            print("🚀 Loading sample data into MySQL...")
            
            # Clear existing data (optional)
            print("🧹 Clearing existing data...")
            Medicine.objects.all().delete()
            Supplier.objects.all().delete()
            Category.objects.all().delete()
            
            # Create categories
            print("📂 Creating categories...")
            categories_data = [
                ('Pain Relief', 'Medications for pain management'),
                ('Antibiotics', 'Antimicrobial medications'),
                ('Vitamins', 'Vitamin supplements'),
                ('Cold & Flu', 'Medications for cold and flu symptoms'),
                ('Digestive', 'Medications for digestive issues'),
            ]
            
            categories = {}
            for name, description in categories_data:
                category = Category.objects.create(
                    name=name,
                    description=description
                )
                categories[name] = category
                print(f'  ✓ Created category: {name}')
            
            # Create suppliers
            print("🏢 Creating suppliers...")
            suppliers_data = [
                ('MediSupply Co.', 'John Smith', '555-0101', 'john@medisupply.com', '123 Medical Ave, City, State'),
                ('PharmaDist Inc.', 'Jane Doe', '555-0102', 'jane@pharmadist.com', '456 Pharma St, City, State'),
                ('HealthCorp Ltd.', 'Bob Johnson', '555-0103', 'bob@healthcorp.com', '789 Health Blvd, City, State'),
            ]
            
            suppliers = {}
            for name, contact_person, phone, email, address in suppliers_data:
                supplier = Supplier.objects.create(
                    name=name,
                    contact_person=contact_person,
                    phone=phone,
                    email=email,
                    address=address
                )
                suppliers[name] = supplier
                print(f'  ✓ Created supplier: {name}')
            
            # Create medicines
            print("💊 Creating medicines...")
            medicines_data = [
                ('Tylenol', 'Acetaminophen', 'tablet', '500mg', '123456789012', 8.99, 100, 20, date(2025, 12, 31), 'Pain reliever and fever reducer', 'Pain Relief', 'MediSupply Co.'),
                ('Advil', 'Ibuprofen', 'tablet', '200mg', '123456789013', 9.99, 75, 15, date(2025, 11, 30), 'Anti-inflammatory pain reliever', 'Pain Relief', 'MediSupply Co.'),
                ('Amoxicillin', 'Amoxicillin', 'capsule', '250mg', '123456789014', 15.99, 50, 10, date(2025, 10, 15), 'Antibiotic for bacterial infections', 'Antibiotics', 'PharmaDist Inc.'),
                ('Vitamin C', 'Ascorbic Acid', 'tablet', '1000mg', '123456789015', 12.99, 200, 30, date(2026, 6, 30), 'Immune system support', 'Vitamins', 'HealthCorp Ltd.'),
                ('Robitussin', 'Dextromethorphan', 'syrup', '15mg/5ml', '123456789016', 11.99, 60, 12, date(2025, 8, 20), 'Cough suppressant', 'Cold & Flu', 'PharmaDist Inc.'),
                ('Pepto-Bismol', 'Bismuth Subsalicylate', 'liquid', '262mg/15ml', '123456789017', 7.99, 40, 8, date(2025, 9, 15), 'Upset stomach relief', 'Digestive', 'HealthCorp Ltd.'),
                ('Aspirin', 'Acetylsalicylic Acid', 'tablet', '325mg', '123456789018', 6.99, 150, 25, date(2025, 7, 10), 'Pain reliever and blood thinner', 'Pain Relief', 'MediSupply Co.'),
                ('Multivitamin', 'Mixed Vitamins', 'tablet', 'Daily', '123456789019', 14.99, 80, 15, date(2026, 3, 20), 'Daily vitamin supplement', 'Vitamins', 'HealthCorp Ltd.'),
                ('Cough Drops', 'Menthol', 'lozenge', '5mg', '123456789020', 3.99, 120, 20, date(2025, 5, 15), 'Throat soothing lozenges', 'Cold & Flu', 'MediSupply Co.'),
                ('Antacid', 'Calcium Carbonate', 'tablet', '750mg', '123456789021', 5.99, 90, 18, date(2025, 4, 30), 'Heartburn relief', 'Digestive', 'HealthCorp Ltd.'),
            ]
            
            for (name, generic_name, form, strength, barcode, price, quantity, 
                 min_quantity, expiry_date, description, category_name, supplier_name) in medicines_data:
                
                medicine = Medicine.objects.create(
                    name=name,
                    generic_name=generic_name,
                    form=form,
                    strength=strength,
                    barcode=barcode,
                    price=price,
                    quantity=quantity,
                    min_quantity=min_quantity,
                    expiry_date=expiry_date,
                    description=description,
                    category=categories[category_name],
                    supplier=suppliers[supplier_name],
                )
                print(f'  ✓ Created medicine: {name}')
            
            print("\n🎉 Sample data loaded successfully!")
            print(f"📊 Created {len(categories)} categories")
            print(f"🏢 Created {len(suppliers)} suppliers") 
            print(f"💊 Created {len(medicines_data)} medicines")
            print("\n🚀 You can now run: python manage.py runserver")
            
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        print("Make sure XAMPP MySQL is running and database 'pharmacy_db' exists")

if __name__ == '__main__':
    load_sample_data()
