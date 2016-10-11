""""""

import urllib2


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'May 7, 2015'


docs = [
    'CSVReader',
    'CSVWriter',
]


class CSVReader(object):
    """"""

    def __init__(self, filepath, delimiter=',', remote=False):
        self.filepath = filepath
        self.delimiter = delimiter
        self.remote = remote
        self._content = None
        self._headers = []
        self._rows = []
        self.open()
        self.read()

    # this actually opens AND reads
    # too many responsibilities
    # is resp similar to fh ?
    def open(self):
        if self.remote:
            resp = urllib2.urlopen(self.filepath)
            self._content = resp.readlines()
        else:
            with open(self.filepath) as fh:
                self._content = fh.readlines()

    def read(self):
        self._headers = self._content[0].strip().split(self.delimiter)
        for line in iter(self._content[1:]):
            line = line.strip()
            row = line.split(self.delimiter)
            self._rows.append(row)

    def headers(self):
        return self._headers

    def rows(self, headers=False):
        if headers:
            return [dict((self._headers[i], row[i]) for i in range(len(row))) for row in self._rows]
        return self._rows

    def columns(self, headers=False):
        columns = zip(*self._rows)
        if headers:
            return dict((self._headers[i], columns[i]) for i in range(len(columns)))
        return columns


class CSVWriter(object):
    """"""
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    csv = CSVReader('make_blocks.csv', ',')
    print csv.headers()
    print csv.rows()
    print csv.columns(True)
