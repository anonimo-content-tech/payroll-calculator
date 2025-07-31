rates_by_year = {
    "2023": [0.03150, 0.03281, 0.03575, 0.03751, 0.03869, 0.03953, 0.04016, 0.04241],
    "2024": [0.03150, 0.03413, 0.04000, 0.04353, 0.04588, 0.04756, 0.04882, 0.05331],
    "2025": [0.03150, 0.03544, 0.04426, 0.04954, 0.05307, 0.05559, 0.05747, 0.06422],
    "2026": [0.03150, 0.03676, 0.04851, 0.05556, 0.06026, 0.06361, 0.06613, 0.07513],
    "2027": [0.03150, 0.03807, 0.05276, 0.06157, 0.06745, 0.07164, 0.07479, 0.08603],
    "2028": [0.03150, 0.03939, 0.05701, 0.06759, 0.07464, 0.07967, 0.08345, 0.09694],
    "2029": [0.03150, 0.04070, 0.06126, 0.07360, 0.08183, 0.08770, 0.09211, 0.10784],
    "2030": [0.03150, 0.04202, 0.06552, 0.07962, 0.08902, 0.09573, 0.10077, 0.11875],
}

limits = [
    {"lower_limit":   0.01, "upper_limit":   278.80},
    {"lower_limit": 278.81, "upper_limit":   169.71},
    {"lower_limit": 170.84, "upper_limit":   226.28},
    {"lower_limit": 227.41, "upper_limit":   282.85},
    {"lower_limit": 283.98, "upper_limit":   339.42},
    {"lower_limit": 340.55, "upper_limit":   395.99},
    {"lower_limit": 397.12, "upper_limit":   452.56},
    {"lower_limit": 453.69, "upper_limit": float("inf")},
]

severance_and_old_age_by_year = {
    year: [
        {
            "lower_limit": limits[i]["lower_limit"],
            "upper_limit": limits[i]["upper_limit"],
            "percentage": pct
        }
        for i, pct in enumerate(rates_by_year[year])
    ]
    for year in rates_by_year
}

def get_rcv_table_by_year(year):
    """
    Obtiene la tabla RCV para un año específico.
    
    Args:
        year (str): El año para el cual se requiere la tabla RCV
        
    Returns:
        list: Lista de diccionarios con lower_limit, upper_limit y percentage
        
    Raises:
        KeyError: Si el año no está disponible en las tablas
    """
    if str(year) not in severance_and_old_age_by_year:
        available_years = list(severance_and_old_age_by_year.keys())
        raise KeyError(f"Año {year} no disponible. Años disponibles: {available_years}")
    
    return severance_and_old_age_by_year[str(year)]