import pytest
from src.imss import IMSS
from src.parameters import Parameters
from src.employees import Employee

class TestIMSSCalculations:
    @pytest.fixture
    def imss_calculator(self):
        return IMSS(5710.64)

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
            expected_surplus = ((daily_wage - imss_calculator.tcf) * imss_calculator.surplus) * imss_calculator.days
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
