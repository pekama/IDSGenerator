__author__ = 'eyal'
import os


class IdsFIller:

    def fill_ids(self, jar_path ,original_ids_path, data_xml_path, output_path):
        os.system('java -jar "%s" "%s" "%s" "%s"' % (jar_path, original_ids_path, data_xml_path, output_path,))


