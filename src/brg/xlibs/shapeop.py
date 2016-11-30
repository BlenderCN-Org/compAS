"""Wrapper for the ShapeOp library."""

import sys

sys.path.insert(0, "/Users/vanmelet/bitbucket/brg_framework/libs/ShapeOp.0.1.0/build/libShapeOp/bindings/python")

import shapeopPython


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


def planarize_mesh_faces(mesh):
    key_index = mesh.key_index()
    vcount = len(mesh)
    points = shapeopPython.doubleArray(3 * vcount)
    for i, (key, attr) in mesh.vertices_enum(True):
        i *= 3
        points[i]   = attr['x']
        points[i+1] = attr['y']
        points[i+2] = attr['z']
    solver = shapeopPython.shapeop_create()
    shapeopPython.shapeop_setPoints(solver, points, vcount)
    # add a plane constraint to all faces
    for fkey in mesh.face:
        vertices = mesh.face_vertices(fkey, ordered=True)
        v = len(vertices)
        indices = shapeopPython.intArray(v)
        for i in range(v):
            key = vertices[i]
            indices[i] = key_index[key]
        shapeopPython.shapeop_addConstraint(solver, 'Plane', indices, v, 0.5)
    # add a closeness constraint to the fixed vertices
    anchors = [key_index[key] for key in mesh if mesh.vertex_degree(key) == 2]
    for a in anchors:
        indices = shapeopPython.intArray(1)
        indices[0] = a
        shapeopPython.shapeop_addConstraint(solver, 'Closeness', indices, 1, 1.0)
    # add a mild closeness constraint to the boundaries and other vertices
    for key in mesh:
        if mesh.is_vertex_on_boundary(key):
            indices = shapeopPython.intArray(1)
            indices[0] = key_index[key]
            shapeopPython.shapeop_addConstraint(solver, 'Closeness', indices, 1, 0.5)
        else:
            indices = shapeopPython.intArray(1)
            indices[0] = key_index[key]
            shapeopPython.shapeop_addConstraint(solver, 'Closeness', indices, 1, 0.1)
    # solve
    shapeopPython.shapeop_init(solver)
    shapeopPython.shapeop_solve(solver, 500)
    shapeopPython.shapeop_getPoints(solver, points, vcount)
    shapeopPython.shapeop_delete(solver)
    # update
    for i, (key, attr) in mesh.vertices_enum(True):
        i *= 3
        attr['x'] = points[i]
        attr['y'] = points[i + 1]
        attr['z'] = points[i + 2]


def circularize_mesh_faces(mesh):
    key_index = mesh.key_index()
    vcount = len(mesh)
    points = shapeopPython.doubleArray(3 * vcount)
    for i, (key, attr) in mesh.vertices_enum(True):
        i *= 3
        points[i]   = attr['x']
        points[i+1] = attr['y']
        points[i+2] = attr['z']
    solver = shapeopPython.shapeop_create()
    shapeopPython.shapeop_setPoints(solver, points, vcount)
    for fkey in mesh.face:
        vertices = mesh.face_vertices(fkey, ordered=True)
        v = len(vertices)
        indices = shapeopPython.intArray(v)
        for i in range(v):
            key = vertices[i]
            index = key_index[key]
            indices[i] = index
        shapeopPython.shapeop_addConstraint(solver, 'Circle', indices, v, 0.5)
    # add closeness constraint to anchors
    anchors = [key_index[key] for key in mesh if mesh.vertex_degree(key) == 2]
    for a in anchors:
        indices = shapeopPython.intArray(1)
        indices[0] = a
        shapeopPython.shapeop_addConstraint(solver, 'Closeness', indices, 1, 1.0)
    # add a mild closeness constraint to the boundaries and other vertices
    for key in mesh:
        if mesh.is_vertex_on_boundary(key):
            indices = shapeopPython.intArray(1)
            indices[0] = key_index[key]
            shapeopPython.shapeop_addConstraint(solver, 'Closeness', indices, 1, 0.25)
        else:
            indices = shapeopPython.intArray(1)
            indices[0] = key_index[key]
            shapeopPython.shapeop_addConstraint(solver, 'Closeness', indices, 1, 0.1)
    # solve
    shapeopPython.shapeop_init(solver)
    shapeopPython.shapeop_solve(solver, 1000)
    shapeopPython.shapeop_getPoints(solver, points, vcount)
    shapeopPython.shapeop_delete(solver)
    # update
    for i, (key, attr) in mesh.vertices_enum(True):
        i *= 3
        attr['x'] = points[i]
        attr['y'] = points[i + 1]
        attr['z'] = points[i + 2]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    
    import brg

    from brg.datastructures.mesh.mesh import Mesh
    from brg.datastructures.mesh.viewer import MultiMeshViewer
    from brg.datastructures.mesh.numerical.methods import mesh_fd
    
    mesh = Mesh.from_obj(brg.find_resource('faces.obj'))

    mesh.set_dva({'is_anchor': False, 'pz': -0.5})
    mesh.set_dea({'q': 1.0})

    for key in mesh:
        mesh.vertex[key]['is_anchor'] = mesh.vertex_degree(key) == 2

    mesh_fd(mesh)    
    
    p_mesh = mesh.copy()
    c_mesh = p_mesh.copy()

    # meshes = [mesh, p_mesh, c_mesh]
    meshes = [c_mesh]
    
    # planarize_mesh_faces(p_mesh)
    circularize_mesh_faces(c_mesh)

    # colors = [(1.0, 0.5, 0.5, 1.0), (0.5, 1.0, 0.5, 1.0), (0.5, 0.5, 1.0, 1.0)]
    # colors = [(1.0, 0.5, 0.5, 1.0), (0.5, 0.5, 1.0, 1.0)]
    colors = [(1.0, 0.5, 0.5, 1.0)]
    
    viewer = MultiMeshViewer(meshes, colors, 800, 600)
    viewer.grid_on = False
    viewer.setup()
    viewer.show()
