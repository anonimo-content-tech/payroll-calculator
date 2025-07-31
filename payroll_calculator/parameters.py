class Parameters:
    # FACTOR DE INTEGRACIÓN
    INTEGRATION_FACTOR = 1.0493

    # VALOR SALARIAL DIARIO FISCAL (Probablemente signifique eso, pero es la UMA)
    VSDF = 108.57

    # TOPE CF
    TCF = VSDF * 3

    # NOTA: Desconozco porque hay más de un TC si se calculan de la misma forma, pero lo dejamos así.

    # Tope de cotización a 25 SMG (TC1)
    CONTRIBUTION_CEILING = VSDF * 25

    # Tope de cotización a 25 SMG (TC2)
    CONTRIBUTION_CEILING_2 = VSDF * 25

    # Cuota fija patrón (20.4000%)
    FIXED_FEE = 0.204

    # Excedente patrón
    SURPLUS_EMPLOYER = 0.011

    # Excedente trabajador
    SURPLUS_EMPLOYEE = 0.004

    # Salario mínimo del área geográfica
    SMG = 278.80

    # Prestaciones en dinero Patrón
    CASH_BENEFITS_EMPLOYER = 0.0070

    # Prestaciones en dinero Trabajador
    CASH_BENEFITS_EMPLOYEE = 0.0025

    # Prestaciones en especie Patrón
    BENEFITS_IN_KIND_EMPLOYER = 0.0105

    # Prestaciones en especie Trabajador
    BENEFITS_IN_KIND_EMPLOYEE = 0.00375

    # Invalidez y vida Patrón
    INVALIDITY_AND_RETIREMENT_EMPLOYER = 0.0175

    # Invalidez y vida Trabajador
    INVALIDITY_AND_RETIREMENT_EMPLOYEE = 0.00625

    # Guarderías y prestaciones sociales
    CHILDCARE = 0.01

    # Retiro patrón
    RETIREMENT_EMPLOYER = 0.02

    # Tabla de Retiro, Cesantía y Vejez
    RETIREMENT_TABLE = [
        {'lower_limit': 0.01, 'upper_limit': 278.80, 'percentage': 3.1500},
        {'lower_limit': 278.81, 'upper_limit': 162.86, 'percentage': 3.2810},
        {'lower_limit': 163.94, 'upper_limit': 217.14, 'percentage': 3.5750},
        {'lower_limit': 218.23, 'upper_limit': 271.43, 'percentage': 3.7510},
        {'lower_limit': 272.51, 'upper_limit': 325.71, 'percentage': 3.8690},
        {'lower_limit': 326.80, 'upper_limit': 380.00, 'percentage': 3.9530},
        {'lower_limit': 381.08, 'upper_limit': 434.28, 'percentage': 4.0160},
        {'lower_limit': 435.37, 'upper_limit': float(
            'inf'), 'percentage': 4.2410}
    ]

    # INFONAVIT del Patrón %
    INFONAVIT_EMPLOYER = 0.05

    # Impuesto estatal sobre nómina
    STATE_PAYROLL_TAX = 0.03

    # Cesantía y vejez Trabajador
    SEVERANCE_AND_OLD_AGE_EMPLOYEE = 0.01125

    # 2.5 INCREMENTO
    INCREASE = 0.025

    def __init__(self):
        self.integration_factor = self.INTEGRATION_FACTOR
        self.vsdf = self.VSDF

    # Porcentajes de riesgo en el trabajo
    RISK_LEVELS = {
        'I': 0.0054355,    # RIESGO BAJO DE VIDA
        'II': 0.0113065,   # RIESGO ORDINARIO DE VIDA
        'III': 0.025984,  # RIESGO MEDIO DE VIDA
        'IV': 0.0465325,   # RIESGO ALTO DE VIDA
        'V': 0.0758875    # RIESGO MAXIMO DE VIDA
    }

    @staticmethod
    def get_isr_table(payment_period):
        """
        Obtiene la tabla ISR para el periodo de pago especificado
        Args:
            payment_period (int): Periodo de pago (1, 7, 10, 15, 30)
        Returns:
            list: Tabla ISR correspondiente al periodo
        """
        from .isr_tables import get_isr_table
        return get_isr_table(payment_period)
    
    # Tabla de Crédito Salarial
    @staticmethod
    def get_employee_subsidy_table(payment_period):
        """
        Obtiene la tabla de subsidio para el periodo de pago especificado
        Args:
            payment_period (int): Periodo de pago (1, 7, 10, 15, 30)
        Returns:
            list: Tabla de subsidio correspondiente al periodo
        """
        from.isr_tables import get_employee_subsidy_table
        return get_employee_subsidy_table(payment_period)

    @staticmethod
    def get_risk_percentage(risk_class):
        risk_class = str(risk_class).upper()
        if risk_class not in Parameters.RISK_LEVELS:
            raise ValueError(
                "Invalid risk class. Must be one of: I, II, III, IV, V, is receiving: ", risk_class)
        return Parameters.RISK_LEVELS[risk_class]

    @staticmethod
    def get_retirement_percentage(salary_daily_wage):
        """
        Determina el porcentaje de retiro basado en el salario diario
        Args:
            salary_daily_wage (float): Salario diario
        Returns:
            float: Porcentaje aplicable
        """
        # Obtener la tabla RCV del año actual
        rcv_table = Parameters.get_rcv_table_by_year()
        
        for range_data in rcv_table:
            if range_data['lower_limit'] <= salary_daily_wage <= range_data['upper_limit']:
                return range_data['percentage']
        
        # Último rango por defecto
        return rcv_table[-1]['percentage']

    @staticmethod
    def calculate_wage_and_salary_dsi(smg_multiplier, payment_period=None):
        
        """
        Calcula el salario DSI basado en un múltiplo del salario mínimo
        
        Args:
            salary (float): Salario base
            smg_multiplier (float): Multiplicador del salario mínimo (1, 1.05, 2, etc.)
            payment_period (int): Periodo de pago (1, 7, 15, 30)
            
        Returns:
            float: Valor calculado para wage_and_salary_dsi
        """
        daily_smg_value = Parameters.SMG * smg_multiplier
        
        if payment_period is None:
            return daily_smg_value
        
        period_smg_value = daily_smg_value * payment_period
        
        # Si el salario es menor que el valor calculado, usar el salario
        return period_smg_value
    
    @staticmethod
    def get_rcv_table_by_year():
        from datetime import datetime
        from .rcv_tables import get_rcv_table_by_year
        
        current_year = str(datetime.now().year)
        return get_rcv_table_by_year(current_year)
