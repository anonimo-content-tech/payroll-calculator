from src.imss import IMSS
from src.isr import ISR
from src.saving import Saving
from src.totals import TotalCalculator
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
        print("You can also provide a file path with salaries (one per line):")
        print("Example: /path/to/salaries.txt")
        
        salary_input = input("Enter salaries or file path: ")
        
        # Check if input is a file path
        if salary_input.startswith('/') and ('.' in salary_input.split('/')[-1]):
            try:
                with open(salary_input, 'r') as file:
                    salary_lines = file.readlines()
                    # Process each line and combine into a single comma-separated string
                    salary_input = ','.join([line.strip() for line in salary_lines if line.strip()])
                print(f"Successfully loaded {len(salary_input.split(','))} salaries from file")
            except FileNotFoundError:
                print(f"File not found: {salary_input}. Processing as direct input.")
        
        payment_period = int(input("Enter payment period (e.g., 15 for biweekly, 7 for weekly): "))
        
        # Clean and parse the input - handle large inputs by processing in chunks
        salary_input = salary_input.replace('[', '').replace(']', '')
        salary_chunks = salary_input.split(',')
        
        # Process all salaries
        salaries = []
        for chunk in salary_chunks:
            try:
                if chunk.strip():
                    salaries.append(float(chunk.strip()))
            except ValueError:
                print(f"Warning: Skipping invalid salary value: {chunk.strip()}")
        
        if not salaries:
            print("No valid salaries entered.")
            return
        
        print(f"Processing {len(salaries)} salaries...")
        
        # Rest of the function remains the same
        risk_class = input("Enter risk class (I, II, III, IV, V) [default: I]: ") or 'I'
        
        # Savings parameters
        wage_and_salary_dsi = float(input("Enter wage and salary DSI: "))
        fixed_fee_dsi = float(input("Enter fixed fee DSI: "))
        commission_percentage_dsi = float(input("Enter commission percentage DSI (e.g., 0.05 for 5%): "))
        
        # Calculate results for all salaries
        imss_results = []
        isr_results = []
        saving_results = []
        
        # Process salaries with a progress indicator
        total_salaries = len(salaries)
        for i, salary in enumerate(salaries):
            if i % 10 == 0 or i == total_salaries - 1:
                print(f"Processing salary {i+1}/{total_salaries}...")
                
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
            
            # Add the new ISR calculations
            isr_amount = isr.get_isr()
            salary_credit = isr.get_salary_credit()
            tax_payable = isr.get_tax_payable()
            tax_in_favor = isr.get_tax_in_favor()
            
            isr_results.append([
                salary,
                lower_limit,
                surplus,
                percentage_applied_to_excess,
                surplus_tax,
                fixed_fee,
                total_tax,
                isr_amount,
                salary_credit,
                tax_payable,
                tax_in_favor
            ])
            
            # Savings calculations
            saving = Saving(
                wage_and_salary=salary,
                wage_and_salary_dsi=wage_and_salary_dsi,
                fixed_fee_dsi=fixed_fee_dsi,
                commission_percentage_dsi=commission_percentage_dsi,
                imss_instance=imss,
                isr_instance=isr
            )
            
            saving_results.append([
                salary,
                wage_and_salary_dsi,
                saving.get_productivity(),
                saving.get_commission_dsi(),
                saving.get_traditional_scheme_biweekly_total(),
                saving.get_dsi_scheme_biweekly_total(),
                saving.get_amount(),
                saving.get_percentage() * 100,
                saving.get_current_perception(),
                saving.get_current_perception_dsi(),
                saving.get_increment(),
                saving.get_increment_percentage() * 100
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
        
        
        
        # Calculate and display IMSS totals
        imss_totals = TotalCalculator.calculate_traditional_scheme_totals(imss_results)
        print("\nIMSS Totales:")
        print(tabulate(TotalCalculator.format_totals_table(imss_totals, column_references={
            "total_salary": "Salario Base",
            "total_imss_employer": "Col. V",
            "total_imss_employee": "Col. W",
            "total_rcv_employer": "Col. AB",
            "total_rcv_employee": "Col. AD",
            "total_infonavit": "Col. AE",
            "total_tax_payroll": "Col. AF",
            "total_social_cost": "Col. AP"
        }), headers=["Concepto", "Total", "Columna"], tablefmt="grid", floatfmt=".2f"))
        
        # Display ISR results in table format with new headers
        isr_headers = [
            "Salario Base",
            "Límite Inferior (Col. E)",
            "Excedente (Col. F)",
            "Porcentaje excedente a aplicar (Col. G)",
            "Impuesto excedente (Col. H)",
            "Cuota fija (Col. I)",
            "IMPUESTO (Col. J)",
            "ISR (Col. L)",
            "Crédito al Salario (Col. N)",
            "Impuesto a Cargo (Col. O)",
            "Impuesto a Favor (Col. P)"
        ]
        
        print("\nISR Resultados Detallados:")
        print(tabulate(isr_results, headers=isr_headers, tablefmt="grid", floatfmt=".2f"))
        
        # Calculate and display ISR totals
        isr_totals = TotalCalculator.calculate_isr_totals(isr_results)
        print("\nISR Totales:")
        print(tabulate(TotalCalculator.format_totals_table(isr_totals, column_references={
            "total_salary": "Salario Base",
            "total_isr": "Col. L",
            "total_salary_credit": "Col. N",
            "total_tax_payable": "Col. O",
            "total_tax_in_favor": "Col. P"
        }), headers=["Concepto", "Total", "Columna"], tablefmt="grid", floatfmt=".2f"))
        
        # Display Savings results in table format
        saving_headers = [
            "Salario Base",
            "Salario DSI",
            "Productividad (Col. N)",
            "Comisión DSI (Col. Q)",
            "Esquema Tradicional (Col. K)",
            "Esquema DSI (Col. R)",
            "Ahorro (Col. T)",
            "Ahorro % (Col. U)",
            "Percepción Actual (Col. AF)",
            "Percepción DSI (Col. AO)",
            "Incremento (Col. AQ)",
            "Incremento % (Col. AR)"
        ]
        
        print("\nAhorro Resultados Detallados:")
        print(tabulate(saving_results, headers=saving_headers, tablefmt="grid", floatfmt=".2f"))
        
        # Calculate and display Savings totals
        saving_totals = TotalCalculator.calculate_saving_totals(saving_results)
        percentage_fields = ["avg_saving_percentage", "avg_increment_percentage"]
        print("\nAhorro Totales:")
        print(tabulate(TotalCalculator.format_totals_table(saving_totals, percentage_fields, column_references={
            "total_salary": "Salario Base",
            "total_wage_and_salary_dsi": "Salario DSI",
            "total_productivity": "Col. N",
            "total_commission_dsi": "Col. Q",
            "total_traditional_scheme": "Col. K",
            "total_dsi_scheme": "Col. R",
            "total_saving_amount": "Col. T",
            "avg_saving_percentage": "Col. U",
            "total_current_perception": "Col. AF",
            "total_current_perception_dsi": "Col. AO",
            "total_increment": "Col. AQ",
            "avg_increment_percentage": "Col. AR"
        }), headers=["Concepto", "Total", "Columna"], tablefmt="grid", floatfmt=".2f"))
        
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
        
        # Savings parameters
        wage_and_salary_dsi = float(input("Enter wage and salary DSI: "))
        fixed_fee_dsi = float(input("Enter fixed fee DSI: "))
        commission_percentage_dsi = float(input("Enter commission percentage DSI (e.g., 0.05 for 5%): "))
        
        # IMSS calculations
        imss = IMSS(imss_salary=salary, payment_period=payment_period, risk_class=risk_class)
        
        # ISR calculations
        isr = ISR(monthly_salary=salary, payment_period=payment_period, employee=imss.employee)
        
        # Savings calculations
        saving = Saving(
            wage_and_salary=salary,
            wage_and_salary_dsi=wage_and_salary_dsi,
            fixed_fee_dsi=fixed_fee_dsi,
            commission_percentage_dsi=commission_percentage_dsi,
            imss_instance=imss,
            isr_instance=isr
        )
        
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
        
        # Display ISR calculations with the new methods
        print_section_header("ISR Calculations")
        print_row("Salario Base", salary)
        print_row("Límite Inferior (Col. E)", isr.get_lower_limit() if isr.get_lower_limit() else 0)
        print_row("Excedente (Col. F)", isr.get_surplus() if isr.get_surplus() else 0)
        print_row("Porcentaje excedente a aplicar (Col. G)", isr.get_percentage_applied_to_excess() if isr.get_percentage_applied_to_excess() else 0)
        print_row("Impuesto excedente (Col. H)", isr.get_surplus_tax() if isr.get_surplus_tax() else 0)
        print_row("Cuota fija (Col. I)", isr.get_fixed_fee() if isr.get_fixed_fee() else 0)
        print_row("IMPUESTO (Col. J)", isr.get_total_tax() if isr.get_lower_limit() else 0)
        
        # Add the new ISR calculations to the display
        print_row("ISR (Col. L)", isr.get_isr() if isr.get_isr() else 0)
        print_row("Rango crédito al Salario", isr.get_range_credit_to_salary() if isr.get_range_credit_to_salary() else 0, "(Col. M)")
        print_row("Crédito al Salario", isr.get_salary_credit() if isr.get_salary_credit() else 0, "(Col. N)")
        print_row("Impuesto a Cargo", isr.get_tax_payable() if isr.get_tax_payable() else 0, "(Col. O)")
        print_row("Impuesto a Favor", isr.get_tax_in_favor() if isr.get_tax_in_favor() else 0, "(Col. P)")
        
        # Display Savings calculations
        print_section_header("Savings Calculations")
        
        print_section_header("Traditional Scheme (Biweekly)", width=90)
        print_row("Total Wage and Salary", salary)
        print_row("Total Costo Fiscal IMSS (Col. F)", imss.get_quota_employer())
        print_row("Total Costo Fiscal (Col. J)", imss.get_total_employer())
        print_row("Traditional Scheme Total", saving.get_traditional_scheme_biweekly_total(), "(Col. K)")
        
        print_section_header("DSI Scheme (Biweekly)", width=90)
        print_row("Wage and Salary DSI", wage_and_salary_dsi)
        print_row("Productivity", saving.get_productivity(), "(Col. N)")
        print_row("Fixed Fee DSI", fixed_fee_dsi)
        print_row("Commission DSI", saving.get_commission_dsi(), "(Col. Q)")
        print_row("DSI Scheme Total", saving.get_dsi_scheme_biweekly_total(), "(Col. R)")
        
        print_section_header("Savings", width=90)
        print_row("Savings Amount", saving.get_amount(), "(Col. T)")
        print_row("Savings Percentage", saving.get_percentage() * 100, "% (Col. U)")
        
        print_section_header("Traditional Scheme (Monthly)", width=90)
        print_row("ISR Retention", saving.get_isr_retention(), "(Col. AB)")
        print_row("Total Retentions", saving.get_total_retentions(), "(Col. AE)")
        print_row("Current Perception", saving.get_current_perception(), "(Col. AF)")
        
        print_section_header("DSI Scheme (Monthly)", width=90)
        print_row("Assimilated", saving.get_assimilated(), "(Col. AI)")
        print_row("Total Wage and Salary DSI", saving.get_total_wage_and_salary_dsi(), "(Col. AJ)")
        print_row("Current Perception DSI", saving.get_current_perception_dsi(), "(Col. AO)")
        
        print_section_header("Increment", width=90)
        print_row("Increment Amount", saving.get_increment(), "(Col. AQ)")
        print_row("Increment Percentage", saving.get_increment_percentage() * 100, "% (Col. AR)")
        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()