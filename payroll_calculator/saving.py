from .imss import IMSS
from .isr import ISR
from typing import Optional


class Saving:
    # ------------------------------------------------------ INICIALIZACIÓN DE CLASE ------------------------------------------------------

    # Remove fixed_fee_dsi from parameters, make imss_instance non-optional
    def __init__(self, wage_and_salary, wage_and_salary_dsi, commission_percentage_dsi, count_minimum_salary, imss_instance: IMSS, isr_instance: Optional[ISR] = None, minimum_threshold_salary: Optional[float] = None, productivity: Optional[float] = None):
        self.wage_and_salary = wage_and_salary
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

    # Obtener el esquema tradicional de ahorro ------- Columna Knumero
    def get_traditional_scheme_biweekly_total(self):
        """Calcula el esquema tradicional"""
        if self.imss is None:
            raise ValueError(
                "IMSS instance is not set. Use set_imss() method first.")
        return self.wage_and_salary + self.imss.get_total_employer()

    # ------------------------------------------------------ CALCULO DE ESQUEMA DSI QUINCENAL ------------------------------------------------------

    # Calcular la productividad según el Total de Ingresos y Sueldos y Salarios DSI ------- Columna Nnumero
    def get_productivity(self):
        employee_productivity = self.wage_and_salary - self.wage_and_salary_dsi 
        return employee_productivity if self.current_productivity is None else employee_productivity + self.current_productivity

    # Calcular la Comisión DSI ------- Columna Qnumero
    def get_commission_dsi(self):
        return self.wage_and_salary * self.commission_percentage_dsi

    # Calcular el Costo Total DSI ------- Columna Rnumero
    def get_dsi_scheme_biweekly_total(self, use_imss_breakdown=False):
        if self.imss is None:
            raise ValueError(
                "IMSS instance is not set. Use set_imss() method first.")
            
        total_to_use = self.fixed_fee_dsi
        if use_imss_breakdown:
            total_to_use = self.fixed_fee_dsi if self.imss.total_tax_cost_breakdown <= 0 else self.imss.total_tax_cost_breakdown
        # This method now correctly uses the internally calculated self.fixed_fee_dsi
        print("SELF.WAGE AND SALARY: ", self.wage_and_salary, " TOTAL TO USE: ", total_to_use," COMISSION DSI: ", self.get_commission_dsi())
        return self.wage_and_salary + total_to_use + self.get_commission_dsi()

    # ------------------------------------------------------ CALCULO DE AHORRO ------------------------------------------------------

    # Calcular el ahorro ------- Columna Tnumero
    def get_amount(self, use_imss_breakdown=False):
        if use_imss_breakdown:
            print("==================== DENTRO DEL IF ==================== GET TRADITIONAL SCHEME BIWEEKLY TOTAL: ", self.get_traditional_scheme_biweekly_total(), " GET DSI SCHEME BIWEEKLY TOTAL: ", self.get_dsi_scheme_biweekly_total()," ====================")
            return self.get_traditional_scheme_biweekly_total() - self.get_dsi_scheme_biweekly_total(use_imss_breakdown=True)
        print("==================== GET TRADITIONAL SCHEME BIWEEKLY TOTAL: ", self.get_traditional_scheme_biweekly_total(), " GET DSI SCHEME BIWEEKLY TOTAL: ", self.get_dsi_scheme_biweekly_total()," ====================")
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
    def get_total_retentions(self):
        # Columna AB + Columna AC + Columna AD
        return self.isr.get_tax_payable() + self.imss.get_quota_employee() + self.imss.get_total_rcv_employee()

    # Calcular percepción actual ------- Columna AFnumero
    def get_current_perception(self):
        return self.wage_and_salary - self.get_total_retentions()

    # ------------------------------------------------------ CALCULO DE ESQUEMA DSI MENSUAL ------------------------------------------------------

    # Obtener Asimilados ------- Columna AInumero
    def get_assimilated(self):
        return self.get_productivity()

    # Calcular Total de Ingresos ------- Columna AJnumero
    def get_total_wage_and_salary_dsi(self):
        return self.wage_and_salary_dsi + self.get_assimilated()
    
    # Calcular Total de Retenciones DSI ------- Columna AKnumero
    def get_total_isr_retention_dsi(self):
        return self.get_isr_retention(True) if self.count_minimum_salary > 1 else 0

    # Calcular Percepción Actual DSI ------- Columna AOnumero
    def get_current_perception_dsi(self):
        # Columna AJ - Columna AK - Columna AL - Columna AM - Columna AN
        return self.get_total_wage_and_salary_dsi() - self.get_total_isr_retention_dsi() - 0 - 0 - 0
    
    # ------------------------------------------------------ CALCULO DE INCREMENTO ------------------------------------------------------
    
    # Calcular el incremento ------- Columna AQnumero
    def get_increment(self):
        return self.get_current_perception_dsi() - self.get_current_perception()
    
    # Calcular el incremento en porcentaje ------- Columna ARnumero
    def get_increment_percentage(self):
        return self.get_increment() / self.get_current_perception()

    def calculate_breakdown_values_for_dsi(self):
        """
        Calcula y almacena los valores desglosados usando el esquema DSI.
        """
        print("Ejecutando calculate_breakdown_values_for_dsi con wage_and_salary_dsi de:", self.wage_and_salary_dsi)

        if self.imss is None:
            raise ValueError("IMSS instance is not set. Use set_imss() method first.")

        # Invocar la función get_dsi_scheme_biweekly_total con use_imss_breakdown=True
        dsi_total = self.get_dsi_scheme_biweekly_total(use_imss_breakdown=True)
        print("Total DSI calculado:", dsi_total)
        
        saving_amount = self.get_amount(use_imss_breakdown=True)
        
        saving_percentage = self.get_percentage(use_imss_breakdown=True)

        # Aquí puedes almacenar el resultado en una variable si es necesario
        self.dsi_total_with_breakdown = dsi_total
        return { 'dsi_total': dsi_total, 'saving_amount': saving_amount, 'saving_percentage': saving_percentage }
