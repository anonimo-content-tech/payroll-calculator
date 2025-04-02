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
        {'lower_limit': 453.69, 'upper_limit': float('inf'), 'percentage': 4.241}
    ]

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
    def get_risk_percentage(risk_class):
        risk_class = str(risk_class).upper()
        if risk_class not in Parameters.RISK_LEVELS:
            raise ValueError(
                "Invalid risk class. Must be one of: I, II, III, IV, V")
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
        return Parameters.RETIREMENT_TABLE[-1]['percentage'] / 100  # Último rango por defecto
