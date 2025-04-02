import pytest
from src.employees import Employee

class TestEmployee:
    @pytest.fixture
    def employee(self):
        # Fixture que crea una instancia de Employee con un salario base para las pruebas
        return Employee(5710.64)

    def test_daily_salary_calculation(self, employee):
        # Verifica que el cálculo del salario diario sea correcto
        # dividiendo el salario base entre el período de pago (15 días)
        expected_daily_salary = 5710.64 / 15
        assert round(employee.calculate_salary_dialy(), 2) == 380.71

    def test_payment_period_constant(self):
        # Verifica que el período de pago esté configurado correctamente como 15 días
        assert Employee.PAYMENT_PERIOD == 15

    def test_employee_with_christmas_bonus(self):
        # Verifica que el bono navideño se asigne correctamente al crear un empleado
        employee = Employee(5710.64, christmas_bonus=1000)
        assert employee.christmas_bonus == 1000

    def test_calculate_total_salary_without_bonus(self, employee):
        # Verifica el cálculo del salario total cuando no hay bono navideño
        assert employee.calculate_total_salary() == 5710.64

    def test_calculate_total_salary_with_bonus(self):
        # Verifica el cálculo del salario total incluyendo el bono navideño
        employee = Employee(5710.64, christmas_bonus=1000)
        assert employee.calculate_total_salary() == 6710.64