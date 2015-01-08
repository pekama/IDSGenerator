import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import pdfkit
from xhtml2pdf import pisa             # import python module


class PdfMerger():

    def merge_pdf(self, pdf_files_list, output_file):
        output = PdfFileWriter()

        for pdf_file in pdf_files_list:
            f = file(pdf_file, "rb")
            input = PdfFileReader(f)
            self.append_pdf(input, output)

        output.write(output_file)


    def append_pdf(self, input, output):
        [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]


class HtmlToPdfConverter():

    def convert_from_file(self, input_path, output_path, options=''):
        if options == '':
            pdfkit.from_file(input_path, output_path)
        else:
            pdfkit.from_file(input_path, output_path, options=options)

    def convert_from_string(self, input_string, output_path, options=''):
        if options == '':
            pdfkit.from_string(input_string, output_path)
        else:
            pdfkit.from_string(input_string, output_path, options=options)


class XHtmlToPdfConverter():

    def convert_from_string(self, input_string, output_path):

        result_file = open(output_path, "w+b")
        pisa_status = pisa.CreatePDF(input_string, dest=result_file)
        result_file.close()

        return pisa_status.err