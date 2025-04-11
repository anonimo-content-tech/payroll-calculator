import pandas as pd
import os
from datetime import datetime

def export_to_excel(imss_results, imss_headers, imss_totals, 
                   isr_results, isr_headers, isr_totals,
                   saving_results, saving_headers, saving_totals):
    """
    Export calculation results to an Excel file with separate sheets
    """
    try:
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
        
        # Convert results to DataFrames
        df_imss = pd.DataFrame(imss_results, columns=imss_headers)
        df_isr = pd.DataFrame(isr_results, columns=isr_headers)
        df_saving = pd.DataFrame(saving_results, columns=saving_headers)
        
        # Format totals for Excel
        imss_totals_formatted = format_totals_for_excel(imss_totals)
        isr_totals_formatted = format_totals_for_excel(isr_totals)
        saving_totals_formatted = format_totals_for_excel(saving_totals)
        
        # Write each DataFrame to a different worksheet
        df_imss.to_excel(writer, sheet_name='IMSS', index=False)
        pd.DataFrame(imss_totals_formatted).to_excel(writer, sheet_name='IMSS', startrow=len(df_imss) + 2, index=False)
        
        df_isr.to_excel(writer, sheet_name='ISR', index=False)
        pd.DataFrame(isr_totals_formatted).to_excel(writer, sheet_name='ISR', startrow=len(df_isr) + 2, index=False)
        
        df_saving.to_excel(writer, sheet_name='Ahorro', index=False)
        pd.DataFrame(saving_totals_formatted).to_excel(writer, sheet_name='Ahorro', startrow=len(df_saving) + 2, index=False)
        
        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        
        # Add formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        # Apply formatting to each worksheet
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            # Set column width for all columns
            for col_num in range(len(df_imss.columns) if sheet_name == 'IMSS' else 
                               (len(df_isr.columns) if sheet_name == 'ISR' else 
                                len(df_saving.columns))):
                worksheet.set_column(col_num, col_num, 15)
                
            # Apply header format to the first row
            for col_num in range(len(df_imss.columns) if sheet_name == 'IMSS' else 
                               (len(df_isr.columns) if sheet_name == 'ISR' else 
                                len(df_saving.columns))):
                worksheet.write(0, col_num, 
                              df_imss.columns[col_num] if sheet_name == 'IMSS' else 
                              (df_isr.columns[col_num] if sheet_name == 'ISR' else 
                               df_saving.columns[col_num]), 
                              header_format)
                
        # Close the Pandas Excel writer and output the Excel file
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