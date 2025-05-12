from .parameters import Parameters
from .employees import Employee


class RCV:
    def __init__(self, daily_integrated_wage):
        self.daily_integrated_wage = daily_integrated_wage
        self.days = Employee.PAYMENT_PERIOD
        self.parameters = Parameters()

    # Porcentaje de integración ------- Columna Enumero
    def get_retirement_percentage(self):
        return Parameters.get_retirement_percentage(self.daily_integrated_wage)

    # Cuota patronal ------- Columna Fnumero
    def get_quota_employer(self):
        # Prevent negative quotas
        if self.daily_integrated_wage <= 0:
            return 0
        retirement_percentage = self.get_retirement_percentage()
        return (self.daily_integrated_wage * retirement_percentage) * self.days
