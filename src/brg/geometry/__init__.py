"""brg.geometry : A package defining common geometric functions and objects."""

from brg.geometry.functions import cross
from brg.geometry.functions import dot

from brg.geometry.functions import angles  # angles_vectors, angles_points, angles_lines, angles_planes
from brg.geometry.functions import angle_smallest  # angle_...
from brg.geometry.functions import length  # length_vector
from brg.geometry.functions import length_sqrd
from brg.geometry.functions import distance  # distance_point_point, distance_point_line, distance_point_plane, distance_line_line
from brg.geometry.functions import distance_sqrd
from brg.geometry.functions import area  # area_polygon, area_triangle
from brg.geometry.functions import centroid  # centroid_points
from brg.geometry.functions import center_of_mass  # center_of_mass_polygon, center_of_mass_polyhedron
from brg.geometry.functions import midpoint  # midpoint_line
from brg.geometry.functions import normal  # normal_triangle, normal_polygon
from brg.geometry.functions import normal2  # FLAG => 'perimeter', 'fitplane', 'centroid'
from brg.geometry.functions import vector_component

from brg.geometry.arithmetic import add_vectorlist  # remove
from brg.geometry.arithmetic import add_vectors  # add variable number of arguments
from brg.geometry.arithmetic import subtract_vectors  # add variable number of arguments

from brg.geometry.transformations import translate  # translate_points, translate_lines
from brg.geometry.transformations import rotate  # rotate_points (point, axis, angle)
from brg.geometry.transformations import normalize  # normalize_vectors (unitize alias)
from brg.geometry.transformations import scale  # scale_points (optional origin)
from brg.geometry.transformations import mirror  # mirror_points_point, mirror_points_plane
from brg.geometry.transformations import project  # project_points_plane, project_points_line
# from transformations import skew

# add pull_...
# add -ed variations (in-place transformations)

from brg.geometry.spatial import sort_points  # remove
from brg.geometry.spatial import closest_point  # closest_points_point, closest_points_line, closest_points_plane
from brg.geometry.spatial import closest_point_on_line
from brg.geometry.spatial import closest_point_on_segment
from brg.geometry.spatial import closest_point_on_polyline
from brg.geometry.spatial import closest_point_on_plane

# FLAG: return_index
# add closest_ppoint_on_polygon

from brg.geometry.queries import is_colinear
from brg.geometry.queries import is_coplanar
from brg.geometry.queries import is_coplanar4
# from queries import is_convex
from brg.geometry.queries import is_closed  # remove
from brg.geometry.queries import is_point_on_plane
from brg.geometry.queries import is_point_on_line
from brg.geometry.queries import is_closest_point_on_segment  # is_point_on_segment
from brg.geometry.queries import is_point_on_segment
from brg.geometry.queries import is_point_on_polyline

# from queries import is_ray_intersecting_triangle
# from queries import is_line_line_intersection_2d

# from intersections import line_line_intersection_2d
# from intersections import circle_circle_intersections_2d


docs = [
	{'elements'        : []},
	{'shapes'          : []},
    {'arithmetic'      : ['add_vectors', 'subtract_vectors', ]},
    {'functions'       : ['angles', 'angle_smallest', 'length', 'length_sqrd', 'distance', 'distance_sqrd', 'area', 'centroid', 'center_of_mass', 'midpoint', 'normal', 'vector_component', ]},
    {'intersections'   : ['line_line_intersection', 'line_line_intersection_2d', 'lines_intersection', 'lines_intersection_2d', 'circle_circle_intersections', 'circle_circle_intersections_2d', ]},
    {'planar'          : ['is_ccw', 'is_convex', 'is_intersecting', 'is_selfintersecting', 'is_point_in_polygon', 'is_point_in_triangle', 'closest_part_of_triangle', ]},
    {'queries'         : ['is_colinear', 'is_coplanar', 'is_coplanar4', 'is_point_on_plane', 'is_point_on_line', 'is_point_on_segment', 'is_point_on_polyline', ]},
    {'spatial'         : ['sort_points', 'closest_point', 'closest_point_on_line', 'closest_point_on_segment', 'closest_point_on_polyline', 'closest_point_on_plane', ]},
    {'transformations' : ['translate', 'rotate', 'normalize', 'scale', 'mirror', 'project', ]},
    {'utilities'       : []}
]
