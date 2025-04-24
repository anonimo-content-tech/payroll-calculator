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
    Process multiple calculations for IMSS, ISR, and Savings, adding column references to labels.
    This function now only returns the individual results for each salary.
    Total calculations should be handled by the calling code after grouping if necessary.
    """

    # Initialize a list to store combined results for each salary
    individual_results = []
    # --- REMOVED: Initialization of lists for totals ---
    # imss_data_for_totals = []
    # isr_data_for_totals = []
    # saving_data_for_totals = []

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
            "RCV Patrón (Col. AC)": imss.get_total_rcv_employer(),
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
            "Porcentaje de Incremento (Col. AR)": saving.get_increment_percentage() * 100,
            
            "Cuota Fija Esquema DSI (Col. P)": saving.fixed_fee_dsi,
            "Salario (TOTAL INGRESOS) (Col. E)": salary,
        }

        # Append the combined result to the main list
        individual_results.append(combined_result)

        # --- REMOVED: Preparation and appending of data for TotalCalculator ---
        # imss_row = [...]
        # imss_data_for_totals.append(imss_row)
        # isr_row = [...]
        # isr_data_for_totals.append(isr_row)
        # saving_row = [...]
        # saving_data_for_totals.append(saving_row)

    # --- REMOVED: Calculation of Totals using TotalCalculator ---
    # imss_totals = TotalCalculator.calculate_traditional_scheme_totals(imss_data_for_totals)
    # isr_totals = TotalCalculator.calculate_isr_totals(isr_data_for_totals)
    # saving_totals = TotalCalculator.calculate_saving_totals(saving_data_for_totals)

    # --- MODIFIED: Return only the list of individual results ---
    return individual_results
    # --- REMOVED: Returning dictionary with totals ---
    # return {
    #     "individual_results": individual_results,
    #     "totals": { ... }
    # }


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
