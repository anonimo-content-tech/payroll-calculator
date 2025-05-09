class Parameters:
    # FACTOR DE INTEGRACIÓN
    INTEGRATION_FACTOR = 1.0493

    # VALOR SALARIAL DIARIO FISCAL (Probablemente signifique eso, pero es la UMA)
    VSDF = 113.14

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
        {'lower_limit': 0.01, 'upper_limit': 278.80, 'percentage': 3.150},
        {'lower_limit': 278.81, 'upper_limit': 169.71, 'percentage': 3.281},
        {'lower_limit': 170.84, 'upper_limit': 226.28, 'percentage': 3.575},
        {'lower_limit': 227.41, 'upper_limit': 282.85, 'percentage': 3.751},
        {'lower_limit': 283.98, 'upper_limit': 339.42, 'percentage': 3.869},
        {'lower_limit': 340.55, 'upper_limit': 395.99, 'percentage': 3.953},
        {'lower_limit': 397.12, 'upper_limit': 452.56, 'percentage': 4.016},
        {'lower_limit': 453.69, 'upper_limit': float(
            'inf'), 'percentage': 4.241}
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

    # Tabla de Crédito Salarial
    SALARY_CREDIT_TABLE = [
        {'lower_limit': 0.01, 'upper_limit': 872.85, 'credit': 407.02},
        {'lower_limit': 872.86, 'upper_limit': 1309.20, 'credit': 406.83},
        {'lower_limit': 1309.21, 'upper_limit': 1713.60, 'credit': 406.62},
        {'lower_limit': 1713.61, 'upper_limit': 1745.70, 'credit': 392.77},
        {'lower_limit': 1745.71, 'upper_limit': 2193.75, 'credit': 382.46},
        {'lower_limit': 2193.76, 'upper_limit': 2327.55, 'credit': 354.23},
        {'lower_limit': 2327.56, 'upper_limit': 2632.65, 'credit': 324.87},
        {'lower_limit': 2632.66, 'upper_limit': 3071.40, 'credit': 294.63},
        {'lower_limit': 3071.41, 'upper_limit': 3510.15, 'credit': 253.54},
        {'lower_limit': 3510.16, 'upper_limit': 3642.60, 'credit': 217.61},
        {'lower_limit': 3642.61, 'upper_limit': float('inf'), 'credit': 192.45},
    ]

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
        for range_data in Parameters.RETIREMENT_TABLE:
            if range_data['lower_limit'] <= salary_daily_wage <= range_data['upper_limit']:
                return range_data['percentage'] / 100  # Convertir a decimal
        # Último rango por defecto
        return Parameters.RETIREMENT_TABLE[-1]['percentage'] / 100

    @staticmethod
    def calculate_wage_and_salary_dsi(smg_multiplier, payment_period):
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
        period_smg_value = daily_smg_value * payment_period
        
        # Si el salario es menor que el valor calculado, usar el salario
        return period_smg_value
