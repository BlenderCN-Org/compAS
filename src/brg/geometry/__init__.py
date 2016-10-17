"""brg.geometry : A package defining common geometric functions and objects."""

# import elements
# import arithmetic
# import functions
# import intersections
# import planar
# import queries
# import spatial
# import transformations
# import utilities

# __all__ = [
#     'arithmetic',
#     'functions',
#     'intersections',
#     'planar',
#     'queries',
#     'spatial',
#     'transformations',
#     'utilities'
# ]

from functions import cross
from functions import dot
from functions import angles
from functions import angle_smallest
from functions import length
from functions import length_sqrd
from functions import distance
from functions import distance_sqrd
from functions import area
from functions import centroid
from functions import center_of_mass
from functions import midpoint
from functions import normal
from functions import normal2
from functions import vector_component

from arithmetic import add_vectorlist
from arithmetic import add_vectors
from arithmetic import subtract_vectors

from transformations import translate
from transformations import rotate
from transformations import normalize
from transformations import scale
from transformations import mirror
from transformations import project
from transformations import skew

from spatial import sort_points
from spatial import closest_point
from spatial import closest_point_on_line
from spatial import closest_point_on_segment
from spatial import closest_point_on_polyline
from spatial import closest_point_on_plane

from queries import is_colinear
from queries import is_coplanar
from queries import is_coplanar4
from queries import is_convex
from queries import is_closed
from queries import is_point_on_plane
from queries import is_point_on_line
from queries import is_closest_point_on_segment
from queries import is_point_on_segment
from queries import is_point_on_polyline
from queries import is_ray_intersecting_triangle
from queries import is_line_line_intersection_2d

from intersections import line_line_intersection_2d
from intersections import circle_circle_intersections_2d

docs = [
    'arithmetic',
    'functions',
    'intersections',
    'planar',
    'queries',
    'spatial',
    'transformations',
    'utilities'
]
