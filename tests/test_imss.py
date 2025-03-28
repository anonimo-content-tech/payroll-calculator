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
