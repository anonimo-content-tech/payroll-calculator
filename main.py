from src.imss import IMSS
from src.isr import ISR
from tabulate import tabulate

def main():
    print("=== IMSS & ISR Simulator ===")
    display_menu()

def display_menu():
    while True:
        print("\nMain Menu:")
        print("1. Calculate Single IMSS & ISR Quote")
        print("2. Calculate Multiple IMSS & ISR Quotes")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ")
        
        if choice == "1":
            calculate_imss_quotas()
        elif choice == "2":
            calculate_multiple_imss_quotas()
        elif choice == "3":
            print("Thank you for using IMSS & ISR Simulator!")
            break
        else:
            print("Invalid option. Please try again.")

def calculate_multiple_imss_quotas():
    try:
        print("\nEnter salaries as a comma-separated list or array:")
        print("Example: 5000.50, 6000.75, 7500.25")
        salary_input = input("Enter salaries: ")
        payment_period = int(input("Enter payment period (e.g., 15 for biweekly, 7 for weekly): "))
        
        # Clean and parse the input
        salary_input = salary_input.replace('[', '').replace(']', '')
        salaries = [float(s.strip()) for s in salary_input.split(',') if s.strip()]
        
        if not salaries:
            print("No salaries entered.")
            return
        
        risk_class = input("Enter risk class (I, II, III, IV, V) [default: I]: ") or 'I'
        
        # Calculate results for all salaries
        imss_results = []
        isr_results = []
        
        for salary in salaries:
            # IMSS calculations
            imss = IMSS(imss_salary=salary, payment_period=payment_period, risk_class=risk_class)
            imss_results.append([
                salary,
                imss.employee.calculate_salary_dialy(),
                imss.get_integrated_daily_wage(),
                imss.get_quota_employer(),
                imss.get_quota_employee(),
                imss.get_total_rcv_employer(),
                imss.get_total_rcv_employee(),
                imss.get_infonavit_employer(),
                imss.get_tax_payroll(),
                imss.get_total_social_cost_suggested()
            ])
            
            # ISR calculations
            isr = ISR(monthly_salary=salary, payment_period=payment_period, employee=imss.employee)
            lower_limit = isr.get_lower_limit()
            surplus = isr.get_surplus()
            percentage_applied_to_excess = isr.get_percentage_applied_to_excess()
            surplus_tax = isr.get_surplus_tax()
            fixed_fee = isr.get_fixed_fee()
            total_tax = isr.get_total_tax()
            
            isr_results.append([
                salary,
                lower_limit,
                surplus,
                percentage_applied_to_excess,
                surplus_tax,
                fixed_fee,
                total_tax
                # Add more ISR calculations as they become available in the ISR class
            ])
        
        # Display IMSS results in table format
        imss_headers = [
            "Salario Base",
            "Salario Diario",
            "SDI (Col. D)",
            "IMSS Patrón (Col. V)",
            "IMSS Trab. (Col. W)",
            "RCV Patrón (Col. AB)",
            "RCV Trab. (Col. AD)",
            "INFONAVIT (Col. AE)",
            "ISN (Col. AF)",
            "Costo Total (Col. AP)"
        ]
        
        print("\nIMSS Resultados Detallados:")
        print(tabulate(imss_results, headers=imss_headers, tablefmt="grid", floatfmt=".2f"))
        
        # Display ISR results in table format
        isr_headers = [
            "Salario Base",
            "Límite Inferior (Col. E)",
            "Excedente (Col. F)",
            "Porcentaje excedente a aplicar (Col. G)",
            "Impuesto excedente (Col. H)",
            "Cuota fija (Col. I)",
            "IMPUESTO (Col. J)",
            # Add more headers as ISR calculations are implemented
        ]
        
        print("\nISR Resultados Detallados:")
        print(tabulate(isr_results, headers=isr_headers, tablefmt="grid", floatfmt=".2f"))
        
    except ValueError:
        print("Error: Please enter valid numbers separated by commas")

def print_section_header(title, width=100):
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)

def print_row(concept, value, column="", width=75):
    print(f"{concept + ' ' + column:<{width}} ${value:>10.2f}")

def calculate_imss_quotas():
    try:
        salary = float(input("\nEnter total salary: "))
        payment_period = int(input("Enter payment period (e.g., 15 for biweekly, 7 for weekly): "))
        risk_class = input("Enter risk class (I, II, III, IV, V) [default: I]: ") or 'I'
        
        # IMSS calculations
        imss = IMSS(imss_salary=salary, payment_period=payment_period, risk_class=risk_class)
        
        # ISR calculations
        isr = ISR(monthly_salary=salary, payment_period=payment_period, employee=imss.employee)
        
        # Display IMSS calculations
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
        
        # Display ISR calculations
        print_section_header("ISR Calculations")
        print_row("Salario Base", salary)
        print_row("Límite Inferior (Col. E)", isr.get_lower_limit() if isr.get_lower_limit() else 0)
        print_row("Excedente (Col. F)", isr.get_surplus() if isr.get_surplus() else 0)
        print_row("Porcentaje excedente a aplicar (Col. G)", isr.get_percentage_applied_to_excess() if isr.get_percentage_applied_to_excess() else 0)
        print_row("Impuesto excedente (Col. H)", isr.get_surplus_tax() if isr.get_surplus_tax() else 0)
        print_row("Cuota fija (Col. I)", isr.get_fixed_fee() if isr.get_fixed_fee() else 0)
        print_row("IMPUESTO (Col. J)", isr.get_total_tax() if isr.get_lower_limit() else 0)
        # Add more ISR calculations as they become available in the ISR class
        
    except ValueError:
        print("Please enter a valid number for salary")

if __name__ == "__main__":
    main()