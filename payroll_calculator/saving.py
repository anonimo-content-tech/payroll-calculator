from .imss import IMSS
from .isr import ISR
from typing import Optional


class Saving:
    # ------------------------------------------------------ INICIALIZACIÓN DE CLASE ------------------------------------------------------

    # Remove fixed_fee_dsi from parameters, make imss_instance non-optional
    def __init__(self, wage_and_salary, wage_and_salary_dsi, commission_percentage_dsi, count_minimum_salary, imss_instance: IMSS, isr_instance: Optional[ISR] = None, minimum_threshold_salary: Optional[float] = None, productivity: Optional[float] = None):
        self.wage_and_salary = wage_and_salary
        self.original_wage_and_salary = wage_and_salary  # Guardar el valor original
        self.imss: IMSS = imss_instance # Now non-optional
        self.isr: Optional[ISR] = isr_instance
        self.wage_and_salary_dsi = wage_and_salary_dsi
        self.minimum_threshold_salary = minimum_threshold_salary # Store the new parameter
        # Calculate fixed_fee_dsi using the IMSS instance method and pass minimum_threshold_salary
        self.fixed_fee_dsi = self.imss.get_fixed_fee_for_smg(minimum_threshold_salary_override=self.minimum_threshold_salary)
        self.commission_percentage_dsi = commission_percentage_dsi
        self.count_minimum_salary = count_minimum_salary
        self.current_productivity = productivity
        
        self.dsi_total_with_breakdown = None

    # set_imss might be less necessary if IMSS is required at init, but keep for flexibility
    def set_imss(self, imss_instance: IMSS) -> None:
        """Establece una instancia de IMSS para usar sus métodos"""
        self.imss = imss_instance
        # Recalculate fixed_fee_dsi if IMSS instance changes, passing minimum_threshold_salary
        self.fixed_fee_dsi = self.imss.get_fixed_fee_for_smg(minimum_threshold_salary_override=self.minimum_threshold_salary)

    def set_isr(self, isr_instance: ISR) -> None:
        """Establece una instancia de ISR para usar sus métodos"""
        self.isr = isr_instance

    # ------------------------------------------------------ CALCULO DE ESQUEMA TRADICIONAL QUINCENAL ------------------------------------------------------

    # Obtener el total de esquema tradicional ------- Columna Jnumero
    def get_total_traditional_scheme(self):
        return self.imss.get_total_employer()

    # Obtener el esquema tradicional de ahorro ------- Columna Knumero
    def get_traditional_scheme_biweekly_total(self):
        """Calcula el esquema tradicional"""
        if self.imss is None:
            raise ValueError(
                "IMSS instance is not set. Use set_imss() method first.")
        return self.wage_and_salary + self.imss.get_total_employer()

    # ------------------------------------------------------ CALCULO DE ESQUEMA DSI QUINCENAL ------------------------------------------------------

    # Calcular la productividad según el Total de Ingresos y Sueldos y Salarios DSI ------- Columna Nnumero
    def get_productivity(self, use_original_wage=False):
        # Usar el valor original si se especifica o si wage_and_salary ha sido modificado
        wage_to_use = self.original_wage_and_salary if use_original_wage else self.wage_and_salary
        employee_productivity = wage_to_use - self.wage_and_salary_dsi
        print("EMPLOYEE PRODUCTIVITY: ", employee_productivity, " WAGE_TO_USE: ", wage_to_use, " SELF.WAGE AND SALARY DSI: ", self.wage_and_salary_dsi)
        return employee_productivity if self.current_productivity is None else employee_productivity + self.current_productivity

    # Calcular la Comisión DSI ------- Columna Qnumero
    def get_commission_dsi(self):
        return self.wage_and_salary * self.commission_percentage_dsi

    # Calcular el Costo Total DSI ------- Columna Rnumero
    def get_dsi_scheme_biweekly_total(self, original_wage_and_salary=None, use_imss_breakdown=False):
        if self.imss is None:
            raise ValueError(
                "IMSS instance is not set. Use set_imss() method first.")
            
        total_to_use = self.fixed_fee_dsi
        if use_imss_breakdown:
            # Usar self.wage_and_salary si original_wage_and_salary es None
            wage_to_use = self.wage_and_salary if original_wage_and_salary is None else original_wage_and_salary
            return wage_to_use + self.imss.total_tax_cost_breakdown + self.get_commission_dsi()
            total_to_use = self.fixed_fee_dsi if self.imss.total_tax_cost_breakdown <= 0 else self.imss.total_tax_cost_breakdown
        # This method now correctly uses the internally calculated self.fixed_fee_dsi
        return self.wage_and_salary + self.fixed_fee_dsi + self.get_commission_dsi()

    # ------------------------------------------------------ CALCULO DE AHORRO ------------------------------------------------------

    # Calcular el ahorro ------- Columna Tnumero
    def get_amount(self, use_imss_breakdown=False):
        if use_imss_breakdown:
            return self.get_traditional_scheme_biweekly_total() - self.get_dsi_scheme_biweekly_total(use_imss_breakdown=True)
        return self.get_traditional_scheme_biweekly_total() - self.get_dsi_scheme_biweekly_total()

    # Calcular el porcentaje de ahorro ------- Columna Unumero
    def get_percentage(self, use_imss_breakdown=False):
        if use_imss_breakdown:
            return self.get_amount(use_imss_breakdown=True) / self.get_traditional_scheme_biweekly_total()
        return self.get_amount() / self.get_traditional_scheme_biweekly_total()

    # ------------------------------------------------------ CALCULO DE ESQUEMA TRADICIONAL MENSUAL ------------------------------------------------------

    # Obtener el ISR de Retenciones ------- Columna ABnumero
    def get_isr_retention(self, use_smg=False):
        if self.isr is None:
            raise ValueError(
                "ISR instance is not set. Use set_isr() method first.")
        return self.isr.get_tax_payable(use_smg) if self.isr.get_tax_payable(use_smg) > self.isr.get_tax_in_favor() else (self.isr.get_tax_in_favor() * -1)

    # Obtener el total de Retenciones ------- Columna AEnumero
    def get_total_retentions(self, use_imss_breakdown=False):
        if use_imss_breakdown:
            # Columna AB + Columna AC + Columna AD
            print("self.get_total_isr_retention_dsi(): ", self.get_total_isr_retention_dsi(), " self.imss.get_quota_employee(use_imss_breakdown): ", self.imss.get_quota_employee(use_imss_breakdown), " self.imss.get_severance_and_old_age_employee(use_imss_breakdown): ", self.imss.get_severance_and_old_age_employee(use_imss_breakdown), )
            isr_employee_dsi = self.isr.isr_imss_breakdown.get_tax_payable() if self.isr.isr_imss_breakdown is not None else 0
            return isr_employee_dsi + self.imss.get_quota_employee(use_imss_breakdown) + self.imss.get_severance_and_old_age_employee(use_imss_breakdown)
        # Columna AB + Columna AC + Columna AD
        return self.isr.get_tax_payable() + self.imss.get_quota_employee() + self.imss.get_total_rcv_employee()

    # Calcular percepción actual ------- Columna AFnumero
    def get_current_perception(self, original_wage_and_salary=None, use_imss_breakdown=False):
        if use_imss_breakdown:
            # print("================================================ ORIGINAL WAGE AND SALARY: ", original_wage_and_salary, " SELF.GET_TOTAL_RETENTIONS: ", self.get_total_retentions(), " SELF.GET_TOTAL_RETENTIONS DS ================================================")
            return original_wage_and_salary - self.get_total_retentions()
        return self.wage_and_salary - self.get_total_retentions(use_imss_breakdown)

    # ------------------------------------------------------ CALCULO DE ESQUEMA DSI MENSUAL ------------------------------------------------------

    # Obtener Asimilados ------- Columna AInumero
    def get_assimilated(self):
        return self.get_productivity()

    # Calcular Total de Ingresos ------- Columna AJnumero
    def get_total_wage_and_salary_dsi(self):
        # print("================== SELF.WAGE AND SALARY: ", self.wage_and_salary_dsi, " SELF.GET_ASSIMILATED QUE ES LA PRODUCTIVIDAD(): ", self.get_assimilated(), " ==================")
        return self.wage_and_salary_dsi + self.get_assimilated()
    
    # Calcular Total de Retenciones DSI ------- Columna AKnumero
    def get_total_isr_retention_dsi(self, use_imss_breakdown=False):
        if use_imss_breakdown:
            # print("SELF.GET_ISR_RETENTION(TRUE): ", self.get_isr_retention(True), " SELF.COUNT_MINIMUM_SALARY: ", self.count_minimum_salary, " SELF.WAGE AND SALARY: ", self.wage_and_salary, " SELF.WAGE AND SALARY DSI: ", self.wage_and_salary_dsi)
            return self.get_isr_retention(True) if self.wage_and_salary > self.wage_and_salary_dsi else 0
        # print("SELF.GET_ISR_RETENTION(TRUE): ", self.get_isr_retention(True), " SELF.COUNT_MINIMUM_SALARY: ", self.count_minimum_salary, " SELF.WAGE AND SALARY: ", self.wage_and_salary, " SELF.WAGE AND SALARY DSI: ", self.wage_and_salary_dsi)
        return self.get_isr_retention(True) if self.wage_and_salary > self.wage_and_salary_dsi else 0
        return self.get_isr_retention(True) if self.count_minimum_salary > 1 else 0

    # Calcular Percepción Actual DSI ------- Columna AOnumero
    def get_current_perception_dsi(self, original_wage_and_salary=None, use_imss_breakdown=False):
        if use_imss_breakdown:
            # print(" DENTRO DEL IFFFFFFFFF SELF.WAGE AND SALARY DSI: ", self.get_total_wage_and_salary_dsi(), " SELF.GET_TOTAL_ISR_RETENTION_DSI: ", self.get_total_retentions(use_imss_breakdown))
            return original_wage_and_salary - self.get_total_retentions(use_imss_breakdown)
        # Columna AJ - Columna AK - Columna AL - Columna AM - Columna AN
        # return self.get_total_wage_and_salary_dsi() - self.get_total_isr_retention_dsi() - 0 - 0 - 0
        return self.get_total_wage_and_salary_dsi() - self.get_total_isr_retention_dsi()
    
    # ------------------------------------------------------ CALCULO DE INCREMENTO ------------------------------------------------------
    
    # Calcular el incremento ------- Columna AQnumero
    def get_increment(self):
        return self.get_current_perception_dsi() - self.get_current_perception()
    
    # Calcular el incremento en porcentaje ------- Columna ARnumero
    def get_increment_percentage(self):
        return self.get_increment() / self.get_current_perception()

    def calculate_breakdown_values_for_dsi(self, use_direct_daily_salary=False, period_salary=None):
        """
        Calcula y almacena los valores desglosados usando el esquema DSI.
        
        Parameters:
        - use_direct_daily_salary: Si es True, utiliza el salario diario directo para los cálculos
        - period_salary: Salario del período a utilizar cuando use_direct_daily_salary es True
        """
        
        if self.imss is None:
            raise ValueError("IMSS instance is not set. Use set_imss() method first.")
            
        # Guardar el valor original de wage_and_salary
        original_wage_and_salary = self.wage_and_salary
        
        # Si use_direct_daily_salary es True y se proporciona period_salary, usar ese valor
        if use_direct_daily_salary and period_salary is not None:
            # Temporalmente reemplazar wage_and_salary con period_salary
            self.wage_and_salary = period_salary
        
        try:
            # Invocar la función get_dsi_scheme_biweekly_total con use_imss_breakdown=
            # print("ORIGINAL WAGE AND SALARY: ", original_wage_and_salary)
            dsi_total_fiscal_cost = self.get_dsi_scheme_biweekly_total(original_wage_and_salary, use_imss_breakdown=True)
            
            saving_amount = self.get_amount(use_imss_breakdown=True)
            
            saving_percentage = self.get_percentage(use_imss_breakdown=True)
            
            saving_traditional_scheme_total = self.get_traditional_scheme_biweekly_total()
            # print("================================== SAVING TRADITIONAL SCHEME TOTAL: ", saving_traditional_scheme_total, " =========================================")

            saving_total_retentions_isr = self.isr.get_tax_payable()
            
            # print("SELF.WAGE AND SALARY: ", self.wage_and_salary)
            saving_total_retentions_isr_dsi = self.get_total_isr_retention_dsi(use_imss_breakdown=True)
            # print("VALOR DE SAVING TOTAL RETENTIONS ISR DSI: ", saving_total_retentions_isr_dsi)
            
            saving_total_retentions_dsi = self.get_total_retentions(use_imss_breakdown=True)
            
            saving_total_current_perception_dsi = self.get_current_perception_dsi(original_wage_and_salary, use_imss_breakdown=True)
            # print("SAVING TOTAL CURRENT PERCEPTION: ", saving_total_current_perception_dsi)

            # Guardar temporalmente los valores actuales para calcular el incremento
            current_perception = self.get_current_perception(original_wage_and_salary, use_imss_breakdown=True)
            # print("CURRENT PERCEPTION: ", current_perception, " CON ORIGINAL WAGE AND SALARY: ", original_wage_and_salary)
            
            # Calcular el incremento y porcentaje de incremento usando los valores guardados
            saving_get_increment = saving_total_current_perception_dsi - current_perception
            saving_get_increment_percentage = saving_get_increment / current_perception if current_perception != 0 else 0
            
            saving_productivity = self.get_productivity(use_original_wage=True)
            print("SAVING PRODUCTIVITY: ", saving_productivity)
            
            # Aquí puedes almacenar el resultado en una variable si es necesario
            self.dsi_total_with_breakdown = dsi_total_fiscal_cost
            return { 
                'dsi_total_fiscal_cost': dsi_total_fiscal_cost, 
                'saving_amount': saving_amount, 
                'saving_percentage': saving_percentage, 
                'saving_total_retentions_isr_dsi': saving_total_retentions_isr_dsi,
                'saving_total_retentions_dsi': saving_total_retentions_dsi,
                'saving_total_current_perception_dsi': saving_total_current_perception_dsi,
                'saving_total_current_perception': current_perception,
                'saving_get_increment': saving_get_increment,
                'saving_get_increment_percentage': saving_get_increment_percentage,
                'saving_wage_and_salary': self.wage_and_salary,
                'saving_productivity': saving_productivity,
                'use_direct_daily_salary': use_direct_daily_salary  # Agregar este valor al resultado
            }
        finally:
            # Restaurar el valor original de wage_and_salary
            if use_direct_daily_salary and period_salary is not None:
                self.wage_and_salary = original_wage_and_salary
