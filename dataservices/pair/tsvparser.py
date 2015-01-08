__author__ = 'Eyal Fisher'

class TsvParser():

    def __init__(self):
        pass

    def get_lines(self, opened_file):
        text = opened_file.read()

        results = []

        rows = text.split('\n')
        if len(rows) == 0:
            rows = text.split('\n\r')
        for row in rows:
            row = results.append(row.split('\t'))

        return results