from django.utils import timezone
from clinics.models import Clinic, PatientClinicAffiliation, ClinicProcedure
from doctors.models import Doctor, DoctorClinicAffiliation, PatientDoctorAffiliation, DoctorProcedure
from patients.models import Patient
from procedures.models import Procedure
from appointments.models import Appointment, AppointmentProcedure, Visit, VisitProcedure

def run():
    # Create Procedures
    procedures = [
        Procedure.objects.create(name="Cleaning", description="Regular dental cleaning", duration_minutes=30),
        Procedure.objects.create(name="Filling", description="Dental filling procedure", duration_minutes=45),
        Procedure.objects.create(name="Root Canal", description="Root canal treatment", duration_minutes=90),
        Procedure.objects.create(name="Crown", description="Dental crown installation", duration_minutes=60),
        Procedure.objects.create(name="Teeth Whitening", description="Professional teeth whitening", duration_minutes=60),
    ]

    # Create Clinics
    clinics = [
        Clinic.objects.create(name="Bright Smile New Brunswick", address="123 George St", city="New Brunswick", state="NJ", phone_number="7321234567", email="newbrunswick@brightsmile.com"),
        Clinic.objects.create(name="Bright Smile Edison", address="456 Oak Tree Rd", city="Edison", state="NJ", phone_number="7329876543", email="edison@brightsmile.com"),
        Clinic.objects.create(name="Bright Smile Piscataway", address="789 Centennial Ave", city="Piscataway", state="NJ", phone_number="7328765432", email="piscataway@brightsmile.com"),
        Clinic.objects.create(name="Bright Smile Highland Park", address="321 Raritan Ave", city="Highland Park", state="NJ", phone_number="7323456789", email="highlandpark@brightsmile.com"),
        Clinic.objects.create(name="Bright Smile Somerset", address="654 Easton Ave", city="Somerset", state="NJ", phone_number="7325678901", email="somerset@brightsmile.com"),
    ]

    # Create Doctors
    doctors = [
        Doctor.objects.create(npi="1234567890", name="Dr. John Smith", email="jsmith@brightsmile.com", phone_number="7321112222"),
        Doctor.objects.create(npi="2345678901", name="Dr. Emily Johnson", email="ejohnson@brightsmile.com", phone_number="7322223333"),
        Doctor.objects.create(npi="3456789012", name="Dr. Michael Brown", email="mbrown@brightsmile.com", phone_number="7323334444"),
        Doctor.objects.create(npi="4567890123", name="Dr. Sarah Davis", email="sdavis@brightsmile.com", phone_number="7324445555"),
        Doctor.objects.create(npi="5678901234", name="Dr. David Wilson", email="dwilson@brightsmile.com", phone_number="7325556666"),
        Doctor.objects.create(npi="6789012345", name="Dr. Lisa Anderson", email="landerson@brightsmile.com", phone_number="7326667777"),
        Doctor.objects.create(npi="7890123456", name="Dr. Robert Taylor", email="rtaylor@brightsmile.com", phone_number="7327778888"),
        Doctor.objects.create(npi="8901234567", name="Dr. Jennifer Martinez", email="jmartinez@brightsmile.com", phone_number="7328889999"),
        Doctor.objects.create(npi="9012345678", name="Dr. William Lee", email="wlee@brightsmile.com", phone_number="7329990000"),
        Doctor.objects.create(npi="0123456789", name="Dr. Karen White", email="kwhite@brightsmile.com", phone_number="7320001111"),
    ]

    # Create Patients
    patients = [
        Patient.objects.create(name="Alice Johnson", address="10 College Ave, New Brunswick, NJ", phone_number="7329876543", date_of_birth="1985-03-15", ssn_last_4="1234", gender="F"),
        Patient.objects.create(name="Bob Williams", address="20 Easton Ave, New Brunswick, NJ", phone_number="7321234567", date_of_birth="1990-07-22", ssn_last_4="5678", gender="M"),
        Patient.objects.create(name="Carol Brown", address="30 George St, New Brunswick, NJ", phone_number="7325678901", date_of_birth="1978-11-30", ssn_last_4="9012", gender="F"),
        Patient.objects.create(name="David Miller", address="40 Hamilton St, New Brunswick, NJ", phone_number="7328901234", date_of_birth="1995-01-05", ssn_last_4="3456", gender="M"),
        Patient.objects.create(name="Eva Davis", address="50 Louis St, New Brunswick, NJ", phone_number="7322345678", date_of_birth="1988-09-18", ssn_last_4="7890", gender="F"),
        Patient.objects.create(name="Frank Wilson", address="60 Neilson St, New Brunswick, NJ", phone_number="7326789012", date_of_birth="1982-06-25", ssn_last_4="2345", gender="M"),
        Patient.objects.create(name="Grace Taylor", address="70 Paterson St, New Brunswick, NJ", phone_number="7320123456", date_of_birth="1992-12-10", ssn_last_4="6789", gender="F"),
        Patient.objects.create(name="Henry Anderson", address="80 Somerset St, New Brunswick, NJ", phone_number="7323456789", date_of_birth="1975-04-03", ssn_last_4="0123", gender="M"),
        Patient.objects.create(name="Ivy Martinez", address="90 Spring St, New Brunswick, NJ", phone_number="7327890123", date_of_birth="1998-08-20", ssn_last_4="4567", gender="F"),
        Patient.objects.create(name="Jack Lee", address="100 Stone St, New Brunswick, NJ", phone_number="7321567890", date_of_birth="1987-02-14", ssn_last_4="8901", gender="M"),
    ]

    # Create Affiliations and Appointments
    for i, doctor in enumerate(doctors):
        # Affiliate doctor with clinic
        clinic = clinics[i % len(clinics)]
        DoctorClinicAffiliation.objects.create(
            doctor=doctor,
            clinic=clinic,
            office_address=clinic.address,
            working_schedule="Monday to Friday, 9 AM to 5 PM"
        )

        # Affiliate doctor with procedures
        for procedure in procedures:
            DoctorProcedure.objects.create(doctor=doctor, procedure=procedure)

        # Affiliate clinic with procedures
        for procedure in procedures:
            ClinicProcedure.objects.create(clinic=clinic, procedure=procedure)

        # Create patient affiliations and appointments
        for j in range(3):  # Each doctor gets 3 patients
            patient = patients[(i * 3 + j) % len(patients)]
            PatientDoctorAffiliation.objects.create(patient=patient, doctor=doctor)
            PatientClinicAffiliation.objects.create(patient=patient, clinic=clinic)

            # Create an appointment
            appointment_date = timezone.now().date() + timezone.timedelta(days=j+1)
            appointment_time = timezone.now().time().replace(hour=9+j, minute=0, second=0, microsecond=0)
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                clinic=clinic,
                date=appointment_date,
                time=appointment_time
            )
            AppointmentProcedure.objects.create(appointment=appointment, procedure=procedures[j % len(procedures)])

            # Create a past visit
            visit_date = timezone.now().date() - timezone.timedelta(days=30+j)
            visit_time = timezone.now().time().replace(hour=14+j, minute=0, second=0, microsecond=0)
            visit = Visit.objects.create(
                patient=patient,
                doctor=doctor,
                clinic=clinic,
                date=visit_date,
                time=visit_time,
                doctor_notes=f"Regular checkup for {patient.name}"
            )
            VisitProcedure.objects.create(visit=visit, procedure=procedures[(j+1) % len(procedures)])

    print("Database populated successfully!")

if __name__ == "__main__":
    run()