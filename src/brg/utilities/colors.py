
__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Jun 12, 2015'


BASE16  = '0123456789abcdef'
try:
    HEX2DEC = dict((v, int(v, base=16)) for v in [x + y for x in BASE16 for y in BASE16])
except:
    HEX2DEC = dict((v, int(v, 16)) for v in [x + y for x in BASE16 for y in BASE16])


def i2rgb(i):
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


def i2red(i):
    i  = max(i, 0.0)
    i  = min(i, 1.0)
    gb = min((1 - i) * 255, 255)
    return (255, int(gb), int(gb))


def i2green(i):
    i  = max(i, 0.0)
    i  = min(i, 1.0)
    rb = min((1 - i) * 255, 255)
    return (int(rb), 255, int(rb))


def i2blue(i):
    i  = max(i, 0.0)
    i  = min(i, 1.0)
    rg = min((1 - i) * 255, 255)
    return (int(rg), int(rg), 255)


def i2white(i):
    i   = max(i, 0.0)
    i   = min(i, 1.0)
    rgb = min((1 - i) * 255, 255)
    return (int(rgb), int(rgb), int(rgb))


def i2black(i):
    i   = max(i, 0.0)
    i   = min(i, 1.0)
    rgb = min(i * 255, 255)
    return (int(rgb), int(rgb), int(rgb))


# see: http://stackoverflow.com/questions/4296249/how-do-i-convert-a-hex-triplet-to-an-rgb-tuple-and-back


def rgb2hex(rgb, g=None, b=None):
    if g is None and b is None:
        r, g, b = rgb
    else:
        r = rgb
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    # return format(r << 16 | g << 8 | b, '06x')
    return '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)


def hex2rgb(value):
    value = value.lstrip('#').lower()
    return HEX2DEC[0:2], HEX2DEC[2:4], HEX2DEC[4:6]


def color_to_colordict(color, dictkeys, defcolor=None):
    color = color or defcolor
    if isinstance(color, basestring):
        return dict((key, color) for key in dictkeys)
    if isinstance(color, (tuple, list)) and len(color) == 3:
        color = rgb2hex(color)
        return dict((key, color) for key in dictkeys)
    if isinstance(color, dict):
        for k, c in color.items():
            if isinstance(c, (tuple, list)) and len(c) == 3:
                color[k] = rgb2hex(c)
        return dict((key, defcolor if key not in color else color[key]) for key in dictkeys)
    raise Exception('This is not a valid color format: {0}'.format(type(color)))


def to_rgb(color, normalize=False):
    if isinstance(color, basestring):
        r, g, b = hex2rgb(color)
    elif isinstance(color, int):
        r, g, b = i2rgb(color)
    else:
        r, g, b = color
    if not normalize:
        return r, g, b
    return r / 255., g / 255., b / 255.


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
