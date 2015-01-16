import subprocess

class IdsFIller:

    def fill_ids(self, jar_path, original_ids_path, data_xml_path, output_path):
        subprocess.call(['java', '-jar', jar_path, original_ids_path, data_xml_path, output_path])


