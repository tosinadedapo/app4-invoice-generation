import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path

filepaths = glob.glob("invoices/*xlsx*")
print(filepaths)

for filepath in filepaths:

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    # Get the filename without the extension
    filename = Path(filepath).stem
    invoice_nr, date = filename.split("-")

    pdf.set_font("Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1)

    pdf.set_font("Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)

    df = pd.read_excel(filepath, sheet_name="Sheet 1")

    # Add the headers
    columns = df.columns

    # Replace _ of the headers with space and Initial capitalize
    # the headers
    columns = [item.replace("_", " ").title() for item in columns]

    pdf.set_font("Times", size=10, style="B")
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=30, h=8, txt=columns[0], border=1)
    pdf.cell(w=70, h=8, txt=columns[1], border=1)
    pdf.cell(w=30, h=8, txt=columns[2], border=1)
    pdf.cell(w=30, h=8, txt=columns[3], border=1)
    pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

    # Add rows to to the table
    for index, row in df.iterrows():
        pdf.set_font("Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=str(row["product_id"]), border=1)
        pdf.cell(w=70, h=8, txt=str(row["product_name"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["amount_purchased"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["total_price"]), border=1, ln=1)

    # Sum the total of the total_price column
    total_sum = df["total_price"].sum()

    # Add the total sum to the table putting empty txt in the other columns
    pdf.set_font("Times", size=10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=70, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

    # Add A text of the total sum below the table
    pdf.set_font("Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Total Invoice Amount: {total_sum}", ln=1)

    # Add Company name and logo
    pdf.set_font("Times", size=16, style="B")
    pdf.cell(w=30, h=8, txt=f"PythonHow")
    pdf.image("pythonhow.png", w=10)

    # produce the pdf file
    pdf.output(f"PDFs/{filename}.pdf")

