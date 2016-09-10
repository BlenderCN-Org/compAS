"""This module ...


..  Copyright 2014 BLOCK Research Group
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        `http://www.apache.org/licenses/LICENSE-2.0`_
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

import urllib2


__author__     = ['Tom Van Mele',]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'May 7, 2015'
__contact__    = '''ETH Zurich, 
Institute for Technology in Architecture, 
BLOCK Research Group, 
Stefano-Franscini-Platz 5, 
HIL H 47, 
8093 Zurich, Switzerland
'''


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


#===============================================================================
# Debugging
#===============================================================================

if __name__ == '__main__':
    csv = CSVReader('make_blocks.csv', ',')
    print csv.headers()
    print csv.rows()
    print csv.columns(True)


