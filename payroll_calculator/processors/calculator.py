import os
from payroll_calculator.imss import IMSS
from payroll_calculator.isr import ISR
from payroll_calculator.saving import Saving
from payroll_calculator.parameters import Parameters
# Import the TotalCalculator class
from payroll_calculator.totals import TotalCalculator

# VERIFICAR QUE SMG_MULTIPLIER Y COUNT_MINIMUM_SALARY SEAN LO MISMO, TAL PARECE QUE SÍ
def process_single_calculation(salary, daily_salary, payment_period, periodicity, integration_factor, use_increment_percentage, risk_class, smg_multiplier, commission_percentage_dsi, count_minimum_salary, productivity=None, imss_breakdown=None):
    """
    Process a single calculation for IMSS, ISR, and Savings
    
    Parameters:
    - productivity: Valor opcional de productividad para este cálculo
    """
    # Calculate wage_and_salary_dsi based on SMG multiplier
    wage_and_salary_dsi = Parameters.calculate_wage_and_salary_dsi(
        smg_multiplier, payment_period)
    
    # Calcular el salario mínimo para el período de pago
    smg_for_period = Parameters.SMG * payment_period
    print("EL MISMO PERO DESDE FOKIN DENTRO SMG FOR PERIOD: ", smg_for_period)
    
    # Determinar los umbrales para ISR e IMSS basados en count_minimum_salary
    isr_threshold_salary = smg_for_period * count_minimum_salary if count_minimum_salary > 1 else 0
    print("ISR THRESHOLD SALARY: ", isr_threshold_salary)
    imss_threshold_salary = smg_for_period * count_minimum_salary
    print("IMSS THRESHOLD SALARY: ", imss_threshold_salary)
    
    print("IMSS SALARY: ", salary, " DAILY SALARY: ", daily_salary)
    
    # IMSS calculations
    imss = IMSS(imss_salary=salary, daily_salary=daily_salary, payment_period=payment_period, integration_factor=integration_factor,
                risk_class=risk_class, minimum_threshold_salary=imss_threshold_salary, use_increment_percentage=use_increment_percentage, imss_breakdown=imss_breakdown)
    
    # Calcular los valores de breakdown si es necesario
    if imss_breakdown:
        imss.calculate_breakdown_values()
    
    # ISR calculations
    isr = ISR(monthly_salary=salary, payment_period=payment_period, periodicity=periodicity,
              employee=imss.employee, minimum_threshold_salary=isr_threshold_salary)

    # Savings calculations
    saving = Saving(
        wage_and_salary=salary,
        wage_and_salary_dsi=wage_and_salary_dsi,
        commission_percentage_dsi=commission_percentage_dsi,
        imss_instance=imss,
        isr_instance=isr,
        count_minimum_salary=count_minimum_salary,
        minimum_threshold_salary=imss_threshold_salary,
        productivity=productivity
    )

    return imss, isr, saving, wage_and_salary_dsi


def process_multiple_calculations(salaries, period_salaries, payment_periods, periodicity, integration_factors, use_increment_percentage, risk_class, smg_multiplier, commission_percentage_dsi, count_minimum_salary, stricted_mode, productivities=None, imss_breakdown=None):
    """
    Process multiple calculations for IMSS, ISR, and Savings, adding column references to labels.
    This function now only returns the individual results for each salary.
    Total calculations should be handled by the calling code after grouping if necessary.
    
    Parameters:
    - salaries: Lista de salarios
    - payment_periods: Lista de períodos de pago correspondientes a cada salario
    - risk_class: Clase de riesgo
    - smg_multiplier: Multiplicador de salario mínimo
    - commission_percentage_dsi: Porcentaje de comisión DSI
    - count_minimum_salary: Contador de salario mínimo
    - stricted_mode: Modo estricto para validación de salarios
    - productivity: Lista opcional de valores de productividad correspondientes a cada salario
    """

    # Initialize a list to store combined results for each salary
    individual_results = []

    # Process salaries with a progress indicator
    total_salaries = len(salaries)
    for i, daily_salary in enumerate(salaries):
        # Ignorar salarios que sean 0
        if daily_salary == 0:
            print(f"Salary is 0. Skipping salary at index {i}. {daily_salary}")
            continue
            
        # Obtener el período de pago correspondiente a este salario
        payment_period = payment_periods[i]
        integration_factor = integration_factors[i]
        
        # Obtener el valor de productividad para este salario si existe
        productivity = None
        if productivities is not None and i < len(productivities):
            productivity = productivities[i]
        
        # Calcular el salario mínimo para este período de pago específico
        smg_for_payment_period = Parameters.SMG * payment_period
        print("SMG FOR PAYMENT PERIOD: ", smg_for_payment_period)
        
        if i % 10 == 0 or i == total_salaries - 1:
            print(f"Processing salary {i+1}/{total_salaries}...")
            
        salary = period_salaries[i] if period_salaries else daily_salary * payment_periods[i]

        if stricted_mode:
            if smg_for_payment_period > salary:
                print(
                    f"SMG for {payment_period} days is higher than salary. Skipping salary {salary}.")
                raise ValueError(
                    f"SMG for {payment_period} days is higher than salary. Skipping salary {salary}.")

        # Get calculation instances
        imss, isr, saving, wage_and_salary_dsi = process_single_calculation(
            salary, daily_salary, payment_period, periodicity, integration_factor, use_increment_percentage, risk_class,
            smg_multiplier, commission_percentage_dsi, count_minimum_salary,
            productivity, imss_breakdown
        )
        
        print("IMSS: ", imss)

        # Create a combined dictionary for the current salary with column references
        combined_result = {
            # IMSS results
            "base_salary": salary,  # Col. B - Salario Base
            "daily_salary": imss.employee.calculate_salary_dialy(), # Col. C - Salario Diario
            "salary_for_calculation": daily_salary,
            "integration_factor": integration_factor, # Col. D - Factor de Integración
            "integrated_daily_wage": imss.get_integrated_daily_wage(), # Col. E - Salario Diario Integrado
            "imss_employer_fee": imss.get_quota_employer(),  # Col. V - Cuota Patrón IMSS
            "imss_employee_fee": imss.get_quota_employee(),  # Col. W - Cuota Trabajador IMSS
            "rcv_employer_table": imss.get_severance_and_old_age_employer(),  # Col. AA - CESANTIA Y VEJEZ PATRÓN
            "rcv_employer": imss.get_total_rcv_employer(),  # Col. AC - RCV Patrón
            "rcv_employee": imss.get_total_rcv_employee(),  # Col. AD - RCV Trabajador
            "infonavit_employer": imss.get_infonavit_employer(),  # Col. AE - INFONAVIT Patrón
            "payroll_tax": imss.get_tax_payroll(),  # Col. AF - Impuesto Sobre Nómina
            "suggested_total_social_cost": imss.get_total_social_cost_suggested(), # Col. AP - Costo Social Total Sugerido
            "minimum_salary": imss.smg,  # Col. AP - Costo Social Total Sugerido
            "payment_period": payment_period,  # Período de pago para este salario

            # ISR results
            "isr_lower_limit": isr.get_lower_limit(),  # Col. E - Límite Inferior ISR
            "isr_surplus": isr.get_surplus(),  # Col. F - Excedente ISR
            "isr_percentage_applied_to_surplus": isr.get_percentage_applied_to_excess(), # Col. G - Porcentaje Aplicado al Excedente ISR
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
            "traditional_scheme_biweekly": saving.get_traditional_scheme_biweekly_total(), # Col. K - Esquema Tradicional Quincenal
            "dsi_scheme_biweekly": saving.get_dsi_scheme_biweekly_total(), # Col. R - Esquema DSI Quincenal
            "traditional_scheme_monthly": saving.get_traditional_scheme_biweekly_total() * 2, # Col. S - Esquema Tradicional Mensual
            "dsi_scheme_monthly": saving.get_dsi_scheme_biweekly_total() * 2, # Col. T - Esquema DSI Mensual
            "saving_amount": saving.get_amount(), # Col. U - Ahorro
            "saving_percentage": saving.get_percentage() * 100,  # Col. W - Porcentaje de Ahorro
            "current_perception": saving.get_current_perception(),  # Col. AF - Percepción Actual
            "dsi_perception": saving.get_current_perception_dsi(),  # Col. AO - Percepción DSI
            "increment": saving.get_increment(),  # Col. AQ - Incremento
            "increment_percentage": saving.get_increment_percentage() * 100, # Col. AR - Porcentaje de Incremento
            "dsi_scheme_fixed_fee": saving.fixed_fee_dsi, # Col. P - Cuota Fija Esquema DSI
            "salary_total_income": salary, # Col. E - Salario (TOTAL INGRESOS)

            "commission_percentage_dsi": commission_percentage_dsi * 100, # Col. Q8 - Comisión DSI
            "isr_retention_dsi": saving.get_total_isr_retention_dsi(), # Col. AK9 - ISR Retención DSI
        }

        # Append the combined result to the main list
        individual_results.append(combined_result)

    return individual_results


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
