"""
Payroll Calculator Package
A package for calculating IMSS, ISR, and savings for Mexican payroll.
"""

__version__ = '0.1.0'

from .imss import IMSS
from .isr import ISR
from .saving import Saving
from .employees import Employee
from .totals import TotalCalculator
from .processors import process_single_calculation, process_multiple_calculations
from .exporters import export_to_excel, format_totals_for_excel