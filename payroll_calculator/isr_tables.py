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


def get_employee_subsidy_table(payment_period):
    """
    Retorna la tabla de subsidio de empleados basada en el periodo de pago
    """
    tables = {
        1: [
            { "lower_limit": 0.01, "upper_limit": 58.19,  "credit": 13.39 },
            { "lower_limit": 58.20, "upper_limit": 87.28,  "credit": 13.38 },
            { "lower_limit": 87.29, "upper_limit": 114.24, "credit": 13.38 },
            { "lower_limit": 114.25,"upper_limit": 116.38, "credit": 12.92 },
            { "lower_limit": 116.39,"upper_limit": 146.25, "credit": 12.58 },
            { "lower_limit": 146.26,"upper_limit": 155.17, "credit": 11.65 },
            { "lower_limit": 155.18,"upper_limit": 175.51, "credit": 10.69 },
            { "lower_limit": 175.52,"upper_limit": 204.76, "credit": 9.69  },
            { "lower_limit": 204.77,"upper_limit": 234.01, "credit": 8.34  },
            { "lower_limit": 234.02,"upper_limit": 242.84, "credit": 7.16  },
            { "lower_limit": 242.85,"upper_limit": float("inf"), "credit": 0.00 }
        ],
        7: [
            { "lower_limit": 0.01,   "upper_limit": 407.33,  "credit": 93.73 },
            { "lower_limit": 407.34, "upper_limit": 610.96,  "credit": 93.66 },
            { "lower_limit": 610.97, "upper_limit": 799.68,  "credit": 93.66 },
            { "lower_limit": 799.69, "upper_limit": 814.66,  "credit": 90.44 },
            { "lower_limit": 814.67, "upper_limit": 1023.75, "credit": 88.06 },
            { "lower_limit": 1023.76,"upper_limit": 1086.19, "credit": 81.55 },
            { "lower_limit": 1086.20,"upper_limit": 1228.57, "credit": 74.83 },
            { "lower_limit": 1228.58,"upper_limit": 1433.32, "credit": 67.83 },
            { "lower_limit": 1433.33,"upper_limit": 1638.07, "credit": 58.38 },
            { "lower_limit": 1638.08,"upper_limit": 1699.88, "credit": 50.12 },
            { "lower_limit": 1699.89,"upper_limit": float("inf"), "credit": 0.00 }
        ],
        10: [
            { "lower_limit": 0.01,   "upper_limit": 581.90,  "credit": 133.90 },
            { "lower_limit": 581.91, "upper_limit": 872.80,  "credit": 133.80 },
            { "lower_limit": 872.81, "upper_limit": 1142.40, "credit": 133.80 },
            { "lower_limit": 1142.41,"upper_limit": 1163.80, "credit": 129.20 },
            { "lower_limit": 1163.81,"upper_limit": 1462.50, "credit": 125.80 },
            { "lower_limit": 1462.51,"upper_limit": 1551.70, "credit": 116.50 },
            { "lower_limit": 1551.71,"upper_limit": 1755.10, "credit": 106.90 },
            { "lower_limit": 1755.11,"upper_limit": 2047.60, "credit": 96.90  },
            { "lower_limit": 2047.61,"upper_limit": 2340.10, "credit": 83.40  },
            { "lower_limit": 2340.11,"upper_limit": 2428.40, "credit": 71.60  },
            { "lower_limit": 2428.41,"upper_limit": float("inf"), "credit": 0.00 }
        ],
        15: [
            { "lower_limit": 0.01,   "upper_limit": 872.85,  "credit": 200.85 },
            { "lower_limit": 872.86, "upper_limit": 1309.20, "credit": 200.70 },
            { "lower_limit": 1309.21,"upper_limit": 1713.60, "credit": 200.70 },
            { "lower_limit": 1713.61,"upper_limit": 1745.70, "credit": 193.80 },
            { "lower_limit": 1745.71,"upper_limit": 2193.75, "credit": 188.70 },
            { "lower_limit": 2193.76,"upper_limit": 2327.55, "credit": 174.75 },
            { "lower_limit": 2327.56,"upper_limit": 2632.65, "credit": 160.35 },
            { "lower_limit": 2632.66,"upper_limit": 3071.40, "credit": 145.35 },
            { "lower_limit": 3071.41,"upper_limit": 3510.15, "credit": 125.10 },
            { "lower_limit": 3510.16,"upper_limit": 3642.60, "credit": 107.40 },
            { "lower_limit": 3642.61,"upper_limit": float("inf"), "credit": 0.00 }
        ],
        30: [
            { "lower_limit": 0.01,   "upper_limit": 1768.96, "credit": 407.02 },
            { "lower_limit": 1768.97,"upper_limit": 2653.38, "credit": 406.83 },
            { "lower_limit": 2653.39,"upper_limit": 3472.84, "credit": 406.62 },
            { "lower_limit": 3472.85,"upper_limit": 3537.87, "credit": 392.77 },
            { "lower_limit": 3537.88,"upper_limit": 4446.15, "credit": 382.46 },
            { "lower_limit": 4446.16,"upper_limit": 4717.18, "credit": 354.23 },
            { "lower_limit": 4717.19,"upper_limit": 5335.42, "credit": 324.87 },
            { "lower_limit": 5335.43,"upper_limit": 6224.67, "credit": 294.63 },
            { "lower_limit": 6224.68,"upper_limit": 7113.90, "credit": 253.54 },
            { "lower_limit": 7113.91,"upper_limit": 7382.33, "credit": 217.61 },
            { "lower_limit": 7382.34,"upper_limit": float("inf"), "credit": 0.00 }
        ]
    }
    
    if payment_period not in tables:
        raise ValueError(f"Invalid payment period: {payment_period}. Valid periods are: {list(tables.keys())}")
    
    return tables[payment_period]