import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.menu import display_menu, calculate_single_quote, calculate_multiple_quotes

class TestMenu(unittest.TestCase):
    
    @patch('ui.menu.calculate_multiple_quotes')
    @patch('ui.menu.calculate_single_quote')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_display_menu(self, mock_print, mock_input, mock_calculate_single, mock_calculate_multiple):
        # Test that display_menu displays the menu and calls the correct functions
        # Set up the input sequence: first "1", then "2", then "3" to exit
        mock_input.side_effect = ["1", "2", "3"]
        
        # Call the function
        display_menu()
        
        # Check that the menu was printed
        mock_print.assert_any_call("\nMain Menu:")
        mock_print.assert_any_call("1. Calculate Single IMSS & ISR Quote")
        mock_print.assert_any_call("2. Calculate Multiple IMSS & ISR Quotes")
        mock_print.assert_any_call("3. Exit")
        
        # Check that the input function was called
        self.assertEqual(mock_input.call_count, 3)
        
        # Check that the calculate functions were called
        mock_calculate_single.assert_called_once()
        mock_calculate_multiple.assert_called_once()
        
        # Check that the exit message was printed
        mock_print.assert_any_call("Thank you for using IMSS & ISR Simulator!")
    
    @patch('ui.menu.display_single_calculation_results')
    @patch('ui.menu.process_single_calculation')
    @patch('builtins.input')
    @patch('builtins.float')
    @patch('builtins.int')
    def test_calculate_single_quote(self, mock_int, mock_float, mock_input, mock_process, mock_display):
        # Test that calculate_single_quote gets the correct inputs and calls the correct functions
        # Set up the mock returns
        mock_input.side_effect = ["10000", "15", "I", "8000", "500", "0.05"]
        mock_float.side_effect = [10000.0, 8000.0, 500.0, 0.05]
        mock_int.return_value = 15
        
        # Set up the mock process_single_calculation to return mock objects
        mock_imss = MagicMock()
        mock_isr = MagicMock()
        mock_saving = MagicMock()
        mock_process.return_value = (mock_imss, mock_isr, mock_saving)
        
        # Call the function
        calculate_single_quote()
        
        # Check that the input function was called with the correct prompts
        mock_input.assert_any_call("\nEnter total salary: ")
        mock_input.assert_any_call("Enter payment period (e.g., 15 for biweekly, 7 for weekly): ")
        mock_input.assert_any_call("Enter risk class (I, II, III, IV, V) [default: I]: ")
        mock_input.assert_any_call("Enter wage and salary DSI: ")
        mock_input.assert_any_call("Enter fixed fee DSI: ")
        mock_input.assert_any_call("Enter commission percentage DSI (e.g., 0.05 for 5%): ")
        
        # Check that process_single_calculation was called with the correct arguments
        mock_process.assert_called_with(10000.0, 15, "I", 8000.0, 500.0, 0.05)
        
        # Check that display_single_calculation_results was called with the correct arguments
        mock_display.assert_called_with(mock_imss, mock_isr, mock_saving)
    
    @patch('ui.menu.export_to_excel')
    @patch('ui.menu.display_saving_totals')
    @patch('ui.menu.display_saving_results')
    @patch('ui.menu.display_isr_totals')
    @patch('ui.menu.display_isr_results')
    @patch('ui.menu.display_imss_totals')
    @patch('ui.menu.display_imss_results')
    @patch('ui.menu.TotalCalculator.calculate_saving_totals')
    @patch('ui.menu.TotalCalculator.calculate_isr_totals')
    @patch('ui.menu.TotalCalculator.calculate_traditional_scheme_totals')
    @patch('ui.menu.process_multiple_calculations')
    @patch('ui.menu.parse_salaries_input')
    @patch('builtins.input')
    @patch('builtins.float')
    @patch('builtins.int')
    @patch('builtins.print')
    def test_calculate_multiple_quotes(self, mock_print, mock_int, mock_float, mock_input, 
                                      mock_parse, mock_process, mock_calc_imss, mock_calc_isr, 
                                      mock_calc_saving, mock_display_imss, mock_display_imss_totals,
                                      mock_display_isr, mock_display_isr_totals, mock_display_saving,
                                      mock_display_saving_totals, mock_export):
        # Test that calculate_multiple_quotes gets the correct inputs and calls the correct functions
        # Set up the mock returns
        mock_input.side_effect = ["10000,15000,20000", "15", "I", "8000", "500", "0.05"]
        mock_float.side_effect = [8000.0, 500.0, 0.05]
        mock_int.return_value = 15
        
        # Set up the mock parse_salaries_input to return a list of salaries
        mock_parse.return_value = [10000.0, 15000.0, 20000.0]
        
        # Set up the mock process_multiple_calculations to return mock results
        mock_imss_results = MagicMock()
        mock_isr_results = MagicMock()
        mock_saving_results = MagicMock()
        mock_process.return_value = (mock_imss_results, mock_isr_results, mock_saving_results)
        
        # Set up the mock calculate_*_totals to return mock totals
        mock_imss_totals = MagicMock()
        mock_isr_totals = MagicMock()
        mock_saving_totals = MagicMock()
        mock_calc_imss.return_value = mock_imss_totals
        mock_calc_isr.return_value = mock_isr_totals
        mock_calc_saving.return_value = mock_saving_totals
        
        # Call the function
        calculate_multiple_quotes()
        
        # Check that the input function was called with the correct prompts
        mock_input.assert_any_call("Enter salaries or file path: ")
        mock_input.assert_any_call("Enter payment period (e.g., 15 for biweekly, 7 for weekly): ")
        mock_input.assert_any_call("Enter risk class (I, II, III, IV, V) [default: I]: ")
        mock_input.assert_any_call("Enter wage and salary DSI: ")
        mock_input.assert_any_call("Enter fixed fee DSI: ")
        mock_input.assert_any_call("Enter commission percentage DSI (e.g., 0.05 for 5%): ")
        
        # Check that parse_salaries_input was called with the correct arguments
        mock_parse.assert_called_with("10000,15000,20000")
        
        # Check that process_multiple_calculations was called with the correct arguments
        mock_process.assert_called_with([10000.0, 15000.0, 20000.0], 15, "I", 8000.0, 500.0, 0.05)
        
        # Check that the calculate_*_totals functions were called with the correct arguments
        mock_calc_imss.assert_called_with(mock_imss_results)
        mock_calc_isr.assert_called_with(mock_isr_results)
        mock_calc_saving.assert_called_with(mock_saving_results)
        
        # Check that the display functions were called with the correct arguments
        mock_display_imss.assert_called()
        mock_display_imss_totals.assert_called_with(mock_imss_totals)
        mock_display_isr.assert_called()
        mock_display_isr_totals.assert_called_with(mock_isr_totals)
        mock_display_saving.assert_called()
        mock_display_saving_totals.assert_called_with(mock_saving_totals)
        
        # Check that export_to_excel was called
        mock_export.assert_called()

if __name__ == '__main__':
    unittest.main()