# Bright Smile Dental Systems - Database Specification

## 1. Introduction

This document provides a comprehensive specification of the database structure for the Bright Smile Dental Systems. It includes details on all tables, their fields, relationships, and constraints.

## 2. Table Specifications

### 2.1 Clinic

Stores information about dental clinics.

| Field        | Type         | Constraints                 | Description                       |
| ------------ | ------------ | --------------------------- | --------------------------------- |
| id           | Integer      | Primary Key, Auto-increment | Unique identifier for the clinic  |
| name         | Varchar(100) | Not Null                    | Name of the clinic                |
| address      | Text         | Not Null                    | Full address of the clinic        |
| city         | Varchar(50)  | Not Null                    | City where the clinic is located  |
| state        | Varchar(50)  | Not Null                    | State where the clinic is located |
| phone_number | Varchar(20)  | Not Null                    | Contact number for the clinic     |
| email        | Email        | Not Null                    | Email address for the clinic      |

### 2.2 Doctor

Stores information about doctors.

| Field        | Type         | Constraints                 | Description                      |
| ------------ | ------------ | --------------------------- | -------------------------------- |
| id           | Integer      | Primary Key, Auto-increment | Unique identifier for the doctor |
| npi          | Varchar(10)  | Unique, Not Null            | National Provider Identifier     |
| name         | Varchar(100) | Not Null                    | Name of the doctor               |
| email        | Email        | Not Null                    | Email address of the doctor      |
| phone_number | Varchar(20)  | Not Null                    | Contact number for the doctor    |

### 2.3 Patient

Stores information about patients.

| Field         | Type         | Constraints                 | Description                       |
| ------------- | ------------ | --------------------------- | --------------------------------- |
| id            | Integer      | Primary Key, Auto-increment | Unique identifier for the patient |
| name          | Varchar(100) | Not Null                    | Name of the patient               |
| address       | Text         | Not Null                    | Full address of the patient       |
| phone_number  | Varchar(20)  | Not Null                    | Contact number for the patient    |
| date_of_birth | Date         | Not Null                    | Patient's date of birth           |
| ssn_last_4    | Varchar(4)   | Not Null                    | Last 4 digits of SSN              |
| gender        | Varchar(1)   | Not Null, Check (M/F/O)     | Patient's gender                  |

### 2.4 Procedure

Stores information about dental procedures.

| Field            | Type         | Constraints                 | Description                          |
| ---------------- | ------------ | --------------------------- | ------------------------------------ |
| id               | Integer      | Primary Key, Auto-increment | Unique identifier for the procedure  |
| name             | Varchar(100) | Unique, Not Null            | Name of the procedure                |
| description      | Text         | Not Null                    | Description of the procedure         |
| duration_minutes | Integer      | Not Null, Positive          | Duration of the procedure in minutes |

### 2.5 Visit

Stores information about patient visits.

| Field        | Type    | Constraints                 | Description                     |
| ------------ | ------- | --------------------------- | ------------------------------- |
| id           | Integer | Primary Key, Auto-increment | Unique identifier for the visit |
| patient_id   | Integer | Foreign Key (Patient)       | Reference to the patient        |
| doctor_id    | Integer | Foreign Key (Doctor)        | Reference to the doctor         |
| clinic_id    | Integer | Foreign Key (Clinic)        | Reference to the clinic         |
| date         | Date    | Not Null                    | Date of the visit               |
| time         | Time    | Not Null                    | Time of the visit               |
| doctor_notes | Text    | Nullable                    | Notes from the doctor           |

### 2.6 Appointment

Stores information about scheduled appointments.

| Field       | Type     | Constraints                 | Description                           |
| ----------- | -------- | --------------------------- | ------------------------------------- |
| id          | Integer  | Primary Key, Auto-increment | Unique identifier for the appointment |
| patient_id  | Integer  | Foreign Key (Patient)       | Reference to the patient              |
| doctor_id   | Integer  | Foreign Key (Doctor)        | Reference to the doctor               |
| clinic_id   | Integer  | Foreign Key (Clinic)        | Reference to the clinic               |
| date        | Date     | Not Null                    | Date of the appointment               |
| time        | Time     | Not Null                    | Time of the appointment               |
| date_booked | DateTime | Not Null, Auto-now-add      | When the appointment was booked       |

### 2.7 DoctorClinicAffiliation

Represents the affiliation between doctors and clinics.

| Field            | Type    | Constraints                 | Description                             |
| ---------------- | ------- | --------------------------- | --------------------------------------- |
| id               | Integer | Primary Key, Auto-increment | Unique identifier for the affiliation   |
| doctor_id        | Integer | Foreign Key (Doctor)        | Reference to the doctor                 |
| clinic_id        | Integer | Foreign Key (Clinic)        | Reference to the clinic                 |
| office_address   | Text    | Not Null                    | Doctor's office address at the clinic   |
| working_schedule | Text    | Nullable                    | Doctor's working schedule at the clinic |

### 2.8 PatientClinicAffiliation

Represents the affiliation between patients and clinics.

| Field      | Type    | Constraints                 | Description                           |
| ---------- | ------- | --------------------------- | ------------------------------------- |
| id         | Integer | Primary Key, Auto-increment | Unique identifier for the affiliation |
| patient_id | Integer | Foreign Key (Patient)       | Reference to the patient              |
| clinic_id  | Integer | Foreign Key (Clinic)        | Reference to the clinic               |

### 2.9 PatientDoctorAffiliation

Represents the affiliation between patients and doctors.

| Field      | Type    | Constraints                 | Description                           |
| ---------- | ------- | --------------------------- | ------------------------------------- |
| id         | Integer | Primary Key, Auto-increment | Unique identifier for the affiliation |
| patient_id | Integer | Foreign Key (Patient)       | Reference to the patient              |
| doctor_id  | Integer | Foreign Key (Doctor)        | Reference to the doctor               |

### 2.10 DoctorProcedure

Represents the procedures a doctor can perform.

| Field        | Type    | Constraints                 | Description                     |
| ------------ | ------- | --------------------------- | ------------------------------- |
| id           | Integer | Primary Key, Auto-increment | Unique identifier for the entry |
| doctor_id    | Integer | Foreign Key (Doctor)        | Reference to the doctor         |
| procedure_id | Integer | Foreign Key (Procedure)     | Reference to the procedure      |

### 2.11 ClinicProcedure

Represents the procedures offered at a clinic.

| Field        | Type    | Constraints                 | Description                     |
| ------------ | ------- | --------------------------- | ------------------------------- |
| id           | Integer | Primary Key, Auto-increment | Unique identifier for the entry |
| clinic_id    | Integer | Foreign Key (Clinic)        | Reference to the clinic         |
| procedure_id | Integer | Foreign Key (Procedure)     | Reference to the procedure      |

### 2.12 VisitProcedure

Represents the procedures performed during a visit.

| Field        | Type    | Constraints                 | Description                     |
| ------------ | ------- | --------------------------- | ------------------------------- |
| id           | Integer | Primary Key, Auto-increment | Unique identifier for the entry |
| visit_id     | Integer | Foreign Key (Visit)         | Reference to the visit          |
| procedure_id | Integer | Foreign Key (Procedure)     | Reference to the procedure      |

### 2.13 AppointmentProcedure

Represents the procedures scheduled for an appointment.

| Field          | Type    | Constraints                 | Description                     |
| -------------- | ------- | --------------------------- | ------------------------------- |
| id             | Integer | Primary Key, Auto-increment | Unique identifier for the entry |
| appointment_id | Integer | Foreign Key (Appointment)   | Reference to the appointment    |
| procedure_id   | Integer | Foreign Key (Procedure)     | Reference to the procedure      |

## 3. Relationships and Constraints

1. A Clinic can have multiple Doctors (through DoctorClinicAffiliation)
2. A Clinic can have multiple Patients (through PatientClinicAffiliation)
3. A Clinic can offer multiple Procedures (through ClinicProcedure)
4. A Doctor can work at multiple Clinics (through DoctorClinicAffiliation)
5. A Doctor can have multiple Patients (through PatientDoctorAffiliation)
6. A Doctor can perform multiple Procedures (through DoctorProcedure)
7. A Patient can be affiliated with multiple Clinics (through PatientClinicAffiliation)
8. A Patient can be affiliated with multiple Doctors (through PatientDoctorAffiliation)
9. A Patient can have multiple Visits and Appointments
10. A Visit is associated with one Patient, one Doctor, and one Clinic
11. An Appointment is associated with one Patient, one Doctor, and one Clinic
12. A Visit can involve multiple Procedures (through VisitProcedure)
13. An Appointment can involve multiple Procedures (through AppointmentProcedure)

## 4. Indexes

To optimize query performance, we can consider adding indexes on:

- Clinic: name, city, state
- Doctor: npi, name
- Patient: name, date_of_birth
- Procedure: name
- Visit: date, patient_id, doctor_id, clinic_id
- Appointment: date, patient_id, doctor_id, clinic_id

## 5. Data Integrity

- Using foreign key constraints to maintain referential integrity between related tables.
- Implementing appropriate CHECK constraints (e.g., for gender in the Patient table).
- Using UNIQUE constraints where appropriate (e.g., Doctor's NPI, Procedure name).
- Implementing proper validation at the application level to ensure data quality and consistency.

This database specification provides a comprehensive structure for the Bright Smile Dental Systems, allowing for efficient management of clinics, doctors, patients, procedures, visits, and appointments.
