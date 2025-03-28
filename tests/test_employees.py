import pytest
from src.employees import Employee

class TestEmployee:
    @pytest.fixture
    def employee(self):
        return Employee(5710.64)

    def test_daily_salary_calculation(self, employee):
        expected_daily_salary = 5710.64 / 15
        assert round(employee.calculate_salary_dialy(), 2) == 380.71

    def test_payment_period_constant(self):
        assert Employee.PAYMENT_PERIOD == 15