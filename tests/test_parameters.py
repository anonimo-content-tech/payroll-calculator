import pytest
from src.parameters import Parameters

class TestParameters:
    def test_parameters_constants(self):
        params = Parameters()
        assert params.INTEGRATION_FACTOR == 1.0493
        assert params.VSDF == 113.14
        assert params.CONTRIBUTION_CEILING == params.VSDF * 25
        assert params.FIXED_FEE == 0.204
        assert params.SURPLUS_EMPLOYER == 0.011
        assert params.SURPLUS_EMPLOYEE == 0.004
        assert params.SMG == 278.80
        assert params.TCF == params.VSDF * 3
        assert params.CONTRIBUTION_CEILING_2 == params.VSDF * 25

    def test_benefit_constants(self):
        params = Parameters()
        assert params.CASH_BENEFITS_EMPLOYER == 0.0070
        assert params.CASH_BENEFITS_EMPLOYEE == 0.0025
        assert params.BENEFITS_IN_KIND_EMPLOYER == 0.0105
        assert params.BENEFITS_IN_KIND_EMPLOYEE == 0.00375
        assert params.INVALIDITY_AND_RETIREMENT_EMPLOYER == 0.0175
        assert params.INVALIDITY_AND_RETIREMENT_EMPLOYEE == 0.00625
        assert params.CHILDCARE == 0.01

    def test_parameters_initialization(self):
        params = Parameters()
        assert params.integration_factor == Parameters.INTEGRATION_FACTOR
        assert params.vsdf == Parameters.VSDF

    def test_risk_levels_dictionary(self):
        assert Parameters.RISK_LEVELS['I'] == 0.0054355
        assert Parameters.RISK_LEVELS['II'] == 0.0113065
        assert Parameters.RISK_LEVELS['III'] == 0.025984
        assert Parameters.RISK_LEVELS['IV'] == 0.0465325
        assert Parameters.RISK_LEVELS['V'] == 0.0758875

    @pytest.mark.parametrize("risk_class,expected_percentage", [
        ('I', 0.0054355),
        ('II', 0.0113065),
        ('III', 0.0259840),
        ('IV', 0.0465325),
        ('V', 0.0758875)
    ])
    def test_risk_percentages(self, risk_class, expected_percentage):
        assert Parameters.get_risk_percentage(risk_class) == expected_percentage

    def test_invalid_risk_class(self):
        with pytest.raises(ValueError) as exc_info:
            Parameters.get_risk_percentage('VI')
        assert "Invalid risk class" in str(exc_info.value)

    def test_risk_class_case_insensitive(self):
        assert Parameters.get_risk_percentage('i') == Parameters.RISK_LEVELS['I']
        assert Parameters.get_risk_percentage('ii') == Parameters.RISK_LEVELS['II']
        assert Parameters.get_risk_percentage('iii') == Parameters.RISK_LEVELS['III']

    def test_contribution_ceiling_calculation(self):
        params = Parameters()
        expected_ceiling = params.VSDF * 25
        assert params.CONTRIBUTION_CEILING == expected_ceiling
        assert params.CONTRIBUTION_CEILING_2 == expected_ceiling

    def test_tcf_calculation(self):
        params = Parameters()
        expected_tcf = params.VSDF * 3
        assert params.TCF == expected_tcf