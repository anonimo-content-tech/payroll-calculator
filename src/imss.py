from .employees import Employee
from .parameters import Parameters
from .rcv import RCV
import math


class IMSS:
    def __init__(self, imss_salary, payment_period_or_risk='I', risk_class='I'):
        # Handle the case where payment_period_or_risk might be a risk class
        if isinstance(payment_period_or_risk, str):
            payment_period = 15
            risk_class = payment_period_or_risk
        else:
            payment_period = payment_period_or_risk

        # Inicialización de parámetros base
        self._init_base_parameters(imss_salary, risk_class, payment_period)
        # Inicialización de parámetros de beneficios
        self._init_benefit_parameters()

    # Método auxiliar para inicializar parámetros base
    def _init_base_parameters(self, imss_salary, risk_class, payment_period):
        self.parameters = Parameters()
        self.employee = Employee(imss_salary, payment_period=int(payment_period))  # Ensure payment_period is int
        self.days = self.employee.payment_period
        self.integration_factor = Parameters.INTEGRATION_FACTOR
        self.fixed_fee = Parameters.FIXED_FEE
        self.vsdf = Parameters.VSDF
        self.contribution_ceiling = Parameters.CONTRIBUTION_CEILING
        self.contribution_ceiling_2 = Parameters.CONTRIBUTION_CEILING_2
        self.surplus_employer = Parameters.SURPLUS_EMPLOYER
        self.surplus_employee = Parameters.SURPLUS_EMPLOYEE
        self.tcf = Parameters.TCF
        self.smg = Parameters.SMG
        self.risk_percentage = Parameters.get_risk_percentage(risk_class)
        self.retirement_employer = Parameters.RETIREMENT_EMPLOYER
        self.increase = Parameters.INCREASE

        # Inicializamos RCV después de tener el salario diario integrado
        self.rcv = None  # Se inicializará cuando se necesite
        self.infonavit_employer = Parameters.INFONAVIT_EMPLOYER
        self.total_salary = self.employee.calculate_total_salary()
        self.state_payroll_tax = Parameters.STATE_PAYROLL_TAX
        self.severance_and_old_age_employee = Parameters.SEVERANCE_AND_OLD_AGE_EMPLOYEE

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

    # ------------------------------------------------------ CALCULO DE CUOTAS DEL IMSS PATRÓN ------------------------------------------------------

    #  TOPE DE SALARIO 25 SMG DF ------- Columna Gnumero
    def get_salary_cap_25_smg(self):
        return min(self.get_integrated_daily_wage(), self.contribution_ceiling)

    # SALARIO DIARIO INTEGRADO, después de aplicar el factor de integración ------- Columna Enumero
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
        return ((salary_cap_25_smg - self.tcf) * self.surplus_employer * self.days) if salary_cap_25_smg > self.tcf else 0

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

    # ------------------------------------------------------ CALCULO DE CUOTAS DEL IMSS TRABAJADOR ------------------------------------------------------

    # ENFERMEDADES Y MATERNIDAD EXCEDENTE DEL TRABAJADOR ------- Columna Jnumero
    def get_diseases_and_maternity_employee_surplus(self):
        salary_cap_25_smg = self.get_salary_cap_25_smg()
        return ((salary_cap_25_smg - self.tcf) * self.surplus_employee * self.days) if salary_cap_25_smg > self.tcf else 0

    # PRESTACIONES EN ESPECIE TRABAJADOR (GASTOS MÉDICOS) ------- Columna Nnumero
    def get_benefits_in_kind_medical_expenses_employee(self):
        salary_cap_25_smg = self.get_salary_cap_25_smg()
        return ((salary_cap_25_smg * self.benefits_in_kind_employee) * self.days) if salary_cap_25_smg > self.smg else 0

    # INVALIDEZ Y VIDA TRABAJADOR ------- Columna Snumero
    def get_invalidity_and_retirement_employee(self):
        salary_cap_25_smg_2 = self.get_salary_cap_25_smg_2()
        return ((salary_cap_25_smg_2 * self.invalidity_and_retirement_employee) * self.days) if salary_cap_25_smg_2 > self.smg else 0

    # CUOTAS IMSS TRABAJADOR ------- Columna Wnumero
    def get_quota_employee(self):
        quotas = [
            self.get_diseases_and_maternity_employee_surplus(),
            self.get_employee_cash_benefits(),
            self.get_benefits_in_kind_medical_expenses_employee(),
            self.get_invalidity_and_retirement_employee()
        ]
        return sum(quotas)

    # ------------------------------------------------------ TOTAL IMSS ------------------------------------------------------

    # CUOTAS IMSS TOTAL ------- Columna Xnumero
    def get_total_imss(self):
        return self.get_quota_employer() + self.get_quota_employee()

    # ------------------------------------------------------ CALCULO DE TOTAL DEL RCV PATRÓN ------------------------------------------------------

    # RETIRO PATRÓN ------- Columna Znumero
    def get_retirement_employer(self):
        return self.get_salary_cap_25_smg() * self.days * self.retirement_employer

    # CESANTIA Y VEJEZ PATRÓN ------- Columna AAnumero
    def _get_rcv(self):
        if self.rcv is None:
            self.rcv = RCV(self.get_integrated_daily_wage())
        return self.rcv

    # CESANTIA Y VEJEZ PATRÓN ------- Columna AAnumero
    def get_severance_and_old_age_employer(self):
        return self._get_rcv().get_quota_employer()

    # ------------------------------------------------------ TOTAL RCV PATRÓN ------------------------------------------------------
    # TOTAL RCV PATRÓN ------- Columna ACnumero
    def get_total_rcv_employer(self):
        return self.get_retirement_employer() + self.get_severance_and_old_age_employer()

    # ------------------------------------------------------ CALCULO DE INFONAVIT DEL PATRÓN ------------------------------------------------------

    # INFONAVIT PATRÓN ------- Columna AEnumero
    def get_infonavit_employer(self):
        return self.get_salary_cap_25_smg_2() * self.days * self.infonavit_employer

    # ------------------------------------------------------ CALCULO DE IMPUESTO SOBRE NÓMINA ------------------------------------------------------

    # IMPUESTO SOBRE NÓMINA ------- Columna AFnumero
    def get_tax_payroll(self):
        return self.total_salary * self.state_payroll_tax

    # ------------------------------------------------------ CALCULO TOTAL DEL PATRÓN ------------------------------------------------------

    # TOTAL PATRÓN ------- Columna AHnumero
    def get_total_employer(self):
        return (self.get_quota_employer() + self.get_total_rcv_employer() + self.get_infonavit_employer() + self.get_tax_payroll())

    # ------------------------------------------------------ CALCULO DE TOTAL DEL RCV TRABAJADOR ------------------------------------------------------

    # CESANTÍA Y VEJEZ TRABAJADOR ------- Columna ABnumero
    def get_severance_and_old_age_employee(self):
        return (self.get_salary_cap_25_smg_2() * self.severance_and_old_age_employee) * self.days if self.get_salary_cap_25_smg_2() > self.smg else 0

    # TOTAL RCV TRABAJADOR ------- Columna ADnumero
    def get_total_rcv_employee(self):
        return self.get_severance_and_old_age_employee()

    # ------------------------------------------------------ CALCULO TOTAL DEL PATRÓN ------------------------------------------------------

    # TOTAL TRABAJADOR ------- Columna AJnumero
    def get_total_employee(self):
        return self.get_quota_employee() + self.get_total_rcv_employee()

    # ------------------------------------------------------ CALCULO TOTAL SUMA COSTO SOCIAL ------------------------------------------------------

    # SUMA COSTO SOCIAL ------- Columna ALnumero
    def get_total_social_cost(self):
        return self.get_total_employer() + self.get_total_employee()

    # ------------------------------------------------------ CALCULO 2.5 INCREMENTO ------------------------------------------------------

    # 2.5 INCREMENTO ------- Columna ANnumero
    def get_increment(self):
        return self.get_total_social_cost() * self.increase

    # ------------------------------------------------------ CALCULO SUMA COSTO SOCIAL SUGERIDO ------------------------------------------------------

    # SUMA COSTO SOCIAL SUGERIDO ------- Columna APnumero
    def get_total_social_cost_suggested(self):
        return math.ceil(self.get_total_social_cost() + self.get_increment())
