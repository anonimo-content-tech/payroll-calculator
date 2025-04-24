from typing import List, Dict, Any
from .imss import IMSS
from .isr import ISR
from .saving import Saving


class TotalCalculator:
    """
    Utility class to calculate totals across multiple salary calculations.
    This class aggregates results from multiple IMSS, ISR, and Saving instances.
    """
    # Define column references for each total key
    IMSS_COLUMN_REFS = {
        "total_salary": "Col. A (Base)", # Assuming base salary is the reference
        "total_imss_employer": "Col. V",
        "total_imss_employee": "Col. W",
        "total_rcv_employer": "Col. AC", # Based on get_total_rcv_employer
        "total_rcv_employee": "Col. AD",
        "total_infonavit": "Col. AE",
        "total_tax_payroll": "Col. AF",
        "total_social_cost": "Col. AP" # Based on get_total_social_cost_suggested
    }

    ISR_COLUMN_REFS = {
        "total_salary": "Col. A (Base)", # Assuming base salary is the reference
        "total_isr": "Col. L",
        "total_salary_credit": "Col. N",
        "total_tax_payable": "Col. O",
        "total_tax_in_favor": "Col. P"
    }

    SAVING_COLUMN_REFS = {
        "total_salary": "Col. A (Base)", # Assuming base salary is the reference
        "total_wage_and_salary_dsi": "Col. B (DSI Input)", # Input value
        "total_productivity": "Col. N",
        "total_commission_dsi": "Col. Q",
        "total_traditional_scheme": "Col. K (Biweekly)", # Based on get_traditional_scheme_biweekly_total
        "total_dsi_scheme": "Col. R (Biweekly)", # Based on get_dsi_scheme_biweekly_total
        "total_saving_amount": "Col. T",
        "avg_saving_percentage": "Col. U (%)",
        "total_current_perception": "Col. AF",
        "total_current_perception_dsi": "Col. AO",
        "total_increment": "Col. AQ",
        "avg_increment_percentage": "Col. AR (%)"
    }

    @staticmethod
    def calculate_traditional_scheme_totals(results: List[List[float]]) -> Dict[str, float]:
        """
        Calculate totals for the traditional scheme (IMSS) from a list of results.

        Args:
            results: List of lists containing calculation results

        Returns:
            Dictionary with total values for the traditional scheme
        """
        totals = {
            "total_salary": sum(row[0] for row in results),
            "total_imss_employer": sum(row[3] for row in results),
            "total_imss_employee": sum(row[4] for row in results),
            "total_rcv_employer": sum(row[5] for row in results), # Corresponds to get_total_rcv_employer
            "total_rcv_employee": sum(row[6] for row in results),
            "total_infonavit": sum(row[7] for row in results),
            "total_tax_payroll": sum(row[8] for row in results),
            "total_social_cost": sum(row[9] for row in results) # Corresponds to get_total_social_cost_suggested
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
        # Note: Indices match the structure in process_multiple_calculations
        totals = {
            "total_salary": sum(row[0] for row in results),
            "total_wage_and_salary_dsi": sum(row[1] for row in results),
            "total_productivity": sum(row[2] for row in results),
            "total_commission_dsi": sum(row[3] for row in results),
            "total_traditional_scheme": sum(row[4] for row in results), # Biweekly
            "total_dsi_scheme": sum(row[5] for row in results),          # Biweekly
            "total_saving_amount": sum(row[8] for row in results), # Index 8 is get_amount() in saving_results
            "total_current_perception": sum(row[10] for row in results),
            "total_current_perception_dsi": sum(row[11] for row in results),
            "total_increment": sum(row[12] for row in results)
        }

        # Calculate average percentages
        num_results = len(results)
        if num_results > 0:
            # Index 9 is saving percentage, Index 13 is increment percentage
            totals["avg_saving_percentage"] = sum(row[9] for row in results) / num_results
            totals["avg_increment_percentage"] = sum(row[13] for row in results) / num_results
        else:
            totals["avg_saving_percentage"] = 0
            totals["avg_increment_percentage"] = 0

        return totals


    @staticmethod
    def format_totals_table(totals: Dict[str, float], scheme_type: str) -> List[List[Any]]:
        """
        Format totals dictionary into a table format including column references.

        Args:
            totals: Dictionary with total values
            scheme_type: Type of scheme ('imss', 'isr', 'saving') to get correct column refs

        Returns:
            List of lists containing formatted totals [Concepto, Total, Columna]
        """
        table = []
        column_references = {}
        is_percentage_keys = []

        if scheme_type == 'imss':
            column_references = TotalCalculator.IMSS_COLUMN_REFS
        elif scheme_type == 'isr':
            column_references = TotalCalculator.ISR_COLUMN_REFS
        elif scheme_type == 'saving':
            column_references = TotalCalculator.SAVING_COLUMN_REFS
            is_percentage_keys = ["avg_saving_percentage", "avg_increment_percentage"]

        for key, value in totals.items():
            formatted_key = key.replace('_', ' ').title()
            if key in is_percentage_keys:
                formatted_value = f"{value:.2f}%" # Keep as string for display
            else:
                # Keep raw number for Excel formatting
                formatted_value = value

            # Add column reference if available
            column_ref = column_references.get(key, "")

            table.append([formatted_key, formatted_value, column_ref])

        return table