from unittest import TestCase, mock
import os

from pdfyeah.enums import KEYS_REQUIRED_FOR_GAP_FILLER_WORKSHEET
from pdfyeah.pdf_creator import (
    validate_lazy_data_dict,
    PdfException,
    get_filename,
    make_pdf_worksheet
)


def clean_up_pdfs():
    """
    removes pdfs from previous failed tests and cleans up after current test
    :return:
    """
    cwd = os.getcwd()
    files_in_cwd = (os.listdir(cwd))
    for i_file in files_in_cwd:
        if i_file.endswith('.pdf'):
            os.remove(os.path.join(cwd, i_file))


class TestPdf(TestCase):

    def test_validate_lazy_data_dict__success(self):
        input_dict = {'title': 1,
                      'instructions': 1,
                      'main_text_final': 1,
                      'question_title': 1,
                      'removed_words_final': 1,
                      'answer_title': 1,
                      'answers_final': 1,
                      'url': 1,
                      'exercise_type': 1}

        validate_lazy_data_dict(input_dict=input_dict, expected_keys=KEYS_REQUIRED_FOR_GAP_FILLER_WORKSHEET)

    def test_validate_lazy_data_dict__failure_not_dict(self):
        input_dict = ['not a dict!']

        with self.assertRaisesRegex(PdfException, 'input not dict'):
            validate_lazy_data_dict(input_dict=input_dict, expected_keys=KEYS_REQUIRED_FOR_GAP_FILLER_WORKSHEET)

    def test_validate_lazy_data_dict__different_keys(self):
        input_dict = {'title': 1,
                      'instructions': 1,
                      'main_text_final': 1,
                      'question_title': 1,
                      'removed_words_final': 1,
                      'answer_title': 1}

        with self.assertRaisesRegex(PdfException, 'incomplete keys'):
            validate_lazy_data_dict(input_dict=input_dict, expected_keys=KEYS_REQUIRED_FOR_GAP_FILLER_WORKSHEET)

    @mock.patch('time.time', return_value=123)
    def test_get_filename__worksheet(self, mock_time):
        url = 'test.com'
        exercise_type = 'test_exercise'

        expected_output = f"c97c1b3671fef2055e175ca2154d217a_123_{exercise_type}_worksheet.pdf"

        self.assertEqual(expected_output, get_filename(url=url, exercise_type=exercise_type))

    @mock.patch('time.time', return_value=123)
    def test_get_filename__answers(self, mock_time):
        url = 'test.com'
        exercise_type = 'test_exercise'

        expected_output = f"c97c1b3671fef2055e175ca2154d217a_123_{exercise_type}_answers.pdf"

        self.assertEqual(expected_output, get_filename(url=url, exercise_type=exercise_type, worksheet_type='answers'))

    @mock.patch('pdfyeah.pdf_creator.get_filename', return_value='my_test.pdf')
    def test_make_pdf_worksheet(self, mock_filename):
        clean_up_pdfs()

        input_dict = {'title': 'Fill the Gaps!',
                      'instructions': 'Read the below text. Can you fill the gaps with the words in the list below?',
                      'main_text_final': 'this is the main text   ' * 400,
                      'question_title': 1,
                      'removed_words_final': 'word_1,\n word_2',
                      'answer_title': 1,
                      'answers_final': 1,
                      'url': 'test36636.com',
                      'exercise_type': 'worksheet_test_type'}

        make_pdf_worksheet(input_dict)

        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(), 'my_test.pdf')))
        os.remove(os.path.join(os.getcwd(), 'my_test.pdf'))
