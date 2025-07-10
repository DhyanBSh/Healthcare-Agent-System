from mesa import Agent
from rdflib import Graph, Namespace


ontology_file = "ontology/healthcareonto.rdf"
ontology = Graph()
try:
    ontology.parse(ontology_file, format="xml")
except Exception as e:
    print(f"Error loading ontology file: {e}")
    exit(1) 


HEALTH = Namespace("http://www.semanticweb.org/hansa/ontologies/2024/11/untitled-ontology-15/")


class PatientAgent(Agent):
    """Represents a patient with a disease."""
    def __init__(self, unique_id, model, disease):
        super().__init__(unique_id, model)
        self.disease = disease
        self.treatment = None  
        self.doctor = None     
        self.nurse = None     
        self.ward = None      

    def assign_treatment(self):
        """Retrieve treatment for the patient's disease from the ontology."""
        print(f"Searching for treatment for disease: {self.disease}")
        try:
            treatment_query = f"""
            SELECT ?treatment
            WHERE {{
                ?disease <http://www.semanticweb.org/hansa/ontologies/2024/11/untitled-ontology-15#hasTreatment> ?treatment .
                FILTER (?disease = <http://www.semanticweb.org/hansa/ontologies/2024/11/untitled-ontology-15#{self.disease}>)
            }}
            """
            treatment_results = list(ontology.query(treatment_query))
            if treatment_results:
                self.treatment = str(treatment_results[0][0].split("#")[-1])
            else:
                self.treatment = "No treatment found in ontology"
        except Exception as e:
            print(f"Error retrieving treatment for patient {self.unique_id}: {e}")

    def assign_doctor(self):
        """Assign a doctor to the patient based on the ontology."""
        try:
            doctor_query = f"""
            SELECT ?doctor
            WHERE {{
                ?treatment rdf:type <http://www.semanticweb.org/hansa/ontologies/2024/11/untitled-ontology-15#Treatment> .
                ?treatment <http://www.semanticweb.org/hansa/ontologies/2024/11/untitled-ontology-15#assignto> ?doctor .
                FILTER (?treatment = <http://www.semanticweb.org/hansa/ontologies/2024/11/untitled-ontology-15#{self.treatment}>)
            }}
            """
            doctor_results = list(ontology.query(doctor_query))
            if doctor_results:
                self.doctor = str(doctor_results[0][0].split("#")[-1])
            else:
                self.doctor = "No doctor found in ontology"
        except Exception as e:
            print(f"Error retrieving doctor for patient {self.unique_id}: {e}")

    def assign_nurse(self):
        """Assign a nurse to the patient based on the ontology."""
        try:
            nurse_query = f"""
            SELECT ?nurse
            WHERE {{
                ?nurse rdf:type <http://www.semanticweb.org/hansa/ontologies/2024/11/untitled-ontology-15#Nurse> .
                ?doctor<http://www.semanticweb.org/hansa/ontologies/2024/11/untitled-ontology-15#hasNurse> ?nurse . 
                FILTER (?doctor = <http://www.semanticweb.org/hansa/ontologies/2024/11/untitled-ontology-15#{self.doctor}>)
            }}
            """
            nurse_results = list(ontology.query(nurse_query))
            if nurse_results:
                self.nurse = str(nurse_results[0][0].split("#")[-1])
            else:
                self.nurse = "No nurse found in ontology"
        except Exception as e:
            print(f"Error retrieving nurse for patient {self.unique_id}: {e}")

    def assign_ward(self):
        """Assign a ward to the patient based on the ontology."""
        try:
            ward_query = f"""
            SELECT ?ward
            WHERE {{
                ?disease <http://www.semanticweb.org/hansa/ontologies/2024/11/untitled-ontology-15#hasward> ?ward .
                FILTER (?disease = <http://www.semanticweb.org/hansa/ontologies/2024/11/untitled-ontology-15#{self.disease}>)
            }}
            """
            ward_results = list(ontology.query(ward_query))
            if ward_results:
                self.ward = str(ward_results[0][0].split("#")[-1])
            else:
                self.ward = "No ward found in ontology"
        except Exception as e:
            print(f"Error retrieving ward for patient {self.unique_id}: {e}")

    def step(self):
        """Simulate the patient's step in the environment."""
        try:
            self.assign_treatment()
            self.assign_doctor()
            self.assign_nurse()
            self.assign_ward()
            print(f"Patient {self.unique_id} treated for {self.disease}:")
            print(f"  - Treatment: {self.treatment}")
            print(f"  - Doctor: {self.doctor}")
            print(f"  - Nurse: {self.nurse}")
            print(f"  - Ward: {self.ward}")
        except Exception as e:
            print(f"Error in step for patient {self.unique_id}: {e}")


class DoctorAgent(Agent):
    """Represents a doctor."""
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model)
        self.name = name

    def assign_patient(self, patient):
        """Assign a patient to the doctor based on ontology."""
        patient.assign_doctor()



class NurseAgent(Agent):
    """Represents a nurse."""
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model)
        self.name = name

    def assign_patient(self, patient):
        """Assign a nurse to the patient based on ontology."""
        patient.assign_nurse()


class WardAgent(Agent):
    """Represents a ward in the hospital."""
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model)
        self.name = name

    def assign_patient(self, patient):
        """Assign a ward to the patient based on ontology."""
        patient.assign_ward()