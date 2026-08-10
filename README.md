# hospital-management-system-dbms
# Hospital Management System

## About the Project

The Hospital Management System is a database management project designed to manage hospital-related information efficiently. The system stores and organizes patient, doctor, department, appointment, treatment, medicine, prescription, and billing information.

## Problem Statement

Managing hospital records manually can lead to data duplication, errors, and difficulty in retrieving information. This project provides a centralized relational database to store and manage hospital information efficiently.

## Objectives

- To maintain patient records.
- To manage doctor and department information.
- To schedule and manage appointments.
- To store patient treatment and diagnosis details.
- To manage medicines and prescriptions.
- To maintain patient billing information.
- To reduce data duplication and improve data management.
- To provide efficient access to hospital records.

## Entities

The database contains the following entities:

1. Patient
2. Doctor
3. Department
4. Appointment
5. Treatment
6. Medicine
7. Prescription
8. Bill

## Entity Relationships

| Entity 1 | Entity 2 | Relationship |
|---|---|---|
| Patient | Appointment | One-to-Many |
| Doctor | Appointment | One-to-Many |
| Department | Doctor | One-to-Many |
| Patient | Treatment | One-to-Many |
| Doctor | Treatment | One-to-Many |
| Patient | Bill | One-to-Many |
| Doctor | Prescription | One-to-Many |
| Medicine | Prescription | One-to-Many |
| Patient | Doctor | Many-to-Many |

## Database Schema

```text
PATIENT(Patient_ID PK, Name, DOB, Gender, Phone, Address, Blood_Group)

DEPARTMENT(Department_ID PK, Department_Name, Location)

DOCTOR(Doctor_ID PK, Name, Specialization, Phone, Email, Department_ID FK)

APPOINTMENT(Appointment_ID PK, Patient_ID FK, Doctor_ID FK, Appointment_Date, Appointment_Time, Status)

TREATMENT(Treatment_ID PK, Patient_ID FK, Doctor_ID FK, Diagnosis, Treatment_Details, Treatment_Date)

MEDICINE(Medicine_ID PK, Medicine_Name, Category, Quantity, Price)

PRESCRIPTION(Prescription_ID PK, Patient_ID FK, Doctor_ID FK, Medicine_ID FK, Dosage, Duration)

BILL(Bill_ID PK, Patient_ID FK, Bill_Date, Consultation_Fee, Medicine_Charge, Total_Amount, Payment_Status)
