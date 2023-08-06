'''
pdf2textbox.py

:param url: A URL pointing at a PDF file with max 3 columns and a header
:returns: Returns a dict containing text items that have been extracted from PDF
:raises NameError
:raises UnboundLocalError
:raises PDFTextExtractionNotAllowed
'''

from pdf2txt.page_layout import PageLayout
from pdf2txt.utils import get_page_layout




def pdf_to_text_all(pdf, detect_regions=False):
    '''
    Converts PDF documents with up to three columns into text.
    Will convert the whole document, or die trying.
    Determine layout (vertical/horizontal) first.
    Calculate the number of columns:
        - get the width of boxes
        - divide max horizontal width by max box width
          --> nr of columns
    Determine if there is a header. This is done in two steps.
    Create a dictionary organized in pagenumber, header, columns.
    Enter text into dictionary.
    Return dictionary.
    '''



    layout_kwargs = {}
#    pages_layouts=get_pdf_layout(pdf, **layout_kwargs)
    texts={}
    page=0
    for layout, _ in get_page_layout(pdf):
        page+=1
        region_parser = PageLayout(edge_tol=50)
        region_parser._set_page_layout(layout)

        if detect_regions:
            region_parser.extract_regions()
            texts['page'+str(page)]=region_parser.extract_texts()
        else:
            texts['page'+str(page)]=region_parser.extract_simple()

    return texts
