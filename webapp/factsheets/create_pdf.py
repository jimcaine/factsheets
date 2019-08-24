import os
import random
import numpy as np
import pandas as pd
from fpdf import FPDF
from functools import reduce

STATIC_PATH = os.getcwd() + '/webapp/static'
print(STATIC_PATH)



def generate_random_return():
    ret = random.random() * random.choice([-1, 1]) * 10
    return '%0.2f' % ret

def geometric_return(returns):
    returns = [(ret / 100.) + 1 for ret in returns]
    geo_return = np.prod(returns)**(1.0 / len(returns))
    geo_return = (geo_return - 1) * 100
    geo_return = '%0.2f' % geo_return
    return geo_return


class PDFComponent:
    def __init__(self, x, y, width, height, margin=0, padding=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.margin = margin
        self.padding = padding

class TextComponent(PDFComponent):
    def __init__(self, txt,
                 fill=False, fill_color=(256,256,256),
                 font_family='Arial', style='', size=12, font_color=(0,0,0),
                 **kwargs):
        super(TextComponent, self).__init__(**kwargs)
        self.txt= txt
        self.fill = fill
        self.fill_color = fill_color
        self.font_family = font_family
        self.style = style
        self.size = size
        self.font_color = font_color

    def render(self, pdf):
        # set position
        pdf.set_xy(self.x, self.y)

        # set font
        pdf.set_font(
            family=self.font_family,
            style=self.style,
            size=self.size)
        pdf.set_text_color(*self.font_color)

        # draw cell
        pdf.cell(
            w=self.width,
            h=self.height,
            txt=self.txt,
            align='L')
        return pdf

class ImageComponent(PDFComponent):
    def __init__(self, img_path, img_type='PNG', **kwargs):
        super(ImageComponent, self).__init__(**kwargs)
        self.img_path = img_path
        self.img_type = img_type

    def render(self, pdf):
        # set position
        pdf.set_xy(self.x, self.y)

        # draw image
        pdf.image(
            self.img_path,
            x=self.x,
            y=self.y,
            w=self.width,
            h=self.height,
            type=self.img_type)
        return pdf


class TableComponent(PDFComponent):
    def __init__(self, df, striped=False, **kwargs):
        super(TableComponent, self).__init__(**kwargs)
        self.df = df
        self.striped = striped

        # calculate cell height and cell width
        nrows, ncols = df.shape
        self.cell_height = self.height / float(nrows)
        self.cell_width = self.width / float(ncols)

        # set fill color(s)
        self.fill_color = (223,223,223)
        


    def render(self, pdf):
        # set position
        pdf.set_xy(self.x, self.y)
        x0 = self.x

        # set font
        pdf.set_font(family='Arial', style='', size=6)

        # set fill color
        pdf.set_fill_color(*self.fill_color)

        # write header
        pdf.cell(self.cell_width, self.cell_height, '', 0, 0, 'C')
        for col in self.df.columns:
            pdf.cell(self.cell_width, self.cell_height, str(col), 0, 0, 'C')

        # shift cursor
        pdf.set_x(x0)
        pdf.set_y(pdf.get_y() + self.cell_height)

        # write data
        fill = False
        for index, row in self.df.iterrows():
            print('fill=%s' % fill)
            # write index as first col
            pdf.cell(self.cell_width, self.cell_height, str(index), 0, 0, 'C', fill)

            # write the remaining cols
            for col in row.values:
                pdf.cell(self.cell_width, self.cell_height, str(col), 0, 0, 'C', fill)

            # shift cursor
            pdf.set_x(x0)
            pdf.set_y(pdf.get_y() + self.cell_height)

            if self.striped:
                if not fill:
                    fill = True
                else:
                    fill = False

        # return pdf back
        return pdf


def generate_fact_sheet(fund_name, fund_overview):
    components = [
        # header background
        ImageComponent(
            '/Users/jimcaine/projects/factsheets/webapp/static/img/background.png',
            x=0, y=0, width=210, height=30),
        
        # header logo
        ImageComponent(
            '/Users/jimcaine/projects/factsheets/webapp/static/img/logo.png',
            x=5, y=5, width=20, height=20),
        
        TextComponent(
            'Jimbos Fund',
            x=30, y=15, width=0, height=0,
            size=16, font_color=(256,256,256)),
        
        TextComponent(
            'this is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summarythis is my fund summary',
            x=0, y=30, height=6, width=210,
            size=8,
            fill=True, fill_color=(223,223,223)),
        
        ImageComponent(
            '/Users/jimcaine/projects/factsheets/notebooks/test.png',
            relative=True, x=0, y=0, width=100, height=50),
        
        TableComponent(df, striped=True,
            x=5, y=120, width=100, height=30),
    ]

    pdf = FPDF()
    pdf.add_page()
    for component in components:
        pdf = component.render(pdf)
    pdf.output('test.pdf', 'F')
