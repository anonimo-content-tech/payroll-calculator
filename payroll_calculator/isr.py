from .employees import Employee
from .parameters import Parameters


class ISR:
    def __init__(self, monthly_salary, payment_period, employee: Employee, minimum_threshold_salary=None):
        self.employee = employee
        self.parameters = Parameters()
        self.monthly_salary = monthly_salary
        self.payment_period = payment_period
        self.SALARY_CREDIT_TABLE = Parameters.SALARY_CREDIT_TABLE
        self.smg = Parameters.SMG
        self.monthly_smg = minimum_threshold_salary

    # ------------------------------------------------------ CALCULO DEL IMPUESTO ------------------------------------------------------

    # Obtener la tabla del ISR según el periodo de pago
    def get_isr_table(self):
        return self.parameters.get_isr_table(self.payment_period)

    # Calcula el ISR mensual ------- Columna Enumero
    def get_lower_limit(self, use_smg=False):
        # Encuentra el mayor valor en lower_limit que sea menor o igual al salario mensual
        applicable_limit = None
        isr_table = self.get_isr_table()
        
        user_salary = self.monthly_smg if use_smg else self.monthly_salary
        
        for row in isr_table:
            if row['lower_limit'] <= user_salary:
                if applicable_limit is None or row['lower_limit'] > applicable_limit:
                    applicable_limit = row['lower_limit']
        return applicable_limit
    
    # Calcula el excedente ------- Columna Fnumero
    def get_surplus(self, use_smg=False):
        lower_limit = self.get_lower_limit(use_smg)
        if lower_limit is None:
            return 0
        salary = self.monthly_smg if use_smg else self.monthly_salary
        return salary - lower_limit

    # Calcular el Porcentaje a aplicar en el excedente ------- Columna Gnumero
    def get_percentage_applied_to_excess(self, use_smg=False):
        lower_limit = self.get_lower_limit(use_smg)
        if lower_limit is None:
            return 0
            
        isr_table = self.get_isr_table()
        for row in isr_table:
            if row['lower_limit'] == lower_limit:
                return row['percentage']
        return 0  # Default to 0 if no matching row is found
            
    # Calcula el impuesto sobre el excedente ------- Columna Hnumero
    def get_surplus_tax(self, use_smg=False):
        return self.get_surplus(use_smg) * self.get_percentage_applied_to_excess(use_smg)
    
    # Calcula la Cuota Fija ------- Columna Inumero
    def get_fixed_fee(self, use_smg=False):
        lower_limit = self.get_lower_limit(use_smg)
        if lower_limit is None:
            return 0
            
        get_isr_table = self.get_isr_table()
        # Busca la cuota fija en la tabla ISR
        for row in get_isr_table:
            if row['lower_limit'] == lower_limit:
                return row['fixed_fee']
        return 0  # Default to 0 if no matching row is found

    # Calcula el impuesto total ------- Columna Jnumero
    def get_total_tax(self, use_smg=False):
        return self.get_surplus_tax(use_smg) + self.get_fixed_fee(use_smg)

    # ------------------------------------------------------ CALCULO DE TOTALES ISR ------------------------------------------------------

    # Es el ISR ------- Columna Lnumero
    def get_isr(self, use_smg=False):
        return self.get_total_tax(use_smg)

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
    def get_tax_payable(self, use_smg=False):
        return self.get_isr(use_smg) - self.get_salary_credit() if self.get_isr(use_smg) > self.get_salary_credit() else 0
    
    # Calculo del Impuesto a Favor ------- Columna Pnumero
    def get_tax_in_favor(self):
        return self.get_salary_credit() - self.get_isr() if self.get_isr() < self.get_salary_credit() else 0
