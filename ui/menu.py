from payroll_calculator.parameters import Parameters
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
        smg_multiplier = float(input(f"Enter SMG multiplier (e.g., 1, 1.05, 2) [default: 1]: ") or 1.0)
        fixed_fee_dsi = float(input("Enter fixed fee DSI: "))
        commission_percentage_dsi = float(input("Enter commission percentage DSI (e.g., 0.05 for 5%): "))
        
        # Process calculations
        imss, isr, saving = process_single_calculation(
            salary, payment_period, risk_class, 
            smg_multiplier, fixed_fee_dsi, commission_percentage_dsi
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
        smg_multiplier = float(input(f"Enter SMG multiplier (e.g., 1, 1.05, 2) [default: 1]: ") or 1.0)
        fixed_fee_dsi = float(input("Enter fixed fee DSI: "))
        commission_percentage_dsi = float(input("Enter commission percentage DSI (e.g., 0.05 for 5%): "))
        
        # Process calculations
        imss_results, isr_results, saving_results = process_multiple_calculations(
            salaries, payment_period, risk_class,
            smg_multiplier, fixed_fee_dsi, commission_percentage_dsi # Note: smg_multiplier is not used here, consider removing or using it
        )
        
        # Define headers (kept for display functions)
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
            # Updated based on process_multiple_calculations output structure
            "Salario Base",
            "Salario DSI",
            "Productividad", # Index 2
            "Comisión DSI", # Index 3
            "Esquema Tradicional Quincenal", # Index 4
            "Esquema DSI Quincenal", # Index 5
            "Esquema Tradicional Mensual", # Index 6
            "Esquema DSI Mensual", # Index 7
            "Ahorro Monto", # Index 8
            "Ahorro %", # Index 9
            "Percepción Actual Tradicional", # Index 10
            "Percepción Actual DSI", # Index 11
            "Incremento Monto", # Index 12
            "Incremento %" # Index 13
        ]
        
        # Calculate totals dictionaries
        imss_totals_dict = TotalCalculator.calculate_traditional_scheme_totals(imss_results)
        isr_totals_dict = TotalCalculator.calculate_isr_totals(isr_results)
        saving_totals_dict = TotalCalculator.calculate_saving_totals(saving_results)
        
        # Format totals tables for display and export (includes column refs)
        imss_totals_table = TotalCalculator.format_totals_table(imss_totals_dict, 'imss')
        isr_totals_table = TotalCalculator.format_totals_table(isr_totals_dict, 'isr')
        saving_totals_table = TotalCalculator.format_totals_table(saving_totals_dict, 'saving')
        
        # Display results (using original totals dictionaries for display functions)
        display_imss_results(imss_results, imss_headers)
        display_imss_totals(imss_totals_dict) # Keep using dict for console display
        
        display_isr_results(isr_results, isr_headers)
        display_isr_totals(isr_totals_dict) # Keep using dict for console display
        
        display_saving_results(saving_results, saving_headers)
        display_saving_totals(saving_totals_dict) # Keep using dict for console display
        
        # Export to Excel using the formatted tables for the new Totals sheet
        export_to_excel(
            imss_results=imss_results,
            imss_headers=imss_headers,
            imss_totals_table=imss_totals_table, # Pass formatted table
            isr_results=isr_results,
            isr_headers=isr_headers,
            isr_totals_table=isr_totals_table,   # Pass formatted table
            saving_results=saving_results,
            saving_headers=saving_headers,       # Pass updated headers
            saving_totals_table=saving_totals_table # Pass formatted table
        )

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e: # Catch other potential errors
        print(f"An unexpected error occurred: {e}")