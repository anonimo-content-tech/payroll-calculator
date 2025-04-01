from .employees import Employee
from .parameters import Parameters


class IMSS:
    def __init__(self, total_salary, risk_class='I'):
        # Inicialización de parámetros base
        self._init_base_parameters(total_salary, risk_class)
        # Inicialización de parámetros de beneficios
        self._init_benefit_parameters()

    # Método auxiliar para inicializar parámetros base
    def _init_base_parameters(self, total_salary, risk_class):
        self.parameters = Parameters()
        self.employee = Employee(total_salary)
        self.days = Employee.PAYMENT_PERIOD
        self.integration_factor = Parameters.INTEGRATION_FACTOR
        self.fixed_fee = Parameters.FIXED_FEE
        self.vsdf = Parameters.VSDF
        self.contribution_ceiling = Parameters.CONTRIBUTION_CEILING
        self.contribution_ceiling_2 = Parameters.CONTRIBUTION_CEILING_2
        self.surplus = Parameters.SURPLUS
        self.tcf = Parameters.TCF
        self.smg = Parameters.SMG
        self.risk_percentage = Parameters.get_risk_percentage(risk_class)

    # Método auxiliar para inicializar parámetros de beneficios
    def _init_benefit_parameters(self):
        self.cash_benefits_employer = Parameters.CASH_BENEFITS_EMPLOYER
        self.cash_benefits_employee = Parameters.CASH_BENEFITS_EMPLOYEE
        self.benefits_in_kind_employer = Parameters.BENEFITS_IN_KIND_EMPLOYER
        self.benefits_in_kind_employee = Parameters.BENEFITS_IN_KIND_EMPLOYEE
        self.invalidity_and_retirement_employer = Parameters.INVALIDITY_AND_RETIREMENT_EMPLOYER
        self.invalidity_and_retirement_employee = Parameters.INVALIDITY_AND_RETIREMENT_EMPLOYEE
        self.childcare = Parameters.CHILDCARE

    def get_integration_factor(self):
        return self.integration_factor

    #  TOPE DE SALARIO 25 SMG DF ------- Columna Gnumero
    def get_salary_cap_25_smg(self):
        return min(self.get_integrated_daily_wage(), self.contribution_ceiling)

    # SALARIO DIARIO INTEGRADO, después de aplicar el factor de integración ------- Columna Dnumero
    def get_integrated_daily_wage(self):
        daily_salary_integrated = self.employee.calculate_salary_dialy()
        return daily_salary_integrated * self.integration_factor

    # ENFERMEDADES Y MATERNIDAD CUOTA DEL PATRÓN ------- Columna Hnumero
    def get_diseases_and_maternity_employer_quota(self):
        daily_wage = self.get_integrated_daily_wage()
        return self.vsdf * self.days * self.fixed_fee if daily_wage > 0 else 0

    # ENFERMEDADES Y MATERNIDAD EXCEDENTE DEL PATRÓN ------- Columna Inumero
    def get_diseases_and_maternity_employer_surplus(self):
        salary_cap_25_smg = self.get_salary_cap_25_smg()
        return ((salary_cap_25_smg - self.tcf) * self.surplus * self.days) if salary_cap_25_smg > self.tcf else 0

    # Método auxiliar para calcular beneficios con lógica común
    def _calculate_benefit(self, base_salary, employer_rate, employee_rate):
        """Calcula los beneficios basados en el salario y las tasas proporcionadas"""
        if base_salary > self.smg:
            return (base_salary * employer_rate) * self.days
        return (base_salary * (employer_rate + employee_rate)) * self.days

    # PRESTACIONES EN DINERO PATRÓN ------- Columna Knumero
    def get_employer_cash_benefits(self):
        return self._calculate_benefit(
            self.get_salary_cap_25_smg(),
            self.cash_benefits_employer,
            self.cash_benefits_employee
        )

    # PRESTACIONES EN DINERO TRABAJADOR ------- Columna Lnumero
    def get_employee_cash_benefits(self):
        salary_cap_25_smg = self.get_salary_cap_25_smg()
        return (salary_cap_25_smg * self.cash_benefits_employee * self.days) if salary_cap_25_smg > self.smg else 0

    # PRESTACIONES EN ESPECIE PATRÓN (GASTOS MÉDICOS) ------- Columna Mnumero
    def get_benefits_in_kind_medical_expenses_employer(self):
        return self._calculate_benefit(
            self.get_salary_cap_25_smg(),
            self.benefits_in_kind_employer,
            self.benefits_in_kind_employee
        )

    # RIESGOS DEL TRABAJO PATRÓN ------- Columna Onumero
    def get_occupational_risks_employer(self):
        return self.days * self.get_salary_cap_25_smg() * self.risk_percentage

    # TOPE DE SALARIO 25 SMG DF CON TC2 ------- Columna Qnumero
    def get_salary_cap_25_smg_2(self):
        return min(self.get_integrated_daily_wage(), self.contribution_ceiling_2)

    # INVALIDEZ Y VIDA PATRÓN ------- Columna Rnumero
    def get_invalidity_and_retirement_employer(self):
        return self._calculate_benefit(
            self.get_salary_cap_25_smg_2(),
            self.invalidity_and_retirement_employer,
            self.invalidity_and_retirement_employee
        )

    # GUARDERIAS Y PS PATRÓN ------- Columna Tnumero
    def get_childcare_employer(self):
        return self.childcare * self.get_salary_cap_25_smg() * self.days

    # CUOTAS IMSS PATRÓN ------- Columna Vnumero
    def get_quota_employer(self):
        quotas = [
            self.get_diseases_and_maternity_employer_quota(),
            self.get_diseases_and_maternity_employer_surplus(),
            self.get_employer_cash_benefits(),
            self.get_benefits_in_kind_medical_expenses_employer(),
            self.get_occupational_risks_employer(),
            self.get_invalidity_and_retirement_employer(),
            self.get_childcare_employer()
        ]
        return sum(quotas)