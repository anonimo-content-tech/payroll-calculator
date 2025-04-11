from processors.calculator import process_single_calculation, process_multiple_calculations, parse_salaries_input
from ui.display import (
    display_single_calculation_results, 
    display_imss_results, display_imss_totals,
    display_isr_results, display_isr_totals,
    display_saving_results, display_saving_totals
)
from exporters.excel_exporter import export_to_excel
from src.totals import TotalCalculator

def display_menu():
    while True:
        print("\nMain Menu:")
        print("1. Calculate Single IMSS & ISR Quote")
        print("2. Calculate Multiple IMSS & ISR Quotes")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ")
        
        if choice == "1":
            calculate_single_quote()
        elif choice == "2":
            calculate_multiple_quotes()
        elif choice == "3":
            print("Thank you for using IMSS & ISR Simulator!")
            break
        else:
            print("Invalid option. Please try again.")

def calculate_single_quote():
    try:
        # Get user inputs
        salary = float(input("\nEnter total salary: "))
        payment_period = int(input("Enter payment period (e.g., 15 for biweekly, 7 for weekly): "))
        risk_class = input("Enter risk class (I, II, III, IV, V) [default: I]: ") or 'I'
        
        # Savings parameters
        wage_and_salary_dsi = float(input("Enter wage and salary DSI: "))
        fixed_fee_dsi = float(input("Enter fixed fee DSI: "))
        commission_percentage_dsi = float(input("Enter commission percentage DSI (e.g., 0.05 for 5%): "))
        
        # Process calculations
        imss, isr, saving = process_single_calculation(
            salary, payment_period, risk_class, 
            wage_and_salary_dsi, fixed_fee_dsi, commission_percentage_dsi
        )
        
        # Display results
        display_single_calculation_results(imss, isr, saving)
        
    except ValueError as e:
        print(f"Error: {e}")

def calculate_multiple_quotes():
    try:
        # Get user inputs
        print("\nEnter salaries as a comma-separated list or array:")
        print("Example: 5000.50, 6000.75, 7500.25")
        print("You can also provide a file path with salaries (one per line):")
        print("Example: /path/to/salaries.txt")
        
        salary_input = input("Enter salaries or file path: ")
        payment_period = int(input("Enter payment period (e.g., 15 for biweekly, 7 for weekly): "))
        
        # Parse salaries
        salaries = parse_salaries_input(salary_input)
        
        if not salaries:
            print("No valid salaries entered.")
            return
        
        print(f"Processing {len(salaries)} salaries...")
        
        # Get additional parameters
        risk_class = input("Enter risk class (I, II, III, IV, V) [default: I]: ") or 'I'
        
        # Savings parameters
        wage_and_salary_dsi = float(input("Enter wage and salary DSI: "))
        fixed_fee_dsi = float(input("Enter fixed fee DSI: "))
        commission_percentage_dsi = float(input("Enter commission percentage DSI (e.g., 0.05 for 5%): "))
        
        # Process calculations
        imss_results, isr_results, saving_results = process_multiple_calculations(
            salaries, payment_period, risk_class, 
            wage_and_salary_dsi, fixed_fee_dsi, commission_percentage_dsi
        )
        
        # Define headers
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
        
        # Calculate totals
        imss_totals = TotalCalculator.calculate_traditional_scheme_totals(imss_results)
        isr_totals = TotalCalculator.calculate_isr_totals(isr_results)
        saving_totals = TotalCalculator.calculate_saving_totals(saving_results)
        
        # Display results
        display_imss_results(imss_results, imss_headers)
        display_imss_totals(imss_totals)
        
        display_isr_results(isr_results, isr_headers)
        display_isr_totals(isr_totals)
        
        display_saving_results(saving_results, saving_headers)
        display_saving_totals(saving_totals)
        
        # Export to Excel
        export_to_excel(
            imss_results=imss_results,
            imss_headers=imss_headers,
            imss_totals=imss_totals,
            isr_results=isr_results,
            isr_headers=isr_headers,
            isr_totals=isr_totals,
            saving_results=saving_results,
            saving_headers=saving_headers,
            saving_totals=saving_totals
        )
        
    except ValueError as e:
        print(f"Error: {e}")