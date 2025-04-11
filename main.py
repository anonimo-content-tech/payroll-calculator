from src.imss import IMSS
from src.isr import ISR
from src.saving import Saving
from src.totals import TotalCalculator
from tabulate import tabulate
import pandas as pd
from datetime import datetime
import os
from ui.menu import display_menu

def main():
    print("=== IMSS & ISR Simulator ===")
    display_menu()

if __name__ == "__main__":
    main()