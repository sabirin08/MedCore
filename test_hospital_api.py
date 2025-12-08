import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def print_response(title, response):
    """Helper function to print API responses"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_health_check():
    """Test API health check"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200

def test_patient_operations():
    """Test all patient CRUD operations"""
    print("\n" + "="*60)
    print("TESTING PATIENT OPERATIONS")
    print("="*60)
    
    # CREATE - Add new patient
    new_patient = {
        "First_name": "Test",
        "Last_name": "Patient",
        "DOB": "1990-01-01",
        "Gender": "Other",
        "Phone_Number": "555-9999",
        "Address": "999 Test St, Test City, TS 99999"
    }
    response = requests.post(f"{BASE_URL}/patients", json=new_patient)
    print_response("CREATE Patient", response)
    patient_id = response.json().get('patient_id') if response.status_code == 201 else 1
    
    # READ - Get all patients
    response = requests.get(f"{BASE_URL}/patients")
    print_response("READ All Patients", response)
    
    # READ - Get specific patient
    response = requests.get(f"{BASE_URL}/patients/{patient_id}")
    print_response(f"READ Patient ID {patient_id}", response)
    
    # UPDATE - Update patient
    updated_patient = {
        "First_name": "Updated",
        "Last_name": "Patient",
        "DOB": "1990-01-01",
        "Gender": "Other",
        "Phone_Number": "555-8888",
        "Address": "888 Updated St, Test City, TS 88888"
    }
    response = requests.put(f"{BASE_URL}/patients/{patient_id}", json=updated_patient)
    print_response(f"UPDATE Patient ID {patient_id}", response)
    
    # Get patient medical history
    response = requests.get(f"{BASE_URL}/patients/{patient_id}/medical-history")
    print_response(f"GET Patient Medical History", response)
    
    return patient_id

def test_provider_operations():
    """Test all provider CRUD operations"""
    print("\n" + "="*60)
    print("TESTING PROVIDER OPERATIONS")
    print("="*60)
    
    # CREATE - Add new provider
    new_provider = {
        "First_name": "Dr. Test",
        "Last_name": "Provider",
        "Department": "Test Department",
        "Specialty": "Test Specialist",
        "Phone_Number": "555-7777",
        "Email": "test.provider@hospital.com"
    }
    response = requests.post(f"{BASE_URL}/providers", json=new_provider)
    print_response("CREATE Provider", response)
    provider_id = response.json().get('provider_id') if response.status_code == 201 else 1
    
    # READ - Get all providers
    response = requests.get(f"{BASE_URL}/providers")
    print_response("READ All Providers", response)
    
    # READ - Get specific provider
    response = requests.get(f"{BASE_URL}/providers/{provider_id}")
    print_response(f"READ Provider ID {provider_id}", response)
    
    # UPDATE - Update provider
    updated_provider = {
        "First_name": "Dr. Updated",
        "Last_name": "Provider",
        "Department": "Updated Department",
        "Specialty": "Updated Specialist",
        "Phone_Number": "555-6666",
        "Email": "updated.provider@hospital.com"
    }
    response = requests.put(f"{BASE_URL}/providers/{provider_id}", json=updated_provider)
    print_response(f"UPDATE Provider ID {provider_id}", response)
    
    # Get provider schedule
    response = requests.get(f"{BASE_URL}/providers/{provider_id}/schedule")
    print_response(f"GET Provider Schedule", response)
    
    return provider_id

def test_medical_record_operations(patient_id, provider_id):
    """Test all medical record CRUD operations"""
    print("\n" + "="*60)
    print("TESTING MEDICAL RECORD OPERATIONS")
    print("="*60)
    
    # CREATE - Add new medical record
    new_record = {
        "Patient_id": patient_id,
        "Provider_id": provider_id,
        "Diagnosis": "Test Diagnosis",
        "Treatment": "Test Treatment Plan",
        "Prescription": "Test Medication"
    }
    response = requests.post(f"{BASE_URL}/medical-records", json=new_record)
    print_response("CREATE Medical Record", response)
    record_id = response.json().get('record_id') if response.status_code == 201 else 1
    
    # READ - Get all medical records
    response = requests.get(f"{BASE_URL}/medical-records")
    print_response("READ All Medical Records", response)
    
    # READ - Get specific medical record
    response = requests.get(f"{BASE_URL}/medical-records/{record_id}")
    print_response(f"READ Medical Record ID {record_id}", response)
    
    # UPDATE - Update medical record
    updated_record = {
        "Patient_id": patient_id,
        "Provider_id": provider_id,
        "Diagnosis": "Updated Diagnosis",
        "Treatment": "Updated Treatment Plan",
        "Prescription": "Updated Medication"
    }
    response = requests.put(f"{BASE_URL}/medical-records/{record_id}", json=updated_record)
    print_response(f"UPDATE Medical Record ID {record_id}", response)
    

def test_stats():
    """Test database statistics endpoint"""
    response = requests.get(f"{BASE_URL}/stats")
    print_response("Database Statistics", response)

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("HOSPITAL MANAGEMENT SYSTEM API TESTS")
    print("="*60)
    
    # Check if API is running
    if not test_health_check():
        print("\nERROR: API is not running. Please start the Flask server first.")
        print("Run: python app.py")
        return
    
    # Test all operations
    patient_id = test_patient_operations()
    provider_id = test_provider_operations()
    test_medical_record_operations(patient_id, provider_id)
    test_stats()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)

if __name__ == "__main__":
    main()
