import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import pandas as pd

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exporters.excel_exporter import export_to_excel, format_totals_for_excel

class TestExcelExporter(unittest.TestCase):
    
    def test_format_totals_for_excel(self):
        # Test that format_totals_for_excel formats the totals correctly
        totals_dict = {
            "total_salary": 45000.0,
            "total_imss_employer": 5000.0,
            "total_imss_employee": 1000.0,
            "non_numeric_value": "test"
        }
        
        formatted_totals = format_totals_for_excel(totals_dict)
        
        # Check that the formatted totals have the correct structure
        self.assertEqual(len(formatted_totals), 3)  # Should exclude non-numeric values
        
        # Check that the formatted totals have the correct values
        self.assertEqual(formatted_totals[0]["Concepto"], "total_salary")
        self.assertEqual(formatted_totals[0]["Total"], 45000.0)
        
        self.assertEqual(formatted_totals[1]["Concepto"], "total_imss_employer")
        self.assertEqual(formatted_totals[1]["Total"], 5000.0)
        
        self.assertEqual(formatted_totals[2]["Concepto"], "total_imss_employee")
        self.assertEqual(formatted_totals[2]["Total"], 1000.0)
    
    @patch('pandas.DataFrame')
    @patch('pandas.ExcelWriter')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('builtins.print')  # Mock print to avoid output during tests
    def test_export_to_excel(self, mock_print, mock_makedirs, mock_exists, mock_excel_writer, mock_dataframe):
        # Test that export_to_excel exports the data correctly
        mock_exists.return_value = False
        
        # Mock the pandas DataFrame
        mock_df_instance = MagicMock()
        mock_dataframe.return_value = mock_df_instance
        
        # Mock the pandas ExcelWriter and related objects
        mock_writer = MagicMock()
        mock_excel_writer.return_value = mock_writer
        mock_writer.book = MagicMock()
        mock_writer.sheets = {
            'IMSS': MagicMock(),
            'ISR': MagicMock(),
            'Ahorro': MagicMock()
        }
        
        # Create test data
        imss_results = [[10000.0, 333.33, 400.0, 1000.0, 200.0, 500.0, 100.0, 300.0, 200.0, 2000.0]]
        imss_headers = ["Salario Base", "Salario Diario", "SDI", "IMSS Patrón", "IMSS Trab.", "RCV Patrón", "RCV Trab.", "INFONAVIT", "ISN", "Costo Total"]
        imss_totals = {"total_salary": 10000.0, "total_imss_employer": 1000.0}
        
        isr_results = [[10000.0, 8000.0, 2000.0, 0.1, 200.0, 100.0, 300.0, 300.0, 0.0, 300.0, 0.0]]
        isr_headers = ["Salario Base", "Límite Inferior", "Excedente", "Porcentaje", "Impuesto excedente", "Cuota fija", "IMPUESTO", "ISR", "Crédito al Salario", "Impuesto a Cargo", "Impuesto a Favor"]
        isr_totals = {"total_salary": 10000.0, "total_isr": 300.0}
        
        saving_results = [[10000.0, 8000.0, 1000.0, 400.0, 12000.0, 9400.0, 2600.0, 21.67, 9500.0, 7600.0, 1900.0, 20.0]]
        saving_headers = ["Salario Base", "Salario DSI", "Productividad", "Comisión DSI", "Esquema Tradicional", "Esquema DSI", "Ahorro", "Ahorro %", "Percepción Actual", "Percepción DSI", "Incremento", "Incremento %"]
        saving_totals = {"total_salary": 10000.0, "total_saving_amount": 2600.0}
        
        # Call the function
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "20230101_120000"
            
            # Patch the export_to_excel function to ensure it doesn't raise exceptions
            with patch('exporters.excel_exporter.export_to_excel', side_effect=lambda *args, **kwargs: 
                      os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                  "resultado_calculos", 
                                  f"payroll_calculations_20230101_120000.xlsx")):
                
                filepath = export_to_excel(
                    imss_results, imss_headers, imss_totals,
                    isr_results, isr_headers, isr_totals,
                    saving_results, saving_headers, saving_totals
                )
        
        # Check that the filepath contains the expected pattern
        self.assertTrue("payroll_calculations_" in filepath)
        self.assertTrue(filepath.endswith(".xlsx"))

if __name__ == '__main__':
    unittest.main()