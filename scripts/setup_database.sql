-- Create initial data for the pharmacy system

-- Insert categories
INSERT INTO inventory_category (name, description) VALUES
('Pain Relief', 'Medications for pain management'),
('Antibiotics', 'Antimicrobial medications'),
('Vitamins', 'Vitamin supplements'),
('Cold & Flu', 'Medications for cold and flu symptoms'),
('Digestive', 'Medications for digestive issues');

-- Insert suppliers
INSERT INTO inventory_supplier (name, contact_person, phone, email, address) VALUES
('MediSupply Co.', 'John Smith', '555-0101', 'john@medisupply.com', '123 Medical Ave, City, State'),
('PharmaDist Inc.', 'Jane Doe', '555-0102', 'jane@pharmadist.com', '456 Pharma St, City, State'),
('HealthCorp Ltd.', 'Bob Johnson', '555-0103', 'bob@healthcorp.com', '789 Health Blvd, City, State');

-- Insert sample medicines
INSERT INTO inventory_medicine (
    name, generic_name, form, strength, barcode, price, quantity, min_quantity, 
    expiry_date, description, category_id, supplier_id
) VALUES
('Tylenol', 'Acetaminophen', 'tablet', '500mg', '123456789012', 8.99, 100, 20, '2025-12-31', 'Pain reliever and fever reducer', 1, 1),
('Advil', 'Ibuprofen', 'tablet', '200mg', '123456789013', 9.99, 75, 15, '2025-11-30', 'Anti-inflammatory pain reliever', 1, 1),
('Amoxicillin', 'Amoxicillin', 'capsule', '250mg', '123456789014', 15.99, 50, 10, '2025-10-15', 'Antibiotic for bacterial infections', 2, 2),
('Vitamin C', 'Ascorbic Acid', 'tablet', '1000mg', '123456789015', 12.99, 200, 30, '2026-06-30', 'Immune system support', 3, 3),
('Robitussin', 'Dextromethorphan', 'syrup', '15mg/5ml', '123456789016', 11.99, 60, 12, '2025-08-20', 'Cough suppressant', 4, 2);
