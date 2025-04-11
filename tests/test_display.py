import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.display import (
    print_section_header, print_row, format_totals_table,
    display_imss_results, display_imss_totals,
    display_isr_results, display_isr_totals,
    display_saving_results, display_saving_totals,
    display_single_calculation_results
)

class TestDisplay(unittest.TestCase):
    
    @patch('builtins.print')
    def test_print_section_header(self, mock_print):
        # Test that print_section_header prints the correct header
        print_section_header("Test Header", width=50)
        
        # Check that print was called with the correct arguments
        # The first call doesn't include the newline character
        mock_print.assert_called_with("=" * 50)
        
        # Check the second call
        calls = mock_print.call_args_list
        self.assertEqual(calls[1], unittest.mock.call("Test Header".center(50)))
        self.assertEqual(calls[2], unittest.mock.call("=" * 50))
    
    @patch('builtins.print')
    def test_print_row(self, mock_print):
        # Test that print_row prints the correct row
        print_row("Test Concept", 1000.0, "(Col. A)", width=50)
        
        # Check that print was called with the correct arguments
        # Use a more flexible assertion that checks the format but not exact spacing
        actual_call = mock_print.call_args[0][0]
        self.assertTrue(actual_call.startswith("Test Concept (Col. A)"))
        self.assertTrue(actual_call.endswith("$   1000.00"))
    
    def test_format_totals_table(self):
        # Test that format_totals_table formats the totals correctly
        totals_dict = {
            "total_salary": 45000.0,
            "total_imss_employer": 5000.0,
            "avg_saving_percentage": 20.0,
            "non_numeric_value": "test"
        }
        
        percentage_fields = ["avg_saving_percentage"]
        column_references = {
            "total_salary": "Col. A",
            "total_imss_employer": "Col. B",
            "avg_saving_percentage": "Col. C"
        }
        
        formatted_table = format_totals_table(totals_dict, percentage_fields, column_references)
        
        # Check that the formatted table has the correct structure
        self.assertEqual(len(formatted_table), 3)  # Should exclude non-numeric values
        
        # Check that the formatted table has the correct values
        self.assertEqual(formatted_table[0][0], "total_salary")
        self.assertEqual(formatted_table[0][1], 45000.0)
        self.assertEqual(formatted_table[0][2], "Col. A")
        
        self.assertEqual(formatted_table[1][0], "total_imss_employer")
        self.assertEqual(formatted_table[1][1], 5000.0)
        self.assertEqual(formatted_table[1][2], "Col. B")
        
        self.assertEqual(formatted_table[2][0], "avg_saving_percentage")
        self.assertEqual(formatted_table[2][1], "20.00%")
        self.assertEqual(formatted_table[2][2], "Col. C")
    
    @patch('ui.display.tabulate')
    @patch('builtins.print')
    def test_display_imss_results(self, mock_print, mock_tabulate):
        # Test that display_imss_results displays the results correctly
        mock_tabulate.return_value = "Tabulated IMSS Results"
        
        imss_results = [[10000.0, 333.33, 400.0, 1000.0, 200.0, 500.0, 100.0, 300.0, 200.0, 2000.0]]
        imss_headers = ["Salario Base", "Salario Diario", "SDI", "IMSS Patrón", "IMSS Trab.", "RCV Patrón", "RCV Trab.", "INFONAVIT", "ISN", "Costo Total"]
        
        display_imss_results(imss_results, imss_headers)
        
        # Check that tabulate was called with the correct arguments
        mock_tabulate.assert_called_with(imss_results, headers=imss_headers, tablefmt="grid", floatfmt=".2f")
        
        # Check that print was called with the correct arguments
        mock_print.assert_called_with("Tabulated IMSS Results")
    
    @patch('ui.display.format_totals_table')
    @patch('ui.display.tabulate')
    @patch('builtins.print')
    def test_display_imss_totals(self, mock_print, mock_tabulate, mock_format_totals_table):
        # Test that display_imss_totals displays the totals correctly
        mock_format_totals_table.return_value = "Formatted IMSS Totals"
        mock_tabulate.return_value = "Tabulated IMSS Totals"
        
        imss_totals = {"total_salary": 10000.0, "total_imss_employer": 1000.0}
        
        display_imss_totals(imss_totals)
        
        # Check that format_totals_table was called with the correct arguments
        mock_format_totals_table.assert_called_with(imss_totals, column_references={
            "total_salary": "Salario Base",
            "total_imss_employer": "Col. V",
            "total_imss_employee": "Col. W",
            "total_rcv_employer": "Col. AB",
            "total_rcv_employee": "Col. AD",
            "total_infonavit": "Col. AE",
            "total_tax_payroll": "Col. AF",
            "total_social_cost": "Col. AP"
        })
        
        # Check that tabulate was called with the correct arguments
        mock_tabulate.assert_called_with("Formatted IMSS Totals", headers=["Concepto", "Total", "Columna"], tablefmt="grid", floatfmt=".2f")
        
        # Check that print was called with the correct arguments
        mock_print.assert_called_with("Tabulated IMSS Totals")
    
    @patch('ui.display.print_section_header')
    @patch('ui.display.print_row')
    def test_display_single_calculation_results(self, mock_print_row, mock_print_section_header):
        # Test that display_single_calculation_results displays the results correctly
        # Create mock objects for IMSS, ISR, and Saving
        mock_imss = MagicMock()
        mock_imss.employee.calculate_salary_dialy.return_value = 333.33
        mock_imss.get_integrated_daily_wage.return_value = 400.0
        mock_imss.get_salary_cap_25_smg.return_value = 5000.0
        mock_imss.get_salary_cap_25_smg_2.return_value = 5000.0
        mock_imss.get_diseases_and_maternity_employer_quota.return_value = 200.0
        mock_imss.get_diseases_and_maternity_employer_surplus.return_value = 100.0
        mock_imss.get_employer_cash_benefits.return_value = 50.0
        mock_imss.get_benefits_in_kind_medical_expenses_employer.return_value = 150.0
        mock_imss.get_occupational_risks_employer.return_value = 100.0
        mock_imss.get_invalidity_and_retirement_employer.return_value = 100.0
        mock_imss.get_childcare_employer.return_value = 50.0
        mock_imss.get_quota_employer.return_value = 1000.0
        
        mock_isr = MagicMock()
        mock_saving = MagicMock()
        
        # Call the function
        display_single_calculation_results(mock_imss, mock_isr, mock_saving)
        
        # Check that print_section_header was called with the correct arguments
        # The first call is to "Cuotas Patronales" not "IMSS Calculations"
        mock_print_section_header.assert_any_call("Cuotas Patronales")
        
        # Verify at least one print_row call
        mock_print_row.assert_any_call("Salario diario", 333.33)
        mock_print_row.assert_any_call("Salario diario integrado", 400.0, "(Col. D)")
        mock_print_row.assert_any_call("Salario tope 25 SMG", 5000.0, "(Col. G)")

if __name__ == '__main__':
    unittest.main()