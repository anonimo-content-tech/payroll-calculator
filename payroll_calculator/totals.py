from typing import List, Dict, Any
from .imss import IMSS
from .isr import ISR
from .saving import Saving


class TotalCalculator:
    """
    Utility class to calculate totals across multiple salary calculations.
    This class aggregates results from multiple IMSS, ISR, and Saving instances.
    """

    @staticmethod
    def calculate_traditional_scheme_totals(results: List[List[float]]) -> Dict[str, float]:
        """
        Calculate totals for the traditional scheme from a list of results.
        
        Args:
            results: List of lists containing calculation results
            
        Returns:
            Dictionary with total values for the traditional scheme
        """
        totals = {
            "total_salary": sum(row[0] for row in results),
            "total_imss_employer": sum(row[3] for row in results),
            "total_imss_employee": sum(row[4] for row in results),
            "total_rcv_employer": sum(row[5] for row in results),
            "total_rcv_employee": sum(row[6] for row in results),
            "total_infonavit": sum(row[7] for row in results),
            "total_tax_payroll": sum(row[8] for row in results),
            "total_social_cost": sum(row[9] for row in results)
        }
        return totals

    @staticmethod
    def calculate_isr_totals(results: List[List[float]]) -> Dict[str, float]:
        """
        Calculate totals for ISR from a list of results.
        
        Args:
            results: List of lists containing ISR calculation results
            
        Returns:
            Dictionary with total values for ISR
        """
        totals = {
            "total_salary": sum(row[0] for row in results),
            "total_isr": sum(row[7] for row in results),
            "total_salary_credit": sum(row[8] for row in results),
            "total_tax_payable": sum(row[9] for row in results),
            "total_tax_in_favor": sum(row[10] for row in results)
        }
        return totals

    @staticmethod
    def calculate_saving_totals(results: List[List[float]]) -> Dict[str, float]:
        """
        Calculate totals for savings from a list of results.
        
        Args:
            results: List of lists containing saving calculation results
            
        Returns:
            Dictionary with total values for savings
        """
        # --- Inicio: Debugging ---
        num_records = len(results)

        totals = {
            "total_salary": sum(row[0] for row in results),
            "total_wage_and_salary_dsi": sum(row[1] for row in results),
            "total_productivity": sum(row[2] for row in results),
            "total_commission_dsi": sum(row[3] for row in results),
            "total_traditional_scheme": sum(row[4] for row in results),
            "total_dsi_scheme": sum(row[5] for row in results),
            "total_saving_amount": sum(row[6] for row in results),
            "total_current_perception": sum(row[8] for row in results),
            "total_current_perception_dsi": sum(row[9] for row in results),
            "total_increment": sum(row[10] for row in results),
            "total_fixed_fee_dsi": sum(row[12] for row in results),
            "total_income": sum(row[13] for row in results),
            "total_isr_retention_dsi": sum(row[15] for row in results)
        }
        
        # Calculate average percentages
        if num_records > 0: # Usar la variable ya calculada
            totals["avg_saving_percentage"] = sum(row[7] for row in results) / num_records
            totals["avg_increment_percentage"] = sum(row[11] for row in results) / num_records
        else:
            totals["avg_saving_percentage"] = 0
            totals["avg_increment_percentage"] = 0

        # --- Inicio: Debugging ---
        # print(f"Calculated Totals:")
        # for key, value in totals.items():
        #       print(f"  {key}: {value}")
        # print(f"--- End Debugging calculate_saving_totals ---")
        # --- Fin: Debugging ---
            
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