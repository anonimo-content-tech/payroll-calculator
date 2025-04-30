from payroll_calculator.imss import IMSS
from payroll_calculator.isr import ISR
from payroll_calculator.saving import Saving
from payroll_calculator.parameters import Parameters
# Import the TotalCalculator class
from payroll_calculator.totals import TotalCalculator


def process_single_calculation(salary, payment_period, risk_class, smg_multiplier, commission_percentage_dsi, count_minimum_salary):
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
        commission_percentage_dsi=commission_percentage_dsi,
        imss_instance=imss,
        isr_instance=isr,
        count_minimum_salary=count_minimum_salary
    )

    return imss, isr, saving, wage_and_salary_dsi


def process_multiple_calculations(salaries, payment_period, risk_class, smg_multiplier, commission_percentage_dsi, count_minimum_salary):
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
            smg_multiplier, commission_percentage_dsi, count_minimum_salary
        )

        # Create a combined dictionary for the current salary with column references
        combined_result = {
            # IMSS results
            "base_salary": salary,  # Col. B - Salario Base
            "daily_salary": imss.employee.calculate_salary_dialy(),  # Col. C - Salario Diario
            "integrated_daily_wage": imss.get_integrated_daily_wage(),  # Col. D - Salario Diario Integrado
            "imss_employer_fee": imss.get_quota_employer(),  # Col. V - Cuota Patrón IMSS
            "imss_employee_fee": imss.get_quota_employee(),  # Col. W - Cuota Trabajador IMSS
            "rcv_employer": imss.get_total_rcv_employer(),  # Col. AC - RCV Patrón
            "rcv_employee": imss.get_total_rcv_employee(),  # Col. AD - RCV Trabajador
            "infonavit_employer": imss.get_infonavit_employer(),  # Col. AE - INFONAVIT Patrón
            "payroll_tax": imss.get_tax_payroll(),  # Col. AF - Impuesto Sobre Nómina
            "suggested_total_social_cost": imss.get_total_social_cost_suggested(),  # Col. AP - Costo Social Total Sugerido
            "minimum_salary": imss.smg,  # Col. AP - Costo Social Total Sugerido

            # ISR results
            "isr_lower_limit": isr.get_lower_limit(),  # Col. E - Límite Inferior ISR
            "isr_surplus": isr.get_surplus(),  # Col. F - Excedente ISR
            "isr_percentage_applied_to_surplus": isr.get_percentage_applied_to_excess(),  # Col. G - Porcentaje Aplicado al Excedente ISR
            "isr_surplus_tax": isr.get_surplus_tax(),  # Col. H - Impuesto al Excedente ISR
            "isr_fixed_fee": isr.get_fixed_fee(),  # Col. I - Cuota Fija ISR
            "isr_total_tax": isr.get_total_tax(),  # Col. J - Impuesto Total ISR
            "isr": isr.get_isr(),  # Col. L - ISR
            "salary_credit": isr.get_salary_credit(),  # Col. N - Crédito al Salario
            "isr_tax_payable": isr.get_tax_payable(),  # Col. O - Impuesto a Cargo ISR
            "isr_tax_in_favor": isr.get_tax_in_favor(),  # Col. P - Impuesto a Favor ISR

            # Savings results
            "dsi_salary": wage_and_salary_dsi,  # Col. M - Salario DSI
            "productivity": saving.get_productivity(),  # Col. N - Productividad
            "dsi_commission": saving.get_commission_dsi(),  # Col. Q - Comisión DSI
            "traditional_scheme_biweekly": saving.get_traditional_scheme_biweekly_total(),  # Col. K - Esquema Tradicional Quincenal
            "dsi_scheme_biweekly": saving.get_dsi_scheme_biweekly_total(),  # Col. R - Esquema DSI Quincenal
            "traditional_scheme_monthly": saving.get_traditional_scheme_biweekly_total() * 2,  # Col. S - Esquema Tradicional Mensual
            "dsi_scheme_monthly": saving.get_dsi_scheme_biweekly_total() * 2,  # Col. T - Esquema DSI Mensual
            "saving_amount": saving.get_amount(),  # Col. U - Ahorro
            "saving_percentage": saving.get_percentage() * 100,  # Col. W - Porcentaje de Ahorro
            "current_perception": saving.get_current_perception(),  # Col. AF - Percepción Actual
            "dsi_perception": saving.get_current_perception_dsi(),  # Col. AO - Percepción DSI
            "increment": saving.get_increment(),  # Col. AQ - Incremento
            "increment_percentage": saving.get_increment_percentage() * 100,  # Col. AR - Porcentaje de Incremento
            
            "dsi_scheme_fixed_fee": saving.fixed_fee_dsi,  # Col. P - Cuota Fija Esquema DSI
            "salary_total_income": salary,  # Col. E - Salario (TOTAL INGRESOS)
            
            "commission_percentage_dsi": commission_percentage_dsi * 100,  # Col. Q8 - Comisión DSI
            "isr_retention_dsi": saving.get_total_isr_retention_dsi(),  # Col. AK9 - ISR Retención DSI
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
