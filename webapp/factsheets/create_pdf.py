import os
import random
import pandas as pd
from fpdf import FPDF
from functools import reduce

STATIC_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../static'

def generate_random_return():
    ret = random.random() * random.choice([-1, 1]) * 10
    return '%0.2f' % ret

def geometric_mean(returns):
    returns = [float(ret) for ret in returns]
    return reduce((lambda x, y: x * y), returns)

class FactsheetPDF(FPDF):
    """
    Renders a PDF file.  Set state with self.set_state
    """
    def set_state(self, props):
        # save props to object
        self.props = props
        print(self.props)

        # store here for now
        self.path = STATIC_PATH + '/fact_sheet.pdf'
        self.header_background_img_path = STATIC_PATH + '/img/background.png'
        self.logo_img_path = STATIC_PATH + '/img/logo.png'
        
        # add fonts
        self.add_font(
            family='gebody',
            style='',
            fname=STATIC_PATH + '/fonts/GeBody-x0zj.ttf',
            uni=True)
        
        # define section sizes
        self.page_width = 210
        self.page_height = 297
        self.border = 4
        
        self.header_height = 30
        self.logo_width=20
        self.logo_height=20

    def print_state(self):
        print('----')
        print('Printing PDF state.')
        print('\tFund Name: %s' % self.props['fund_name'])
        print('\tFund Overview: %s' % self.props['fund_overview'])
        print('----')

    def header(self):
        pass

    def footer(self):
        pass

    def render_header_background(self):
        x = self.border
        y = self.border
        width = self.page_width - (self.border*2)
        height = self.header_height - (self.border)
        self.image(
            self.header_background_img_path,
            x=self.border,
            y=self.border,
            w=width,
            h=height,
            type='PNG')
        
    def render_logo(self):
        self.image(
            self.logo_img_path,
            x=self.border + 2,
            y=self.border+2,
            w=self.logo_width,
            h=self.logo_height,
            type='PNG')

    def render_fund_name(self):
        self.set_font(family='gebody', style='', size=15)
        self.set_text_color(231, 237, 238)
        self.set_xy(self.border + self.logo_width + 5, 0)
        self.cell(
            w=self.page_width-50,
            h=30,
            txt=self.props['fund_name'],
            border=0,
            ln=2,
            align='L')
        
    def render_fund_overview(self):
        self.set_xy(self.border, self.header_height)
        self.set_text_color(0,0,0)
        self.set_fill_color(223,223,223)
        self.set_font('Arial', '', 8)
        self.multi_cell(
            w=self.page_width - (2*self.border),
            h=5,
            txt=self.props['fund_overview'],
            border=0,
            fill=True)
        
    def render_table(self):
        cell_height = 5
        cell_width = 8
        self.set_x(self.border
                )
        # header
        self.set_font(
            family='Arial',
            style='B',
            size=12)
        self.set_text_color(0,0,0)
        self.cell(
            w=0,
            h=10,
            txt='Monthly Returns Net Of Fees',
            border=0,
            ln=2)

        # table
        x0 = self.get_x()
        self.set_fill_color(223,223,223)
        self.set_font(family='Arial', style='', size=6)

        df = pd.DataFrame(self.props['returns'])
        df['return'] = df['return'].apply(lambda x: '%0.2f' % (float(x)*1000))
        year_min = df['year'].min()
        year_max = df['year'].max()
        month_min = df[df['year'] == year_min]['month'].min()
        month_max = df[df['year'] == year_max]['month'].max()
        for month in range(1, month_min):
            df = df.append({
                'year': year_min,
                'month': month,
                'return': ''
                }, ignore_index=True)

        for month in range(month_max + 1, 13):
            df = df.append({
                'year': year_max,
                'month': month,
                'return': ''
                }, ignore_index=True)
        df = df.pivot(index='year', columns='month', values='return')
        df['Year'] = df.apply(lambda row: \
            geometric_mean([float(x) for x in [y for y in row.values if y != '']]), axis=1)
        print(df)

        # for year, months in df.iterrows():
        #     for month_ret in months.iteritems():
        #         print(year, month_ret)



        for month in ['', 'Jan', 'Feb', 'Mar', 'Apr',
                      'May', 'Jun', 'Jul', 'Aug',
                      'Sep', 'Oct', 'Nov', 'Dec', 'Year']:
            self.cell(cell_width,cell_height,month,'B',0,'C')
        self.set_x(x0)
        self.set_y(self.get_y() + cell_height)


        fill = True
        for year, months in df.iterrows():
            self.set_x(x0)
            self.cell(cell_width,cell_height,str(year),0,0,'C',fill)
            for month_ret in months.iteritems():
                month = str(month_ret[0])
                ret = str(month_ret[1])
                self.cell(cell_width,cell_height,ret,0,0,'C',fill)
            self.set_y(self.get_y() + cell_height)

            if fill:
                fill = False
            else:
                fill = True

        # fill = True
        # for year in [str(e) for e in range(2003,2009)]:
        #     self.set_x(x0)
        #     self.cell(cell_width,cell_height,year,0,0,'C',fill)
        #     for i in range(13):
        #         self.cell(cell_width,cell_height,generate_random_return(),0,0,'C',fill)
        #     self.set_y(self.get_y() + cell_height)
            
        #     if fill:
        #         fill = False
        #     else:
        #         fill = True
        
    def build(self):
        self.alias_nb_pages()
        self.add_page()
        
        # header
        self.render_header_background()
        self.render_logo()
        self.render_fund_name()
        
        # fund overview
        self.render_fund_overview()
        
        # Monthly Returns
        self.render_table()
        
        # save pdf to fs
        self.output(self.path, 'F')

def generate_fact_sheet(fund_name, fund_overview):
    pdf = FactsheetPDF()
    pdf.set_state(
        props={
            'fund_name': fund_name,
            'fund_overview': fund_overview,
        })
    pdf.build()
