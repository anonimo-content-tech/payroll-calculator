import pytest
from src.imss import IMSS
from src.parameters import Parameters
from src.employees import Employee
import math

class TestIMSSCalculations:
    @pytest.fixture
    def imss_calculator(self):
        return IMSS(5710.64, payment_period=15)

    @pytest.fixture
    def high_salary_calculator(self):
        # Salario alto para probar casos límite
        return IMSS(50000.00, payment_period=15)

    def test_integrated_daily_wage(self, imss_calculator):
        expected_daily_wage = (5710.64 / 15) * Parameters.INTEGRATION_FACTOR
        assert round(imss_calculator.get_integrated_daily_wage(), 2) == 399.48

    def test_salary_cap_25_smg(self, imss_calculator):
        # Since the integrated daily wage (399.48) is less than the contribution ceiling (2828.5),
        # it should return the integrated daily wage
        assert round(imss_calculator.get_salary_cap_25_smg(), 2) == 399.48

    def test_diseases_and_maternity_employer_quota(self, imss_calculator):
        # Formula: VSDF * days * fixed_fee
        expected_quota = Parameters.VSDF * Employee.PAYMENT_PERIOD * Parameters.FIXED_FEE
        assert round(imss_calculator.get_diseases_and_maternity_employer_quota(), 2) == 346.21

    def test_diseases_and_maternity_employer_surplus(self, imss_calculator):
        # Since the integrated daily wage (399.48) is less than TCF (339.42),
        # it should return the surplus calculation
        daily_wage = imss_calculator.get_integrated_daily_wage()
        if daily_wage > imss_calculator.tcf:
            expected_surplus = ((daily_wage - imss_calculator.tcf) * imss_calculator.surplus_employer) * imss_calculator.days
            assert round(imss_calculator.get_diseases_and_maternity_employer_surplus(), 2) == round(expected_surplus, 2)
        else:
            assert imss_calculator.get_diseases_and_maternity_employer_surplus() == 0

    def test_integration_factor(self, imss_calculator):
        assert imss_calculator.get_integration_factor() == Parameters.INTEGRATION_FACTOR

    def test_employer_cash_benefits(self, imss_calculator):
        salary_cap = imss_calculator.get_salary_cap_25_smg()
        expected = (salary_cap * Parameters.CASH_BENEFITS_EMPLOYER) * Employee.PAYMENT_PERIOD
        assert round(imss_calculator.get_employer_cash_benefits(), 2) == round(expected, 2)

    def test_employee_cash_benefits(self, imss_calculator):
        salary_cap = imss_calculator.get_salary_cap_25_smg()
        expected = (salary_cap * Parameters.CASH_BENEFITS_EMPLOYEE) * Employee.PAYMENT_PERIOD
        assert round(imss_calculator.get_employee_cash_benefits(), 2) == round(expected, 2)

    def test_benefits_in_kind_medical_expenses_employer(self, imss_calculator):
        salary_cap = imss_calculator.get_salary_cap_25_smg()
        expected = (salary_cap * Parameters.BENEFITS_IN_KIND_EMPLOYER) * Employee.PAYMENT_PERIOD
        assert round(imss_calculator.get_benefits_in_kind_medical_expenses_employer(), 2) == round(expected, 2)

    def test_occupational_risks_employer(self, imss_calculator):
        salary_cap = imss_calculator.get_salary_cap_25_smg()
        expected = Employee.PAYMENT_PERIOD * salary_cap * Parameters.get_risk_percentage('I')
        assert round(imss_calculator.get_occupational_risks_employer(), 2) == round(expected, 2)

    def test_occupational_risks_employer_with_different_risk_classes(self):
        # Testing with risk class III as an example
        imss = IMSS(5710.64, 'III')
        salary_cap = imss.get_salary_cap_25_smg()
        risk_percentage = Parameters.get_risk_percentage('III')
        expected = Employee.PAYMENT_PERIOD * salary_cap * risk_percentage
        assert round(imss.get_occupational_risks_employer(), 2) == round(expected, 2)

    def test_salary_cap_25_smg_2(self, imss_calculator):
        daily_wage = imss_calculator.get_integrated_daily_wage()
        expected = min(daily_wage, Parameters.CONTRIBUTION_CEILING_2)
        assert round(imss_calculator.get_salary_cap_25_smg_2(), 2) == round(expected, 2)

    def test_invalidity_and_retirement_employer(self, imss_calculator):
        salary_cap = imss_calculator.get_salary_cap_25_smg_2()
        expected = (salary_cap * Parameters.INVALIDITY_AND_RETIREMENT_EMPLOYER) * Employee.PAYMENT_PERIOD
        assert round(imss_calculator.get_invalidity_and_retirement_employer(), 2) == round(expected, 2)

    def test_childcare_employer(self, imss_calculator):
        salary_cap = imss_calculator.get_salary_cap_25_smg()
        expected = Parameters.CHILDCARE * salary_cap * Employee.PAYMENT_PERIOD
        assert round(imss_calculator.get_childcare_employer(), 2) == round(expected, 2)

    def test_quota_employer(self, imss_calculator):
        expected = (
            imss_calculator.get_diseases_and_maternity_employer_quota() +
            imss_calculator.get_diseases_and_maternity_employer_surplus() +
            imss_calculator.get_employer_cash_benefits() +
            imss_calculator.get_benefits_in_kind_medical_expenses_employer() +
            imss_calculator.get_occupational_risks_employer() +
            imss_calculator.get_invalidity_and_retirement_employer() +
            imss_calculator.get_childcare_employer()
        )
        assert round(imss_calculator.get_quota_employer(), 2) == round(expected, 2)

    def test_calculate_benefit_above_smg(self, imss_calculator):
        salary_cap = 400.0  # Mayor que SMG
        employer_rate = 0.01
        employee_rate = 0.005
        expected = (salary_cap * employer_rate) * Employee.PAYMENT_PERIOD
        result = imss_calculator._calculate_benefit(salary_cap, employer_rate, employee_rate)
        assert round(result, 2) == round(expected, 2)

    def test_calculate_benefit_below_smg(self, imss_calculator):
        salary_cap = 50.0  # Menor que SMG
        employer_rate = 0.01
        employee_rate = 0.005
        expected = (salary_cap * (employer_rate + employee_rate)) * Employee.PAYMENT_PERIOD
        result = imss_calculator._calculate_benefit(salary_cap, employer_rate, employee_rate)
        assert round(result, 2) == round(expected, 2)

    def test_high_salary_cap_25_smg(self, high_salary_calculator):
        # Debe retornar el tope máximo cuando el salario excede el límite
        assert round(high_salary_calculator.get_salary_cap_25_smg(), 2) == Parameters.CONTRIBUTION_CEILING

    def test_high_salary_cap_25_smg_2(self, high_salary_calculator):
        # Debe retornar el tope máximo cuando el salario excede el límite
        assert round(high_salary_calculator.get_salary_cap_25_smg_2(), 2) == Parameters.CONTRIBUTION_CEILING_2

    def test_zero_salary_diseases_and_maternity(self):
        zero_salary_calculator = IMSS(0, payment_period=15)
        assert zero_salary_calculator.get_diseases_and_maternity_employer_quota() == 0

    def test_zero_salary_employee_benefits(self):
        # Prueba para verificar cálculos con salario cero para beneficios del empleado
        zero_salary_calculator = IMSS(0, payment_period=15)
        assert zero_salary_calculator.get_diseases_and_maternity_employee_surplus() == 0
        assert zero_salary_calculator.get_benefits_in_kind_medical_expenses_employee() == 0
        assert zero_salary_calculator.get_invalidity_and_retirement_employee() == 0
        assert zero_salary_calculator.get_quota_employee() == 0

    def test_smg_threshold_employee_benefits(self):
        # Prueba para verificar cálculos cuando el salario es exactamente igual al SMG
        smg_salary = Parameters.SMG * 15 / Parameters.INTEGRATION_FACTOR  # Ajuste para obtener el salario integrado exacto
        smg_salary_calculator = IMSS(smg_salary, payment_period=15)
        
        # Verificamos que el salario diario integrado sea igual al SMG
        assert round(smg_salary_calculator.get_integrated_daily_wage(), 2) == round(Parameters.SMG, 2)
        
        # Las prestaciones deben ser cero cuando el salario es igual al SMG
        assert smg_salary_calculator.get_benefits_in_kind_medical_expenses_employee() == 0
        assert smg_salary_calculator.get_invalidity_and_retirement_employee() == 0

    def test_tcf_threshold_employee_surplus(self):
        # Prueba para verificar cálculos cuando el salario es igual al TCF
        tcf_salary = Parameters.TCF * 15 / Parameters.INTEGRATION_FACTOR
        tcf_calculator = IMSS(tcf_salary, payment_period=15)
        assert tcf_calculator.get_diseases_and_maternity_employee_surplus() == 0

    def test_zero_salary_rcv(self):
        zero_salary_calculator = IMSS(0, payment_period=15)
        assert zero_salary_calculator.get_retirement_employer() == 0
        assert zero_salary_calculator.get_severance_and_old_age_employer() == 0
        assert zero_salary_calculator.get_total_rcv_employer() == 0

    def test_zero_salary_employer_totals(self):
        zero_salary_calculator = IMSS(0, payment_period=15)
        assert zero_salary_calculator.get_infonavit_employer() == 0
        assert zero_salary_calculator.get_tax_payroll() == 0
        assert zero_salary_calculator.get_total_employer() == 0

    def test_zero_salary_rcv_employee(self):
        zero_salary_calculator = IMSS(0, payment_period=15)
        assert zero_salary_calculator.get_severance_and_old_age_employee() == 0
        assert zero_salary_calculator.get_total_rcv_employee() == 0
        assert zero_salary_calculator.get_total_employee() == 0

    def test_smg_threshold_rcv_employee(self):
        smg_salary = Parameters.SMG * 15 / Parameters.INTEGRATION_FACTOR
        smg_calculator = IMSS(smg_salary, payment_period=15)
        assert smg_calculator.get_severance_and_old_age_employee() == 0
        assert smg_calculator.get_total_rcv_employee() == 0

    def test_init_parameters(self, imss_calculator):
        assert imss_calculator.days == Employee.PAYMENT_PERIOD
        assert imss_calculator.integration_factor == Parameters.INTEGRATION_FACTOR
        assert imss_calculator.fixed_fee == Parameters.FIXED_FEE
        assert imss_calculator.risk_percentage == Parameters.get_risk_percentage('I')

    @pytest.mark.parametrize("risk_class,expected_percentage", [
        ('I', Parameters.get_risk_percentage('I')),
        ('II', Parameters.get_risk_percentage('II')),
        ('III', Parameters.get_risk_percentage('III')),
        ('IV', Parameters.get_risk_percentage('IV')),
        ('V', Parameters.get_risk_percentage('V'))
    ])
    def test_risk_percentage_initialization(self, risk_class, expected_percentage):
        calculator = IMSS(5710.64, risk_class)
        assert calculator.risk_percentage == expected_percentage

    def test_diseases_and_maternity_employer_surplus_edge_case(self, imss_calculator):
        # Caso donde el salario es exactamente igual al TCF
        original_salary = imss_calculator.get_salary_cap_25_smg()
        imss_calculator.tcf = original_salary
        assert imss_calculator.get_diseases_and_maternity_employer_surplus() == 0

    def test_quota_employer_components(self, imss_calculator):
        total_quota = imss_calculator.get_quota_employer()
        components = [
            imss_calculator.get_diseases_and_maternity_employer_quota(),
            imss_calculator.get_diseases_and_maternity_employer_surplus(),
            imss_calculator.get_employer_cash_benefits(),
            imss_calculator.get_benefits_in_kind_medical_expenses_employer(),
            imss_calculator.get_occupational_risks_employer(),
            imss_calculator.get_invalidity_and_retirement_employer(),
            imss_calculator.get_childcare_employer()
        ]
        assert round(total_quota, 2) == round(sum(components), 2)

    def test_diseases_and_maternity_employee_surplus(self, imss_calculator):
        salary_cap_25_smg = imss_calculator.get_salary_cap_25_smg()
        expected = ((salary_cap_25_smg - imss_calculator.tcf) * imss_calculator.surplus_employee * imss_calculator.days) if salary_cap_25_smg > imss_calculator.tcf else 0
        assert round(imss_calculator.get_diseases_and_maternity_employee_surplus(), 2) == round(expected, 2)

    def test_benefits_in_kind_medical_expenses_employee(self, imss_calculator):
        salary_cap_25_smg = imss_calculator.get_salary_cap_25_smg()
        expected = ((salary_cap_25_smg * imss_calculator.benefits_in_kind_employee) * imss_calculator.days) if salary_cap_25_smg > imss_calculator.smg else 0
        assert round(imss_calculator.get_benefits_in_kind_medical_expenses_employee(), 2) == round(expected, 2)

    def test_invalidity_and_retirement_employee(self, imss_calculator):
        salary_cap_25_smg_2 = imss_calculator.get_salary_cap_25_smg_2()
        expected = ((salary_cap_25_smg_2 * imss_calculator.invalidity_and_retirement_employee) * imss_calculator.days) if salary_cap_25_smg_2 > imss_calculator.smg else 0
        assert round(imss_calculator.get_invalidity_and_retirement_employee(), 2) == round(expected, 2)

    def test_quota_employee(self, imss_calculator):
        expected = sum([
            imss_calculator.get_diseases_and_maternity_employee_surplus(),
            imss_calculator.get_employee_cash_benefits(),
            imss_calculator.get_benefits_in_kind_medical_expenses_employee(),
            imss_calculator.get_invalidity_and_retirement_employee()
        ])
        assert round(imss_calculator.get_quota_employee(), 2) == round(expected, 2)

    def test_total_imss(self, imss_calculator):
        expected = imss_calculator.get_quota_employer() + imss_calculator.get_quota_employee()
        assert round(imss_calculator.get_total_imss(), 2) == round(expected, 2)

    def test_high_salary_employee_benefits(self, high_salary_calculator):
        # Prueba para verificar cálculos con salario alto para beneficios del empleado
        salary_cap = high_salary_calculator.get_salary_cap_25_smg()
        assert salary_cap == Parameters.CONTRIBUTION_CEILING
        expected = (salary_cap * Parameters.BENEFITS_IN_KIND_EMPLOYEE * Employee.PAYMENT_PERIOD)
        assert round(high_salary_calculator.get_benefits_in_kind_medical_expenses_employee(), 2) == round(expected, 2)

    def test_zero_salary_employee_benefits(self):
        # Prueba para verificar cálculos con salario cero para beneficios del empleado
        zero_salary_calculator = IMSS(0, payment_period=15)
        assert zero_salary_calculator.get_diseases_and_maternity_employee_surplus() == 0
        assert zero_salary_calculator.get_benefits_in_kind_medical_expenses_employee() == 0
        assert zero_salary_calculator.get_invalidity_and_retirement_employee() == 0
        assert zero_salary_calculator.get_quota_employee() == 0

    def test_smg_threshold_employee_benefits(self):
        # Prueba para verificar cálculos cuando el salario es exactamente igual al SMG
        smg_salary = Parameters.SMG * 15 / Parameters.INTEGRATION_FACTOR  # Ajuste para obtener el salario integrado exacto
        smg_salary_calculator = IMSS(smg_salary, payment_period=15)
        
        # Verificamos que el salario diario integrado sea igual al SMG
        assert round(smg_salary_calculator.get_integrated_daily_wage(), 2) == round(Parameters.SMG, 2)
        
        # Las prestaciones deben ser cero cuando el salario es igual al SMG
        assert smg_salary_calculator.get_benefits_in_kind_medical_expenses_employee() == 0
        assert smg_salary_calculator.get_invalidity_and_retirement_employee() == 0

    def test_tcf_threshold_employee_surplus(self):
        # Prueba para verificar cálculos cuando el salario es igual al TCF
        tcf_salary = Parameters.TCF * 15 / Parameters.INTEGRATION_FACTOR
        tcf_calculator = IMSS(tcf_salary, payment_period=15)
        assert tcf_calculator.get_diseases_and_maternity_employee_surplus() == 0

    def test_retirement_employer(self, imss_calculator):
        salary_cap = imss_calculator.get_salary_cap_25_smg()
        expected = salary_cap * Employee.PAYMENT_PERIOD * Parameters.RETIREMENT_EMPLOYER
        assert round(imss_calculator.get_retirement_employer(), 2) == round(expected, 2)

    def test_severance_and_old_age_employer(self, imss_calculator):
        # First call to initialize RCV
        result = imss_calculator.get_severance_and_old_age_employer()
        # Verify RCV was initialized
        assert imss_calculator.rcv is not None
        # Verify the result matches RCV employer quota
        assert round(result, 2) == round(imss_calculator.rcv.get_quota_employer(), 2)

    def test_total_rcv_employer(self, imss_calculator):
        expected = (
            imss_calculator.get_retirement_employer() +
            imss_calculator.get_severance_and_old_age_employer()
        )
        assert round(imss_calculator.get_total_rcv_employer(), 2) == round(expected, 2)

    def test_rcv_initialization(self, imss_calculator):
        # RCV should be None initially
        assert imss_calculator.rcv is None
        # After calling any RCV-related method, it should be initialized
        imss_calculator.get_severance_and_old_age_employer()
        assert imss_calculator.rcv is not None

    def test_high_salary_rcv(self, high_salary_calculator):
        # Test RCV calculations with a high salary
        result = high_salary_calculator.get_total_rcv_employer()
        assert result > 0
        # Verify it's using the salary cap
        assert round(high_salary_calculator.get_salary_cap_25_smg(), 2) == Parameters.CONTRIBUTION_CEILING

    def test_zero_salary_rcv(self):
        zero_salary_calculator = IMSS(0, payment_period=15)
        assert zero_salary_calculator.get_retirement_employer() == 0
        assert zero_salary_calculator.get_severance_and_old_age_employer() == 0
        assert zero_salary_calculator.get_total_rcv_employer() == 0

    def test_infonavit_employer(self, imss_calculator):
        salary_cap = imss_calculator.get_salary_cap_25_smg_2()
        expected = salary_cap * Employee.PAYMENT_PERIOD * Parameters.INFONAVIT_EMPLOYER
        assert round(imss_calculator.get_infonavit_employer(), 2) == round(expected, 2)

    def test_tax_payroll(self, imss_calculator):
        expected = imss_calculator.total_salary * Parameters.STATE_PAYROLL_TAX
        assert round(imss_calculator.get_tax_payroll(), 2) == round(expected, 2)

    def test_total_employer(self, imss_calculator):
        expected = (
            imss_calculator.get_quota_employer() +
            imss_calculator.get_total_rcv_employer() +
            imss_calculator.get_infonavit_employer() +
            imss_calculator.get_tax_payroll()
        )
        assert round(imss_calculator.get_total_employer(), 2) == round(expected, 2)

    def test_high_salary_infonavit(self, high_salary_calculator):
        # Should use the contribution ceiling for high salaries
        salary_cap = high_salary_calculator.get_salary_cap_25_smg_2()
        assert salary_cap == Parameters.CONTRIBUTION_CEILING_2
        expected = salary_cap * Employee.PAYMENT_PERIOD * Parameters.INFONAVIT_EMPLOYER
        assert round(high_salary_calculator.get_infonavit_employer(), 2) == round(expected, 2)

    def test_zero_salary_employer_totals(self):
        zero_salary_calculator = IMSS(0, payment_period=15)
        assert zero_salary_calculator.get_infonavit_employer() == 0
        assert zero_salary_calculator.get_tax_payroll() == 0
        assert zero_salary_calculator.get_total_employer() == 0

    def test_total_employer_components(self, imss_calculator):
        total = imss_calculator.get_total_employer()
        components = [
            imss_calculator.get_quota_employer(),
            imss_calculator.get_total_rcv_employer(),
            imss_calculator.get_infonavit_employer(),
            imss_calculator.get_tax_payroll()
        ]
        assert round(total, 2) == round(sum(components), 2)

    def test_severance_and_old_age_employee(self, imss_calculator):
        salary_cap = imss_calculator.get_salary_cap_25_smg_2()
        expected = (salary_cap * Parameters.SEVERANCE_AND_OLD_AGE_EMPLOYEE * Employee.PAYMENT_PERIOD) if salary_cap > imss_calculator.smg else 0
        assert round(imss_calculator.get_severance_and_old_age_employee(), 2) == round(expected, 2)

    def test_total_rcv_employee(self, imss_calculator):
        expected = imss_calculator.get_severance_and_old_age_employee()
        assert round(imss_calculator.get_total_rcv_employee(), 2) == round(expected, 2)

    def test_total_employee(self, imss_calculator):
        expected = imss_calculator.get_quota_employee() + imss_calculator.get_total_rcv_employee()
        assert round(imss_calculator.get_total_employee(), 2) == round(expected, 2)

    def test_total_social_cost(self, imss_calculator):
        expected = imss_calculator.get_total_employer() + imss_calculator.get_total_employee()
        assert round(imss_calculator.get_total_social_cost(), 2) == round(expected, 2)

    def test_increment(self, imss_calculator):
        expected = imss_calculator.get_total_social_cost() * Parameters.INCREASE
        assert round(imss_calculator.get_increment(), 2) == round(expected, 2)

    def test_total_social_cost_suggested(self, imss_calculator):
        expected = math.ceil(imss_calculator.get_total_social_cost() + imss_calculator.get_increment())
        assert imss_calculator.get_total_social_cost_suggested() == expected

    def test_high_salary_rcv_employee(self, high_salary_calculator):
        salary_cap = high_salary_calculator.get_salary_cap_25_smg_2()
        assert salary_cap == Parameters.CONTRIBUTION_CEILING_2
        expected = salary_cap * Parameters.SEVERANCE_AND_OLD_AGE_EMPLOYEE * Employee.PAYMENT_PERIOD
        assert round(high_salary_calculator.get_severance_and_old_age_employee(), 2) == round(expected, 2)

    def test_zero_salary_rcv_employee(self):
        zero_salary_calculator = IMSS(0, payment_period=15)
        assert zero_salary_calculator.get_severance_and_old_age_employee() == 0
        assert zero_salary_calculator.get_total_rcv_employee() == 0
        assert zero_salary_calculator.get_total_employee() == 0

    def test_smg_threshold_rcv_employee(self):
        smg_salary = Parameters.SMG * 15 / Parameters.INTEGRATION_FACTOR
        smg_calculator = IMSS(smg_salary, payment_period=15)
        assert smg_calculator.get_severance_and_old_age_employee() == 0
        assert smg_calculator.get_total_rcv_employee() == 0
