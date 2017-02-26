from __future__ import print_function

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


class CSVReader(object):
    """Read the contents of a *csv* file.

    Parameters:
        filepath (str): Path to the file.
        delimiter (str): Optional. Cell delimiter. Default is ``','``.
        remote (bool): Optional. Is the file in a remote location? Default is ``False``.

    """

    def __init__(self, filepath, delimiter=',', remote=False):
        self.filepath = filepath
        self.delimiter = delimiter
        self.remote = remote
        self._content = None
        self._headers = []
        self._rows = []
        self.open()
        self.pre()
        self.read()
        self.post()

    def open(self):
        if self.remote:
            resp = urllib2.urlopen(self.filepath)
            self._content = resp.readlines()
        else:
            with open(self.filepath) as fh:
                self._content = fh.readlines()

    def pre(self):
        pass

    def read(self):
        self._headers = self._content[0].strip().split(self.delimiter)
        for line in iter(self._content[1:]):
            line = line.strip()
            row = line.split(self.delimiter)
            self._rows.append(row)

    def post(self):
        pass

    def headers(self):
        return self._headers

    def rows(self, include_headers=False):
        """Retrieve the row data.

        Parameters:
            include_headers (bool): Optional. If ``True``, return per row a
                dictionary with the headers as keys and the corresponding columns
                as values. Default is ``False``.

        Returns:
            list of list: If ``include_headers=False``. The row data.
            list of dict: If ``include_headers=True``. The row data as a list of dicts.

        """
        if include_headers:
            return [dict((self._headers[i], row[i]) for i in range(len(row))) for row in self._rows]
        return self._rows

    def columns(self, include_headers=False):
        """Retrieve the column data.

        Parameters:
            include_headers (bool): Optional. Default is ``False``.

        Returns:
            list of list: If ``include_headers=False``. The column data.
            list of dict: If ``include_headers=True``. The column data as a dictionary.

        """
        columns = zip(*self._rows)
        if include_headers:
            return dict((self._headers[i], columns[i]) for i in range(len(columns)))
        return columns


class CSVWriter(object):
    """Write the contents of a *csv* file.

    Parameters:
        filepath (str): Path to the file.
        rows (list of list, list of dict): The row data.
        headers (list): Optional. Column headers. Default is ``None``.
        delimiter (str): Optional. Cell delimiter. Default is ``','``.

    """

    def __init__(self, filepath, rows, headers=None, delimiter=','):
        self.filepath = filepath
        self.rows = rows
        self.headers = headers
        self.delimiter = delimiter
        self.pre()
        self.write()

    def pre(self):
        if self.headers:
            h = len(self.headers)
            assert all([len(row) <= h for row in self.rows]), 'Some rows contain more data than there are headers.'

    def write(self):
        with open(self.filepath, 'wb+') as fp:
            if self.headers:
                fp.write('{0}\n'.format(self.delimiter.join(self.headers)))
            for row in self.rows:
                if isinstance(row, dict):
                    pass
                else:
                    fp.write('{0}\n'.format(self.delimiter.join(row)))


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    csv = CSVReader('make_blocks.csv', ',')
    print(csv.headers())
    print(csv.rows())
    print(csv.columns(True))
