from typing import Union
import hashlib
import time
from fpdf import FPDF


class PdfException(Exception):
    """
    Need to inherit from base exception explicitly
    """


def get_filename(url: str, exercise_type: str, worksheet_type: str = 'worksheet') -> str:
    m = hashlib.md5()

    m.update(url.encode('UTF-8'))

    return f"{m.hexdigest()}_{str(round(time.time()))}_{exercise_type}_{worksheet_type}.pdf"


def validate_lazy_data_dict(input_dict: dict):
    """
        output_dict = {'title': title,
                       'instructions': instructions,
                       'main_text_final': main_text_final,
                       'question_title': question_title,
                       'removed_words_final': removed_words_final,
                       'answer_title': answer_title,
                       'answers_final': answers_final,
                       'url': url_output_dict['url'],
                       'exercise_type': 'gap fill worksheet'}
    :param input_dict:
    :return:
    """

    if not isinstance(input_dict, dict):
        raise PdfException('input not dict')

    expected_keys = {'title',
                     'instructions',
                     'main_text_final',
                     'question_title',
                     'removed_words_final',
                     'answer_title',
                     'answers_final',
                     'exercise_type',
                     'url',
                     'exercise_type'}

    actual_keys = set(input_dict.keys())

    if expected_keys.intersection(actual_keys) != expected_keys:
        raise PdfException('incomplete keys')


class PdfException(Exception):
    """
    Need to inherit from base exception explicitly
    """


class PageException(PdfException):

    def __init__(self, error_msg: str):
        self.error_msg = error_msg


class PDF(FPDF):

    def header(self):
        # self.set_doc_option('core_fonts_encoding', 'utf8')

        DEFAULT_HEADER_TEXT = 'Created by lazyworksheets.ai, AI powered free language teaching resources!'
        DEFAULT_HEADER_LINK = 'www.lazyworksheets.io'

        # Arial bold 15
        self.set_font('Arial', 'I', 8)
        # Calculate width of title and position
        w = self.get_string_width(DEFAULT_HEADER_TEXT) + 6
        self.set_x((210 - w) / 2)
        # Title
        self.cell(w, txt=DEFAULT_HEADER_TEXT, align='R', link=DEFAULT_HEADER_LINK)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')


class PdfYeah:

    def __init__(self, pdf_name, pdf_directory=None, font_dict=None):
        self.document = PDF()

        if pdf_directory is not None:
            output_directory = pdf_directory
        else:
            output_directory = ''

        self.filename = output_directory + pdf_name

        if font_dict is None:
            self.font_type = 'Arial'
            self.font_size = 10
        else:
            self.font_type = font_dict['type']
            self.font_size = font_dict['size']

        self.document.set_font(family=self.font_type, size=self.font_size)

    def add_title(self, title_text: str):

        if not isinstance(title_text, str):
            raise PageException('incorrect data type to add to title')

        if len(self.document.pages) != 0:
            raise PageException('Title must be added before text')

        # set font characteristics for title
        self.document.set_font(family=self.font_type, style='BU', size=30)
        self.document.add_page()
        self.document.cell(w=0, h=30, align='C', txt=title_text)

        # reset font characteristics for other pages
        self.document.set_font(family=self.font_type, style='', size=self.font_size)

        # set title is like a meta data title, doesn't actually add anything to the page
        # obviously...
        self.document.set_title(title_text)
        self.document.ln()

    def add_text_to_page(self, text_to_add: Union[str, list, tuple]):

        if isinstance(text_to_add, list) or isinstance(text_to_add, tuple):
            raise PageException('TODO - handle lists')

        self.document.multi_cell(w=0, h=5, txt=str(text_to_add))
        # print('self.document.get_y() = ', self.document.get_y())
        self.document.ln()
        self.document.cell(w=0, h=30, align='C', txt='')
        self.document.ln()
        # else:
        #    raise PageException('incorrect data type to add to page')

    def add_page(self):
        self.document.add_page()

    def save_pdf(self):
        self.document.output(self.filename)


def make_pdf_worksheet(lazy_data_object: dict):
    """
    This function takes a dictionary from a lazy worksheet function and converts that to a pdf and
    saves the file

    Assumed structure of the data object

    output_dict = {'title': title,
                       'instructions': instructions,
                       'main_text_final': main_text_final,
                       'question_title': question_title,
                       'removed_words_final': removed_words_final,
                       'answer_title': answer_title,
                       'answers_final': answers_final,
                       'url': url_output_dict['url'],
                       'exercise_type': 'gap fill worksheet'}


    :param lazy_data_object:
    :return:
    """

    validate_lazy_data_dict(lazy_data_object)

    this_pdf = PdfYeah(get_filename(lazy_data_object['url'], lazy_data_object['exercise_type']))
    this_pdf.add_title(lazy_data_object['title'])
    this_pdf.add_text_to_page(lazy_data_object['instructions'])
    this_pdf.add_text_to_page(f"{lazy_data_object['main_text_final']}\n\nText extracted from {lazy_data_object['url']}.")
    this_pdf.add_page()
    this_pdf.add_text_to_page(lazy_data_object['removed_words_final'])

    this_pdf.save_pdf()


def make_pdf_answers(lazy_data_object: dict):
    """
    This function takes a dictionary from a lazy worksheet function and converts that to a pdf and
    saves the file

    Assumed structure of the data object

    output_dict = {'title': title,
                       'instructions': instructions,
                       'main_text_final': main_text_final,
                       'question_title': question_title,
                       'removed_words_final': removed_words_final,
                       'answer_title': answer_title,
                       'answers_final': answers_final,
                       'url': url_output_dict['url'],
                       'exercise_type': 'gap fill worksheet'}


    :param lazy_data_object:
    :return:
    """

    validate_lazy_data_dict(lazy_data_object)

    this_pdf = PdfYeah(
        get_filename(lazy_data_object['url'], lazy_data_object['exercise_type'], worksheet_type='answers'))
    this_pdf.add_title(lazy_data_object['title'])
    this_pdf.add_text_to_page(lazy_data_object['answers_final'])
    this_pdf.add_page()

    this_pdf.save_pdf()


if __name__ == "__main__":
    pass
