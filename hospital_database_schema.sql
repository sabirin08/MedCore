DROP TABLE IF EXISTS Payment CASCADE;
DROP TABLE IF EXISTS Appointment CASCADE;
DROP TABLE IF EXISTS Medical_Record CASCADE;
DROP TABLE IF EXISTS Provider CASCADE;
DROP TABLE IF EXISTS Patient CASCADE;

-- Patient Table
CREATE TABLE Patient (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    First_name VARCHAR(100) NOT NULL,
    Last_name VARCHAR(100) NOT NULL,
    DOB DATE NOT NULL,
    Gender VARCHAR(20),
    Phone_Number VARCHAR(20),
    Address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Provider Table
CREATE TABLE Provider (
    Provider_id INT PRIMARY KEY AUTO_INCREMENT,
    First_name VARCHAR(100) NOT NULL,
    Last_name VARCHAR(100) NOT NULL,
    Department VARCHAR(100),
    Specialty VARCHAR(100),
    Phone_Number VARCHAR(20),
    Email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Medical Record Table
CREATE TABLE Medical_Record (
    Record_ID INT PRIMARY KEY AUTO_INCREMENT,
    Patient_id INT NOT NULL,
    Provider_id INT NOT NULL,
    Diagnosis TEXT,
    Treatment TEXT,
    Prescription TEXT,
    record_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Patient_id) REFERENCES Patient(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (Provider_id) REFERENCES Provider(Provider_id) ON DELETE CASCADE
);

-- Appointment Table
CREATE TABLE Appointment (
    Appointment_number INT PRIMARY KEY AUTO_INCREMENT,
    Patient_id INT NOT NULL,
    Provider_ID INT NOT NULL,
    Appointment_date DATETIME NOT NULL,
    status VARCHAR(50) DEFAULT 'Scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Patient_id) REFERENCES Patient(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (Provider_ID) REFERENCES Provider(Provider_id) ON DELETE CASCADE
);

-- Payment Table
CREATE TABLE Payment (
    Payment_id INT PRIMARY KEY AUTO_INCREMENT,
    Patient_ID INT NOT NULL,
    Appointment_ID INT NOT NULL,
    Payment_detail VARCHAR(255),
    Payment_date DATE NOT NULL,
    Payment_amount DECIMAL(10, 2) NOT NULL,
    payment_status VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (Patient_ID) REFERENCES Patient(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (Appointment_ID) REFERENCES Appointment(Appointment_number) ON DELETE CASCADE
);

CREATE INDEX idx_patient_name ON Patient(Last_name, First_name);
CREATE INDEX idx_provider_specialty ON Provider(Specialty);
CREATE INDEX idx_appointment_date ON Appointment(Appointment_date);
CREATE INDEX idx_medical_record_patient ON Medical_Record(Patient_id);
CREATE INDEX idx_payment_status ON Payment(payment_status);

-- Patients
INSERT INTO Patient (First_name, Last_name, DOB, Gender, Phone_Number, Address) VALUES
('John', 'Smith', '1985-03-15', 'Male', '555-0101', '123 Main St, City, ST 12345'),
('Sarah', 'Johnson', '1990-07-22', 'Female', '555-0102', '456 Oak Ave, City, ST 12346'),
('Michael', 'Williams', '1978-11-08', 'Male', '555-0103', '789 Pine Rd, City, ST 12347'),
('Emily', 'Brown', '1995-05-30', 'Female', '555-0104', '321 Elm St, City, ST 12348'),
('David', 'Jones', '1982-09-14', 'Male', '555-0105', '654 Maple Dr, City, ST 12349');

-- Providers
INSERT INTO Provider (First_name, Last_name, Department, Specialty, Phone_Number, Email) VALUES
('Dr. Lisa', 'Anderson', 'Cardiology', 'Cardiologist', '555-0201', 'l.anderson@hospital.com'),
('Dr. Robert', 'Taylor', 'Orthopedics', 'Orthopedic Surgeon', '555-0202', 'r.taylor@hospital.com'),
('Dr. Jennifer', 'Martinez', 'Pediatrics', 'Pediatrician', '555-0203', 'j.martinez@hospital.com'),
('Dr. James', 'Wilson', 'General Medicine', 'General Practitioner', '555-0204', 'j.wilson@hospital.com'),
('Dr. Maria', 'Garcia', 'Neurology', 'Neurologist', '555-0205', 'm.garcia@hospital.com');

-- Medical Records
INSERT INTO Medical_Record (Patient_id, Provider_id, Diagnosis, Treatment, Prescription) VALUES
(1, 1, 'Hypertension', 'Lifestyle modifications and medication', 'Lisinopril 10mg daily'),
(2, 3, 'Seasonal Allergies', 'Antihistamine therapy', 'Cetirizine 10mg as needed'),
(3, 2, 'Knee Pain', 'Physical therapy and pain management', 'Ibuprofen 400mg twice daily'),
(4, 4, 'Annual Checkup', 'Routine examination - all normal', 'None'),
(5, 5, 'Migraine', 'Pain management and preventive care', 'Sumatriptan 50mg as needed');

-- Appointments
INSERT INTO Appointment (Patient_id, Provider_ID, Appointment_date, status, notes) VALUES
(1, 1, '2025-11-15 10:00:00', 'Scheduled', 'Follow-up for hypertension'),
(2, 3, '2025-11-16 14:30:00', 'Scheduled', 'New patient consultation'),
(3, 2, '2025-11-17 09:00:00', 'Scheduled', 'Post-treatment check'),
(4, 4, '2025-11-18 11:00:00', 'Scheduled', 'Annual physical exam'),
(5, 5, '2025-11-19 15:00:00', 'Scheduled', 'Migraine management');

-- Payments
INSERT INTO Payment (Patient_ID, Appointment_ID, Payment_detail, Payment_date, Payment_amount, payment_status) VALUES
(1, 1, 'Consultation fee', '2025-11-15', 150.00, 'Paid'),
(2, 2, 'New patient visit', '2025-11-16', 200.00, 'Pending'),
(3, 3, 'Follow-up appointment', '2025-11-17', 100.00, 'Pending'),
(4, 4, 'Annual checkup', '2025-11-18', 175.00, 'Pending'),
(5, 5, 'Specialist consultation', '2025-11-19', 250.00, 'Pending');
