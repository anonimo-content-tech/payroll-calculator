from .employees import Employee
from .parameters import Parameters
from .rcv import RCV
import math
from typing import Optional
import inspect


class IMSS:
    def __init__(self, imss_salary, daily_salary, payment_period, integration_factor, risk_class='I', minimum_threshold_salary=None, use_increment_percentage=None, imss_breakdown=None):
        # Handle the case where payment_period might be a risk class
        if isinstance(payment_period, str):
            risk_class = risk_class
            payment_period = payment_period

        # Inicialización de parámetros base
        self._init_base_parameters(imss_salary, daily_salary, integration_factor, risk_class, payment_period, minimum_threshold_salary, use_increment_percentage, imss_breakdown)
        # Inicialización de parámetros de beneficios
        self._init_benefit_parameters()

    # Método auxiliar para inicializar parámetros base
    def _init_base_parameters(self, imss_salary, daily_salary, integration_factor, risk_class, payment_period, minimum_threshold_salary=None, use_increment_percentage=None, imss_breakdown=None):
        self.salary = imss_salary
        self.daily_salary = daily_salary
        self.payment_period = payment_period
        self.risk_class = risk_class
        self.parameters = Parameters()
        self.employee = Employee(imss_salary, payment_period)
        self.days = self.employee.payment_period
        self.integration_factor = integration_factor
        self.imss_breakdown = imss_breakdown
        self.fixed_fee = Parameters.FIXED_FEE
        self.vsdf = Parameters.VSDF
        self.contribution_ceiling = Parameters.CONTRIBUTION_CEILING
        self.contribution_ceiling_2 = Parameters.CONTRIBUTION_CEILING_2
        self.surplus_employer = Parameters.SURPLUS_EMPLOYER
        self.surplus_employee = Parameters.SURPLUS_EMPLOYEE
        self.tcf = Parameters.TCF
        self.smg = Parameters.SMG
        self.risk_percentage = Parameters.get_risk_percentage(risk_class) if type(risk_class) == str else risk_class
        self.retirement_employer = Parameters.RETIREMENT_EMPLOYER
        self.increase = Parameters.INCREASE if use_increment_percentage else 0

        # Inicializamos RCV después de tener el salario diario integrado
        self.rcv = None  # Se inicializará cuando se necesite
        self.infonavit_employer = Parameters.INFONAVIT_EMPLOYER
        self.total_salary = self.employee.calculate_total_salary()
        self.state_payroll_tax = Parameters.STATE_PAYROLL_TAX
        self.severance_and_old_age_employee = Parameters.SEVERANCE_AND_OLD_AGE_EMPLOYEE
        self.smg_total_salary = self.employee.calculate_total_minimum_salary(self.smg)
        self.smg_total_monthly_salary = minimum_threshold_salary
        
        # Variables para almacenar los resultados cuando imss_breakdown es True
        self.quota_employer_with_daily_salary = None
        self.total_rcv_employer_with_daily_salary = None
        self.infonavit_employer_with_daily_salary = None
        self.tax_payroll_with_daily_salary = None

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
    def get_integrated_daily_wage(self, use_direct_daily_salary=False):
        if use_direct_daily_salary:
            return self.daily_salary * self.integration_factor
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
                
    def get_quota_employer(self, use_direct_daily_salary=False):
        # Guardar el método original
        original_method = self.get_integrated_daily_wage
        if use_direct_daily_salary:
            # Override que usa daily_salary directo (captura original_method)
            def get_integrated_daily_wage_override():
                return original_method(True)
            self.get_integrated_daily_wage = get_integrated_daily_wage_override
        try:
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
        finally:
            if use_direct_daily_salary:
                self.get_integrated_daily_wage = original_method


    # ------------------------------------------------------ CALCULO DE CUOTAS DEL IMSS TRABAJADOR ------------------------------------------------------

    # ENFERMEDADES Y MATERNIDAD EXCEDENTE DEL TRABAJADOR ------- Columna Jnumero
    def get_diseases_and_maternity_employee_surplus(self):
        salary_cap_25_smg = self.get_salary_cap_25_smg()
        # print("Columna G: ", salary_cap_25_smg, "Columna H: ", self.get_diseases_and_maternity_employer_quota(), "Columna I: ", self.get_diseases_and_maternity_employer_surplus())
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
        # print("Columna J: ", self.get_diseases_and_maternity_employee_surplus(), "Columna L: ", self.get_employee_cash_benefits(), "Columna N: ", self.get_benefits_in_kind_medical_expenses_employee(), "Columna S: ", self.get_invalidity_and_retirement_employee())
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
    def get_retirement_employer(self, use_direct_daily_salary=False):
        if use_direct_daily_salary:
            # Tope con salario diario directo
            salary_cap = min(self.get_integrated_daily_wage(True), self.contribution_ceiling)
        else:
            # Tope estándar
            salary_cap = self.get_salary_cap_25_smg()
        return salary_cap * self.days * self.retirement_employer

    # CESANTIA Y VEJEZ PATRÓN ------- Columna AAnumero
    def _get_rcv(self, use_direct_daily_salary=False):
        caller_frame = inspect.currentframe().f_back
        info = inspect.getframeinfo(caller_frame)
        # print(f"_get_rcv invocada desde {info.filename}, función {info.function}, línea {info.lineno}")
        # Siempre crear una nueva instancia con el valor actual del salario diario integrado
        result_rcv = self.get_integrated_daily_wage(use_direct_daily_salary)
        self.rcv = RCV(result_rcv, self.payment_period)
        return self.rcv

    # CESANTIA Y VEJEZ PATRÓN ------- Columna AAnumero
    def get_severance_and_old_age_employer(self, use_direct_daily_salary=False):
        return self._get_rcv(use_direct_daily_salary).get_quota_employer()

    # ------------------------------------------------------ TOTAL RCV PATRÓN ------------------------------------------------------
    # TOTAL RCV PATRÓN ------- Columna ACnumero
    def get_total_rcv_employer(self, use_direct_daily_salary=False):
        # Ya no necesitamos reemplazar temporalmente el método
        # Simplemente pasamos el parámetro a los métodos que lo necesitan
        return self.get_retirement_employer() + self.get_severance_and_old_age_employer(use_direct_daily_salary)

    # ------------------------------------------------------ CALCULO DE INFONAVIT DEL PATRÓN ------------------------------------------------------

    # INFONAVIT PATRÓN ------- Columna AEnumero
    def get_infonavit_employer(self, use_direct_daily_salary=False):
        original_method = self.get_integrated_daily_wage

        if use_direct_daily_salary:
            # Override que usa daily_salary directamente
            def get_integrated_daily_wage_override():
                return original_method(True)
            self.get_integrated_daily_wage = get_integrated_daily_wage_override

        try:
            return self.get_salary_cap_25_smg_2() * self.days * self.infonavit_employer
        finally:
            if use_direct_daily_salary:
                # Restaurar el método original
                self.get_integrated_daily_wage = original_method


    # ------------------------------------------------------ CALCULO DE IMPUESTO SOBRE NÓMINA ------------------------------------------------------

    # IMPUESTO SOBRE NÓMINA ------- Columna AFnumero
    def get_tax_payroll(self, use_smg=False, minimum_threshold_salary_override: Optional[float] = None, use_direct_daily_salary=False):
        if use_direct_daily_salary and not use_smg:
            # Calcular el total_salary basado en daily_salary
            total_salary = self.daily_salary * self.payment_period
        elif use_smg:
            if minimum_threshold_salary_override is not None:
                total_salary = minimum_threshold_salary_override
            else:
                total_salary = self.smg_total_monthly_salary
        else:
            total_salary = self.total_salary
        
        # Asegurarse de que total_salary no sea None antes de la multiplicación
        if total_salary is None:
            return 0
            
        return total_salary * self.state_payroll_tax

    # ------------------------------------------------------ CALCULO TOTAL DEL PATRÓN ------------------------------------------------------

    # TOTAL PATRÓN ------- Columna AHnumero
    def get_total_employer(self, use_smg=False, minimum_threshold_salary_override: Optional[float] = None):
        return self.get_quota_employer() + self.get_total_rcv_employer() + self.get_infonavit_employer() + self.get_tax_payroll(use_smg, minimum_threshold_salary_override=minimum_threshold_salary_override)

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
    def get_total_social_cost(self, use_smg=False, minimum_threshold_salary_override: Optional[float] = None):
        return self.get_total_employer(use_smg, minimum_threshold_salary_override=minimum_threshold_salary_override) + self.get_total_employee()

    # ------------------------------------------------------ CALCULO 2.5 INCREMENTO ------------------------------------------------------

    # 2.5 INCREMENTO ------- Columna ANnumero
    def get_increment(self, use_smg=False, minimum_threshold_salary_override: Optional[float] = None):
        return self.get_total_social_cost(use_smg, minimum_threshold_salary_override=minimum_threshold_salary_override) * self.increase

    # ------------------------------------------------------ CALCULO SUMA COSTO SOCIAL SUGERIDO ------------------------------------------------------

    # SUMA COSTO SOCIAL SUGERIDO ------- Columna APnumero
    def get_total_social_cost_suggested(self):
        return math.ceil(self.get_total_social_cost() + self.get_increment())
    
    # SALARIO DIARIO INTEGRADO PARA SMG, después de aplicar el factor de integración
    def get_integrated_daily_wage_for_smg(self, minimum_threshold_salary_override: Optional[float] = None):
        """Calcula el salario diario integrado basado en el salario mínimo en lugar del salario del empleado"""
        if minimum_threshold_salary_override is not None:
            daily_salary = minimum_threshold_salary_override / self.days
        elif self.smg_total_monthly_salary is not None:
            daily_salary = self.smg_total_monthly_salary / self.days
        else:
            # Si no hay override ni salario mensual SMG, usar el SMG base
            daily_salary = self.smg
        
        return daily_salary * self.integration_factor
    
    # SUMA COSTO SOCIAL SUGERIDO PARA OBTENER LA CUOTA FIJA ------- Columna APnumero
    def get_fixed_fee_for_smg(self, minimum_threshold_salary_override: Optional[float] = None):
        original_method = self.get_integrated_daily_wage

        # Override que ignora los args y usa siempre el SMG
        def get_integrated_daily_wage_override(*args, **kwargs):
            return self.get_integrated_daily_wage_for_smg(minimum_threshold_salary_override)

        # Patch temporal
        self.get_integrated_daily_wage = get_integrated_daily_wage_override

        try:
            # Cálculo usando salario mínimo integrado
            total_social = self.get_total_social_cost(
                use_smg=True,
                minimum_threshold_salary_override=minimum_threshold_salary_override
            )
            increment = self.get_increment(
                use_smg=True,
                minimum_threshold_salary_override=minimum_threshold_salary_override
            )
            return math.ceil(total_social + increment)
        finally:
            # Restaurar método original
            self.get_integrated_daily_wage = original_method



    # Método para calcular y almacenar los valores con daily_salary cuando imss_breakdown es True
    def calculate_breakdown_values(self):
        """
        Calcula y almacena los valores desglosados usando salario diario directo.
        """
        print("SE VA A EJECUTAR EL CALCULATE BREAKDOWN VALUES CON DAILY SALARY DE:", self.daily_salary)

        if not self.imss_breakdown:
            return

        # 1) Obtiene el salario diario integrado directo
        integrated_direct = self.get_integrated_daily_wage(use_direct_daily_salary=True)
        # 2) Crea una única instancia de RCV con ese salario
        rcv_obj = RCV(integrated_direct, self.payment_period)

        # 3) Cuota IMSS Patrón con salario diario
        self.quota_employer_with_daily_salary = self.get_quota_employer(use_direct_daily_salary=True)
        # 4) Cesantía y vejez (solo componente RCV) — reutiliza rcv_obj
        self.severance_and_old_age_employer = rcv_obj.get_quota_employer()
        # 5) Retiro PATRÓN con salario directo
        retiro_direct = self.get_retirement_employer(use_direct_daily_salary=True)
        # 6) Total RCV Patrón con salario diario = Retiro + Cesantía
        self.total_rcv_employer_with_daily_salary = retiro_direct + self.severance_and_old_age_employer

        # 7) INFONAVIT y Nómina también con salario directo
        self.infonavit_employer_with_daily_salary = self.get_infonavit_employer(use_direct_daily_salary=True)
        self.tax_payroll_with_daily_salary = self.get_tax_payroll(use_direct_daily_salary=True)
        
        totals = [
            self.quota_employer_with_daily_salary,
            self.total_rcv_employer_with_daily_salary,
            self.infonavit_employer_with_daily_salary,
            self.tax_payroll_with_daily_salary,
        ]
        total_tax_cost_breakdown = sum(totals)

        # Crear un diccionario con los valores para devolver
        return {
            'integrated_direct': integrated_direct,
            'quota_employer_with_daily_salary': self.quota_employer_with_daily_salary,
            'total_rcv_employer_with_daily_salary': self.total_rcv_employer_with_daily_salary,
            'infonavit_employer_with_daily_salary': self.infonavit_employer_with_daily_salary,
            'tax_payroll_with_daily_salary': self.tax_payroll_with_daily_salary,
            'total_tax_cost_breakdown': total_tax_cost_breakdown,
        }

    def __str__(self):
        """Método para mostrar información detallada de la instancia IMSS cuando se imprime"""
        # Formatear números para mejor legibilidad
        def fmt(value):
            if value is None:
                return "None"
            elif isinstance(value, float):
                return f"{value:.4f}"
            return str(value)
        
        # Construir la representación en secciones
        sections = []
        
        # Sección 1: Parámetros de inicialización
        init_params = [
            f"Salario IMSS: {fmt(self.salary)}",
            f"Salario Diario: {fmt(self.daily_salary)}",
            f"Período de Pago: {fmt(self.payment_period)}",
            f"Factor de Integración: {fmt(self.integration_factor)}",
            f"Clase de Riesgo: {fmt(self.risk_class)}",
            f"Porcentaje de Riesgo: {fmt(self.risk_percentage)}%",
            f"Salario Mínimo: {fmt(self.smg)}",
            f"Salario Mínimo Mensual: {fmt(self.smg_total_monthly_salary)}",
            f"Desglose IMSS: {fmt(self.imss_breakdown)}"
        ]
        sections.append("\n== PARÁMETROS DE INICIALIZACIÓN ==\n" + "\n".join(init_params))
        
        # Sección 2: Valores calculados principales
        calculated_values = [
            f"Salario Diario Integrado: {fmt(self.get_integrated_daily_wage())}",
            f"Cuota IMSS Patrón (V): {fmt(self.get_quota_employer())}",
            f"Cuota IMSS Trabajador (W): {fmt(self.get_quota_employee())}",
            f"Total IMSS (X): {fmt(self.get_total_imss())}",
            f"Retiro Patrón (Z): {fmt(self.get_retirement_employer())}",
            f"Cesantía y Vejez Patrón (AA): {fmt(self.get_severance_and_old_age_employer())}",
            f"RCV Patrón (AC): {fmt(self.get_total_rcv_employer())}",
            f"RCV Trabajador (AD): {fmt(self.get_total_rcv_employee())}",
            f"INFONAVIT Patrón (AE): {fmt(self.get_infonavit_employer())}",
            f"Impuesto Sobre Nómina (AF): {fmt(self.get_tax_payroll())}",
            f"Costo Total Patrón (AH): {fmt(self.get_total_employer())}",
            f"Costo Total Trabajador (AJ): {fmt(self.get_total_employee())}",
            f"Costo Social Total (AL): {fmt(self.get_total_social_cost())}",
            f"Costo Social Sugerido (AP): {fmt(self.get_total_social_cost_suggested())}"
        ]
        sections.append("\n== VALORES CALCULADOS ==\n" + "\n".join(calculated_values))
        
        # Sección 3: Valores de desglose (si están disponibles)
        if self.imss_breakdown and hasattr(self, 'quota_employer_with_daily_salary') and self.quota_employer_with_daily_salary is not None:
            breakdown_values = [
                f"Cuota IMSS Patrón con Salario Diario (V): {fmt(self.quota_employer_with_daily_salary)}",
                f"Cesantía y Vejez Patrón (AA): {fmt(self.severance_and_old_age_employer)}",
                f"RCV Patrón con Salario Diario (AC): {fmt(self.total_rcv_employer_with_daily_salary)}",
                f"INFONAVIT Patrón con Salario Diario (AE): {fmt(self.infonavit_employer_with_daily_salary)}",
                f"Impuesto Sobre Nómina con Salario Diario (AF): {fmt(self.tax_payroll_with_daily_salary)}"
            ]
            sections.append("\n== VALORES DE DESGLOSE (con Salario Diario) ==\n" + "\n".join(breakdown_values))
        
        # Unir todas las secciones
        return "\n\n".join(sections)
