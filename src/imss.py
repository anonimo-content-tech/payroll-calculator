from .employees import Employee
from .parameters import Parameters


class IMSS:
    def __init__(self, total_salary, risk_class='I'):
        self.parameters = Parameters()
        self.employee = Employee(total_salary)
        self.days = Employee.PAYMENT_PERIOD
        self.integration_factor = Parameters.INTEGRATION_FACTOR
        self.fixed_fee = Parameters.FIXED_FEE
        self.vsdf = Parameters.VSDF
        self.contribution_ceiling = Parameters.CONTRIBUTION_CEILING
        self.surplus = Parameters.SURPLUS
        self.tcf = Parameters.TCF
        self.smg = Parameters.SMG
        self.cash_benefits_employer = Parameters.CASH_BENEFITS_EMPLOYER
        self.cash_benefits_employee = Parameters.CASH_BENEFITS_EMPLOYEE
        self.benefits_in_kind_employer = Parameters.BENEFITS_IN_KIND_EMPLOYER
        self.benefits_in_kind_employee = Parameters.BENEFITS_IN_KIND_EMPLOYEE
        self.risk_percentage = Parameters.get_risk_percentage(risk_class)
        self.contribution_ceiling_2 = Parameters.CONTRIBUTION_CEILING_2
        self.invalidity_and_retirement_employer = Parameters.INVALIDITY_AND_RETIREMENT_EMPLOYER
        self.invalidity_and_retirement_employee = Parameters.INVALIDITY_AND_RETIREMENT_EMPLOYEE
        self.childcare = Parameters.CHILDCARE

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
        if salary_cap_25_smg > self.tcf:
            return ((salary_cap_25_smg - self.tcf) * self.surplus) * self.days
        else:
            return 0

    # PRESTACIONES EN DINERO PATRÓN ------- Columna Knumero
    def get_employer_cash_benefits(self):
        salary_cap_25_smg = self.get_salary_cap_25_smg()
        if salary_cap_25_smg > self.smg:
            return (salary_cap_25_smg * self.cash_benefits_employer) * self.days
        else:
            return (salary_cap_25_smg * (self.cash_benefits_employer + self.cash_benefits_employee)) * self.days

    # PRESTACIONES EN DINERO TRABAJADOR ------- Columna Lnumero
    def get_employee_cash_benefits(self):
        salary_cap_25_smg = self.get_salary_cap_25_smg()
        if salary_cap_25_smg > self.smg:
            return (salary_cap_25_smg * self.cash_benefits_employee) * self.days
        else:
            return 0

    # PRESTACIONES EN ESPECIE PATRÓN (GASTOS MÉDICOS) ------- Columna Mnumero
    def get_benefits_in_kind_medical_expenses_employer(self):
        salary_cap_25_smg = self.get_salary_cap_25_smg()
        if salary_cap_25_smg > self.smg:
            return (salary_cap_25_smg * self.benefits_in_kind_employer) * self.days
        else:
            return (salary_cap_25_smg * (self.benefits_in_kind_employer + self.benefits_in_kind_employee)) * self.days

    # RIESGOS DEL TRABAJO PATRÓN ------- Columna Onumero
    def get_occupational_risks_employer(self):
        salary_cap_25_smg = self.get_salary_cap_25_smg()
        return self.days * salary_cap_25_smg * self.risk_percentage

    # TOPE DE SALARIO 25 SMG DF CON TC2 ------- Columna Qnumero
    def get_salary_cap_25_smg_2(self):
        daily_salary_integrated = self.get_integrated_daily_wage()
        if daily_salary_integrated > self.contribution_ceiling_2:
            return self.contribution_ceiling_2
        else:
            return daily_salary_integrated

    # INVALIDEZ Y VIDA PATRÓN ------- Columna Rnumero
    def get_invalidity_and_retirement_employer(self):
        salary_cap_25_smg_2 = self.get_salary_cap_25_smg_2()
        if salary_cap_25_smg_2 > self.smg:
            return (salary_cap_25_smg_2 * self.invalidity_and_retirement_employer) * self.days
        else:
            return (salary_cap_25_smg_2 * (self.invalidity_and_retirement_employer + self.invalidity_and_retirement_employee)) * self.days

    # GUARDERIAS Y PS PATRÓN ------- Columna Tnumero
    def get_childcare_employer(self):
        salary_cap_25_smg = self.get_salary_cap_25_smg()
        return self.childcare * salary_cap_25_smg * self.days

    # CUOTAS IMSS PATRÓN ------- Columna Vnumero
    def get_quota_employer(self):
        return self.get_diseases_and_maternity_employer_quota() + self.get_diseases_and_maternity_employer_surplus() + self.get_employer_cash_benefits() + self.get_benefits_in_kind_medical_expenses_employer() + self.get_occupational_risks_employer() + self.get_invalidity_and_retirement_employer() + self.get_childcare_employer()

# 5710.64