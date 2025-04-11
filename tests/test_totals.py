import unittest
from src.totals import TotalCalculator


class TestTotalCalculator(unittest.TestCase):
    """Test cases for the TotalCalculator class."""

    def test_calculate_traditional_scheme_totals(self):
        """Test the calculation of traditional scheme totals."""
        # Sample data: [salary, daily_salary, sdi, imss_employer, imss_employee, rcv_employer, rcv_employee, infonavit, tax_payroll, social_cost]
        test_data = [
            [5000.0, 166.67, 250.0, 500.0, 100.0, 200.0, 50.0, 125.0, 150.0, 975.0],
            [6000.0, 200.0, 300.0, 600.0, 120.0, 240.0, 60.0, 150.0, 180.0, 1170.0],
        ]
        
        result = TotalCalculator.calculate_traditional_scheme_totals(test_data)
        
        self.assertEqual(result["total_salary"], 11000.0)
        self.assertEqual(result["total_imss_employer"], 1100.0)
        self.assertEqual(result["total_imss_employee"], 220.0)
        self.assertEqual(result["total_rcv_employer"], 440.0)
        self.assertEqual(result["total_rcv_employee"], 110.0)
        self.assertEqual(result["total_infonavit"], 275.0)
        self.assertEqual(result["total_tax_payroll"], 330.0)
        self.assertEqual(result["total_social_cost"], 2145.0)

    def test_calculate_isr_totals(self):
        """Test the calculation of ISR totals."""
        # Sample data: [salary, lower_limit, surplus, percentage, surplus_tax, fixed_fee, total_tax, isr, salary_credit, tax_payable, tax_in_favor]
        test_data = [
            [5000.0, 4000.0, 1000.0, 0.1, 100.0, 200.0, 300.0, 300.0, 0.0, 300.0, 0.0],
            [6000.0, 5000.0, 1000.0, 0.15, 150.0, 250.0, 400.0, 400.0, 0.0, 400.0, 0.0],
        ]
        
        result = TotalCalculator.calculate_isr_totals(test_data)
        
        self.assertEqual(result["total_salary"], 11000.0)
        self.assertEqual(result["total_isr"], 700.0)
        self.assertEqual(result["total_salary_credit"], 0.0)
        self.assertEqual(result["total_tax_payable"], 700.0)
        self.assertEqual(result["total_tax_in_favor"], 0.0)

    def test_calculate_saving_totals(self):
        """Test the calculation of saving totals."""
        # Sample data: [salary, wage_dsi, productivity, commission_dsi, trad_scheme, dsi_scheme, saving_amount, 
        #               saving_percentage, current_perception, current_perception_dsi, increment, increment_percentage]
        test_data = [
            [5000.0, 3000.0, 1500.0, 200.0, 5500.0, 4700.0, 800.0, 14.55, 4500.0, 4700.0, 200.0, 4.44],
            [6000.0, 3500.0, 2000.0, 250.0, 6600.0, 5750.0, 850.0, 12.88, 5400.0, 5750.0, 350.0, 6.48],
        ]
        
        result = TotalCalculator.calculate_saving_totals(test_data)
        
        self.assertEqual(result["total_salary"], 11000.0)
        self.assertEqual(result["total_wage_and_salary_dsi"], 6500.0)
        self.assertEqual(result["total_productivity"], 3500.0)
        self.assertEqual(result["total_commission_dsi"], 450.0)
        self.assertEqual(result["total_traditional_scheme"], 12100.0)
        self.assertEqual(result["total_dsi_scheme"], 10450.0)
        self.assertEqual(result["total_saving_amount"], 1650.0)
        self.assertEqual(result["total_current_perception"], 9900.0)
        self.assertEqual(result["total_current_perception_dsi"], 10450.0)
        self.assertEqual(result["total_increment"], 550.0)
        self.assertAlmostEqual(result["avg_saving_percentage"], 13.715, places=3)
        self.assertAlmostEqual(result["avg_increment_percentage"], 5.46, places=2)

    def test_format_totals_table(self):
        """Test the formatting of totals into a table."""
        test_totals = {
            "total_salary": 10000.0,
            "total_tax": 1500.0,
            "avg_percentage": 15.5
        }
        
        # Test without percentage fields or column references
        result = TotalCalculator.format_totals_table(test_totals)
        expected = [
            ["Total Salary", 10000.0, ""],
            ["Total Tax", 1500.0, ""],
            ["Avg Percentage", 15.5, ""]
        ]
        self.assertEqual(result, expected)
        
        # Test with percentage fields
        result = TotalCalculator.format_totals_table(test_totals, ["avg_percentage"])
        expected = [
            ["Total Salary", 10000.0, ""],
            ["Total Tax", 1500.0, ""],
            ["Avg Percentage", "15.50%", ""]
        ]
        self.assertEqual(result, expected)
        
        # Test with column references
        column_refs = {
            "total_salary": "Col. A",
            "total_tax": "Col. B"
        }
        result = TotalCalculator.format_totals_table(test_totals, ["avg_percentage"], column_refs)
        expected = [
            ["Total Salary", 10000.0, "Col. A"],
            ["Total Tax", 1500.0, "Col. B"],
            ["Avg Percentage", "15.50%", ""]
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()