from .employees import Employee
from .parameters import Parameters

class IMSS:
    def __init__(self, total_salary):
        self.parameters = Parameters()
        self.employee = Employee(total_salary)
        self.days = Employee.PAYMENT_PERIOD
        self.integration_factor = Parameters.INTEGRATION_FACTOR
        self.fixed_fee = Parameters.FIXED_FEE
        self.vsdf = Parameters.VSDF
        self.contribution_ceiling = Parameters.CONTRIBUTION_CEILING
        self.surplus = Parameters.SURPLUS
    
    def get_integration_factor(self):
        return self.integration_factor
    
    #  TOPE DE SALARIO 25 SMG DF ------- Columna Gnumero
    def get_salary_cap_25_smg(self):
        daily_salary_integrated = self.get_integrated_daily_wage()
        if daily_salary_integrated > self.contribution_ceiling:
            return self.contribution_ceiling
        else: 
            return daily_salary_integrated
    
    # SALARIO DIARIO INTEGRADO, después de aplicar el factor de integración ------- Columna Dnumero
    def get_integrated_daily_wage(self):
        daily_salary_integrated = self.employee.calculate_salary_dialy()
        return daily_salary_integrated * self.integration_factor
    
    # ENFERMEDADES Y MATERNIDAD CUOTA DEL PATRÓN ------- Columna Hnumero
    def get_diseases_and_maternity_employer_quota(self):
        daily_wage = self.get_integrated_daily_wage()
        if daily_wage > 0:
            return self.vsdf * self.days * self.fixed_fee
        else:
            return 0
    
    # ENFERMEDADES Y MATERNIDAD EXCEDENTE DEL PATRÓN ------- Columna Inumero    
    def get_diseases_and_maternity_employer_surplus(self):
        salary_cap_25_smg = self.get_salary_cap_25_smg()
        if salary_cap_25_smg > self.contribution_ceiling:
            return ((salary_cap_25_smg - self.contribution_ceiling) * self.surplus) * self.days
        else:
            return 0