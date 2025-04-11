import pandas as pd
import os
from datetime import datetime

def export_to_excel(imss_results, imss_headers, imss_totals, 
                   isr_results, isr_headers, isr_totals,
                   saving_results, saving_headers, saving_totals):
    try:
        # Create traditional and DSI scheme DataFrames
        traditional_headers = [
            'Salario',
            'Productividad',
            'Esquema Tradicional Quincenal',
            'Esquema Tradicional Mensual',
            'Percepción Actual',
        ]
        
        dsi_headers = [
            'Salario',
            'Salario DSI',
            'Comisión DSI',
            'Esquema DSI Quincenal',
            'Esquema DSI Mensual',
            'Percepción DSI',
        ]
        
        comparison_headers = [
            'Salario',
            'Incremento',
            'Porcentaje Incremento'
        ]

        # Extract data for each scheme
        traditional_data = [[row[0], row[2], row[4], row[6], row[10]] for row in saving_results]
        dsi_data = [[row[0], row[1], row[3], row[5], row[7], row[11]] for row in saving_results]
        comparison_data = [[row[0], row[12], row[13]] for row in saving_results]  # Removed division by 100

        # Create timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"payroll_calculations_{timestamp}.xlsx"
        
        # Create results directory if it doesn't exist
        results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resultado_calculos")
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
            
        filepath = os.path.join(results_dir, filename)
        
        # Create a Pandas Excel writer using XlsxWriter as the engine
        writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
        workbook = writer.book

        # Add number formats
        number_format = workbook.add_format({'num_format': '#,##0.00'})
        percentage_format = workbook.add_format({'num_format': '0.00"%"'})  # Changed format to show actual percentage
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })

        # Write IMSS and ISR sheets with number formatting
        df_imss = pd.DataFrame(imss_results, columns=imss_headers)
        df_isr = pd.DataFrame(isr_results, columns=isr_headers)
        
        df_imss.to_excel(writer, sheet_name='IMSS', index=False)
        df_isr.to_excel(writer, sheet_name='ISR', index=False)

        # Create and write savings comparison sheets
        df_traditional = pd.DataFrame(traditional_data, columns=traditional_headers)
        df_dsi = pd.DataFrame(dsi_data, columns=dsi_headers)
        df_comparison = pd.DataFrame(comparison_data, columns=comparison_headers)

        # Write to Ahorro sheet with side-by-side comparison
        worksheet = writer.book.add_worksheet('Ahorro')
        
        # Write Traditional Scheme
        df_traditional.to_excel(writer, sheet_name='Ahorro', startrow=1, startcol=0, index=False)
        worksheet.write(0, 0, 'Esquema Tradicional', header_format)
        
        # Write DSI Scheme
        df_dsi.to_excel(writer, sheet_name='Ahorro', startrow=1, startcol=len(traditional_headers) + 1, index=False)
        worksheet.write(0, len(traditional_headers) + 1, 'Esquema DSI', header_format)
        
        # Write Comparison
        df_comparison.to_excel(writer, sheet_name='Ahorro', 
                             startrow=1, 
                             startcol=len(traditional_headers) + len(dsi_headers) + 2, 
                             index=False)
        worksheet.write(0, len(traditional_headers) + len(dsi_headers) + 2, 'Comparativa', header_format)

        # Apply number formatting to all sheets
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            
            if sheet_name == 'Ahorro':
                # Format numbers in Traditional scheme
                for col in range(len(traditional_headers)):
                    worksheet.set_column(col, col, 15, number_format)
                
                # Format numbers in DSI scheme
                start_col = len(traditional_headers) + 1
                for col in range(start_col, start_col + len(dsi_headers)):
                    worksheet.set_column(col, col, 15, number_format)
                
                # Format comparison section
                start_col = len(traditional_headers) + len(dsi_headers) + 2
                worksheet.set_column(start_col, start_col, 15, number_format)  # Salary
                worksheet.set_column(start_col + 1, start_col + 1, 15, number_format)  # Increment
                worksheet.set_column(start_col + 2, start_col + 2, 15, percentage_format)  # Percentage
            else:
                # Format all numeric columns in IMSS and ISR sheets
                for col in range(worksheet.dim_colmax + 1):
                    worksheet.set_column(col, col, 15, number_format)

        writer.close()
        print(f"\nResults exported successfully to: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error exporting to Excel: {e}")
        print("Results were not exported. Please check if pandas and xlsxwriter are installed.")
        print("You can install them with: pip install pandas xlsxwriter")
        return None

def format_totals_for_excel(totals_dict):
    """
    Format totals dictionary into a format suitable for Excel export
    """
    formatted_totals = []
    
    # Convert the totals dictionary to a list of dictionaries for pandas
    for key, value in totals_dict.items():
        if isinstance(value, (int, float)):
            formatted_totals.append({"Concepto": key, "Total": value})
    
    return formatted_totals