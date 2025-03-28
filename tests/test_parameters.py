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