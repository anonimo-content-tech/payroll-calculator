import pytest
from src.saving import Saving
from src.imss import IMSS
from src.isr import ISR
from unittest.mock import Mock


class TestSaving:
    @pytest.fixture
    def mock_imss(self):
        mock = Mock(spec=IMSS)
        mock.get_total_employer.return_value = 1000
        mock.get_quota_employee.return_value = 200
        mock.get_total_rcv_employee.return_value = 100
        return mock

    @pytest.fixture
    def mock_isr(self):
        mock = Mock(spec=ISR)
        mock.get_tax_payable.return_value = 500
        mock.get_tax_in_favor.return_value = 0
        return mock

    @pytest.fixture
    def saving_instance(self, mock_imss, mock_isr):
        saving = Saving(
            wage_and_salary=10000,
            wage_and_salary_dsi=8000,
            fixed_fee_dsi=500,
            commission_percentage_dsi=0.05,
            imss_instance=mock_imss,
            isr_instance=mock_isr
        )
        return saving

    def test_initialization(self):
        saving = Saving(
            wage_and_salary=10000,
            wage_and_salary_dsi=8000,
            fixed_fee_dsi=500,
            commission_percentage_dsi=0.05
        )
        assert saving.wage_and_salary == 10000
        assert saving.wage_and_salary_dsi == 8000
        assert saving.fixed_fee_dsi == 500
        assert saving.commission_percentage_dsi == 0.05
        assert saving.imss is None
        assert saving.isr is None

    def test_set_imss(self, mock_imss):
        saving = Saving(10000, 8000, 500, 0.05)
        saving.set_imss(mock_imss)
        assert saving.imss == mock_imss

    def test_set_isr(self, mock_isr):
        saving = Saving(10000, 8000, 500, 0.05)
        saving.set_isr(mock_isr)
        assert saving.isr == mock_isr

    def test_get_traditional_scheme_biweekly_total(self, saving_instance, mock_imss):
        result = saving_instance.get_traditional_scheme_biweekly_total()
        assert result == 11000  # 10000 (wage_and_salary) + 1000 (total_employer)

    def test_get_traditional_scheme_biweekly_total_no_imss(self):
        saving = Saving(10000, 8000, 500, 0.05)
        with pytest.raises(ValueError, match="IMSS instance is not set. Use set_imss\\(\\) method first."):
            saving.get_traditional_scheme_biweekly_total()

    def test_get_productivity(self, saving_instance):
        result = saving_instance.get_productivity()
        assert result == 2000  # 10000 - 8000

    def test_get_commission_dsi(self, saving_instance):
        result = saving_instance.get_commission_dsi()
        assert result == 500  # 10000 * 0.05

    def test_get_dsi_scheme_biweekly_total(self, saving_instance):
        result = saving_instance.get_dsi_scheme_biweekly_total()
        assert result == 11000  # 10000 + 500 + 500

    def test_get_amount(self, saving_instance):
        result = saving_instance.get_amount()
        assert result == 0  # 11000 - 11000

    def test_get_percentage(self, saving_instance):
        result = saving_instance.get_percentage()
        assert result == 0  # 0 / 11000

    def test_get_isr_retention(self, saving_instance, mock_isr):
        result = saving_instance.get_isr_retention()
        assert result == 500  # tax_payable > tax_in_favor

    def test_get_isr_retention_tax_in_favor(self, saving_instance, mock_isr):
        mock_isr.get_tax_payable.return_value = 0
        mock_isr.get_tax_in_favor.return_value = 200
        result = saving_instance.get_isr_retention()
        assert result == -200  # tax_in_favor * -1

    def test_get_isr_retention_no_isr(self):
        saving = Saving(10000, 8000, 500, 0.05)
        with pytest.raises(ValueError, match="ISR instance is not set. Use set_isr\\(\\) method first."):
            saving.get_isr_retention()

    def test_get_total_retentions(self, saving_instance, mock_imss, mock_isr):
        result = saving_instance.get_total_retentions()
        assert result == 800  # 500 (tax_payable) + 200 (quota_employee) + 100 (total_rcv_employee)

    def test_get_current_perception(self, saving_instance):
        result = saving_instance.get_current_perception()
        assert result == 9200  # 10000 - 800

    def test_get_assimilated(self, saving_instance):
        result = saving_instance.get_assimilated()
        assert result == 2000  # Same as get_productivity()

    def test_get_total_wage_and_salary_dsi(self, saving_instance):
        result = saving_instance.get_total_wage_and_salary_dsi()
        assert result == 10000  # 8000 + 2000

    def test_get_current_perception_dsi(self, saving_instance):
        result = saving_instance.get_current_perception_dsi()
        assert result == 10000  # 10000 - 0 - 0 - 0 - 0

    def test_get_increment(self, saving_instance):
        result = saving_instance.get_increment()
        assert result == 800  # 10000 - 9200

    def test_get_increment_percentage(self, saving_instance):
        result = saving_instance.get_increment_percentage()
        assert result == 800 / 9200  # 800 / 9200