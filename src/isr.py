from .employees import Employee
from .parameters import Parameters


class ISR:
    def __init__(self, monthly_salary, payment_period, employee: Employee):
        self.employee = employee
        self.parameters = Parameters()
        self.monthly_salary = monthly_salary
        self.payment_period = payment_period
        self.SALARY_CREDIT_TABLE = Parameters.SALARY_CREDIT_TABLE

    # ------------------------------------------------------ CALCULO DEL IMPUESTO ------------------------------------------------------

    # Obtener la tabla del ISR según el periodo de pago
    def get_isr_table(self):
        return self.parameters.get_isr_table(self.payment_period)

    # Calcula el ISR mensual ------- Columna Enumero
    def get_lower_limit(self):
        # Encuentra el mayor valor en lower_limit que sea menor o igual al salario mensual
        applicable_limit = None
        isr_table = self.get_isr_table()
        
        for row in isr_table:
            if row['lower_limit'] <= self.monthly_salary:
                if applicable_limit is None or row['lower_limit'] > applicable_limit:
                    applicable_limit = row['lower_limit']
        
        return applicable_limit
    
    # Calcula el excedente ------- Columna Fnumero
    def get_surplus(self):
        lower_limit = self.get_lower_limit()
        if lower_limit is None:
            return 0
        return self.monthly_salary - lower_limit

    # Calcular el Porcentaje a aplicar en el excedente ------- Columna Gnumero
    def get_percentage_applied_to_excess(self):
        lower_limit = self.get_lower_limit()
        if lower_limit is None:
            return 0
            
        isr_table = self.get_isr_table()
        for row in isr_table:
            if row['lower_limit'] == lower_limit:
                return row['percentage']
        return 0  # Default to 0 if no matching row is found
            
    # Calcula el impuesto sobre el excedente ------- Columna Hnumero
    def get_surplus_tax(self):
        return self.get_surplus() * self.get_percentage_applied_to_excess()
    
    # Calcula la Cuota Fija ------- Columna Inumero
    def get_fixed_fee(self):
        lower_limit = self.get_lower_limit()
        if lower_limit is None:
            return 0
            
        get_isr_table = self.get_isr_table()
        # Busca la cuota fija en la tabla ISR
        for row in get_isr_table:
            if row['lower_limit'] == lower_limit:
                return row['fixed_fee']
        return 0  # Default to 0 if no matching row is found

    # Calcula el impuesto total ------- Columna Jnumero
    def get_total_tax(self):
        return self.get_surplus_tax() + self.get_fixed_fee()

    # ------------------------------------------------------ CALCULO DE TOTALES ISR ------------------------------------------------------

    # Es el ISR ------- Columna Lnumero
    def get_isr(self):
        return self.get_total_tax()

    # Calcula el Rango crédito al Salario ------- Columna Mnumero
    def get_range_credit_to_salary(self):
        # Encuentra el mayor valor en lower_limit que sea menor o igual al salario mensual
        applicable_limit = None
        for row in self.SALARY_CREDIT_TABLE:
            if row['lower_limit'] <= self.monthly_salary:
                if applicable_limit is None or row['lower_limit'] > applicable_limit:
                    applicable_limit = row['lower_limit']
        return applicable_limit

    # Calcula el Crédito al Salario ------- Columna Nnumero
    def get_salary_credit(self):
        range_limit = self.get_range_credit_to_salary()
        if range_limit is None:
            return 0
            
        for row in self.SALARY_CREDIT_TABLE:
            if row['lower_limit'] == range_limit:
                return row['credit']
        return 0

    # Calculo del Impuesto a Cargo ------- Columna Onumero
    def get_tax_payable(self):
        return self.get_isr() - self.get_salary_credit() if self.get_isr() > self.get_salary_credit() else 0
    
    # Calculo del Impuesto a Favor ------- Columna Pnumero
    def get_tax_in_favor(self):
        return self.get_salary_credit() - self.get_isr() if self.get_isr() < self.get_salary_credit() else 0
