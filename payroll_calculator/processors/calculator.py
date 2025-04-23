from payroll_calculator.imss import IMSS
from payroll_calculator.isr import ISR
from payroll_calculator.saving import Saving
from payroll_calculator.parameters import Parameters
# Import the TotalCalculator class
from payroll_calculator.totals import TotalCalculator


def process_single_calculation(salary, payment_period, risk_class, smg_multiplier, fixed_fee_dsi, commission_percentage_dsi):
    """
    Process a single calculation for IMSS, ISR, and Savings
    """
    # IMSS calculations
    imss = IMSS(imss_salary=salary, payment_period=payment_period,
                risk_class=risk_class)


    # ISR calculations
    isr = ISR(monthly_salary=salary, payment_period=payment_period,
              employee=imss.employee)

    # Calculate wage_and_salary_dsi based on SMG multiplier
    wage_and_salary_dsi = Parameters.calculate_wage_and_salary_dsi(
        smg_multiplier, payment_period)

    # Savings calculations
    saving = Saving(
        wage_and_salary=salary,
        wage_and_salary_dsi=wage_and_salary_dsi,
        fixed_fee_dsi=fixed_fee_dsi,
        commission_percentage_dsi=commission_percentage_dsi,
        imss_instance=imss,
        isr_instance=isr
    )

    return imss, isr, saving, wage_and_salary_dsi


def process_multiple_calculations(salaries, payment_period, risk_class, smg_multiplier, fixed_fee_dsi, commission_percentage_dsi):
    """
    Process multiple calculations for IMSS, ISR, and Savings, adding column references to labels,
    and calculate totals using TotalCalculator by building totals data within the loop.
    """

    # Initialize a list to store combined results for each salary
    individual_results = []
    # Initialize lists to store data formatted for TotalCalculator, built inside the loop
    imss_data_for_totals = []
    isr_data_for_totals = []
    saving_data_for_totals = []

    # Process salaries with a progress indicator
    total_salaries = len(salaries)
    for i, salary in enumerate(salaries):
        if i % 10 == 0 or i == total_salaries - 1:
            print(f"Processing salary {i+1}/{total_salaries}...")

        # Get calculation instances
        imss, isr, saving, wage_and_salary_dsi = process_single_calculation(
            salary, payment_period, risk_class,
            smg_multiplier, fixed_fee_dsi, commission_percentage_dsi
        )

        # Create a combined dictionary for the current salary with column references
        combined_result = {
            # IMSS results
            "Salario Base (Col. B)": salary,
            "Salario Diario (Col. C)": imss.employee.calculate_salary_dialy(),
            "Salario Diario Integrado (Col. D)": imss.get_integrated_daily_wage(),
            "Cuota Patrón IMSS (Col. V)": imss.get_quota_employer(),
            "Cuota Trabajador IMSS (Col. W)": imss.get_quota_employee(),
            "RCV Patrón (Col. AB)": imss.get_total_rcv_employer(),
            "RCV Trabajador (Col. AD)": imss.get_total_rcv_employee(),
            "INFONAVIT Patrón (Col. AE)": imss.get_infonavit_employer(),
            "Impuesto Sobre Nómina (Col. AF)": imss.get_tax_payroll(),
            "Costo Social Total Sugerido (Col. AP)": imss.get_total_social_cost_suggested(),

            # ISR results
            "Límite Inferior ISR (Col. E)": isr.get_lower_limit(),
            "Excedente ISR (Col. F)": isr.get_surplus(),
            "Porcentaje Aplicado al Excedente ISR (Col. G)": isr.get_percentage_applied_to_excess(),
            "Impuesto al Excedente ISR (Col. H)": isr.get_surplus_tax(),
            "Cuota Fija ISR (Col. I)": isr.get_fixed_fee(),
            "Impuesto Total ISR (Col. J)": isr.get_total_tax(),
            "ISR (Col. L)": isr.get_isr(),
            "Crédito al Salario (Col. N)": isr.get_salary_credit(),
            "Impuesto a Cargo ISR (Col. O)": isr.get_tax_payable(),
            "Impuesto a Favor ISR (Col. P)": isr.get_tax_in_favor(),

            # Savings results
            "Salario DSI (Col. M)": wage_and_salary_dsi,
            "Productividad (Col. N)": saving.get_productivity(),
            "Comisión DSI (Col. Q)": saving.get_commission_dsi(),
            "Esquema Tradicional Quincenal (Col. K)": saving.get_traditional_scheme_biweekly_total(),
            "Esquema DSI Quincenal (Col. R)": saving.get_dsi_scheme_biweekly_total(),
            "Esquema Tradicional Mensual (Col. S)": saving.get_traditional_scheme_biweekly_total() * 2,
            "Esquema DSI Mensual (Col. T)": saving.get_dsi_scheme_biweekly_total() * 2,
            "Ahorro (Col. U)": saving.get_amount(),
            "Porcentaje de Ahorro (Col. W)": saving.get_percentage() * 100,
            "Percepción Actual (Col. AF)": saving.get_current_perception(),
            "Percepción DSI (Col. AO)": saving.get_current_perception_dsi(),
            "Incremento (Col. AQ)": saving.get_increment(),
            "Porcentaje de Incremento (Col. AR)": saving.get_increment_percentage() * 100
        }

        # Append the combined result to the main list
        individual_results.append(combined_result)

        # --- Prepare and append data for TotalCalculator within the loop ---
        # IMSS data row
        imss_row = [
            combined_result["Salario Base (Col. B)"],  # Index 0
            None,  # Index 1 (Placeholder)
            None,  # Index 2 (Placeholder)
            combined_result["Cuota Patrón IMSS (Col. V)"],  # Index 3
            combined_result["Cuota Trabajador IMSS (Col. W)"],  # Index 4
            combined_result["RCV Patrón (Col. AB)"],  # Index 5
            combined_result["RCV Trabajador (Col. AD)"],  # Index 6
            combined_result["INFONAVIT Patrón (Col. AE)"],  # Index 7
            combined_result["Impuesto Sobre Nómina (Col. AF)"],  # Index 8
            combined_result["Costo Social Total Sugerido (Col. AP)"]  # Index 9
        ]
        imss_data_for_totals.append(imss_row)

        # ISR data row
        isr_row = [
            combined_result["Salario Base (Col. B)"],  # Index 0
            None, None, None, None, None, None, # Indices 1-6 (Placeholders)
            combined_result["ISR (Col. L)"],  # Index 7
            combined_result["Crédito al Salario (Col. N)"],  # Index 8
            combined_result["Impuesto a Cargo ISR (Col. O)"],  # Index 9
            combined_result["Impuesto a Favor ISR (Col. P)"]  # Index 10
        ]
        isr_data_for_totals.append(isr_row)

        # Saving data row
        saving_row = [
            combined_result["Salario Base (Col. B)"],  # Index 0
            combined_result["Salario DSI (Col. M)"],  # Index 1
            combined_result["Productividad (Col. N)"],  # Index 2
            combined_result["Comisión DSI (Col. Q)"],  # Index 3
            combined_result["Esquema Tradicional Quincenal (Col. K)"],  # Index 4
            combined_result["Esquema DSI Quincenal (Col. R)"],  # Index 5
            combined_result["Ahorro (Col. U)"],  # Index 6
            saving.get_percentage(),  # Index 7 (Use original decimal value)
            combined_result["Percepción Actual (Col. AF)"],  # Index 8
            combined_result["Percepción DSI (Col. AO)"],  # Index 9
            combined_result["Incremento (Col. AQ)"],  # Index 10
            saving.get_increment_percentage()  # Index 11 (Use original decimal value)
        ]
        saving_data_for_totals.append(saving_row)

    # --- Calculate Totals using TotalCalculator ---
    # The data is already prepared in the correct format

    imss_totals = TotalCalculator.calculate_traditional_scheme_totals(imss_data_for_totals)
    isr_totals = TotalCalculator.calculate_isr_totals(isr_data_for_totals)
    saving_totals = TotalCalculator.calculate_saving_totals(saving_data_for_totals)

    print("IMSS TOTALS: ", imss_totals)
    print("ISR TOTALS: ", isr_totals)
    print("SAVING TOTALS: ", saving_totals)

    # Return a dictionary containing both the list of individual results and the calculated totals
    return {
        "individual_results": individual_results,
        "totals": {
            "imss": imss_totals,
            "isr": isr_totals,
            "saving": saving_totals
        }
    }


def parse_salaries_input(salary_input):
    """
    Parse salary input from user, handling file paths and direct input
    """
    # Check if input is a file path
    if salary_input.startswith('/') and ('.' in salary_input.split('/')[-1]):
        try:
            with open(salary_input, 'r') as file:
                salary_lines = file.readlines()
                # Process each line and combine into a single comma-separated string
                salary_input = ','.join([line.strip()
                                        for line in salary_lines if line.strip()])
            print(
                f"Successfully loaded {len(salary_input.split(','))} salaries from file")
        except FileNotFoundError:
            print(
                f"File not found: {salary_input}. Processing as direct input.")

    # Clean and parse the input
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

    return salaries
