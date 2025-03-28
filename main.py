from src.IMSS import IMSS

def main():
    print("=== IMSS Simulator ===")
    display_menu()

def display_menu():
    while True:
        print("\nMain Menu:")
        print("1. View Patient Information")
        print("2. View Medical Records")
        print("3. View Appointments")
        print("4. Calculate IMSS Quotas")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ")
        
        if choice == "1":
            display_patient_info()
        elif choice == "2":
            display_medical_records()
        elif choice == "3":
            display_appointments()
        elif choice == "4":
            calculate_imss_quotas()
        elif choice == "5":
            print("Thank you for using IMSS Simulator!")
            break
        else:
            print("Invalid option. Please try again.")

def calculate_imss_quotas():
    try:
        salary = float(input("\nEnter total salary: "))
        imss = IMSS(salary)
        
        print("\n=== IMSS Calculations ===")
        print(f"Salario diario: ${imss.employee.calculate_salary_dialy():.2f}")
        print(f"Salario diario integrado: ${imss.get_integrated_daily_wage():.2f}")
        print(f"Cuota del patrón (Enfermedades y maternidad): ${imss.get_diseases_and_maternity_employer_quota():.2f}")
    except ValueError:
        print("Please enter a valid number for salary")

def display_patient_info():
    print("\n=== Patient Information ===")
    print("Name: John Doe")
    print("Age: 35")
    print("NSS: 12345678901")
    print("Clinic: UMF 123")

def display_medical_records():
    print("\n=== Medical Records ===")
    print("Last Visit: 2023-10-15")
    print("Diagnosis: General checkup")
    print("Medications: None")

def display_appointments():
    print("\n=== Appointments ===")
    print("Next appointment: 2023-11-01")
    print("Time: 10:00 AM")
    print("Doctor: Dr. García")
    print("Department: General Medicine")

if __name__ == "__main__":
    main()