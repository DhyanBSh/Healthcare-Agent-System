import tkinter as tk
from models.agents import PatientAgent
from models.model import HealthcareModel



class HealthcareGUI:
    def __init__(self, root):
       
        self.model = HealthcareModel(num_doctors=3, num_nurses=2, num_wards=2)
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        """Setup the GUI layout."""
        self.root.title("Healthcare Simulation")
        self.root.geometry("700x600") 
        self.root.config(bg="#eaf0f3") 

        main_frame = tk.Frame(self.root, bg="#eaf0f3")
        main_frame.pack(pady=20, padx=20)
     
        header_label = tk.Label(main_frame, text="Healthcare Simulation", font=("Arial", 24, "bold"), bg="#eaf0f3", fg="#4a7c88")
        header_label.pack(pady=20)

        
        control_frame = tk.Frame(main_frame, bg="#eaf0f3")
        control_frame.pack(pady=20)

      
        self.run_button = tk.Button(control_frame, text="Run Step", command=self.run_step, width=20, height=2, 
                                    font=("Arial", 14), bg="#00b894", fg="white", relief="flat", bd=0, padx=10, pady=5)
        self.run_button.pack()

       
        self.run_button.bind("<Enter>", lambda e: self.run_button.config(bg="#00cec9"))
        self.run_button.bind("<Leave>", lambda e: self.run_button.config(bg="#00b894"))


        self.output = tk.Text(self.root, height=15, width=80, font=("Arial", 12), wrap=tk.WORD, bd=2, relief="solid", 
                              bg="#ffffff", fg="#333333", padx=10, pady=10)
        self.output.pack(padx=10, pady=20)


        self.status_label = tk.Label(main_frame, text="Ready to execute steps.", font=("Arial", 12), bg="#eaf0f3", fg="#95a5a6")
        self.status_label.pack(pady=10)


    def run_step(self):
        """Run a single step and display output."""
        self.model.step() 

     
        self.output.delete(1.0, tk.END)
        
       
        output_text = "\n".join(self.get_patient_outputs())
        self.output.insert(tk.END, f"{output_text}")

        self.status_label.config(text="Step executed successfully.")
        self.status_label.config(fg="#2ecc71")


    def get_patient_outputs(self):
        """Generate the output for each patient's current state."""
        outputs = []
    
        for patient in self.model.schedule.agents:
            if isinstance(patient, PatientAgent):
                patient_info = f"Patient {patient.unique_id} with disease {patient.disease}:\n"
                patient_info += f"  - Treatment: {patient.treatment}\n"
                patient_info += f"  - Doctor: {patient.doctor}\n"
                patient_info += f"  - Nurse: {patient.nurse}\n"
                patient_info += f"  - Ward: {patient.ward}\n"
                outputs.append(patient_info)
        
        return outputs

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthcareGUI(root)
    root.mainloop()
