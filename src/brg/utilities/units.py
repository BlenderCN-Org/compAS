
__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Jun 12, 2015'


class TemperatureError(Exception):
    pass


class Temperature(object):
    """"""
    def __init__(self, temp=None, scale='C'):
        self._celcius = None
        self._fahrenheit = None
        if temp:
            if scale in ('c', 'C', 'celcius', 'Celcius'):
                self.celcius = temp
            elif scale in ('f', 'F', 'fahrenheit', 'Fahrenheit'):
                self.fahrenheit = temp
            else:
                raise TemperatureError

    @property
    def celcius(self):
        return self._celcius

    @celcius.setter
    def celcius(self, temp):
        self._celcius = temp
        self._fahrenheit = float('{0:.2f}'.format((temp - 32) * 5 / 9))

    @property
    def fahrenheit(self):
        return self._fahrenheit

    @fahrenheit.setter
    def fahrenheit(self, temp):
        self._celcius = float('{0:.2f}'.format(temp * 9 / 5 + 32))
        self._fahrenheit = temp


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
