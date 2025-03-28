class Parameters:
    INTEGRATION_FACTOR = 1.0493
    # VALOR SALARIAL DIARIO FISCAL (Probablemente signifique eso, pero es la UMA)
    VSDF = 113.14
    
    # TOPE CF
    TCF = VSDF * 3
    
    # Tope de cotización a 25 SMG (TC1)
    CONTRIBUTION_CEILING = VSDF * 25
    
    # Cuota fija patrón (20.4000%)
    FIXED_FEE = 0.204
    
    # Excedente patrón
    SURPLUS = 0.011
    
    def __init__(self):
        self.integration_factor = self.INTEGRATION_FACTOR
        self.vsdf = self.VSDF

        