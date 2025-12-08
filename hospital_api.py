from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database
from datetime import datetime

app = Flask(__name__)
CORS(app)

db = Database()

@app.before_request
def before_request():
    if not db.connection or not db.connection.is_connected():
        db.connect()

# ==================== PATIENT CRUD OPERATIONS ====================

@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Get all patients"""
    try:
        query = "SELECT * FROM Patient ORDER BY Last_name, First_name"
        patients = db.fetch_query(query)
        return jsonify({
            'success': True,
            'data': patients,
            'count': len(patients)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get a specific patient by ID"""
    try:
        query = "SELECT * FROM Patient WHERE patient_id = %s"
        patient = db.fetch_one(query, (patient_id,))
        if patient:
            return jsonify({'success': True, 'data': patient}), 200
        return jsonify({'success': False, 'error': 'Patient not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/patients', methods=['POST'])
def create_patient():
    """Create a new patient"""
    try:
        data = request.get_json()
        query = """
            INSERT INTO Patient (First_name, Last_name, DOB, Gender, Phone_Number, Address)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            data['First_name'],
            data['Last_name'],
            data['DOB'],
            data.get('Gender'),
            data.get('Phone_Number'),
            data.get('Address')
        )
        patient_id = db.execute_query(query, params)
        return jsonify({
            'success': True,
            'message': 'Patient created successfully',
            'patient_id': patient_id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update an existing patient"""
    try:
        data = request.get_json()
        query = """
            UPDATE Patient 
            SET First_name = %s, Last_name = %s, DOB = %s, Gender = %s, 
                Phone_Number = %s, Address = %s
            WHERE patient_id = %s
        """
        params = (
            data['First_name'],
            data['Last_name'],
            data['DOB'],
            data.get('Gender'),
            data.get('Phone_Number'),
            data.get('Address'),
            patient_id
        )
        db.execute_query(query, params)
        return jsonify({
            'success': True,
            'message': 'Patient updated successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete a patient"""
    try:
        query = "DELETE FROM Patient WHERE patient_id = %s"
        db.execute_query(query, (patient_id,))
        return jsonify({
            'success': True,
            'message': 'Patient deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>/medical-history', methods=['GET'])
def get_patient_medical_history(patient_id):
    """Get patient's complete medical history"""
    try:
        query = """
            SELECT mr.*, p.First_name as Provider_First_name, 
                   p.Last_name as Provider_Last_name, p.Specialty
            FROM Medical_Record mr
            JOIN Provider p ON mr.Provider_id = p.Provider_id
            WHERE mr.Patient_id = %s
            ORDER BY mr.record_date DESC
        """
        records = db.fetch_query(query, (patient_id,))
        return jsonify({
            'success': True,
            'data': records,
            'count': len(records)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== PROVIDER CRUD OPERATIONS ====================

@app.route('/api/providers', methods=['GET'])
def get_providers():
    """Get all providers"""
    try:
        query = "SELECT * FROM Provider ORDER BY Last_name, First_name"
        providers = db.fetch_query(query)
        return jsonify({
            'success': True,
            'data': providers,
            'count': len(providers)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/providers/<int:provider_id>', methods=['GET'])
def get_provider(provider_id):
    """Get a specific provider by ID"""
    try:
        query = "SELECT * FROM Provider WHERE Provider_id = %s"
        provider = db.fetch_one(query, (provider_id,))
        if provider:
            return jsonify({'success': True, 'data': provider}), 200
        return jsonify({'success': False, 'error': 'Provider not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/providers', methods=['POST'])
def create_provider():
    """Create a new provider"""
    try:
        data = request.get_json()
        query = """
            INSERT INTO Provider (First_name, Last_name, Department, Specialty, Phone_Number, Email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            data['First_name'],
            data['Last_name'],
            data.get('Department'),
            data.get('Specialty'),
            data.get('Phone_Number'),
            data.get('Email')
        )
        provider_id = db.execute_query(query, params)
        return jsonify({
            'success': True,
            'message': 'Provider created successfully',
            'provider_id': provider_id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/providers/<int:provider_id>', methods=['PUT'])
def update_provider(provider_id):
    """Update an existing provider"""
    try:
        data = request.get_json()
        query = """
            UPDATE Provider 
            SET First_name = %s, Last_name = %s, Department = %s, 
                Specialty = %s, Phone_Number = %s, Email = %s
            WHERE Provider_id = %s
        """
        params = (
            data['First_name'],
            data['Last_name'],
            data.get('Department'),
            data.get('Specialty'),
            data.get('Phone_Number'),
            data.get('Email'),
            provider_id
        )
        db.execute_query(query, params)
        return jsonify({
            'success': True,
            'message': 'Provider updated successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/providers/<int:provider_id>', methods=['DELETE'])
def delete_provider(provider_id):
    """Delete a provider"""
    try:
        query = "DELETE FROM Provider WHERE Provider_id = %s"
        db.execute_query(query, (provider_id,))
        return jsonify({
            'success': True,
            'message': 'Provider deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/providers/<int:provider_id>/schedule', methods=['GET'])
def get_provider_schedule(provider_id):
    """Get provider's appointment schedule"""
    try:
        query = """
            SELECT a.*, p.First_name, p.Last_name, p.Phone_Number
            FROM Appointment a
            JOIN Patient p ON a.Patient_id = p.patient_id
            WHERE a.Provider_ID = %s
            ORDER BY a.Appointment_date
        """
        appointments = db.fetch_query(query, (provider_id,))
        return jsonify({
            'success': True,
            'data': appointments,
            'count': len(appointments)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== MEDICAL RECORD CRUD OPERATIONS ====================

@app.route('/api/medical-records', methods=['GET'])
def get_medical_records():
    """Get all medical records"""
    try:
        query = """
            SELECT mr.*, 
                   pat.First_name as Patient_First_name, pat.Last_name as Patient_Last_name,
                   prov.First_name as Provider_First_name, prov.Last_name as Provider_Last_name
            FROM Medical_Record mr
            JOIN Patient pat ON mr.Patient_id = pat.patient_id
            JOIN Provider prov ON mr.Provider_id = prov.Provider_id
            ORDER BY mr.record_date DESC
        """
        records = db.fetch_query(query)
        return jsonify({
            'success': True,
            'data': records,
            'count': len(records)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/medical-records/<int:record_id>', methods=['GET'])
def get_medical_record(record_id):
    """Get a specific medical record by ID"""
    try:
        query = """
            SELECT mr.*, 
                   pat.First_name as Patient_First_name, pat.Last_name as Patient_Last_name,
                   prov.First_name as Provider_First_name, prov.Last_name as Provider_Last_name
            FROM Medical_Record mr
            JOIN Patient pat ON mr.Patient_id = pat.patient_id
            JOIN Provider prov ON mr.Provider_id = prov.Provider_id
            WHERE mr.Record_ID = %s
        """
        record = db.fetch_one(query, (record_id,))
        if record:
            return jsonify({'success': True, 'data': record}), 200
        return jsonify({'success': False, 'error': 'Medical record not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/medical-records', methods=['POST'])
def create_medical_record():
    """Create a new medical record"""
    try:
        data = request.get_json()
        query = """
            INSERT INTO Medical_Record (Patient_id, Provider_id, Diagnosis, Treatment, Prescription)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            data['Patient_id'],
            data['Provider_id'],
            data.get('Diagnosis'),
            data.get('Treatment'),
            data.get('Prescription')
        )
        record_id = db.execute_query(query, params)
        return jsonify({
            'success': True,
            'message': 'Medical record created successfully',
            'record_id': record_id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/medical-records/<int:record_id>', methods=['PUT'])
def update_medical_record(record_id):
    """Update an existing medical record"""
    try:
        data = request.get_json()
        query = """
            UPDATE Medical_Record 
            SET Patient_id = %s, Provider_id = %s, Diagnosis = %s, 
                Treatment = %s, Prescription = %s
            WHERE Record_ID = %s
        """
        params = (
            data['Patient_id'],
            data['Provider_id'],
            data.get('Diagnosis'),
            data.get('Treatment'),
            data.get('Prescription'),
            record_id
        )
        db.execute_query(query, params)
        return jsonify({
            'success': True,
            'message': 'Medical record updated successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/medical-records/<int:record_id>', methods=['DELETE'])
def delete_medical_record(record_id):
    """Delete a medical record"""
    try:
        query = "DELETE FROM Medical_Record WHERE Record_ID = %s"
        db.execute_query(query, (record_id,))
        return jsonify({
            'success': True,
            'message': 'Medical record deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== APPOINTMENT CRUD OPERATIONS ====================

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    """Get all appointments"""
    try:
        query = """
            SELECT a.*, 
                   p.First_name as Patient_First_name, p.Last_name as Patient_Last_name,
                   prov.First_name as Provider_First_name, prov.Last_name as Provider_Last_name,
                   prov.Specialty
            FROM Appointment a
            JOIN Patient p ON a.Patient_id = p.patient_id
            JOIN Provider prov ON a.Provider_ID = prov.Provider_id
            ORDER BY a.Appointment_date DESC
        """
        appointments = db.fetch_query(query)
        return jsonify({
            'success': True,
            'data': appointments,
            'count': len(appointments)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """Get a specific appointment by ID"""
    try:
        query = """
            SELECT a.*, 
                   p.First_name as Patient_First_name, p.Last_name as Patient_Last_name,
                   p.Phone_Number as Patient_Phone,
                   prov.First_name as Provider_First_name, prov.Last_name as Provider_Last_name,
                   prov.Specialty, prov.Department
            FROM Appointment a
            JOIN Patient p ON a.Patient_id = p.patient_id
            JOIN Provider prov ON a.Provider_ID = prov.Provider_id
            WHERE a.Appointment_number = %s
        """
        appointment = db.fetch_one(query, (appointment_id,))
        if appointment:
            return jsonify({'success': True, 'data': appointment}), 200
        return jsonify({'success': False, 'error': 'Appointment not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    """Book a new appointment"""
    try:
        data = request.get_json()
        query = """
            INSERT INTO Appointment (Patient_id, Provider_ID, Appointment_date, status, notes)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            data['Patient_id'],
            data['Provider_ID'],
            data['Appointment_date'],
            data.get('status', 'Scheduled'),
            data.get('notes', '')
        )
        appointment_id = db.execute_query(query, params)
        return jsonify({
            'success': True,
            'message': 'Appointment booked successfully',
            'appointment_id': appointment_id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """Update an existing appointment (reschedule, cancel, etc.)"""
    try:
        data = request.get_json()
        query = """
            UPDATE Appointment 
            SET Patient_id = %s, Provider_ID = %s, Appointment_date = %s, 
                status = %s, notes = %s
            WHERE Appointment_number = %s
        """
        params = (
            data['Patient_id'],
            data['Provider_ID'],
            data['Appointment_date'],
            data.get('status', 'Scheduled'),
            data.get('notes', ''),
            appointment_id
        )
        db.execute_query(query, params)
        return jsonify({
            'success': True,
            'message': 'Appointment updated successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    """Cancel/delete an appointment"""
    try:
        query = "DELETE FROM Appointment WHERE Appointment_number = %s"
        db.execute_query(query, (appointment_id,))
        return jsonify({
            'success': True,
            'message': 'Appointment cancelled successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/appointments/<int:appointment_id>/reschedule', methods=['PUT'])
def reschedule_appointment(appointment_id):
    """Reschedule an appointment to a new date/time"""
    try:
        data = request.get_json()
        query = """
            UPDATE Appointment 
            SET Appointment_date = %s, status = 'Rescheduled'
            WHERE Appointment_number = %s
        """
        params = (data['new_date'], appointment_id)
        db.execute_query(query, params)
        return jsonify({
            'success': True,
            'message': 'Appointment rescheduled successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== PAYMENT CRUD OPERATIONS ====================

@app.route('/api/payments', methods=['GET'])
def get_payments():
    """Get all payments"""
    try:
        query = """
            SELECT pay.*, 
                   p.First_name as Patient_First_name, p.Last_name as Patient_Last_name,
                   a.Appointment_date
            FROM Payment pay
            JOIN Patient p ON pay.Patient_ID = p.patient_id
            JOIN Appointment a ON pay.Appointment_ID = a.Appointment_number
            ORDER BY pay.Payment_date DESC
        """
        payments = db.fetch_query(query)
        return jsonify({
            'success': True,
            'data': payments,
            'count': len(payments)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    """Get a specific payment by ID"""
    try:
        query = """
            SELECT pay.*, 
                   p.First_name as Patient_First_name, p.Last_name as Patient_Last_name,
                   a.Appointment_date
            FROM Payment pay
            JOIN Patient p ON pay.Patient_ID = p.patient_id
            JOIN Appointment a ON pay.Appointment_ID = a.Appointment_number
            WHERE pay.Payment_id = %s
        """
        payment = db.fetch_one(query, (payment_id,))
        if payment:
            return jsonify({'success': True, 'data': payment}), 200
        return jsonify({'success': False, 'error': 'Payment not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/payments', methods=['POST'])
def create_payment():
    """Record a new payment"""
    try:
        data = request.get_json()
        query = """
            INSERT INTO Payment (Patient_ID, Appointment_ID, Payment_detail, 
                               Payment_date, Payment_amount, payment_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            data['Patient_ID'],
            data['Appointment_ID'],
            data.get('Payment_detail', ''),
            data['Payment_date'],
            data['Payment_amount'],
            data.get('payment_status', 'Pending')
        )
        payment_id = db.execute_query(query, params)
        return jsonify({
            'success': True,
            'message': 'Payment recorded successfully',
            'payment_id': payment_id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/payments/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    """Update payment information (e.g., mark as paid)"""
    try:
        data = request.get_json()
        query = """
            UPDATE Payment 
            SET Patient_ID = %s, Appointment_ID = %s, Payment_detail = %s,
                Payment_date = %s, Payment_amount = %s, payment_status = %s
            WHERE Payment_id = %s
        """
        params = (
            data['Patient_ID'],
            data['Appointment_ID'],
            data.get('Payment_detail', ''),
            data['Payment_date'],
            data['Payment_amount'],
            data.get('payment_status', 'Pending'),
            payment_id
        )
        db.execute_query(query, params)
        return jsonify({
            'success': True,
            'message': 'Payment updated successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    """Delete a payment record"""
    try:
        query = "DELETE FROM Payment WHERE Payment_id = %s"
        db.execute_query(query, (payment_id,))
        return jsonify({
            'success': True,
            'message': 'Payment deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/payments/<int:payment_id>/mark-paid', methods=['PUT'])
def mark_payment_paid(payment_id):
    """Mark a payment as paid"""
    try:
        query = "UPDATE Payment SET payment_status = 'Paid' WHERE Payment_id = %s"
        db.execute_query(query, (payment_id,))
        return jsonify({
            'success': True,
            'message': 'Payment marked as paid'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/payments/pending', methods=['GET'])
def get_pending_payments():
    """Get all pending payments"""
    try:
        query = """
            SELECT pay.*, 
                   p.First_name as Patient_First_name, p.Last_name as Patient_Last_name,
                   p.Phone_Number as Patient_Phone
            FROM Payment pay
            JOIN Patient p ON pay.Patient_ID = p.patient_id
            WHERE pay.payment_status = 'Pending'
            ORDER BY pay.Payment_date
        """
        payments = db.fetch_query(query)
        return jsonify({
            'success': True,
            'data': payments,
            'count': len(payments)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== UTILITY ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        if db.connection and db.connection.is_connected():
            return jsonify({
                'success': True,
                'message': 'API is running and database is connected'
            }), 200
        return jsonify({
            'success': False,
            'message': 'Database connection issue'
        }), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        stats = {}
        stats['total_patients'] = db.fetch_one("SELECT COUNT(*) as count FROM Patient")['count']
        stats['total_providers'] = db.fetch_one("SELECT COUNT(*) as count FROM Provider")['count']
        stats['total_appointments'] = db.fetch_one("SELECT COUNT(*) as count FROM Appointment")['count']
        stats['total_medical_records'] = db.fetch_one("SELECT COUNT(*) as count FROM Medical_Record")['count']
        stats['total_payments'] = db.fetch_one("SELECT COUNT(*) as count FROM Payment")['count']
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
