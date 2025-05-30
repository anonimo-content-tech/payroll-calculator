from .parameters import Parameters
from .employees import Employee
import inspect


class RCV:
    def __init__(self, daily_integrated_wage, payment_period):
        frame_llamador = inspect.currentframe().f_back
        info = inspect.getframeinfo(frame_llamador)
        # print(f"Instanciado desde {info.filename}, función {info.function}, línea {info.lineno}")
        self.daily_integrated_wage = daily_integrated_wage
        self.days = payment_period
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
