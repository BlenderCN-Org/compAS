"""..."""

import os
import warnings


DATA = os.path.abspath(os.path.join(__file__, '../../../data'))


def find_resource(filename):
    filename = filename.strip('/')
    return os.path.abspath(os.path.join(DATA, filename))


def get_data(filename):
    warnings.warn(
        'This function is deprecated. Use "brg.find_resource(filename)" instead.'
    )
    return find_resource(filename)


def check_dependencies():
    raise NotImplementedError


docs = [
    {'com': []},
    {'datastructures': []},
    {'files': []},
    {'geometry': []},
    {'numerical': []},
    {'physics': []},
    {'utilities': []},
    {'viewers': []},
]
