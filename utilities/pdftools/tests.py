import os
from tempfile import TemporaryFile
from unittest import TestCase
from utilities.pdftools.pdftools import PdfMerger, HtmlToPdfConverter, XHtmlToPdfConverter


class TestFileFinder(object):
    pdf_file_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_pdf_files'))

    @classmethod
    def get_file_path(cls, *path):
        return os.path.join(cls.pdf_file_directory, *path)



class PdfMergerTests(TestCase):

    def test_merger_pdf(self):
        first_pdf = TestFileFinder.get_file_path('A2-1.pdf')
        second_pdf = TestFileFinder.get_file_path('A2-2.pdf')
        third_pdf = TestFileFinder.get_file_path('A2-3.pdf')

        output_file = TemporaryFile()
        merger = PdfMerger()

        merger.merge_pdf([first_pdf, second_pdf, third_pdf], output_file)

        output_file.seek(0)
        output_content = output_file.read()
        self.assertTrue(len(output_content) > 0)

class HtmlToPdfConverterTests(TestCase):

    def test_convert_from_file(self):
        input_path = TestFileFinder.get_file_path('test.html')
        output_path = TestFileFinder.get_file_path('test.pdf')
        css = TestFileFinder.get_file_path('test.css')

        converter = HtmlToPdfConverter()

        converter.convert_from_file(input_path, output_path)

        self.assertTrue(os.path.isfile(output_path))

    def test_convert_from_string(self):
        string1 = "this is a pdf"

        output_path = TestFileFinder.get_file_path('test2.pdf')

        converter = XHtmlToPdfConverter()

        converter.convert_from_string(string1, output_path)

        self.assertTrue(os.path.isfile(output_path))

