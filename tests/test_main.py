import unittest
from unittest.mock import patch
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main

class TestMain(unittest.TestCase):
    
    @patch('main.display_menu')
    @patch('builtins.print')
    def test_main(self, mock_print, mock_display_menu):
        # Test that main prints the welcome message and calls display_menu
        main()
        
        # Check that the welcome message was printed
        mock_print.assert_called_with("=== IMSS & ISR Simulator ===")
        
        # Check that display_menu was called
        mock_display_menu.assert_called_once()

if __name__ == '__main__':
    unittest.main()