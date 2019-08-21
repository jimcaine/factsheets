import os
from fpdf import FPDF
import base64

class PDF(FPDF):
    """
    Renders a PDF file.  Set state with self.set_state
    """
    def set_state(self, fund_name=None, fund_overview=None):
        self.fund_name = fund_name
        self.fund_overview = fund_overview

    def print_state(self):
        print(self.fund_name)
        print(self.fund_overview)
    def header(self):
        # Logo
        # self.image(self.logo, 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, self.fund_name, 1, 0, 'C')
        # Line break
        self.ln(20)
    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def generate_fact_sheet(fund_name, fund_overview):
    print('from create_pdf')
    print(fund_name)
    print(fund_overview)
    pdf = PDF()
    pdf.set_state(
        fund_name=fund_name,
        fund_overview=fund_overview)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 10, fund_overview, 0, 1)

    # save to pdf
    path = os.path.dirname(os.path.realpath(__file__)) + '/../static/fact_sheet.pdf'
    pdf.output(path, 'F')