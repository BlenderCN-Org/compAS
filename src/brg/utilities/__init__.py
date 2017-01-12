# import colors
# import maps
# import mixing
# import names
# import scripts
# import units
# import webapi
# import xfunc
# import xfuncio


# __all__ = [
#     'colors',
#     'drawing',
#     'maps',
#     'mixing',
#     'names',
#     'scripts',
#     'units',
#     # 'webapi',
#     # 'xfunc',
#     # 'xfuncio',
# ]


from brg.utilities.colors import i2rgb
from brg.utilities.colors import i2red
from brg.utilities.colors import i2green
from brg.utilities.colors import i2blue
from brg.utilities.colors import i2white
from brg.utilities.colors import i2black
from brg.utilities.colors import rgb2hex
from brg.utilities.colors import color_to_colordict

# from scriptserver import ScriptServer
# from scriptserver import ScriptServerError

# from webapi import WebAPI
# from webapi import WebAPIError

# from webservice import Dispatcher
# from webservice import list_methods_wrapper
# from webservice import method_signature_wrapper
# from webservice import method_help_wrapper
# from webservice import test

# from xfunc import XFunc
# from xfuncio import XFuncIO

docs = [
	{'colors': ['i2rgb', 'i2red', 'i2green', 'i2blue', 'i2white', 'i2black', 'rgb2hex', 'color_to_colordict', ]},
	{'_datetime': ['timestamp', ]},
	{'drawing': ['create_matplotlib_axes', 'draw_points', 'draw_points_in_matplotlib', 'draw_lines', 'draw_lines_in_matplotlib', ]},
	{'files': []},
	{'maps': ['geometric_key', 'geometric_key2']},
	{'mixing': ['mix_in_functions', 'mix_in_class_attributes', ]},
	{'names': ['rname', ]},
	{'plotters': ['Axes2', 'Cloud2', 'Axes3', 'Bounds3', 'Cloud3', 'Hull3', 'Box3', 'Network3', 'Mesh3', ]},
	{'scripts': ['ScriptServer', ]},
	{'units': ['Temperature', ]},
	{'xfunc': ['XFunc', 'xecute', ]},
	{'xfuncio': ['XFuncIO', 'xecuteio', ]}
]
