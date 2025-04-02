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

def print_section_header(title, width=100):
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)

def print_row(concept, value, column="", width=75):
    print(f"{concept + ' ' + column:<{width}} ${value:>10.2f}")

def calculate_imss_quotas():
    try:
        salary = float(input("\nEnter total salary: "))
        risk_class = input("Enter risk class (I, II, III, IV, V) [default: I]: ") or 'I'
        imss = IMSS(salary, risk_class)
        
        print_section_header("IMSS Calculations")
        print_row("Salario diario", imss.employee.calculate_salary_dialy())
        print_row("Salario diario integrado", imss.get_integrated_daily_wage(), "(Col. D)")
        print_row("Salario tope 25 SMG", imss.get_salary_cap_25_smg(), "(Col. G)")
        print_row("Salario tope 25 SMG TC2", imss.get_salary_cap_25_smg_2(), "(Col. Q)")

        print_section_header("Cuotas Patronales")
        print_row("Cuota del patrón (Enfermedades y maternidad)", 
                 imss.get_diseases_and_maternity_employer_quota(), "(Col. H)")
        print_row("Excedente del patrón (Enfermedades y maternidad)", 
                 imss.get_diseases_and_maternity_employer_surplus(), "(Col. I)")
        print_row("Prestaciones en dinero (Patrón)", 
                 imss.get_employer_cash_benefits(), "(Col. K)")
        print_row("Prestaciones en especie (Gastos médicos patrón)", 
                 imss.get_benefits_in_kind_medical_expenses_employer(), "(Col. M)")
        print_row("Riesgos de trabajo (Patrón)", 
                 imss.get_occupational_risks_employer(), "(Col. O)")
        print_row("Invalidez y vida (Patrón)", 
                 imss.get_invalidity_and_retirement_employer(), "(Col. R)")
        print_row("Guarderías y prestaciones sociales", 
                 imss.get_childcare_employer(), "(Col. T)")
        print("-" * 90)
        print_row("Total cuotas IMSS (Patrón)", 
                 imss.get_quota_employer(), "(Col. V)")

        print_section_header("Cuotas del Trabajador")
        print_row("Excedente del trabajador (Enfermedades y maternidad)", 
                 imss.get_diseases_and_maternity_employee_surplus(), "(Col. J)")
        print_row("Prestaciones en dinero (Trabajador)", 
                 imss.get_employee_cash_benefits(), "(Col. L)")
        print_row("Prestaciones en especie (Gastos médicos trabajador)", 
                 imss.get_benefits_in_kind_medical_expenses_employee(), "(Col. N)")
        print_row("Invalidez y vida (Trabajador)", 
                 imss.get_invalidity_and_retirement_employee(), "(Col. S)")
        print("-" * 90)
        print_row("Total cuotas IMSS (Trabajador)", 
                 imss.get_quota_employee(), "(Col. W)")

        print_section_header("Total General")
        # Eliminamos la línea que causa el error y usamos print_section_header en su lugar
        print_section_header("RCV Patrón", width=90)
        print_row("Retiro", 
                 imss.get_retirement_employer(), "(Col. Z)")
        print_row("Cesantía y vejez", 
                 imss.get_severance_and_old_age_employer(), "(Col. AA)")
        print("-" * 90)
        print_row("Total RCV (Patrón)", 
                 imss.get_total_rcv_employer(), "(Col. AB)")

        print_section_header("RCV Trabajador", width=90)
        print_row("Cesantía y vejez", 
                 imss.get_severance_and_old_age_employee(), "(Col. AB)")
        print("-" * 90)
        print_row("Total RCV (Trabajador)", 
                 imss.get_total_rcv_employee(), "(Col. AD)")

        print_section_header("INFONAVIT y Otros", width=90)
        print_row("INFONAVIT (Patrón)", 
                 imss.get_infonavit_employer(), "(Col. AE)")
        print_row("Impuesto sobre nómina", 
                 imss.get_tax_payroll(), "(Col. AF)")

        print_section_header("Resumen de Totales")
        print_row("Total cuotas IMSS (Patrón + Trabajador)", 
                 imss.get_total_imss(), "(Col. X)")
        print_row("Total RCV (Patrón)", 
                 imss.get_total_rcv_employer(), "(Col. AC)")
        print_row("Total RCV (Trabajador)", 
                 imss.get_total_rcv_employee(), "(Col. AD)")
        print("-" * 90)
        print_row("Total IMSS + RCV", 
                 imss.get_total_imss() + imss.get_total_rcv_employer() + imss.get_total_rcv_employee(), "(IMSS + RCV)")
        print_row("Total del Patrón", 
                 imss.get_total_employer(), "(Col. AH)")
        print_row("Total del Trabajador", 
                 imss.get_total_employee(), "(Col. AJ)")
        print("-" * 90)
        print_row("Suma Costo Social", 
                 imss.get_total_social_cost(), "(Col. AL)")
        print_row("Incremento 2.5%", 
                 imss.get_increment(), "(Col. AN)")
        print_row("Suma Costo Social Sugerido", 
                 imss.get_total_social_cost_suggested(), "(Col. AP)")

        # Remove or comment out the following line as it's redundant now
        # print_row("Gran Total (IMSS + RCV)", 
        #          imss.get_total_imss() + imss.get_total_rcv_employer(), "(Total)")
        
    except ValueError:
        print("Please enter a valid number for salary")

if __name__ == "__main__":
    main()