from tabulate import tabulate

def print_section_header(title, width=100):
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)

def print_row(concept, value, column="", width=75):
    print(f"{concept + ' ' + column:<{width}} ${value:>10.2f}")

def display_imss_results(imss_results, imss_headers):
    print("\nIMSS Resultados Detallados:")
    print(tabulate(imss_results, headers=imss_headers, tablefmt="grid", floatfmt=".2f"))

def display_imss_totals(imss_totals):
    print("\nIMSS Totales:")
    print(tabulate(format_totals_table(imss_totals, column_references={
        "total_salary": "Salario Base",
        "total_imss_employer": "Col. V",
        "total_imss_employee": "Col. W",
        "total_rcv_employer": "Col. AB",
        "total_rcv_employee": "Col. AD",
        "total_infonavit": "Col. AE",
        "total_tax_payroll": "Col. AF",
        "total_social_cost": "Col. AP"
    }), headers=["Concepto", "Total", "Columna"], tablefmt="grid", floatfmt=".2f"))

def display_isr_results(isr_results, isr_headers):
    print("\nISR Resultados Detallados:")
    print(tabulate(isr_results, headers=isr_headers, tablefmt="grid", floatfmt=".2f"))

def display_isr_totals(isr_totals):
    print("\nISR Totales:")
    print(tabulate(format_totals_table(isr_totals, column_references={
        "total_salary": "Salario Base",
        "total_isr": "Col. L",
        "total_salary_credit": "Col. N",
        "total_tax_payable": "Col. O",
        "total_tax_in_favor": "Col. P"
    }), headers=["Concepto", "Total", "Columna"], tablefmt="grid", floatfmt=".2f"))

def display_saving_results(saving_results, saving_headers):
    print("\nAhorro Resultados Detallados:")
    print(tabulate(saving_results, headers=saving_headers, tablefmt="grid", floatfmt=".2f"))

def display_saving_totals(saving_totals):
    percentage_fields = ["avg_saving_percentage", "avg_increment_percentage"]
    print("\nAhorro Totales:")
    print(tabulate(format_totals_table(saving_totals, percentage_fields, column_references={
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

def format_totals_table(totals_dict, percentage_fields=None, column_references=None):
    if percentage_fields is None:
        percentage_fields = []
    if column_references is None:
        column_references = {}
    
    formatted_table = []
    for key, value in totals_dict.items():
        if isinstance(value, (int, float)):
            concept = key
            column = column_references.get(key, "")
            
            # Format percentage fields
            if key in percentage_fields:
                formatted_table.append([concept, f"{value:.2f}%", column])
            else:
                formatted_table.append([concept, value, column])
    
    return formatted_table

def display_single_calculation_results(imss, isr, saving):
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

    # ... rest of the display code for IMSS, ISR, and Savings
    # (I've truncated this for brevity, but the full implementation would include all the display logic)