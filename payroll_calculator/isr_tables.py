def get_isr_table(payment_period: int):
    """
    Returns the ISR table based on the payment period
    Args:
        payment_period (int): Period type (1, 7, 10, 15, 30 etc)
    Returns:
        list: List of dictionaries containing the ISR ranges and values
    """
    tables = {
        1: [
            {'lower_limit': 0.01, 'upper_limit': 24.54, 'fixed_fee': 0.00, 'percentage': 0.0192},
            {'lower_limit': 24.55, 'upper_limit': 208.29, 'fixed_fee': 0.47, 'percentage': 0.0640},
            {'lower_limit': 208.30, 'upper_limit': 366.05, 'fixed_fee': 12.23, 'percentage': 0.1088},
            {'lower_limit': 366.06, 'upper_limit': 425.52, 'fixed_fee': 29.40, 'percentage': 0.1600},
            {'lower_limit': 425.53, 'upper_limit': 509.46, 'fixed_fee': 38.91, 'percentage': 0.1792},
            {'lower_limit': 509.47, 'upper_limit': 1027.52, 'fixed_fee': 53.95, 'percentage': 0.2136},
            {'lower_limit': 1027.53, 'upper_limit': 1619.51, 'fixed_fee': 164.61, 'percentage': 0.2352},
            {'lower_limit': 1619.52, 'upper_limit': 3091.90, 'fixed_fee': 303.85, 'percentage': 0.3000},
            {'lower_limit': 3091.91, 'upper_limit': 4122.54, 'fixed_fee': 745.56, 'percentage': 0.3200},
            {'lower_limit': 4122.55, 'upper_limit': 12367.62, 'fixed_fee': 1075.37, 'percentage': 0.3400},
            {'lower_limit': 12367.63, 'upper_limit': float('inf'), 'fixed_fee': 3878.69, 'percentage': 0.3500}
        ],
        7: [
            {'lower_limit': 0.01, 'upper_limit': 171.78, 'fixed_fee': 0.00, 'percentage': 0.0192},
            {'lower_limit': 171.79, 'upper_limit': 1458.03, 'fixed_fee': 3.29, 'percentage': 0.0640},
            {'lower_limit': 1458.04, 'upper_limit': 2562.35, 'fixed_fee': 85.61, 'percentage': 0.1088},
            {'lower_limit': 2562.36, 'upper_limit': 2978.64, 'fixed_fee': 205.80, 'percentage': 0.1600},
            {'lower_limit': 2978.65, 'upper_limit': 3566.22, 'fixed_fee': 272.37, 'percentage': 0.1792},
            {'lower_limit': 3566.23, 'upper_limit': 7192.64, 'fixed_fee': 377.65, 'percentage': 0.2136},
            {'lower_limit': 7192.65, 'upper_limit': 11336.57, 'fixed_fee': 1152.27, 'percentage': 0.2352},
            {'lower_limit': 11336.58, 'upper_limit': 21643.30, 'fixed_fee': 2126.95, 'percentage': 0.3000},
            {'lower_limit': 21643.31, 'upper_limit': 28857.78, 'fixed_fee': 5218.92, 'percentage': 0.3200},
            {'lower_limit': 28857.79, 'upper_limit': 86573.34, 'fixed_fee': 7527.59, 'percentage': 0.3400},
            {'lower_limit': 86573.35, 'upper_limit': float('inf'), 'fixed_fee': 27150.83, 'percentage': 0.3500}
        ],
        10: [
            {'lower_limit': 0.01, 'upper_limit': 245.40, 'fixed_fee': 0.00, 'percentage': 0.0192},
            {'lower_limit': 245.41, 'upper_limit': 2082.90, 'fixed_fee': 4.70, 'percentage': 0.0640},
            {'lower_limit': 2082.91, 'upper_limit': 3660.50, 'fixed_fee': 122.30, 'percentage': 0.1088},
            {'lower_limit': 3660.51, 'upper_limit': 4255.20, 'fixed_fee': 294.00, 'percentage': 0.1600},
            {'lower_limit': 4255.21, 'upper_limit': 5094.60, 'fixed_fee': 389.10, 'percentage': 0.1792},
            {'lower_limit': 5094.61, 'upper_limit': 10275.20, 'fixed_fee': 539.50, 'percentage': 0.2136},
            {'lower_limit': 10275.21, 'upper_limit': 16195.10, 'fixed_fee': 1646.10, 'percentage': 0.2352},
            {'lower_limit': 16195.11, 'upper_limit': 30919.00, 'fixed_fee': 3038.50, 'percentage': 0.3000},
            {'lower_limit': 30919.01, 'upper_limit': 41225.40, 'fixed_fee': 7455.60, 'percentage': 0.3200},
            {'lower_limit': 41225.41, 'upper_limit': 123676.20, 'fixed_fee': 10753.70, 'percentage': 0.3400},
            {'lower_limit': 123676.21, 'upper_limit': float('inf'), 'fixed_fee': 38786.90, 'percentage': 0.3500}
        ],
        15: [
            {'lower_limit': 0.01, 'upper_limit': 368.10, 'fixed_fee': 0.00, 'percentage': 0.0192},
            {'lower_limit': 368.11, 'upper_limit': 3124.35, 'fixed_fee': 7.05, 'percentage': 0.0640},
            {'lower_limit': 3124.36, 'upper_limit': 5490.75, 'fixed_fee': 183.45, 'percentage': 0.1088},
            {'lower_limit': 5490.76, 'upper_limit': 6382.80, 'fixed_fee': 441.00, 'percentage': 0.1600},
            {'lower_limit': 6382.81, 'upper_limit': 7641.90, 'fixed_fee': 583.65, 'percentage': 0.1792},
            {'lower_limit': 7641.91, 'upper_limit': 15412.80, 'fixed_fee': 809.25, 'percentage': 0.2136},
            {'lower_limit': 15412.81, 'upper_limit': 24292.65, 'fixed_fee': 2469.15, 'percentage': 0.2352},
            {'lower_limit': 24292.66, 'upper_limit': 46378.50, 'fixed_fee': 4557.75, 'percentage': 0.3000},
            {'lower_limit': 46378.51, 'upper_limit': 61838.10, 'fixed_fee': 11183.40, 'percentage': 0.3200},
            {'lower_limit': 61838.11, 'upper_limit': 185514.30, 'fixed_fee': 16130.55, 'percentage': 0.3400},
            {'lower_limit': 185514.31, 'upper_limit': float('inf'), 'fixed_fee': 58180.35, 'percentage': 0.3500}
        ],
        30: [
            {'lower_limit': 0.01, 'upper_limit': 746.04, 'fixed_fee': 0.00, 'percentage': 0.0192},
            {'lower_limit': 746.05, 'upper_limit': 6332.05, 'fixed_fee': 14.32, 'percentage': 0.0640},
            {'lower_limit': 6332.06, 'upper_limit': 11128.01, 'fixed_fee': 371.83, 'percentage': 0.1088},
            {'lower_limit': 11128.02, 'upper_limit': 12935.82, 'fixed_fee': 893.63, 'percentage': 0.1600},
            {'lower_limit': 12935.83, 'upper_limit': 15487.71, 'fixed_fee': 1182.88, 'percentage': 0.1792},
            {'lower_limit': 15487.72, 'upper_limit': 31236.49, 'fixed_fee': 1640.18, 'percentage': 0.2136},
            {'lower_limit': 31236.50, 'upper_limit': 49233.00, 'fixed_fee': 5004.12, 'percentage': 0.2352},
            {'lower_limit': 49233.01, 'upper_limit': 93993.90, 'fixed_fee': 9236.89, 'percentage': 0.3000},
            {'lower_limit': 93993.91, 'upper_limit': 125325.20, 'fixed_fee': 22665.17, 'percentage': 0.3200},
            {'lower_limit': 125325.21, 'upper_limit': 375975.61, 'fixed_fee': 32691.18, 'percentage': 0.3400},
            {'lower_limit': 375975.62, 'upper_limit': float('inf'), 'fixed_fee': 117912.32, 'percentage': 0.3500}
        ]
    }
    
    if payment_period not in tables:
        raise ValueError(f"Invalid payment period: {payment_period}. Valid periods are: {list(tables.keys())}")
    
    return tables[payment_period]