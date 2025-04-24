import pandas as pd
import os
from datetime import datetime
from typing import List, Dict, Any # Added typing

# Updated function signature to accept formatted total tables
def export_to_excel(imss_results: List[List[Any]], imss_headers: List[str], imss_totals_table: List[List[Any]],
                   isr_results: List[List[Any]], isr_headers: List[str], isr_totals_table: List[List[Any]],
                   saving_results: List[List[Any]], saving_headers: List[str], saving_totals_table: List[List[Any]]):
    try:
        # Create DataFrames for IMSS, ISR, and Savings details
        df_imss = pd.DataFrame(imss_results, columns=imss_headers)
        df_isr = pd.DataFrame(isr_results, columns=isr_headers)

        # --- Prepare Savings DataFrames ---
        # Headers based on saving_results structure from process_multiple_calculations
        # Indices: 0:Salario, 1:SalarioDSI, 2:Productividad, 3:ComisionDSI, 4:TradQ, 5:DSIQ, 6:TradM, 7:DSIM,
        #          8:AhorroMonto, 9:Ahorro%, 10:PercepActualTrad, 11:PercepActualDSI, 12:IncremMonto, 13:Increm%

        traditional_headers = [
            'Salario Base', # 0
            'Productividad', # 2
            'Esquema Tradicional Quincenal', # 4
            'Esquema Tradicional Mensual', # 6
            'Percepción Actual Tradicional', # 10
        ]
        dsi_headers = [
            'Salario Base', # 0
            'Salario DSI', # 1
            'Comisión DSI', # 3
            'Esquema DSI Quincenal', # 5
            'Esquema DSI Mensual', # 7
            'Percepción Actual DSI', # 11
        ]
        comparison_headers = [
            'Salario Base', # 0
            'Ahorro Monto', # 8
            'Ahorro %', # 9
            'Incremento Monto', # 12
            'Incremento %' # 13
        ]

        # Extract data for each scheme using correct indices
        traditional_data = [[row[0], row[2], row[4], row[6], row[10]] for row in saving_results]
        dsi_data = [[row[0], row[1], row[3], row[5], row[7], row[11]] for row in saving_results]
        # Ensure percentages are handled correctly (they are already multiplied by 100 in saving_results)
        comparison_data = [[row[0], row[8], row[9], row[12], row[13]] for row in saving_results]

        df_traditional = pd.DataFrame(traditional_data, columns=traditional_headers)
        df_dsi = pd.DataFrame(dsi_data, columns=dsi_headers)
        df_comparison = pd.DataFrame(comparison_data, columns=comparison_headers)
        # --- End Prepare Savings DataFrames ---


        # Create timestamp and filepath
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"payroll_calculations_{timestamp}.xlsx"
        results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resultado_calculos")
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        filepath = os.path.join(results_dir, filename)

        # Create Excel writer
        writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
        workbook = writer.book

        # Add formats
        number_format = workbook.add_format({'num_format': '#,##0.00'})
        percentage_format = workbook.add_format({'num_format': '0.00"%"'})
        header_format = workbook.add_format({
            'bold': True, 'text_wrap': True, 'valign': 'top',
            'fg_color': '#D7E4BC', 'border': 1, 'align': 'center'
        })
        totals_header_format = workbook.add_format({
            'bold': True, 'fg_color': '#E2EFDA', 'border': 1, 'align': 'center'
        })
        totals_section_header_format = workbook.add_format({
            'bold': True, 'font_size': 12, 'fg_color': '#C6E0B4', 'border': 1, 'align': 'center'
        })


        # --- Write Detail Sheets (IMSS, ISR, Ahorro) ---
        df_imss.to_excel(writer, sheet_name='IMSS', index=False, startrow=1)
        df_isr.to_excel(writer, sheet_name='ISR', index=False, startrow=1)

        # Write Ahorro sheet with side-by-side comparison
        ahorro_sheet = workbook.add_worksheet('Ahorro')
        writer.sheets['Ahorro'] = ahorro_sheet # Assign the worksheet to the writer

        # Write headers with merged cells for sections
        ahorro_sheet.merge_range(0, 0, 0, len(traditional_headers)-1, 'Esquema Tradicional', header_format)
        df_traditional.to_excel(writer, sheet_name='Ahorro', startrow=2, startcol=0, index=False, header=False) # Write data only
        for col_num, value in enumerate(traditional_headers): # Write headers manually
             ahorro_sheet.write(1, col_num, value, header_format)

        dsi_start_col = len(traditional_headers) + 1
        ahorro_sheet.merge_range(0, dsi_start_col, 0, dsi_start_col + len(dsi_headers)-1, 'Esquema DSI', header_format)
        df_dsi.to_excel(writer, sheet_name='Ahorro', startrow=2, startcol=dsi_start_col, index=False, header=False)
        for col_num, value in enumerate(dsi_headers):
             ahorro_sheet.write(1, dsi_start_col + col_num, value, header_format)

        comp_start_col = dsi_start_col + len(dsi_headers) + 1
        ahorro_sheet.merge_range(0, comp_start_col, 0, comp_start_col + len(comparison_headers)-1, 'Comparativa Ahorro/Incremento', header_format)
        df_comparison.to_excel(writer, sheet_name='Ahorro', startrow=2, startcol=comp_start_col, index=False, header=False)
        for col_num, value in enumerate(comparison_headers):
             ahorro_sheet.write(1, comp_start_col + col_num, value, header_format)


        # --- Write Totales Sheet ---
        totals_sheet = workbook.add_worksheet('Totales')
        writer.sheets['Totales'] = totals_sheet # Assign the worksheet to the writer

        totals_headers = ["Concepto", "Total", "Columna Ref."]
        current_row = 0

        # Write IMSS Totals
        totals_sheet.merge_range(current_row, 0, current_row, len(totals_headers)-1, 'Totales IMSS (Esquema Tradicional)', totals_section_header_format)
        current_row += 1
        for col_num, header in enumerate(totals_headers):
            totals_sheet.write(current_row, col_num, header, totals_header_format)
        current_row += 1
        for row_data in imss_totals_table:
            totals_sheet.write_row(current_row, 0, row_data)
            current_row += 1
        current_row += 1 # Add blank row

        # Write ISR Totals
        totals_sheet.merge_range(current_row, 0, current_row, len(totals_headers)-1, 'Totales ISR', totals_section_header_format)
        current_row += 1
        for col_num, header in enumerate(totals_headers):
            totals_sheet.write(current_row, col_num, header, totals_header_format)
        current_row += 1
        for row_data in isr_totals_table:
            totals_sheet.write_row(current_row, 0, row_data)
            current_row += 1
        current_row += 1 # Add blank row

        # Write Saving Totals
        totals_sheet.merge_range(current_row, 0, current_row, len(totals_headers)-1, 'Totales Ahorro/Incremento (Comparativa Esquemas)', totals_section_header_format)
        current_row += 1
        for col_num, header in enumerate(totals_headers):
            totals_sheet.write(current_row, col_num, header, totals_header_format)
        current_row += 1
        for row_data in saving_totals_table:
            # Check if value is percentage string before writing
            if isinstance(row_data[1], str) and '%' in row_data[1]:
                 # Extract number and apply percentage format
                 try:
                     num_val = float(row_data[1].replace('%',''))
                     totals_sheet.write_number(current_row, 1, num_val / 100, percentage_format) # Divide by 100 for Excel % format
                 except ValueError:
                     totals_sheet.write(current_row, 1, row_data[1]) # Write as string if conversion fails
            else:
                 totals_sheet.write(current_row, 1, row_data[1], number_format) # Apply number format

            totals_sheet.write(current_row, 0, row_data[0]) # Concept
            totals_sheet.write(current_row, 2, row_data[2]) # Column Ref
            current_row += 1

        # Set column widths for Totales sheet
        totals_sheet.set_column('A:A', 30) # Concepto
        totals_sheet.set_column('B:B', 18, number_format) # Total (default format)
        totals_sheet.set_column('C:C', 15) # Columna Ref.


        # --- Apply Formatting and Finalize ---
        # Apply formatting to detail sheets
        for sheet_name in ['IMSS', 'ISR']:
            worksheet = writer.sheets[sheet_name]
            # Write main header
            worksheet.merge_range(0, 0, 0, df_imss.shape[1]-1 if sheet_name == 'IMSS' else df_isr.shape[1]-1, f'Detalle {sheet_name}', header_format)
            # Write column headers
            for col_num, value in enumerate(df_imss.columns if sheet_name == 'IMSS' else df_isr.columns):
                 worksheet.write(1, col_num, value, header_format)
            # Apply number format to data rows
            for col in range(worksheet.dim_colmax + 1):
                worksheet.set_column(col, col, 15, number_format)

        # Apply formatting to Ahorro sheet
        ahorro_sheet = writer.sheets['Ahorro']
        # Traditional
        for col in range(len(traditional_headers)):
            ahorro_sheet.set_column(col, col, 18, number_format)
        # DSI
        start_col = len(traditional_headers) + 1
        for col in range(len(dsi_headers)):
            ahorro_sheet.set_column(start_col + col, start_col + col, 18, number_format)
        # Comparison
        start_col = len(traditional_headers) + len(dsi_headers) + 2
        ahorro_sheet.set_column(start_col, start_col, 18, number_format) # Salario Base
        ahorro_sheet.set_column(start_col + 1, start_col + 1, 18, number_format) # Ahorro Monto
        ahorro_sheet.set_column(start_col + 2, start_col + 2, 15, percentage_format) # Ahorro %
        ahorro_sheet.set_column(start_col + 3, start_col + 3, 18, number_format) # Incremento Monto
        ahorro_sheet.set_column(start_col + 4, start_col + 4, 15, percentage_format) # Incremento %


        # Close the Pandas Excel writer and output the Excel file.
        writer.close()
        print(f"\nResults exported successfully to: {filepath}")
        return filepath

    except Exception as e:
        print(f"Error exporting to Excel: {e}")
        # Consider more specific error handling or logging if needed
        print("Results were not exported. Please check file permissions and dependencies (pandas, xlsxwriter).")
        print("You can install them with: pip install pandas XlsxWriter") # Corrected package name
        return None

# Removed the format_totals_for_excel function as it's no longer needed
# with the new approach using format_totals_table from TotalCalculator