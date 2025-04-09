import pytest
from src.isr import ISR
from src.employees import Employee
from src.parameters import Parameters


class TestISR:
    @pytest.fixture
    def employee(self):
        # Fixture que crea una instancia de Employee con un salario base para las pruebas
        return Employee(5710.64)

    @pytest.fixture
    def isr_calculator(self, employee):
        # Fixture que crea una instancia de ISR con un salario mensual y período de pago
        return ISR(5710.64, 15, employee)

    @pytest.fixture
    def high_salary_calculator(self, employee):
        # Fixture para probar con un salario alto
        return ISR(50000.00, 15, employee)

    @pytest.fixture
    def zero_salary_calculator(self, employee):
        # Fixture para probar con un salario cero
        return ISR(0, 15, employee)

    def test_get_isr_table(self, isr_calculator):
        # Verifica que se obtenga la tabla ISR correcta según el período de pago
        isr_table = isr_calculator.get_isr_table()
        assert isinstance(isr_table, list)
        assert len(isr_table) > 0
        # Verificar que cada elemento de la tabla tenga la estructura correcta
        for row in isr_table:
            assert 'lower_limit' in row
            assert 'percentage' in row
            assert 'fixed_fee' in row

    def test_get_lower_limit(self, isr_calculator):
        # Verifica que se obtenga el límite inferior correcto para el salario mensual
        lower_limit = isr_calculator.get_lower_limit()
        assert isinstance(lower_limit, (int, float))
        assert lower_limit <= isr_calculator.monthly_salary

    def test_get_surplus(self, isr_calculator):
        # Verifica que el excedente se calcule correctamente
        surplus = isr_calculator.get_surplus()
        expected = isr_calculator.monthly_salary - isr_calculator.get_lower_limit()
        assert surplus == expected

    def test_get_percentage_applied_to_excess(self, isr_calculator):
        # Verifica que se obtenga el porcentaje correcto para aplicar al excedente
        percentage = isr_calculator.get_percentage_applied_to_excess()
        assert isinstance(percentage, (int, float))
        assert 0 <= percentage <= 1  # El porcentaje debe estar entre 0 y 1

    def test_get_surplus_tax(self, isr_calculator):
        # Verifica que el impuesto sobre el excedente se calcule correctamente
        surplus_tax = isr_calculator.get_surplus_tax()
        expected = isr_calculator.get_surplus() * isr_calculator.get_percentage_applied_to_excess()
        assert surplus_tax == expected

    def test_get_fixed_fee(self, isr_calculator):
        # Verifica que se obtenga la cuota fija correcta
        fixed_fee = isr_calculator.get_fixed_fee()
        assert isinstance(fixed_fee, (int, float))
        assert fixed_fee >= 0  # La cuota fija debe ser no negativa

    def test_get_total_tax(self, isr_calculator):
        # Verifica que el impuesto total se calcule correctamente
        total_tax = isr_calculator.get_total_tax()
        expected = isr_calculator.get_surplus_tax() + isr_calculator.get_fixed_fee()
        assert total_tax == expected

    def test_high_salary_calculations(self, high_salary_calculator):
        # Verifica los cálculos con un salario alto
        assert high_salary_calculator.get_lower_limit() <= high_salary_calculator.monthly_salary
        assert high_salary_calculator.get_surplus() > 0
        assert high_salary_calculator.get_total_tax() > 0

    def test_zero_salary_calculations(self, zero_salary_calculator):
        # Verifica los cálculos con un salario cero
        lower_limit = zero_salary_calculator.get_lower_limit()
        if lower_limit is None:
            assert zero_salary_calculator.get_surplus() == 0
        else:
            assert lower_limit <= 0
            
        assert zero_salary_calculator.get_surplus() == 0
        
        # Si el salario es cero, el impuesto debería ser cero o None
        total_tax = zero_salary_calculator.get_total_tax()
        if total_tax is not None:  # Si devuelve un valor numérico
            assert total_tax == 0

    def test_different_payment_periods(self):
        # Verifica que se obtengan tablas ISR diferentes para distintos períodos de pago
        employee = Employee(5710.64)
        isr_15 = ISR(5710.64, 15, employee)
        isr_30 = ISR(5710.64, 30, employee)
        
        table_15 = isr_15.get_isr_table()
        table_30 = isr_30.get_isr_table()
        
        # Las tablas deben ser diferentes para diferentes períodos de pago
        assert table_15 != table_30

    def test_initialization(self, isr_calculator):
        # Verifica que la inicialización de la clase ISR sea correcta
        assert isr_calculator.monthly_salary == 5710.64
        assert isr_calculator.payment_period == 15
        assert isinstance(isr_calculator.employee, Employee)
        assert isinstance(isr_calculator.parameters, Parameters)
        assert hasattr(isr_calculator, 'SALARY_CREDIT_TABLE')
        assert isinstance(isr_calculator.SALARY_CREDIT_TABLE, list)

    def test_tax_calculation_consistency(self, isr_calculator):
        # Verifica que los cálculos sean consistentes
        # El impuesto total debe ser mayor que cero para un salario positivo
        assert isr_calculator.get_total_tax() > 0
        
        # El impuesto total debe ser mayor que la cuota fija
        assert isr_calculator.get_total_tax() >= isr_calculator.get_fixed_fee()
        
        # El impuesto sobre el excedente debe ser proporcional al excedente
        assert isr_calculator.get_surplus_tax() == isr_calculator.get_surplus() * isr_calculator.get_percentage_applied_to_excess()
    
    # Nuevas pruebas para los métodos adicionales
    
    def test_get_isr(self, isr_calculator):
        # Verifica que get_isr devuelva el mismo valor que get_total_tax
        assert isr_calculator.get_isr() == isr_calculator.get_total_tax()
    
    def test_get_range_credit_to_salary(self, isr_calculator):
        # Verifica que se obtenga un rango de crédito válido
        range_credit = isr_calculator.get_range_credit_to_salary()
        assert isinstance(range_credit, (int, float)) or range_credit is None
        if range_credit is not None:
            assert range_credit <= isr_calculator.monthly_salary
    
    def test_get_salary_credit(self, isr_calculator):
        # Verifica que se obtenga un crédito salarial válido
        credit = isr_calculator.get_salary_credit()
        assert isinstance(credit, (int, float))
        assert credit >= 0
        
        # Verificar que el crédito corresponda al rango correcto
        range_credit = isr_calculator.get_range_credit_to_salary()
        if range_credit is not None:
            for row in isr_calculator.SALARY_CREDIT_TABLE:
                if row['lower_limit'] == range_credit:
                    assert credit == row['credit']
                    break
    
    def test_get_tax_payable(self, isr_calculator):
        # Verifica el cálculo del impuesto a cargo
        isr = isr_calculator.get_isr()
        credit = isr_calculator.get_salary_credit()
        
        if isr > credit:
            expected = isr - credit
        else:
            expected = 0
            
        assert isr_calculator.get_tax_payable() == expected
    
    def test_get_tax_in_favor(self, isr_calculator):
        # Verifica el cálculo del impuesto a favor
        isr = isr_calculator.get_isr()
        credit = isr_calculator.get_salary_credit()
        
        if isr < credit:
            expected = credit - isr
        else:
            expected = 0
            
        assert isr_calculator.get_tax_in_favor() == expected
    
    def test_tax_payable_and_in_favor_are_mutually_exclusive(self, isr_calculator):
        # Verifica que no se pueda tener impuesto a cargo e impuesto a favor al mismo tiempo
        tax_payable = isr_calculator.get_tax_payable()
        tax_in_favor = isr_calculator.get_tax_in_favor()
        
        # Al menos uno de ellos debe ser cero
        assert tax_payable == 0 or tax_in_favor == 0
        
        # Si el ISR es mayor que el crédito, debe haber impuesto a cargo
        if isr_calculator.get_isr() > isr_calculator.get_salary_credit():
            assert tax_payable > 0
            assert tax_in_favor == 0
        
        # Si el ISR es menor que el crédito, debe haber impuesto a favor
        if isr_calculator.get_isr() < isr_calculator.get_salary_credit():
            assert tax_in_favor > 0
            assert tax_payable == 0
    
    def test_edge_cases_for_salary_credit(self):
        # Prueba con salarios en los límites de los rangos de crédito
        employee = Employee(0)
        
        # Probar con el límite inferior del primer rango
        isr_min = ISR(0.01, 15, employee)
        assert isr_min.get_range_credit_to_salary() is not None
        assert isr_min.get_salary_credit() > 0
        
        # Probar con un salario muy alto (más allá del último rango)
        isr_max = ISR(100000, 15, employee)
        assert isr_max.get_range_credit_to_salary() is not None
        assert isr_max.get_salary_credit() >= 0