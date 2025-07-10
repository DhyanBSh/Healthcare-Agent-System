from mesa import Model
from mesa.time import RandomActivation
from rdflib import Graph, Namespace
import random
from .agents import PatientAgent, DoctorAgent, NurseAgent, WardAgent


class HealthcareModel(Model):
    """A healthcare model with patients, doctors, nurses, and wards."""
    def __init__(self, num_doctors, num_nurses, num_wards):
        self.schedule = RandomActivation(self)

        # Add doctors
        self.doctors = []
        for i in range(num_doctors):
            doctor = DoctorAgent(i, self, name=f"Doctor {i}")
            self.schedule.add(doctor)
            self.doctors.append(doctor)

        # Add nurses
        self.nurses = []
        for i in range(num_nurses):
            nurse = NurseAgent(i + num_doctors, self, name=f"Nurse {i}")
            self.schedule.add(nurse)
            self.nurses.append(nurse)

        # Add wards
        self.wards = []
        for i in range(num_wards):
            ward = WardAgent(i + num_doctors + num_nurses, self, name=f"Ward {i}")
            self.schedule.add(ward)
            self.wards.append(ward)

        self.patient_counter = num_doctors + num_nurses + num_wards

    def step(self):
        """Advance the model by one step."""
        disease = random.choice(["Disease1", "Disease2", "Disease3", "Disease4"])
        patient = PatientAgent(self.patient_counter, self, disease)
        self.patient_counter += 1
        self.schedule.add(patient)

        # Assign doctors, nurses, and wards
        doctor = random.choice(self.doctors)
        nurse = random.choice(self.nurses)
        ward = random.choice(self.wards)

        # Assign each agent (doctor, nurse, ward) to the patient
        doctor.assign_patient(patient)
        nurse.assign_patient(patient)
        ward.assign_patient(patient)

        print(f"\nNew Patient {patient.unique_id} arrives with disease: {disease}")
        self.schedule.step()

