from .imss import IMSS
from .isr import ISR
from typing import Optional


class Saving:
    # ------------------------------------------------------ INICIALIZACIÓN DE CLASE ------------------------------------------------------

    def __init__(self, wage_and_salary, wage_and_salary_dsi, fixed_fee_dsi, commission_percentage_dsi, imss_instance: Optional[IMSS] = None, isr_instance: Optional[ISR] = None):
        self.wage_and_salary = wage_and_salary
        self.imss: Optional[IMSS] = imss_instance
        self.isr: Optional[ISR] = isr_instance
        self.wage_and_salary_dsi = wage_and_salary_dsi
        self.fixed_fee_dsi = fixed_fee_dsi
        self.commission_percentage_dsi = commission_percentage_dsi

    def set_imss(self, imss_instance: IMSS) -> None:
        """Establece una instancia de IMSS para usar sus métodos"""
        self.imss = imss_instance

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
        return self.wage_and_salary - self.wage_and_salary_dsi

    # Calcular la Comisión DSI ------- Columna Qnumero
    def get_commission_dsi(self):
        return self.wage_and_salary * self.commission_percentage_dsi

    # Calcular el Costo Total DSI ------- Columna Rnumero
    def get_dsi_scheme_biweekly_total(self):
        return self.wage_and_salary + self.fixed_fee_dsi + self.get_commission_dsi()

    # ------------------------------------------------------ CALCULO DE AHORRO ------------------------------------------------------

    # Calcular el ahorro ------- Columna Tnumero
    def get_amount(self):
        return self.get_traditional_scheme_biweekly_total() - self.get_dsi_scheme_biweekly_total()

    # Calcular el porcentaje de ahorro ------- Columna Unumero
    def get_percentage(self):
        return self.get_amount() / self.get_traditional_scheme_biweekly_total()

    # ------------------------------------------------------ CALCULO DE ESQUEMA TRADICIONAL MENSUAL ------------------------------------------------------

    # Obtener el ISR de Retenciones ------- Columna ABnumero
    def get_isr_retention(self):
        if self.isr is None:
            raise ValueError(
                "ISR instance is not set. Use set_isr() method first.")
        return self.isr.get_tax_payable() if self.isr.get_tax_payable() > self.isr.get_tax_in_favor() else (self.isr.get_tax_in_favor() * -1)

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

    # Calcular Percepción Actual DSI ------- Columna AOnumero
    def get_current_perception_dsi(self):
        # Columna AJ - Columna AK - Columna AL - Columna AM - Columna AN
        return self.get_total_wage_and_salary_dsi() - 0 - 0 - 0 - 0
    
    # ------------------------------------------------------ CALCULO DE INCREMENTO ------------------------------------------------------
    
    # Calcular el incremento ------- Columna AQnumero
    def get_increment(self):
        return self.get_current_perception_dsi() - self.get_current_perception()
    
    # Calcular el incremento en porcentaje ------- Columna ARnumero
    def get_increment_percentage(self):
        return self.get_increment() / self.get_current_perception()