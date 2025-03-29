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
    SURPLUS = 0.011

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

    # Guarderías
    CHILDCARE = 0.01

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
