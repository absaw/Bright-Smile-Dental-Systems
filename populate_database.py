import os
import django
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bright_smile.settings")
django.setup()

from clinics.models import Clinic
from doctors.models import Doctor
from patients.models import Patient
from procedures.models import Procedure

def clear_data():
    Clinic.objects.all().delete()
    Doctor.objects.all().delete()
    Patient.objects.all().delete()
    Procedure.objects.all().delete()
    print("All existing data cleared.")

@transaction.atomic
def populate_data():
    # Create Clinics
    clinics = [
        Clinic(name="New Brunswick Dental Center", address="123 George St", city="New Brunswick", state="NJ", phone_number="732-555-1234", email="info@nbdc.com"),
        Clinic(name="Highland Park Smile Studio", address="456 Raritan Ave", city="Highland Park", state="NJ", phone_number="732-555-5678", email="info@hpss.com"),
        Clinic(name="Edison Family Dentistry", address="789 Oak Tree Rd", city="Edison", state="NJ", phone_number="732-555-9012", email="info@edisonfamily.com"),
    ]
    Clinic.objects.bulk_create(clinics)
    print(f"{len(clinics)} clinics created.")

    # Create Doctors
    doctors = [
        Doctor(npi="1234567890", name="Dr. John Smith", email="john.smith@brightsmiledental.com", phone_number="732-555-2345"),
        Doctor(npi="2345678901", name="Dr. Emily Johnson", email="emily.johnson@brightsmiledental.com", phone_number="732-555-3456"),
        Doctor(npi="3456789012", name="Dr. Michael Lee", email="michael.lee@brightsmiledental.com", phone_number="732-555-4567"),
    ]
    Doctor.objects.bulk_create(doctors)
    print(f"{len(doctors)} doctors created.")

    # Create Patients
    patients = [
        Patient(name="Alice Brown", address="10 College Ave, New Brunswick, NJ", phone_number="732-555-7890", date_of_birth=timezone.now() - timedelta(days=10950), ssn_last_4="1234", gender="F"),
        Patient(name="Bob Wilson", address="20 Easton Ave, New Brunswick, NJ", phone_number="732-555-8901", date_of_birth=timezone.now() - timedelta(days=14600), ssn_last_4="5678", gender="M"),
        Patient(name="Carol Davis", address="30 Hamilton St, New Brunswick, NJ", phone_number="732-555-9012", date_of_birth=timezone.now() - timedelta(days=18250), ssn_last_4="9012", gender="F"),
        Patient(name="David Miller", address="40 Somerset St, New Brunswick, NJ", phone_number="732-555-0123", date_of_birth=timezone.now() - timedelta(days=21900), ssn_last_4="3456", gender="M"),
    ]
    Patient.objects.bulk_create(patients)
    print(f"{len(patients)} patients created.")

    # Create Procedures
    procedures = [
        Procedure(name="Cleaning", description="Standard dental cleaning", duration_minutes=30),
        Procedure(name="Filling", description="Dental filling procedure", duration_minutes=60),
        Procedure(name="Root Canal", description="Root canal treatment", duration_minutes=90),
        Procedure(name="Crown", description="Dental crown placement", duration_minutes=60),
        Procedure(name="Teeth Whitening", description="Professional teeth whitening", duration_minutes=45),
    ]
    Procedure.objects.bulk_create(procedures)
    print(f"{len(procedures)} procedures created.")

def run_population_script():
    # clear_data()
    populate_data()
    print("Database population completed successfully!")

if __name__ == "__main__":
    run_population_script()