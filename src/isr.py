from .employees import Employee
from .parameters import Parameters


class ISR:
    def __init__(self, monthly_salary, payment_period, employee: Employee):
        self.employee = employee
        self.parameters = Parameters()
        self.monthly_salary = monthly_salary
        self.payment_period = payment_period

    # ------------------------------------------------------ CALCULO DEL IMPUESTO ------------------------------------------------------

    # Obtener la tabla del ISR según el periodo de pago
    def get_isr_table(self):
        return self.parameters.get_isr_table(self.payment_period)

    # Calcula el ISR mensual ------- Columna Enumero
    def get_lower_limit(self):
        get_isr_table = self.get_isr_table()
        for i, row in enumerate(get_isr_table):
            if row['lower_limit'] <= self.monthly_salary <= get_isr_table[i + 1]['lower_limit']:
                return row['lower_limit']

    # Calcula el excedente ------- Columna Fnumero
    def get_surplus(self):
        return self.monthly_salary - self.get_lower_limit()
    
    # Calcular el Porcentaje a aplicar en el excedente ------- Columna Gnumero
    def get_percentage_applied_to_excess(self):
        lower_limit = self.get_lower_limit()
        isr_table = self.get_isr_table()
        for row in isr_table:
            if row['lower_limit'] == lower_limit:
                return row['percentage']
            
    # Calcula el impuesto sobre el excedente ------- Columna Hnumero
    def get_surplus_tax(self):
        return self.get_surplus() * self.get_percentage_applied_to_excess()
    
    # Calcula la Cuota Fija ------- Columna Inumero
    def get_fixed_fee(self):
        get_isr_table = self.get_isr_table()
        lower_limit = self.get_lower_limit()
        # Busca la cuota fija en la tabla ISR
        for row in get_isr_table:
            if row['lower_limit'] == lower_limit:
                return row['fixed_fee']
    
    # Calcula el impuesto total ------- Columna Jnumero
    def get_total_tax(self):
        return self.get_surplus_tax() + self.get_fixed_fee()