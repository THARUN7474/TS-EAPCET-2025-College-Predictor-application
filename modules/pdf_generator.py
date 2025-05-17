"""
PDF generation functions for the TS EAMCET College Predictor.
"""

from fpdf import FPDF
import pandas as pd

def dataframe_to_pdf(df):
    """
    Convert DataFrame to PDF.
    
    Args:
        df (pandas.DataFrame): DataFrame to convert
        
    Returns:
        bytes: PDF content as bytes
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Set up the title
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(0, 10, "TS EAMCET College Predictor Results", ln=True, align='C')
    pdf.ln(5)
    
    # Add generation date
    pdf.set_font("Arial", 'I', size=10)
    from datetime import datetime
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)
    
    # Table header
    pdf.set_font("Arial", 'B', size=10)
    
    # Calculate column widths based on data
    num_columns = len(df.columns)
    col_width = pdf.w / (num_columns + 1)  # Adding padding
    col_widths = {}
    
    # Adjust column widths based on content
    for col in df.columns:
        if "College Name" in col or "Branch" in col:
            col_widths[col] = col_width * 1.5
        elif "Closing Rank" in col or "Tuition Fee" in col:
            col_widths[col] = col_width * 0.8
        else:
            col_widths[col] = col_width
    
    # Normalize widths to fit page
    total_width = sum(col_widths.values())
    scale_factor = (pdf.w - 20) / total_width
    for col in col_widths:
        col_widths[col] *= scale_factor
    
    row_height = pdf.font_size * 2

    # Header
    for col in df.columns:
        # Remove or replace non-latin1 characters in header
        safe_col = str(col).encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(col_widths[col], row_height, safe_col, border=1)
    pdf.ln(row_height)

    # Rows
    pdf.set_font("Arial", size=9)
    for i, row in df.iterrows():
        for col, item in zip(df.columns, row):
            # Convert to string and remove/replace non-latin1 characters
            safe_item = str(item).replace("₹", "Rs.").encode(
                'latin-1', 'replace').decode('latin-1')
            pdf.cell(col_widths[col], row_height, safe_item, border=1)
        pdf.ln(row_height)
        
    # Add footer with helpful information
    pdf.ln(10)
    pdf.set_font("Arial", 'I', size=8)
    pdf.multi_cell(0, 5, "Note: This predictor uses TS EAMCET 2024 cutoff ranks. " 
                          "Actual admissions may vary due to special categories, " 
                          "dropouts, or spot admissions.", align='L')
    
    return pdf.output(dest='S').encode('latin-1')

def create_comparison_pdf(phase_comparison):
    """
    Create PDF for phase comparison.
    
    Args:
        phase_comparison (dict): Dictionary with phase as key and dataframe as value
        
    Returns:
        bytes: PDF content as bytes
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Set up the title
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(0, 10, "TS EAMCET Phase Comparison Results", ln=True, align='C')
    pdf.ln(5)
    
    # Add generation date
    pdf.set_font("Arial", 'I', size=10)
    from datetime import datetime
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)
    
    # For each phase
    for phase, data in phase_comparison.items():
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(0, 10, f"{phase} Top Colleges", ln=True)
        
        # Table header
        pdf.set_font("Arial", 'B', size=9)
        
        # Calculate column widths based on data
        num_columns = len(data.columns)
        col_width = pdf.w / (num_columns + 1)  # Adding padding
        row_height = pdf.font_size * 1.5

        # Header
        for col in data.columns:
            # Remove or replace non-latin1 characters in header
            safe_col = str(col).encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(col_width, row_height, safe_col, border=1)
        pdf.ln(row_height)

        # Rows
        pdf.set_font("Arial", size=8)
        for i, row in data.iterrows():
            for item in row:
                # Convert to string and remove/replace non-latin1 characters
                safe_item = str(item).replace("₹", "Rs.").encode(
                    'latin-1', 'replace').decode('latin-1')
                pdf.cell(col_width, row_height, safe_item, border=1)
            pdf.ln(row_height)
        
        pdf.ln(10)
    
    # Add explanation
    pdf.ln(5)
    pdf.set_font("Arial", 'B', size=10)
    pdf.cell(0, 10, "Understanding Phase Comparison:", ln=True)
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(0, 5, "- 1st Phase: Initial cutoffs, typically higher\n"
                          "- 2nd Phase: Often shows reduced cutoffs as seats start getting filled\n"
                          "- Final Phase: Represents the final admission opportunity, usually with lowest cutoffs\n\n"
                          "If you see your preferred college in later phases but not earlier ones, "
                          "it means your chances improve in later rounds of counseling.")
    
    return pdf.output(dest='S').encode('latin-1')