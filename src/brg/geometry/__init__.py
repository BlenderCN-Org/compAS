"""brg.geometry : A package defining common geometric functions and objects."""

from functions import cross
from functions import dot

from functions import angles  # angles_vectors, angles_points, angles_lines, angles_planes
from functions import angle_smallest  # angle_...
from functions import length  # length_vector
from functions import length_sqrd
from functions import distance  # distance_point_point, distance_point_line, distance_point_plane, distance_line_line
from functions import distance_sqrd
from functions import area  # area_polygon, area_triangle
from functions import centroid  # centroid_points
from functions import center_of_mass  # center_of_mass_polygon, center_of_mass_polyhedron
from functions import midpoint  # midpoint_line
from functions import normal  # normal_triangle, normal_polygon
from functions import normal2  # FLAG => 'perimeter', 'fitplane', 'centroid'
from functions import vector_component

from arithmetic import add_vectorlist  # remove
from arithmetic import add_vectors  # add variable number of arguments
from arithmetic import subtract_vectors  # add variable number of arguments

from transformations import translate  # translate_points, translate_lines
from transformations import rotate  # rotate_points (point, axis, angle)
from transformations import normalize  # normalize_vectors (unitize alias)
from transformations import scale  # scale_points (optional origin)
from transformations import mirror  # mirror_points_point, mirror_points_plane
from transformations import project  # project_points_plane, project_points_line
# from transformations import skew

# add pull_...
# add -ed variations (in-place transformations)

from spatial import sort_points  # remove
from spatial import closest_point  # closest_points_point, closest_points_line, closest_points_plane
from spatial import closest_point_on_line
from spatial import closest_point_on_segment
from spatial import closest_point_on_polyline
from spatial import closest_point_on_plane

# always return indices
# FLAG: return_index
# add closest_ppoint_on_polygon

from queries import is_colinear
from queries import is_coplanar
from queries import is_coplanar4
# from queries import is_convex
from queries import is_closed  # remove
from queries import is_point_on_plane
from queries import is_point_on_line
from queries import is_closest_point_on_segment  # is_point_on_segment
from queries import is_point_on_segment
from queries import is_point_on_polyline

# from queries import is_ray_intersecting_triangle
# from queries import is_line_line_intersection_2d

# from intersections import line_line_intersection_2d
# from intersections import circle_circle_intersections_2d


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
