# MedCore

**CSC 4710** — Database Systems, Fall 2025

---

## Overview

A hospital management database system built with Python, Flask, and MySQL. MedCore provides a RESTful API for managing patients, healthcare providers, medical records, appointments, and payments. Designed as a solo project for CSC 4710 to demonstrate relational database design, CRUD operations, and API development.

## Features

- **Patient Management** — Create, read, update, and delete patient records; retrieve full medical history per patient.
- **Provider Management** — Manage healthcare provider profiles with department and specialty info; view provider appointment schedules.
- **Medical Records** — Store diagnoses, treatments, and prescriptions linked to both patients and providers.
- **Appointment Scheduling** — Book, update, reschedule, and cancel appointments with status tracking.
- **Payment Processing** — Record and track payments tied to appointments; mark payments as paid; view all pending payments.
- **Database Statistics** — Utility endpoint returning counts across all tables.
- **Health Check** — API status and database connectivity check.

## Tech Stack

- **Language:** Python 3
- **Framework:** Flask + Flask-CORS
- **Database:** MySQL
- **Connector:** mysql-connector-python
- **Environment:** python-dotenv for configuration

## Project Structure

```
├── hospital_api.py                # Flask REST API with all route handlers
├── database.py                    # Database connection and query helper class
├── hospital_database_schema.sql   # Full schema with tables, indexes, and seed data
├── test_hospital_api.py           # API integration test script
├── ER_Diagram.png                 # Entity-Relationship diagram
├── .env                           # Environment variables (not committed)
└── README.md
```

## Database Schema

The database consists of five tables with foreign key relationships:

- **Patient** — patient_id, name, DOB, gender, phone, address
- **Provider** — provider_id, name, department, specialty, phone, email
- **Medical_Record** — record_id, patient_id (FK), provider_id (FK), diagnosis, treatment, prescription
- **Appointment** — appointment_number, patient_id (FK), provider_id (FK), date, status, notes
- **Payment** — payment_id, patient_id (FK), appointment_id (FK), amount, date, status

Indexes are included on patient name, provider specialty, appointment date, medical record patient, and payment status for query performance.

## Prerequisites

- Python 3.8+
- MySQL Server running on `localhost`
- pip

## Setup

1. **Clone the repo** and navigate into the project directory.

2. **Install dependencies:**

```bash
pip install flask flask-cors mysql-connector-python python-dotenv
```

3. **Create the database:**

```bash
mysql -u root -p < hospital_database_schema.sql
```

This creates the `hospital_management` database, all five tables, indexes, and inserts sample seed data (5 patients, 5 providers, 5 medical records, 5 appointments, and 5 payments).

4. **Configure environment variables** by creating a `.env` file in the project root:

```
DB_HOST=localhost
DB_NAME=hospital_management
DB_USER=root
DB_PASSWORD=your_password_here
```

5. **Start the API server:**

```bash
python hospital_api.py
```

The server will run at `http://localhost:5000`.

## API Endpoints

### Patients
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/patients` | Get all patients |
| GET | `/api/patients/<id>` | Get patient by ID |
| POST | `/api/patients` | Create new patient |
| PUT | `/api/patients/<id>` | Update patient |
| DELETE | `/api/patients/<id>` | Delete patient |
| GET | `/api/patients/<id>/medical-history` | Get patient's medical history |

### Providers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/providers` | Get all providers |
| GET | `/api/providers/<id>` | Get provider by ID |
| POST | `/api/providers` | Create new provider |
| PUT | `/api/providers/<id>` | Update provider |
| DELETE | `/api/providers/<id>` | Delete provider |
| GET | `/api/providers/<id>/schedule` | Get provider's schedule |

### Medical Records
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/medical-records` | Get all records |
| GET | `/api/medical-records/<id>` | Get record by ID |
| POST | `/api/medical-records` | Create new record |
| PUT | `/api/medical-records/<id>` | Update record |
| DELETE | `/api/medical-records/<id>` | Delete record |

### Appointments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/appointments` | Get all appointments |
| GET | `/api/appointments/<id>` | Get appointment by ID |
| POST | `/api/appointments` | Book new appointment |
| PUT | `/api/appointments/<id>` | Update appointment |
| DELETE | `/api/appointments/<id>` | Cancel appointment |
| PUT | `/api/appointments/<id>/reschedule` | Reschedule appointment |

### Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/payments` | Get all payments |
| GET | `/api/payments/<id>` | Get payment by ID |
| POST | `/api/payments` | Record new payment |
| PUT | `/api/payments/<id>` | Update payment |
| DELETE | `/api/payments/<id>` | Delete payment |
| PUT | `/api/payments/<id>/mark-paid` | Mark payment as paid |
| GET | `/api/payments/pending` | Get all pending payments |

### Utility
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | API health check |
| GET | `/api/stats` | Database statistics |

## Testing

Run the integration test suite with the API server running:

```bash
python test_hospital_api.py
```

The test script exercises CRUD operations across patients, providers, and medical records, and checks the stats endpoint.

## ER Diagram

See `ER_Diagram.png` for the full entity-relationship diagram showing all five tables and their relationships.
