import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processors.calculator import process_single_calculation, process_multiple_calculations, parse_salaries_input
from src.imss import IMSS
from src.isr import ISR
from src.saving import Saving

class TestCalculator(unittest.TestCase):
    
    def test_process_single_calculation(self):
        # Test that process_single_calculation returns the correct objects
        salary = 10000.0
        payment_period = 15
        risk_class = 'I'
        wage_and_salary_dsi = 8000.0
        fixed_fee_dsi = 500.0
        commission_percentage_dsi = 0.05
        
        imss, isr, saving = process_single_calculation(
            salary, payment_period, risk_class, 
            wage_and_salary_dsi, fixed_fee_dsi, commission_percentage_dsi
        )
        
        # Check that the returned objects are of the correct type
        self.assertIsInstance(imss, IMSS)
        self.assertIsInstance(isr, ISR)
        self.assertIsInstance(saving, Saving)
        
        # Check that the objects were initialized with the correct values
        self.assertEqual(imss.salary, salary)  # Changed from imss.imss_salary to imss.salary
        self.assertEqual(imss.payment_period, payment_period)
        self.assertEqual(imss.risk_class, risk_class)
        
        self.assertEqual(isr.monthly_salary, salary)
        self.assertEqual(isr.payment_period, payment_period)
        
        self.assertEqual(saving.wage_and_salary, salary)
        self.assertEqual(saving.wage_and_salary_dsi, wage_and_salary_dsi)
        self.assertEqual(saving.fixed_fee_dsi, fixed_fee_dsi)
        self.assertEqual(saving.commission_percentage_dsi, commission_percentage_dsi)
    
    def test_process_multiple_calculations(self):
        # Test that process_multiple_calculations processes multiple salaries correctly
        salaries = [10000.0, 15000.0, 20000.0]
        payment_period = 15
        risk_class = 'I'
        wage_and_salary_dsi = 8000.0
        fixed_fee_dsi = 500.0
        commission_percentage_dsi = 0.05
        
        imss_results, isr_results, saving_results = process_multiple_calculations(
            salaries, payment_period, risk_class, 
            wage_and_salary_dsi, fixed_fee_dsi, commission_percentage_dsi
        )
        
        # Check that the results have the correct length
        self.assertEqual(len(imss_results), len(salaries))
        self.assertEqual(len(isr_results), len(salaries))
        self.assertEqual(len(saving_results), len(salaries))
        
        # Check that the first element of each result contains the correct salary
        self.assertEqual(imss_results[0][0], salaries[0])
        self.assertEqual(isr_results[0][0], salaries[0])
        self.assertEqual(saving_results[0][0], salaries[0])
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="10000.0\n15000.0\n20000.0")
    def test_parse_salaries_input_from_file(self, mock_open):
        # Test parsing salaries from a file
        salary_input = "/path/to/salaries.txt"
        
        with patch('os.path.exists', return_value=True):
            salaries = parse_salaries_input(salary_input)
            
            # Check that the correct number of salaries was parsed
            self.assertEqual(len(salaries), 3)
            self.assertEqual(salaries, [10000.0, 15000.0, 20000.0])
            
            # Check that the file was opened
            mock_open.assert_called_once_with(salary_input, 'r')
    
    def test_parse_salaries_input_from_string(self):
        # Test parsing salaries from a comma-separated string
        salary_input = "10000.0, 15000.0, 20000.0"
        
        salaries = parse_salaries_input(salary_input)
        
        # Check that the correct number of salaries was parsed
        self.assertEqual(len(salaries), 3)
        self.assertEqual(salaries, [10000.0, 15000.0, 20000.0])
    
    def test_parse_salaries_input_with_invalid_values(self):
        # Test parsing salaries with invalid values
        salary_input = "10000.0, invalid, 20000.0"
        
        with patch('builtins.print') as mock_print:
            salaries = parse_salaries_input(salary_input)
            
            # Check that the correct number of valid salaries was parsed
            self.assertEqual(len(salaries), 2)
            self.assertEqual(salaries, [10000.0, 20000.0])
            
            # Check that a warning was printed for the invalid value
            mock_print.assert_called_with("Warning: Skipping invalid salary value: invalid")

if __name__ == '__main__':
    unittest.main()