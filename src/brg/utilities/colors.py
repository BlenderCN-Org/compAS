__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'i_to_rgb', 'i_to_red', 'i_to_green', 'i_to_blue', 'i_to_white', 'i_to_black',
    'rgb_to_hex', 'hex_to_rgb', 'color_to_colordict', 'color_to_rgb',
]


BASE16  = '0123456789abcdef'

try:
    HEX_DEC = dict((v, int(v, base=16)) for v in [x + y for x in BASE16 for y in BASE16])
except:
    HEX_DEC = dict((v, int(v, 16)) for v in [x + y for x in BASE16 for y in BASE16])


def i_to_rgb(i):
    if i == 0.0:
        return 0, 0, 255
    if 0.0 < i < 0.25:
        return 0, int(255 * (4 * i)), 255
    if i == 0.25:
        return 0, 255, 255
    if 0.25 < i < 0.5:
        return 0, 255, int(255 - 255 * 4 * (i - 0.25))
    if i == 0.5:
        return 0, 255, 0
    if 0.5 < i < 0.75:
        return int(0 + 255 * 4 * (i - 0.5)), 255, 0
    if i == 0.75:
        return 255, 255, 0
    if 0.75 < i < 1.0:
        return 255, int(255 - 255 * 4 * (i - 0.75)), 0
    if i == 1.0:
        return 255, 0, 0
    return 0, 0, 0


def i_to_red(i):
    i  = max(i, 0.0)
    i  = min(i, 1.0)
    gb = min((1 - i) * 255, 255)
    return (255, int(gb), int(gb))


def i_to_green(i):
    i  = max(i, 0.0)
    i  = min(i, 1.0)
    rb = min((1 - i) * 255, 255)
    return (int(rb), 255, int(rb))


def i_to_blue(i):
    i  = max(i, 0.0)
    i  = min(i, 1.0)
    rg = min((1 - i) * 255, 255)
    return (int(rg), int(rg), 255)


def i_to_white(i):
    i   = max(i, 0.0)
    i   = min(i, 1.0)
    rgb = min((1 - i) * 255, 255)
    return (int(rgb), int(rgb), int(rgb))


def i_to_black(i):
    i   = max(i, 0.0)
    i   = min(i, 1.0)
    rgb = min(i * 255, 255)
    return (int(rgb), int(rgb), int(rgb))


# see: http://stackoverflow.com/questions/4296249/how-do-i-convert-a-hex-triplet-to-an-rgb-tuple-and-back


def rgb_to_hex(rgb, g=None, b=None):
    if g is None and b is None:
        r, g, b = rgb
    else:
        r = rgb
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    # return format(r << 16 | g << 8 | b, '06x')
    return '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)


def hex_to_rgb(value):
    value = value.lstrip('#').lower()
    return HEX_DEC[value[0:2]], HEX_DEC[value[2:4]], HEX_DEC[value[4:6]]


def color_to_colordict(color, keys, default=None, colorformat='hex', normalize=False):
    color = color or default
    if isinstance(color, basestring):
        if colorformat == 'rgb':
            color = hex_to_rgb(color)
        return dict((key, color) for key in keys)
    if isinstance(color, (tuple, list)) and len(color) == 3:
        if colorformat == 'hex':
            color = rgb_to_hex(color)
        return dict((key, color) for key in keys)
    if isinstance(color, dict):
        for k, c in color.items():
            if isinstance(c, basestring):
                if colorformat == 'rgb':
                    color = hex_to_rgb(color)
            if isinstance(c, (tuple, list)) and len(c) == 3:
                if colorformat == 'hex':
                    color[k] = rgb_to_hex(c)
        return dict((key, default if key not in color else color[key]) for key in keys)
    raise Exception('This is not a valid color format: {0}'.format(type(color)))


def color_to_rgb(color, normalize=False):
    if isinstance(color, basestring):
        r, g, b = hex_to_rgb(color)
    elif isinstance(color, int):
        r, g, b = i_to_rgb(color)
    else:
        r, g, b = color
    if not normalize:
        return r, g, b
    return r / 255., g / 255., b / 255.


class Color(object):
    """"""

    def __init__(self):
        pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
