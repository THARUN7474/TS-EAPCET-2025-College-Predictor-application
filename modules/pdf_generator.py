"""
PDF generation functions for the TS EAMCET College Predictor.
Fixed version with proper column spacing and no overlapping.
"""

from fpdf import FPDF
import pandas as pd


def dataframe_to_pdf(df):
    """
    Convert DataFrame to PDF with proper column spacing.

    Args:
        df (pandas.DataFrame): DataFrame to convert

    Returns:
        bytes: PDF content as bytes
    """
    pdf = FPDF(orientation='L', unit='mm',
               format='A4')  # Landscape for wide tables
    pdf.add_page()

    # Set up the title
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(0, 10, "TS EAMCET College Predictor Results", ln=True, align='C')
    pdf.ln(5)

    # Add generation date
    pdf.set_font("Arial", 'I', size=10)
    from datetime import datetime
    pdf.cell(
        0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)

    # Prepare data - truncate long content to prevent overflow
    df_display = df.copy()

    # Truncate long column names
    new_columns = []
    for col in df_display.columns:
        if len(str(col)) > 20:
            new_columns.append(str(col)[:17] + "...")
        else:
            new_columns.append(str(col))
    df_display.columns = new_columns

    # Truncate long cell content
    for col in df_display.columns:
        df_display[col] = df_display[col].astype(str).apply(
            lambda x: x[:25] + "..." if len(x) > 25 else x
        )

    # Calculate optimal column widths
    page_width = pdf.w - 20  # Page width minus margins
    num_columns = len(df_display.columns)

    # Smart column width allocation
    col_widths = {}
    total_allocated = 0

    for col in df_display.columns:
        if any(keyword in col.lower() for keyword in ['college', 'name', 'branch']):
            # Wider columns for important text fields
            col_widths[col] = min(60, page_width * 0.3)
        elif any(keyword in col.lower() for keyword in ['rank', 'fee']):
            # Medium width for numbers
            col_widths[col] = min(40, page_width * 0.15)
        else:
            # Standard width for other columns
            col_widths[col] = min(35, page_width * 0.12)

        total_allocated += col_widths[col]

    # Scale down if total width exceeds page width
    if total_allocated > page_width:
        scale_factor = page_width / total_allocated
        for col in col_widths:
            col_widths[col] *= scale_factor

    # Ensure minimum column width
    min_width = 25
    for col in col_widths:
        if col_widths[col] < min_width:
            col_widths[col] = min_width

    row_height = 8  # Reduced row height for better fitting

    # Table header
    pdf.set_font("Arial", 'B', size=9)
    pdf.set_fill_color(200, 220, 255)  # Light blue background for header

    for col in df_display.columns:
        safe_col = str(col).encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(col_widths[col], row_height, safe_col,
                 border=1, fill=True, align='C')
    pdf.ln(row_height)

    # Table rows with alternating colors
    pdf.set_font("Arial", size=8)
    pdf.set_fill_color(245, 245, 245)  # Light gray for alternate rows

    for i, (index, row) in enumerate(df_display.iterrows()):
        # Alternate row colors
        fill = i % 2 == 0

        for col in df_display.columns:
            item = row[col]
            # Handle special characters and convert to safe string
            safe_item = str(item).replace("₹", "Rs.").replace("—", "-")
            safe_item = safe_item.encode(
                'latin-1', 'replace').decode('latin-1')

            pdf.cell(col_widths[col], row_height, safe_item,
                     border=1, fill=fill, align='C')

        pdf.ln(row_height)

        # Add new page if needed (leave space for footer)
        if pdf.get_y() > pdf.h - 30:
            pdf.add_page()

            # Re-add header on new page
            pdf.set_font("Arial", 'B', size=9)
            pdf.set_fill_color(200, 220, 255)
            for col in df_display.columns:
                safe_col = str(col).encode(
                    'latin-1', 'replace').decode('latin-1')
                pdf.cell(col_widths[col], row_height,
                         safe_col, border=1, fill=True, align='C')
            pdf.ln(row_height)
            pdf.set_font("Arial", size=8)
            pdf.set_fill_color(245, 245, 245)

    # Add footer with helpful information
    pdf.ln(10)
    pdf.set_font("Arial", 'I', size=8)
    pdf.multi_cell(0, 5, "Note: This predictor uses TS EAMCET 2024 cutoff ranks. "
                   "Actual admissions may vary due to special categories, "
                   "dropouts, or spot admissions. Long text has been truncated for display.",
                   align='L')

    return pdf.output(dest='S').encode('latin-1')


def create_comparison_pdf(phase_comparison):
    """
    Create PDF for phase comparison with proper formatting.

    Args:
        phase_comparison (dict): Dictionary with phase as key and dataframe as value

    Returns:
        bytes: PDF content as bytes
    """
    pdf = FPDF(orientation='L', unit='mm',
               format='A4')  # Landscape orientation
    pdf.add_page()

    # Set up the title
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(0, 10, "TS EAMCET Phase Comparison Results", ln=True, align='C')
    pdf.ln(5)

    # Add generation date
    pdf.set_font("Arial", 'I', size=10)
    from datetime import datetime
    pdf.cell(
        0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)

    # Process each phase
    for phase_idx, (phase, data) in enumerate(phase_comparison.items()):
        # Add new page for each phase except the first one
        if phase_idx > 0:
            pdf.add_page()

        pdf.set_font("Arial", 'B', size=12)
        pdf.set_fill_color(100, 150, 200)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, f"{phase} Top Colleges", ln=True, fill=True, align='C')
        pdf.set_text_color(0, 0, 0)  # Reset to black
        pdf.ln(5)

        # Prepare data for this phase
        data_display = data.copy()

        # Truncate long content
        new_columns = []
        for col in data_display.columns:
            if len(str(col)) > 18:
                new_columns.append(str(col)[:15] + "...")
            else:
                new_columns.append(str(col))
        data_display.columns = new_columns

        # Truncate cell content
        for col in data_display.columns:
            data_display[col] = data_display[col].astype(str).apply(
                lambda x: x[:22] + "..." if len(x) > 22 else x
            )

        # Calculate column widths
        page_width = pdf.w - 20
        num_columns = len(data_display.columns)

        col_widths = {}
        for col in data_display.columns:
            if any(keyword in col.lower() for keyword in ['college', 'name', 'branch']):
                col_widths[col] = min(55, page_width * 0.25)
            elif any(keyword in col.lower() for keyword in ['rank', 'fee']):
                col_widths[col] = min(35, page_width * 0.15)
            else:
                col_widths[col] = min(30, page_width * 0.12)

        # Scale to fit page
        total_width = sum(col_widths.values())
        if total_width > page_width:
            scale_factor = page_width / total_width
            for col in col_widths:
                col_widths[col] *= scale_factor

        row_height = 7

        # Table header
        pdf.set_font("Arial", 'B', size=8)
        pdf.set_fill_color(220, 220, 220)

        for col in data_display.columns:
            safe_col = str(col).encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(col_widths[col], row_height, safe_col,
                     border=1, fill=True, align='C')
        pdf.ln(row_height)

        # Table rows
        pdf.set_font("Arial", size=7)
        pdf.set_fill_color(248, 248, 248)

        for i, (index, row) in enumerate(data_display.iterrows()):
            fill = i % 2 == 0

            for col in data_display.columns:
                item = row[col]
                safe_item = str(item).replace("₹", "Rs.").replace("—", "-")
                safe_item = safe_item.encode(
                    'latin-1', 'replace').decode('latin-1')

                pdf.cell(col_widths[col], row_height,
                         safe_item, border=1, fill=fill, align='C')

            pdf.ln(row_height)

            # Check if we need a new page
            if pdf.get_y() > pdf.h - 40:
                break  # Move to next phase instead of continuing on new page

        pdf.ln(5)

    # Add explanation on the last page or new page
    if pdf.get_y() > pdf.h - 60:
        pdf.add_page()

    pdf.ln(5)
    pdf.set_font("Arial", 'B', size=10)
    pdf.set_fill_color(255, 255, 200)  # Light yellow background
    pdf.cell(0, 8, "Understanding Phase Comparison:", ln=True, fill=True)
    pdf.ln(2)

    pdf.set_font("Arial", size=9)
    explanation_text = """• 1st Phase: Initial cutoffs, typically higher ranks required
• 2nd Phase: Often shows reduced cutoffs as seats start getting filled  
• Final Phase: Last admission opportunity, usually with lowest cutoffs

Strategy: If you see your preferred college in later phases but not earlier ones, 
your chances improve in subsequent rounds of counseling. Plan accordingly!

Note: Data truncated for optimal display. Refer to official websites for complete information."""

    pdf.multi_cell(0, 5, explanation_text, align='L')

    return pdf.output(dest='S').encode('latin-1')
