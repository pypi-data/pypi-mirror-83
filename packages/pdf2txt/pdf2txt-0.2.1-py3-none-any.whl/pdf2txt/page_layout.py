import logging
from collections import namedtuple

import matplotlib.pyplot as plt
from matplotlib import patches

from pdf2txt.core import TextEdges
from pdf2txt.utils import _get_box_borders, _get_MAX, _get_MIN, are_in_same_Line, get_fonts
from pdf2txt.utils import get_text_objects, get_lines
from pdf2txt.utils import is_rotated
from pdf2txt.utils import isRectangleOverlap
from pdf2txt.parser.lattice import Lattice
logger = logging.getLogger("camelot")

class Span():
    def __init__(self, textline):
        self.text = textline.get_text().strip()
        font = get_fonts(textline)
        self.x0, self.x1, self.y0, self.y1=textline.x0, textline.x1, textline.y0, textline.y1
        self.fontsize=font['size']
        self.font=font['name']
        self.font_width= font['width']
        self.textlines=[textline]
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Span):
            return self.text == other.text and self.x0==other.x0 and self.y1==other.y1
        return False

    def __repr__(self):
        return '<'+self.text+'>'

    def add(self, other, separator='\n'):
        self.text += separator + other.text
        self.y0 = min(other.y0, self.y0)
        self.x0 = min(other.x0, self.x0)
        self.y1=max(other.y1, self.y1)
        self.x1 = max(other.x1, self.x1)
        self.textlines.extend(other.textlines)
        return self



class Line():
    def __init__(self):
        self.spans=[]

class PageLayout():

    def __init__(
        self,
        edge_tol=50,
    ):

        self.edge_tol = edge_tol

        self.page_regions=None



    def _get_page_parameters(self, LTPage):
        PAGE_WIDTH = round(LTPage.bbox[2])
        PAGE_HEIGHT = round(LTPage.bbox[3])

        X_MIN = X_MAX = Y_MIN = Y_MAX = 0

        for LTLine in LTPage._objs:
            try:
                text = LTLine.get_text()
                if len(text.strip())<=1 or is_rotated(LTLine, text):
                    continue
            except AttributeError:
                continue

            x0, x1, y0, y1 = _get_box_borders(LTLine)
            X_MIN = _get_MIN(x0, X_MIN)
            X_MAX = _get_MAX(x1, X_MAX)
            Y_MIN = _get_MIN(y0, Y_MIN)
            Y_MAX = _get_MAX(y1, Y_MAX)

        return PAGE_WIDTH, PAGE_HEIGHT, X_MIN, X_MAX, Y_MIN, Y_MAX


    def _set_page_layout(self, page_layout):

        self.layout =page_layout
        self.pdf_width, self.pdf_height, self.margin_left, self.margin_right, self.margin_bottom, self.margin_top=self._get_page_parameters(page_layout)
        self.images = get_text_objects(self.layout, ltype="image")
        self.text_boxes=get_text_objects(self.layout, ltype="text_box")
        self.horizontal_text = get_text_objects(self.layout, ltype="horizontal_text")
        self.vertical_text = get_text_objects(self.layout, ltype="vertical_text")
        self.lines=get_lines(self.layout)


    def _page_detection_algorithm2(self, textlines):

        textedges = TextEdges( edge_tol=2*self.edge_tol)
        textedges.page_width=self.margin_right-self.margin_left
        textedges.page_height=self.margin_top-self.margin_bottom
        textedges.left_margin=self.margin_left

        # generate left, middle and right textedges
        textedges.generate2(textlines)
        # guess vertical areas that are in the midle of a multi-column page
        vertical_bbox = textedges.get_column_separators(textlines, self.lines, textedges.left())
        table_areas=[]

        Area = namedtuple('Area', ['x0', 'y0', 'x1', 'y1'])

        if len(vertical_bbox)==0:
            table_areas.append(Area(0, 0, self.pdf_width, self.pdf_height))
            return table_areas
        else:
            table_areas=self.get_areas_from_separators(vertical_bbox)

        # #sort vertical lines by desending order of top edge (this allow to form the top area
        # vertical_bbox.sort(key=lambda te: -te[3])
        #
        #
        # left=self.margin_left
        # top=self.margin_top
        # right=self.margin_right
        # splitter = vertical_bbox[0]
        # #detect top page area
        # for i in range(0, len(vertical_bbox)):
        #     bottom = vertical_bbox[i][3]
        #     if splitter[1] > vertical_bbox[i][3]:
        #         top=splitter[1]
        #         bottom=vertical_bbox[i][3]
        #     if i>0 and splitter[0] < vertical_bbox[i][0]:
        #         left=splitter[0]
        #     elif i>0 and splitter[1] < vertical_bbox[i][3]:
        #         right=splitter[0]
        #
        #     if self.margin_top - vertical_bbox[i][3] > 10:
        #         table_areas.append(Area(left ,bottom , right, top))
        #
        #     top=vertical_bbox[i][3]
        #     if top>self.margin_top:
        #         top=self.margin_top
        #     splitter=vertical_bbox[i]
        #
        # vertical_bbox.sort(key=lambda te: -te[0])
        # left=self.margin_left
        # bottom=self.margin_bottom
        # right=self.margin_right
        # splitter=vertical_bbox[0]
        # for i in range(0, len(vertical_bbox)):
        #     top = vertical_bbox[i][1]
        #     if i>0 and splitter[0] < vertical_bbox[i][0]:
        #         left=splitter[0]
        #     elif i>0:
        #         right=splitter[0]
        #     if vertical_bbox[i][1]-bottom > 10:
        #         table_areas.append(Area(left, bottom, right, top))
        #     bottom=top
        #     splitter = vertical_bbox[i]
        #
        #     vertical_bbox.sort(key=lambda te: te[0])
        #     for i in range(0, len(vertical_bbox)):
        #         if i==0:
        #             table_areas.append(Area(self.margin_left, vertical_bbox[0][1], vertical_bbox[0][0], vertical_bbox[0][3]))
        #         elif vertical_bbox[i-1][3]<vertical_bbox[i][3]:
        #                 table_areas.append(
        #                     Area(vertical_bbox[i-1][0], vertical_bbox[i-1][1], vertical_bbox[i][0], vertical_bbox[i-1][3]))
        #                 if i ==1:
        #                     table_areas.append(Area(vertical_bbox[i][0], vertical_bbox[i][1], self.margin_right, vertical_bbox[i][3]))
        #                 else:
        #                     raise NotImplemented("Algorithm does not handle the case of more than 3 columns")
        #         else:
        #             table_areas.append(
        #                 Area(vertical_bbox[i - 1][0], vertical_bbox[i][1], vertical_bbox[i][0],
        #                      vertical_bbox[i][3]))
        #             if i == 1:
        #                 table_areas.append(
        #                     Area(vertical_bbox[i][0], vertical_bbox[i][1], self.margin_right, vertical_bbox[i][3]))
        #             else:
        #                 raise NotImplemented("Algorithm does not handle the case of more than 3 columns")
        #
        #         if len(vertical_bbox)==1:
        #             table_areas.append(Area(vertical_bbox[0][0], vertical_bbox[0][1], self.margin_right, vertical_bbox[0][3]))


        # treat whole page as table area if no table areas found
        if not len(table_areas):
            table_areas.append((0, 0, self.pdf_width, self.pdf_height))
        return table_areas


    def get_areas_from_separators(self, separators):
        table_areas = []

        Area = namedtuple('Area', ['x0', 'y0', 'x1', 'y1'])

        # sort vertical lines by desending order of top edge (this allow to form the top area
        separators.sort(key=lambda te: -te.y0)

        left = self.margin_left
        top = self.margin_top
        right = self.margin_right

        # detect top page area
        last_separator=separators[0]
        for separaor in separators:
            bottom = separaor.y1
            if  last_separator.y0 > bottom:
                top = last_separator.y1
            if last_separator.y1 > separaor.y1 > last_separator.y0:
                if last_separator.x0 < separaor.x0:
                    left=last_separator.x0
                else:
                    right=last_separator.x0
            #top area
            table_areas.append(Area(left, bottom, right, top))
            #left area
            top=bottom
            right=separaor.x0
            sep_to_left=self.get_left_separator(separators, separaor)
            if sep_to_left:
                bottom=sep_to_left.y1
            else:
                bottom=separaor.y0
            table_areas.append(Area(left, bottom, right, top))
            # right area
            left=separaor.x0
            right=self.margin_right
            sep_to_right=self.get_right_separator(separators, separaor)
            if sep_to_right:
                bottom=sep_to_right.y1
            else:
                bottom=separaor.y0

            table_areas.append(Area(left, bottom, right, top))
            top=separaor.y1
            last_separator=separaor
            left=self.margin_left

        top=last_separator.y0
        bottom=self.margin_bottom
        left=self.margin_left
        right=self.margin_right
        table_areas.append(Area(left, bottom, right, top))

        return table_areas

    def get_left_separator(self, sparators, separator):
        #separators are sorted acording to  decreasing y0
        for s in sparators:
            if s.x0 < separator.x0 and separator.y1 > s.y1 > separator.y0:
                return s
        return None

    def get_right_separator(self, sparators, separator):
        #separators are sorted acording to  decreasing y0
        for s in sparators:
            if s.x0 > separator.x0 and separator.y1 > s.y1 > separator.y0:
                return s
        return None

    def _find_line_structure(self, textlines):
        textlines.sort(key=lambda x: (-x.y1, x.x0))
        lines=[]
        i=0
        while i < len(textlines)-1:
            text = Span(textlines[i])
            if len(text.text.strip())<=1 and not text.text.strip().isupper():
                i+=1
                continue

            next_text = Span(textlines[i+1])
            line=Line()
            line.spans.append(text)
            while are_in_same_Line(text, next_text) and i<len(textlines)-2:
                if len(next_text.text.strip()) <= 1 and not next_text.text.strip().isupper():
                    i += 1
                    next_text = Span(textlines[i + 1])
                    continue
                separation = abs(text.x1 - next_text.x0)
                if separation <= 1.5 * text.font_width:
                    text.add(next_text, separator=' ')
                else:
                    line.spans.append(next_text)
                i += 1
#                text = Span(textlines[i])
                next_text = Span(textlines[i+1])

                continue

            line.spans.sort(key=lambda x: x.x0, reverse=False)
            lines.append(line)

            i+=1
        #handle the last line
        if i==len(textlines)-1 and next_text not in lines[-1].spans:
            line=Line()
            line.spans.append(next_text)
            lines.append(line)

        return lines



    def draw_rect_bbox(self, x0, y0, x1, y1, ax, color):
        """
        Draws an unfilled rectable onto ax.
        """
        ax.add_patch(
            patches.Rectangle(
                (x0, y0),
                x1 - x0,
                y1 - y0,
                fill=False,
                color=color
            )
        )


    def draw_rect(self, rect, ax, color="black"):
        self.draw_rect_bbox(rect[0],rect[1],rect[2],rect[3], ax, color)

    def plot_page(self, rects):


        xmin, ymin, xmax, ymax = self.margin_left, self.margin_bottom, self.margin_right, self.margin_top
        size = 6

        fig, ax = plt.subplots(figsize=(size, size * (ymax / xmax)))

        for rect in rects:
            self.draw_rect(rect, ax)

        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        plt.show()


    def extract_regions(self):

        self.textedges = []
        hor_text = self.horizontal_text
        self.horizontal_lines_text = self._find_line_structure(hor_text)

        # find tables based on nurminen's detection algorithm
        self.page_regions = self._page_detection_algorithm2(self.horizontal_lines_text)

 #       self.plot_page(self.page_regions)

        return self.page_regions

    def parse_region(self, region):
        lattice_parser=Lattice()

    def get_text_from_region(self, region):
        texts=[]

        for line in self.horizontal_lines_text:
            text_span=[]
            text = ""
            for span in line.spans:
                if isRectangleOverlap(span, region):
                    text_span.append(span.text)
            if len(text_span):
                text='\t'.join(text_span)

            if text !="":
                texts.append(text)

        return '\n'.join(texts)
    def extract_texts(self):
        self.page_regions.sort(key=lambda te: (-te.y1, te.x0))
        if not self.page_regions:
            self.page_regions=self.extract_regions()
        texts=[]
        for region in self.page_regions:
            texts.append(self.get_text_from_region(region))

        return '\n'.join(texts)


    def extract_simple(self):
        self.horizontal_lines_text = self._find_line_structure(self.horizontal_text)
        texts=[]
        for line in self.horizontal_lines_text:
            text='\t'.join([t.text for t in line.spans])
            texts.append(text)

        return '\n'.join(texts)