from typing import List, Dict, Any
from .imss import IMSS
from .isr import ISR
from .saving import Saving


def safe_get(row, idx, default=0):
    return row[idx] if len(row) > idx else default


class TotalCalculator:
    """
    Utility class to calculate totals across multiple salary calculations.
    This class aggregates results from multiple IMSS, ISR, and Saving instances.
    """
    
    @staticmethod
    def calculate_traditional_scheme_totals(imss_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calcula totales IMSS usando diccionarios en lugar de listas."""
        totals = {
            'total_imss_employer': sum(row.get('imss_employer_fee', 0) for row in imss_data),
            'total_imss_employee': sum(row.get('imss_employee_fee', 0) for row in imss_data),
            'total_rcv_employer': sum(row.get('rcv_employer', 0) for row in imss_data),
            'total_rcv_employee': sum(row.get('rcv_employee', 0) for row in imss_data),
            'total_infonavit': sum(row.get('infonavit_employer', 0) for row in imss_data),
            'total_tax_payroll': sum(row.get('payroll_tax', 0) for row in imss_data),
            'total_social_cost': sum(row.get('suggested_total_social_cost', 0) for row in imss_data),
        }
        
        # Agregar totales DSI si existen
        
        totals.update({
            'total_imss_employer_dsi': sum(row.get('first_quota_employer_imss_dsi', 0) for row in imss_data),
            'total_rcv_employer_dsi': sum(row.get('first_total_rcv_employer_dsi', 0) for row in imss_data),
            'total_infonavit_dsi': sum(row.get('first_infonavit_employer_dsi', 0) for row in imss_data),
            'total_tax_payroll_dsi': sum(row.get('first_tax_payroll_employer_dsi', 0) for row in imss_data),
            'total_imss_employee_dsi': sum(row.get('quota_employe_with_daily_salary', 0) for row in imss_data),
            'total_rcv_employee_dsi': sum(row.get('quota_employee_rcv_with_daily_salary', 0) for row in imss_data),
        })
        
        return totals

    @staticmethod
    def calculate_isr_totals(isr_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calcula totales ISR usando diccionarios."""
        totals = {
            'total_isr': sum(row.get('isr', 0) for row in isr_data),
            'total_salary_credit': sum(row.get('salary_credit', 0) for row in isr_data),
            'total_tax_payable': sum(row.get('isr_tax_payable', 0) for row in isr_data),
            'total_tax_in_favor': sum(row.get('isr_tax_in_favor', 0) for row in isr_data),
            'total_isr_tax_payable_dsi': sum(row.get('isr_tax_payable_dsi', 0) for row in isr_data),
        }
        
        if isr_data and 'first_tax_payroll_employer_dsi' in isr_data[0]:
            totals['first_tax_payroll_employer_dsi'] = sum(row.get('first_tax_payroll_employer_dsi', 0) for row in isr_data)
        
        return totals

    @staticmethod
    def calculate_saving_totals(saving_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calcula totales de ahorro usando diccionarios."""
        # print("SAVING DATA: ", saving_data[0])
        totals = {
            'total_wage_and_salary_dsi': sum(row.get('dsi_salary', 0) for row in saving_data),
            'total_productivity': sum(row.get('productivity', 0) for row in saving_data),
            'total_commission_dsi': sum(row.get('dsi_commission', 0) for row in saving_data),
            'total_traditional_scheme': sum(row.get('traditional_scheme_biweekly', 0) for row in saving_data),
            'total_dsi_scheme': sum(row.get('dsi_scheme_biweekly', 0) for row in saving_data),
            'total_saving_amount': sum(row.get('saving_amount', 0) for row in saving_data),
            'total_current_perception': sum(row.get('current_perception', 0) for row in saving_data),
            'total_current_perception_dsi': sum(row.get('dsi_perception', 0) for row in saving_data),
            'total_increment': sum(row.get('increment', 0) for row in saving_data),
            'total_fixed_fee_dsi': sum(row.get('dsi_scheme_fixed_fee', 0) for row in saving_data),
            'total_income': sum(row.get('salary_total_income', 0) for row in saving_data),
            'total_retention': sum(row.get('total_traditional_scheme', 0) for row in saving_data),
            'total_employer_contributions': sum(row.get('total_employer_contributions', 0) for row in saving_data),
            'total_employer_contributions_dsi': sum(row.get('total_employer_contributions_dsi', 0) for row in saving_data)
        }        
        
        # Calcular promedios
        if saving_data:
            totals['avg_saving_percentage'] = sum(row.get('saving_percentage', 0) for row in saving_data) / totals["total_traditional_scheme"]
            totals['avg_dsi_saving_percentage'] = totals["total_increment"] / totals["total_current_perception"]

        
        # Agregar campos condicionales
        if saving_data and 'saving_total_retentions_isr_dsi' in saving_data[0]:
            totals['total_retentions_isr_dsi'] = sum(row.get('saving_total_retentions_isr_dsi', 0) for row in saving_data)
        
        if saving_data and 'other_perception' in saving_data[0]:
            totals['total_other_perceptions'] = sum(row.get('other_perception', 0) for row in saving_data)
        
        return totals

    @staticmethod
    def format_totals_table(totals: Dict[str, float], is_percentage: List[str] = None, column_references: Dict[str, str] = None) -> List[List[Any]]:
        """
        Format totals dictionary into a table format.

        Args:
            totals: Dictionary with total values
            is_percentage: List of keys that should be formatted as percentages
            column_references: Dictionary mapping keys to column references

        Returns:
            List of lists containing formatted totals for display
        """
        if is_percentage is None:
            is_percentage = []

        if column_references is None:
            column_references = {}

        table = []
        for key, value in totals.items():
            formatted_key = key.replace('_', ' ').title()
            if key in is_percentage:
                formatted_value = f"{value:.2f}%"
            else:
                formatted_value = value

            # Add column reference if available
            column_ref = column_references.get(key, "")

            table.append([formatted_key, formatted_value, column_ref])

        return table
