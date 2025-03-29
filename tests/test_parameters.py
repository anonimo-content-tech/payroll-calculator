import pytest
from src.parameters import Parameters

class TestParameters:
    def test_parameters_constants(self):
        params = Parameters()
        assert params.INTEGRATION_FACTOR == 1.0493
        assert params.VSDF == 113.14
        assert params.CONTRIBUTION_CEILING == params.VSDF * 25
        assert params.FIXED_FEE == 0.204
        assert params.SURPLUS == 0.011

    def test_parameters_initialization(self):
        params = Parameters()
        assert params.integration_factor == Parameters.INTEGRATION_FACTOR
        assert params.vsdf == Parameters.VSDF

    @pytest.mark.parametrize("risk_class,expected_percentage", [
        ('I', 0.0054355),
        ('II', 0.0113065),
        ('III', 0.0259840),
        ('IV', 0.0465325),
        ('V', 0.0758875)
    ])
    def test_risk_percentages(self, risk_class, expected_percentage):
        assert Parameters.get_risk_percentage(risk_class) == expected_percentage