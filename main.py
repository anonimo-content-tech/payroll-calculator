from src.imss import IMSS

def main():
    print("=== IMSS Simulator ===")
    display_menu()

def display_menu():
    while True:
        print("\nMain Menu:")
        print("1. Calculate IMSS Quotas")
        print("2. Exit")
        
        choice = input("\nSelect an option (1-2): ")
        
        if choice == "1":
            calculate_imss_quotas()
        elif choice == "2":
            print("Thank you for using IMSS Simulator!")
            break
        else:
            print("Invalid option. Please try again.")

def calculate_imss_quotas():
    try:
        salary = float(input("\nEnter total salary: "))
        risk_class = input("Enter risk class (I, II, III, IV, V) [default: I]: ") or 'I'
        imss = IMSS(salary, risk_class)
        
        print("\n=== IMSS Calculations ===")
        print(f"Salario diario: ${imss.employee.calculate_salary_dialy():.2f}")
        print(f"Salario diario integrado (Col. D): ${imss.get_integrated_daily_wage():.2f}")
        print(f"Salario tope 25 SMG (Col. G): ${imss.get_salary_cap_25_smg():.2f}")
        print(f"Salario tope 25 SMG TC2 (Col. Q): ${imss.get_salary_cap_25_smg_2():.2f}")
        print("\n=== Cuotas Patronales ===")
        print(f"Cuota del patrón (Enfermedades y maternidad) (Col. H): ${imss.get_diseases_and_maternity_employer_quota():.2f}")
        print(f"Excedente del patrón (Enfermedades y maternidad) (Col. I): ${imss.get_diseases_and_maternity_employer_surplus():.2f}")
        print(f"Prestaciones en dinero (Patrón) (Col. K): ${imss.get_employer_cash_benefits():.2f}")
        print(f"Prestaciones en especie (Gastos médicos patrón) (Col. M): ${imss.get_benefits_in_kind_medical_expenses_employer():.2f}")
        print(f"Riesgos de trabajo (Patrón) (Col. O): ${imss.get_occupational_risks_employer():.2f}")
        print(f"Invalidez y vida (Patrón) (Col. R): ${imss.get_invalidity_and_retirement_employer():.2f}")
        print(f"Guarderías y prestaciones sociales (Col. T): ${imss.get_childcare_employer():.2f}")
        print("\n=== Cuotas del Trabajador ===")
        print(f"Prestaciones en dinero (Trabajador) (Col. L): ${imss.get_employee_cash_benefits():.2f}")
        print("\n=== Total ===")
        print(f"Total cuotas IMSS (Patrón) (Col. V): ${imss.get_quota_employer():.2f}")
    except ValueError:
        print("Please enter a valid number for salary")

if __name__ == "__main__":
    main()