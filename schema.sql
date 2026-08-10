-- Hospital Management System
-- Database Schema

CREATE DATABASE hospital_management;
USE hospital_management;

-- 1. Patient Table
CREATE TABLE Patient (
    Patient_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    DOB DATE,
    Gender VARCHAR(10),
    Phone VARCHAR(15),
    Address VARCHAR(200),
    Blood_Group VARCHAR(5)
);

-- 2. Department Table
CREATE TABLE Department (
    Department_ID INT PRIMARY KEY,
    Department_Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100)
);

-- 3. Doctor Table
CREATE TABLE Doctor (
    Doctor_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Specialization VARCHAR(100),
    Phone VARCHAR(15),
    Email VARCHAR(100),
    Department_ID INT,
    FOREIGN KEY (Department_ID)
        REFERENCES Department(Department_ID)
);

-- 4. Appointment Table
CREATE TABLE Appointment (
    Appointment_ID INT PRIMARY KEY,
    Patient_ID INT,
    Doctor_ID INT,
    Appointment_Date DATE,
    Appointment_Time TIME,
    Status VARCHAR(30),
    FOREIGN KEY (Patient_ID)
        REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Doctor_ID)
        REFERENCES Doctor(Doctor_ID)
);

-- 5. Treatment Table
CREATE TABLE Treatment (
    Treatment_ID INT PRIMARY KEY,
    Patient_ID INT,
    Doctor_ID INT,
    Diagnosis VARCHAR(200),
    Treatment_Details VARCHAR(500),
    Treatment_Date DATE,
    FOREIGN KEY (Patient_ID)
        REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Doctor_ID)
        REFERENCES Doctor(Doctor_ID)
);

-- 6. Medicine Table
CREATE TABLE Medicine (
    Medicine_ID INT PRIMARY KEY,
    Medicine_Name VARCHAR(100) NOT NULL,
    Category VARCHAR(100),
    Quantity INT,
    Price DECIMAL(10,2)
);

-- 7. Prescription Table
CREATE TABLE Prescription (
    Prescription_ID INT PRIMARY KEY,
    Patient_ID INT,
    Doctor_ID INT,
    Medicine_ID INT,
    Dosage VARCHAR(100),
    Duration VARCHAR(50),
    FOREIGN KEY (Patient_ID)
        REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Doctor_ID)
        REFERENCES Doctor(Doctor_ID),
    FOREIGN KEY (Medicine_ID)
        REFERENCES Medicine(Medicine_ID)
);

-- 8. Bill Table
CREATE TABLE Bill (
    Bill_ID INT PRIMARY KEY,
    Patient_ID INT,
    Bill_Date DATE,
    Consultation_Fee DECIMAL(10,2),
    Medicine_Charge DECIMAL(10,2),
    Total_Amount DECIMAL(10,2),
    Payment_Status VARCHAR(30),
    FOREIGN KEY (Patient_ID)
        REFERENCES Patient(Patient_ID)
);
