from src.imss import IMSS
from src.isr import ISR
from src.saving import Saving

def process_single_calculation(salary, payment_period, risk_class, wage_and_salary_dsi, fixed_fee_dsi, commission_percentage_dsi):
    """
    Process a single calculation for IMSS, ISR, and Savings
    """
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
    
    return imss, isr, saving

def process_multiple_calculations(salaries, payment_period, risk_class, wage_and_salary_dsi, fixed_fee_dsi, commission_percentage_dsi):
    """
    Process multiple calculations for IMSS, ISR, and Savings
    """
    imss_results = []
    isr_results = []
    saving_results = []
    
    # Process salaries with a progress indicator
    total_salaries = len(salaries)
    for i, salary in enumerate(salaries):
        if i % 10 == 0 or i == total_salaries - 1:
            print(f"Processing salary {i+1}/{total_salaries}...")
            
        # Get calculation instances
        imss, isr, saving = process_single_calculation(
            salary, payment_period, risk_class, 
            wage_and_salary_dsi, fixed_fee_dsi, commission_percentage_dsi
        )
        
        # IMSS results
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
        
        # ISR results
        isr_results.append([
            salary,
            isr.get_lower_limit(),
            isr.get_surplus(),
            isr.get_percentage_applied_to_excess(),
            isr.get_surplus_tax(),
            isr.get_fixed_fee(),
            isr.get_total_tax(),
            isr.get_isr(),
            isr.get_salary_credit(),
            isr.get_tax_payable(),
            isr.get_tax_in_favor()
        ])
        
        # Savings results
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
    
    return imss_results, isr_results, saving_results

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
                salary_input = ','.join([line.strip() for line in salary_lines if line.strip()])
            print(f"Successfully loaded {len(salary_input.split(','))} salaries from file")
        except FileNotFoundError:
            print(f"File not found: {salary_input}. Processing as direct input.")
    
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