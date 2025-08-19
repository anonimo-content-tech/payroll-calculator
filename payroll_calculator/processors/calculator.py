import os
from payroll_calculator.imss import IMSS
from payroll_calculator.isr import ISR
from payroll_calculator.saving import Saving
from payroll_calculator.parameters import Parameters
# Import the TotalCalculator class
from payroll_calculator.totals import TotalCalculator

# VERIFICAR QUE SMG_MULTIPLIER Y COUNT_MINIMUM_SALARY SEAN LO MISMO, TAL PARECE QUE SÍ
def process_single_calculation(salary, daily_salary, payment_period, periodicity, integration_factor, use_increment_percentage, 
                               risk_class, smg_multiplier, commission_percentage_dsi, count_minimum_salary, productivity=None, 
                               imss_breakdown=None, uma=113.14, other_perception=None, is_without_salary_mode=False, is_pure_mode=False, is_percentage_mode=False, is_keep_declared_salary=False):
    """
    Process a single calculation for IMSS, ISR, and Savings
    
    Parameters:
    - productivity: Valor opcional de productividad para este cálculo
    """    
    # Calculate wage_and_salary_dsi based on SMG multiplier
    wage_and_salary_dsi = Parameters.calculate_wage_and_salary_dsi(
        smg_multiplier, payment_period) if count_minimum_salary > 0 else salary
    
    if is_percentage_mode:
        wage_and_salary_dsi = daily_salary * payment_period    
    # Calcular el salario mínimo para el período de pago
    smg_for_period = Parameters.SMG * payment_period
    
    # Determinar los umbrales para ISR e IMSS basados en count_minimum_salary
    isr_threshold_salary = (smg_for_period * count_minimum_salary if count_minimum_salary > 1 else 0) if count_minimum_salary > 0 else 0
    imss_threshold_salary = smg_for_period * count_minimum_salary if count_minimum_salary > 0 else salary
    
    period_salary = daily_salary * payment_period
    is_salary_bigger_than_smg = period_salary > smg_for_period
    # IMSS calculations
    imss = IMSS(uma=uma, imss_salary=salary, daily_salary=daily_salary, payment_period=payment_period, integration_factor=integration_factor,
                risk_class=risk_class, minimum_threshold_salary=imss_threshold_salary, use_increment_percentage=use_increment_percentage, imss_breakdown=imss_breakdown, 
                is_salary_bigger_than_smg=is_salary_bigger_than_smg)
    
    # Calcular los valores de breakdown si es necesario
    # IMSS calculations
    imss_breakdown_result = None
    if imss_breakdown:
        imss_breakdown_result = imss.calculate_breakdown_values()
    
    # Store the breakdown values in the imss instance
    if imss_breakdown_result is not None:
        imss.integrated_direct = imss_breakdown_result['integrated_direct']
        imss.quota_employer_with_daily_salary = imss_breakdown_result['quota_employer_with_daily_salary']
        imss.total_rcv_employer_with_daily_salary = imss_breakdown_result['total_rcv_employer_with_daily_salary']
        imss.infonavit_employer_with_daily_salary = imss_breakdown_result['infonavit_employer_with_daily_salary']
        imss.tax_payroll_with_daily_salary = imss_breakdown_result['tax_payroll_with_daily_salary']
        imss.total_tax_cost_breakdown = imss_breakdown_result['total_tax_cost_breakdown']
        
        imss.quota_employe_with_daily_salary = imss_breakdown_result['quota_employe_with_daily_salary']
        imss.quota_employee_rcv_with_daily_salary = imss_breakdown_result['quota_employee_rcv_with_daily_salary']
        
        
        # print("DAILY SALARY: ", daily_salary)
        # print("IMSS.INTEGRATED_DIRECT: ", imss.integrated_direct)
         
        
        # print("RESULTADOD DESGLOSADO IMSS.QUOTA_EMPLOYER_WITH_DAILY_SALARY: ", imss.quota_employer_with_daily_salary)
        # print("RESULTADOD DESGLOSADO IMSS.TOTAL_RCV_EMPLOYER_WITH_DAILY_SALARY: ", imss.total_rcv_employer_with_daily_salary)
        # print("RESULTADOD DESGLOSADO IMSS.INFOVIT_EMPLOYER_WITH_DAILY_SALARY: ", imss.infonavit_employer_with_daily_salary)
        # print("RESULTADOD DESGLOSADO IMSS.TAX_PAYROLL_WITH_DAILY_SALARY: ", imss.tax_payroll_with_daily_salary)
        
        
        # print("RESULTADOD NORMAL IMSS.GET TOTAL EMPLOYER: ", imss.get_total_employer())
        # print("================ TOTAL ================", imss.total_tax_cost_breakdown)
        # print("================ TOTAL QUOTA_EMPLOYE_WITH_DAILY_SALARY ================", imss.quota_employe_with_daily_salary)
        # print("================ TOTAL QUOTA_EMPLOYEE_RCV_WITH_DAILY_SALARY ================", imss.quota_employee_rcv_with_daily_salary)
    
    # ISR calculations
    isr = ISR(monthly_salary=salary, payment_period=payment_period, periodicity=periodicity,
              employee=imss.employee, minimum_threshold_salary=isr_threshold_salary, is_salary_bigger_than_smg=is_salary_bigger_than_smg)
    # print("PASA ISR")
    isr_with_imss_breakdown = None
    # print("PERIOD SALARY: ", period_salary)
    if imss_breakdown is not None and is_salary_bigger_than_smg:
        # print("PERIOD SALARY DEL IF: ", period_salary)
        # Store the breakdown values in the isr instance
        isr_with_imss_breakdown = ISR(monthly_salary=period_salary, payment_period=payment_period, periodicity=periodicity,
              employee=imss.employee, minimum_threshold_salary=isr_threshold_salary, is_salary_bigger_than_smg=is_salary_bigger_than_smg)
        isr.isr_imss_breakdown = isr_with_imss_breakdown
        
    if not hasattr(isr, 'isr_imss_breakdown'):
        isr.isr_imss_breakdown = None
        
    # Savings calculations
    saving = Saving(
        wage_and_salary=salary,
        wage_and_salary_dsi=wage_and_salary_dsi,
        commission_percentage_dsi=commission_percentage_dsi,
        imss_instance=imss,
        isr_instance=isr,
        count_minimum_salary=count_minimum_salary,
        minimum_threshold_salary=imss_threshold_salary,
        productivity=productivity,
        other_perception=other_perception,
        is_without_salary_mode=is_without_salary_mode,
        is_salary_bigger_than_smg=is_salary_bigger_than_smg,
        is_pure_mode=is_pure_mode,
        is_percentage_mode=is_percentage_mode,
        is_keep_declared_salary=is_keep_declared_salary
    )
    # print("PASA SAVING")
    
    # print("GET_TRADITIONAL_SCHEME_BIWEEKLY_TOTAL: ", saving.get_traditional_scheme_biweekly_total())    
    saving_breakdown_result = None
    # En la parte donde se llama a calculate_breakdown_values_for_dsi
    if imss_breakdown is not None:
        # Store the breakdown values in the saving instance
        saving_breakdown_result = saving.calculate_breakdown_values_for_dsi(use_direct_daily_salary=True, period_salary=period_salary)
        saving.dsi_total_fiscal_cost_with_breakdown = saving_breakdown_result['dsi_total_fiscal_cost']
        saving.saving_amount = saving_breakdown_result['saving_amount']
        saving.saving_percentage = saving_breakdown_result['saving_percentage']
        
        saving.saving_total_retentions_isr_dsi = saving_breakdown_result['saving_total_retentions_isr_dsi']
        # print("SAVING DSI TOTAL WITH BREAKDOWN: ", saving.dsi_total_fiscal_cost_with_breakdown)
        
        # print("SAVING SAVING AMOUNT: ", saving.saving_amount)
        
        saving.saving_total_retentions_dsi = saving_breakdown_result['saving_total_retentions_dsi']
        saving.saving_total_current_perception_dsi = saving_breakdown_result['saving_total_current_perception_dsi']
        saving.current_perception = saving_breakdown_result['saving_total_current_perception']
        saving.saving_get_increment = saving_breakdown_result['saving_get_increment']
        saving.saving_get_increment_percentage = saving_breakdown_result['saving_get_increment_percentage']
        
        saving.saving_wage_and_salary = saving_breakdown_result['saving_wage_and_salary']
        saving.saving_productivity = saving_breakdown_result['saving_productivity']
        
    if is_salary_bigger_than_smg is False:
        saving.employer_contributions = saving.get_employer_contributions_imss_rcv_traditional_scheme()
        
        
        # print("================ TOTAL SAVING.SAVING_TOTAL_RETENTIONS_isr_DSI ================", saving.saving_total_retentions_isr_dsi)
        # print("================ TOTAL SAVING_TOTAL_CURRENT_PERCEPTION_DSI ================", saving.saving_total_current_perception_dsi)
        # print("================ TOTAL SAVING_TOTAL_CURRENT_PERCEPTION ================", saving.current_perception)
        # print("================ TOTAL SAVING_TOTAL_RETENTIONS_DSI ================", saving.saving_total_retentions_dsi)
        # print("================ TOTAL SAVING_GET_INCREMENT ================", saving.saving_get_increment)
        # print("================ TOTAL SAVING_GET_INCREMENT_PERCENTAGE ================", saving.saving_get_increment_percentage)

    return imss, isr, saving, wage_and_salary_dsi


def get_value_or_default(obj, attr_name, default_func=None):
    """
    Obtiene un valor de un objeto si existe el atributo, o ejecuta una función por defecto.
    
    Parameters:
    - obj: El objeto del que se quiere obtener el atributo
    - attr_name: El nombre del atributo a obtener
    - default_func: Una función que se ejecutará si el atributo no existe o es None
    
    Returns:
    - El valor del atributo si existe y no es None, o el resultado de default_func
    """
    value = getattr(obj, attr_name, None)
    if value is None and default_func is not None:
        return default_func()
    return value


def process_multiple_calculations(salaries, period_salaries, payment_periods, periodicity, integration_factors, 
                                  use_increment_percentage, risk_class, smg_multiplier, commission_percentage_dsi, 
                                  count_minimum_salary, stricted_mode, productivities=None, imss_breakdown=None, 
                                  uma=113.14, other_perceptions=None, productivity_to_zero=None, is_pure_mode=None, is_keep_declared_salary=None):
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
    
    salaries_to_use = salaries if total_salaries > 0 else productivities
    is_without_salary_mode = total_salaries == 0
    
    is_percentage_mode = len(salaries) > 0 and productivities is not None and len(productivities) > 0
    
    for i, daily_salary in enumerate(salaries_to_use):
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
        
        other_perception = None
        if other_perceptions is not None and i < len(other_perceptions):
            other_perception = other_perceptions[i]
        
        # Calcular el salario mínimo para este período de pago específico
        smg_for_payment_period = Parameters.SMG * payment_period
        
        if i % 10 == 0 or i == len(salaries_to_use) - 1:
            print(f"Processing salary {i+1}/{len(salaries_to_use)}...")
            
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
            productivity, imss_breakdown, uma, other_perception, is_without_salary_mode, is_pure_mode, is_percentage_mode, is_keep_declared_salary
        )
        
        # Create a combined dictionary for the current salary with column references
        combined_result = {
            # IMSS results
            "base_salary": salary,  # Col. B - Salario Base
            "daily_salary": imss.employee.calculate_salary_dialy(), # Col. C - Salario Diario
            "salary_for_calculation": daily_salary,
            "integration_factor": integration_factor, # Col. D - Factor de Integración
            "integrated_daily_wage": imss.get_integrated_daily_wage(), # Col. E - Salario Diario Integrado
            "imss_employer_fee": imss.get_quota_employer(),  # Col. V - Cuota Patrón IMSS
            "imss_employee_fee": imss.get_quota_employee() if not hasattr(saving, 'employer_contributions') else 0,  # Col. W - Cuota Trabajador IMSS
            "rcv_employer_table": imss.get_severance_and_old_age_employer(),  # Col. AA - CESANTIA Y VEJEZ PATRÓN
            "rcv_employer": imss.get_total_rcv_employer(),  # Col. AC - RCV Patrón
            "rcv_employee": imss.get_total_rcv_employee() if not hasattr(saving, 'employer_contributions') else 0,  # Col. AD - RCV Trabajador
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
            "isr_range_credit_for_salary": isr.get_range_credit_to_salary(),  # Col. M - ISR
            "salary_credit": isr.get_salary_credit(),  # Col. N - Crédito al Salario
            "isr_tax_payable": isr.get_tax_payable(),  # Col. O - Impuesto a Cargo ISR
            "isr_tax_in_favor": isr.get_tax_in_favor(),  # Col. P - Impuesto a Favor ISR

            # Savings results
            "dsi_salary": get_value_or_default(saving, "saving_wage_and_salary_dsi", lambda: wage_and_salary_dsi if wage_and_salary_dsi != 0 else salary),  # Col. M - Salario DSI
            "productivity": get_value_or_default(saving, "saving_productivity", saving.get_productivity) if not productivity_to_zero else 0,  # Col. N - Productividad
            "dsi_commission": saving.get_commission_dsi(),  # Col. Q - Comisión DSI
            "total_traditional_scheme": saving.get_total_traditional_scheme(), # Col. J - Total Esquema Tradicional
            "traditional_scheme_biweekly": saving.get_traditional_scheme_biweekly_total(), # Col. K - Esquema Tradicional Quincenal
            "dsi_scheme_biweekly": get_value_or_default(saving, "dsi_total_fiscal_cost_with_breakdown", saving.get_dsi_scheme_biweekly_total), # Col. R - Esquema DSI Quincenal
            "traditional_scheme_monthly": saving.get_traditional_scheme_biweekly_total() * 2, # Col. S - Esquema Tradicional Mensual
            "dsi_scheme_monthly": saving.get_dsi_scheme_biweekly_total() * 2, # Col. R - Esquema DSI Mensual
            "saving_amount": get_value_or_default(saving, "saving_amount", saving.get_amount), # Col. T - Ahorro
            "saving_percentage": get_value_or_default(saving, "saving_percentage", lambda: saving.get_percentage() * 100),  # Col. U - Porcentaje de Ahorro
            "total_retentions": saving.get_total_retentions(),  # Col. AE - Retenciones Total de Retenciones - ISR + IMSS + RCV
            "current_perception": get_value_or_default(saving, "current_perception", saving.get_current_perception),  # Col. AF - Percepción Actual
            "dsi_perception": get_value_or_default(saving, "saving_total_current_perception_dsi", saving.get_current_perception_dsi),  # Col. AO - Percepción DSI
            "increment": get_value_or_default(saving, "saving_get_increment", saving.get_increment),  # Col. AQ - Incremento
            "increment_percentage": get_value_or_default(saving, "saving_get_increment_percentage", lambda: saving.get_increment_percentage() * 100),  # Col. AR - Porcentaje de Incremento
            "dsi_scheme_fixed_fee": saving.fixed_fee_dsi, # Col. P - Cuota Fija Esquema DSI
            "salary_total_income": salary + other_perception, # Col. E - Salario (TOTAL INGRESOS)
            "other_perception": other_perception, # Col. E Cuando se ocupe el template de Otras Percepciones

            "commission_percentage_dsi": commission_percentage_dsi * 100, # Col. Q8 - Comisión DSI
            "isr_retention_dsi": saving.get_total_isr_retention_dsi(), # Col. AK9 - ISR Retención DSI
            "uma_used": uma # La que se manda como parámetro
        }
        
        if imss_breakdown:
            combined_result["total_retentions_dsi"] = saving.saving_total_retentions_dsi # Col. AR (desglosado) o AN (normal),  - Total Retenciones DSI
            
            employer_contributions_dsi = (imss.quota_employe_with_daily_salary + imss.quota_employee_rcv_with_daily_salary) if hasattr(saving, 'employer_contributions') else 0
            
            combined_result["total_tax_cost_breakdown"] = imss.total_tax_cost_breakdown + employer_contributions_dsi  # Col. AP - Costo Fiscal Total cuando es desglosado
            combined_result["employer_contributions_dsi"] = employer_contributions_dsi # Col. U - Cuotas Patronales
            
            combined_result["first_quota_employer_imss_dsi"] = imss.quota_employer_with_daily_salary # Col. P - Costo Fiscal IMSS para DSI cuando es desglosado - Hoja de Ahorro
            combined_result["first_total_rcv_employer_dsi"] = imss.total_rcv_employer_with_daily_salary # Col. Q - Costo Fiscal RCV para DSI cuando es desglosado - Hoja de Ahorro
            combined_result["first_infonavit_employer_dsi"] = imss.infonavit_employer_with_daily_salary # Col. R - Costo Fiscal Infonavit para DSI cuando es desglosado - Hoja de Ahorro
            combined_result["first_tax_payroll_employer_dsi"] = imss.tax_payroll_with_daily_salary # Col. S - Costo Fiscal Impuesto Estatal para DSI cuando es desglosado - Hoja de Ahorro
            
            combined_result["quota_employe_with_daily_salary"] = imss.quota_employe_with_daily_salary if not hasattr(saving, 'employer_contributions') else 0
            combined_result["quota_employee_rcv_with_daily_salary"] = imss.quota_employee_rcv_with_daily_salary if not hasattr(saving, 'employer_contributions') else 0
            
            
            combined_result["saving_total_retentions_isr_dsi"] = saving.saving_total_retentions_isr_dsi
            
            
            if isr.isr_imss_breakdown is not None:
                # Add ISR breakdown values to combined_result
                combined_result["isr_tax_payable_dsi"] = isr.isr_imss_breakdown.get_tax_payable() # Col. O - Impuesto a Cargo ISR para DSI

        # Añadir employee_contributions si existe en el objeto saving
        if hasattr(saving, 'employer_contributions'):
            combined_result["employer_contributions"] = saving.employer_contributions

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
