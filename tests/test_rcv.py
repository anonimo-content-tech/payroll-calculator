import pytest
from src.rcv import RCV
from src.parameters import Parameters
from src.employees import Employee

class TestRCV:
    @pytest.fixture
    def rcv_calculator(self):
        return RCV(399.48)  # Using a common daily integrated wage for testing

    @pytest.fixture
    def high_wage_calculator(self):
        return RCV(3000.00)  # Using a high daily integrated wage for testing

    def test_init_parameters(self, rcv_calculator):
        assert rcv_calculator.daily_integrated_wage == 399.48
        assert rcv_calculator.days == Employee.PAYMENT_PERIOD
        assert isinstance(rcv_calculator.parameters, Parameters)

    def test_get_retirement_percentage_normal_wage(self, rcv_calculator):
        percentage = rcv_calculator.get_retirement_percentage()
        assert percentage == Parameters.get_retirement_percentage(399.48)

    def test_get_retirement_percentage_high_wage(self, high_wage_calculator):
        percentage = high_wage_calculator.get_retirement_percentage()
        assert percentage == Parameters.get_retirement_percentage(3000.00)

    def test_get_quota_employer_normal_wage(self, rcv_calculator):
        expected = (399.48 * Parameters.get_retirement_percentage(399.48)) * Employee.PAYMENT_PERIOD
        assert round(rcv_calculator.get_quota_employer(), 2) == round(expected, 2)

    def test_get_quota_employer_high_wage(self, high_wage_calculator):
        expected = (3000.00 * Parameters.get_retirement_percentage(3000.00)) * Employee.PAYMENT_PERIOD
        assert round(high_wage_calculator.get_quota_employer(), 2) == round(expected, 2)

    def test_zero_wage(self):
        zero_calculator = RCV(0)
        assert zero_calculator.get_retirement_percentage() == Parameters.get_retirement_percentage(0)
        assert zero_calculator.get_quota_employer() == 0

    def test_negative_wage(self):
        negative_calculator = RCV(-100)
        assert negative_calculator.get_retirement_percentage() == Parameters.get_retirement_percentage(-100)
        assert negative_calculator.get_quota_employer() == 0

    @pytest.mark.parametrize("wage,expected_days", [
        (399.48, 15),  # Normal case
        (3000.00, 15),  # High wage
        (0, 15),       # Zero wage
        (-100, 15),    # Negative wage
    ])
    def test_payment_period(self, wage, expected_days):
        calculator = RCV(wage)
        assert calculator.days == expected_days