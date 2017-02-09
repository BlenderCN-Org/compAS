.. _meshmodeling:

********************************************************************************
Mesh modeling in Rhino
********************************************************************************

The following examples show various meshing, smoothing and remeshing functions. 
All examples in this section are based on the following Rhino model
:download:`geometry.3dm </_downloads/geometry_tests.3dm>`.


.. contents::


Delaunay Triangulation A
------------------------

.. code-block:: python

    # **************************************************************************
    # computes the delaunay triangulation for given set of points in rhino
    # **************************************************************************

    import rhinoscriptsyntax as rs
    from brg.datastructures.mesh.algorithms.triangulation import delaunay_from_points

    objs = rs.GetObjects("Select Points",1)
    pts = [rs.PointCoordinates(obj) for obj in objs]

    faces = delaunay_from_points(pts)
    rs.AddMesh(pts,faces)

.. image:: /_images/delaunay_01.*

.. important::
    
    This delaunay triangulation algorithm works in the xy-plane. However, the 
    input can be 3d points resulting in a 2.5d heightfield mesh.

Delaunay Triangulation B
------------------------

A plain delaunay triangulation will always form a convex boundary and a continuous 
mesh without 'holes'. The following code shows how to include specific boundaries. 

.. code-block:: python

    # **************************************************************************
    # computes the delaunay triangulation for given set of points and
    # polygons to define boundaries in rhino
    # **************************************************************************

    import rhinoscriptsyntax as rs
    from brg.datastructures.mesh.algorithms.triangulation import delaunay_from_points
    from brg.datastructures.mesh import Mesh
    import brg_rhino
    
    objs = rs.GetObjects("Select Points",1)
    pts = [rs.PointCoordinates(obj) for obj in objs]
    
    poly = rs.GetObject("Select polygon bondary",4)
    boundary_polyline = []
    if poly:
        boundary_polyline = rs.CurveEditPoints(poly)
    
    polys = rs.GetObjects("Select polygon holes",4)
    holes_polylines = []
    if polys:
        for poly in polys:
            holes_polylines.append(rs.CurveEditPoints(poly))
    faces = delaunay_from_points(pts,boundary_polyline,holes_polylines)
    
    mesh = Mesh()
    mesh = mesh.from_vertices_and_faces(pts,faces)
    brg_rhino.draw_mesh(mesh)
 
.. image:: /_images/delaunay_02.*

.. seealso::

    * :func:`brg.datastructures.mesh.algorithms.triangulation.delaunay_from_points`
    * Sloan, S. W. (1987) A fast algorithm for constructing Delaunay triangulations in the plane
    
Delaunay Triangulation Exercise
----------------------------------

Create a Voronoi mesh based on the given Delaunay mesh.

.. seealso::

    * :func:`brg.geometry.planar.circle_from_points_2d`
    * :func:`brg.datastructures.algorithms.construct_dual_mesh`
    

    
Mesh Smoothing A
----------------
    
.. code-block:: python

    # **************************************************************************
    # smoothening (relaxation) with fixed boundary points of a 
    # given input mesh in rhino
    # **************************************************************************
    
    import rhinoscriptsyntax as rs

    from brg.datastructures.mesh import Mesh
    from brg.datastructures.mesh.algorithms import smooth_mesh_centroid
    from brg.datastructures.mesh.algorithms import smooth_mesh_area

    import brg_rhino

    
    obj = rs.GetObject("Select Mesh",32)
    mesh = brg_rhino.mesh_from_guid(Mesh,obj)
    
    # get all indices of fixed points along the boundaries
    fixed = mesh.vertices_on_boundary()
    
    smooth_mesh_area(mesh,fixed,kmax=100)
    #smooth_mesh_centroid(mesh,fixed,kmax=100)
    brg_rhino.draw_mesh(mesh)   
    

.. image:: /_images/smoothing_01.*


Mesh Smoothing B
----------------

.. code-block:: python

    # **************************************************************************
    # smoothening (relaxation) with fixed boundary points of a 
    # given input mesh in rhino
    # using a user function (ufunc) and MeshConduit for visualization
    # **************************************************************************
    
    import rhinoscriptsyntax as rs

    from brg.datastructures.mesh import Mesh
    from brg.datastructures.mesh.algorithms import smooth_mesh_centroid
    from brg.datastructures.mesh.algorithms import smooth_mesh_area

    import brg_rhino
    from brg_rhino.conduits.mesh import MeshConduit
    

    def wrapper(conduit, vis):
        def ufunc(mesh,i):
            if i%vis==0:
                rs.Prompt("Iteration {0}".format(i))
                conduit.redraw()
        return ufunc

    
    obj = rs.GetObject("Select Mesh",32)
    mesh = brg_rhino.mesh_from_guid(Mesh,obj)
    
    # get all indices of fixed points along the boundaries
    fixed = mesh.vertices_on_boundary()
    
    conduit = MeshConduit(mesh)
    conduit.Enabled = True
    ufunc = wrapper(conduit, vis=2)
    
    keys = ['161','256']
    for key in keys:
        mesh.vertex[key]['z'] -= 20
        fixed.add(key)  
    
    try:
        smooth_mesh_area(mesh, fixed, kmax=100, ufunc=ufunc)
        #smooth_mesh_centroid(mesh, fixed, kmax=150, ufunc=ufunc)
    except Exception as e:
        print e
    else:
        brg_rhino.draw_mesh(mesh)
    
    finally:
        conduit.Enabled = False
        del conduit


.. image:: /_images/smoothing_02.*


Mesh Smoothing C
----------------
    
.. code-block:: python  

    # **************************************************************************
    # smoothening (relaxation) of a given input mesh in rhino on a target 
    # surface with fixed boundary points
    # using a user function (ufunc) to constrain the points to the target 
    # surface and MeshConduit for visualization
    # **************************************************************************
    
    import rhinoscriptsyntax as rs

    from brg.datastructures.mesh.algorithms.triangulation import delaunay_from_points
    from brg.datastructures.mesh import Mesh
    from brg.datastructures.mesh.algorithms import smooth_mesh_centroid
    from brg.datastructures.mesh.algorithms import smooth_mesh_area

    import brg_rhino
    from brg_rhino.conduits.mesh import MeshConduit
    

    def wrapper(conduit, vis):
        def ufunc(mesh,i):
            for key, a in mesh.vertices_iter(True):
               if a['guide_srf']:
                   pt = (a['x'], a['y'], a['z'])
                   point = rs.coerce3dpoint(pt)
                   pt = a['guide_srf'].ClosestPoint(point)
                   mesh.vertex[key]['x'] = pt[0]
                   mesh.vertex[key]['y'] = pt[1]
                   mesh.vertex[key]['z'] = pt[2] 
            if i%vis==0:
                rs.Prompt("Iteration {0}".format(i))
                conduit.redraw()
        return ufunc
    

    obj = rs.GetObject("Select Mesh",32)
    
    mesh = brg_rhino.mesh_from_guid(Mesh, obj)
    mesh.set_dva({'guide_srf': None})
    
    fixed = mesh.vertices_on_boundary()
    
    srf = rs.GetObject("Select Guide Surface",8)
    srf_id = rs.coerceguid(srf, True)
    brep = rs.coercebrep(srf_id, False)
    
    for key in mesh.vertices():
        if key not in fixed:
            mesh.vertex[key]['guide_srf'] = brep
        
    conduit = MeshConduit(mesh)
    conduit.Enabled = True
    ufunc = wrapper(conduit, vis=1)
    
    try:
        #smooth_mesh_area(mesh, fixed, kmax=100, ufunc=ufunc)
        smooth_mesh_centroid(mesh,fixed, kmax=100, ufunc=ufunc)
    except Exception as e:
        print e
    else:
        brg_rhino.draw_mesh(mesh)
    
    finally:
        conduit.Enabled = False
        del conduit
    

.. image:: /_images/smoothing_02.*
    

.. seealso::

    * :func:`brg.datastructures.mesh.algorithms.smooth_mesh_centroid`
    * :func:`brg.datastructures.mesh.algorithms.smooth_mesh_centerofmass`
    * :func:`brg.datastructures.mesh.algorithms.smooth_mesh_length`
    * :func:`brg.datastructures.mesh.algorithms.smooth_mesh_area` 
    * :func:`brg.datastructures.mesh.algorithms.smooth_mesh_angle` 
    * :mod:`brg_rhino.conduits.mesh`    


Smoothing Exercise
-------------------

Use a color gradient to visualize the edge length (optional: face area) variation 
of relaxed meshes. Analyse and compare meshes resulting from different smoothing
algorithms. 
 

.. seealso::

    * :mod:`brg.utilities.colors` 


Mesh from Boundary
------------------

.. code-block:: python  

    # **************************************************************************
    # creates a triangulated mesh from a given boundary curve and a edge 
    # target length
    # **************************************************************************
    
    import rhinoscriptsyntax as rs

    from brg.datastructures.mesh.algorithms.triangulation import delaunay_from_points
    from brg.datastructures.mesh import Mesh
    from brg.datastructures.mesh.algorithms import optimise_trimesh_topology

    import brg_rhino
    from brg_rhino.conduits.mesh import MeshConduit
    
    
    def wrapper(conduit, vis):
        def ufunc(mesh,i):
            if i%vis==0:
                rs.Prompt("Iteration {0}".format(i))
                conduit.redraw()
        return ufunc
    

    crv = rs.GetObject("Select Boundary Curve",4)
    trg = rs.GetReal("Select Edge Target Length",2.5)
    
    pts = rs.DivideCurve(crv,rs.CurveLength(crv)/trg)
    
    faces = delaunay_from_points(pts,pts)
    mesh = Mesh.from_vertices_and_faces(pts,faces)
    
    conduit = MeshConduit(mesh)
    conduit.Enabled = True
    ufunc = wrapper(conduit, vis=1)
    
    try:
        optimise_trimesh_topology(mesh,trg,kmax=250,ufunc=ufunc)
    except Exception as e:
        print e
    else:
        brg_rhino.draw_mesh(mesh)
    
    finally:
        conduit.Enabled = False
        del conduit
    
    
.. image:: /_images/mesh_from_boundary.*


.. seealso::

    * :func:`brg.datastructures.mesh.algorithms.optimise_trimesh_topology`
    * Botsch M. and Kobbelt L. (2004) A Remeshing Approach to Multiresolution Modeling
    
    
Remeshing Exercise
-------------------

Let the user select edges to be swapped (optional: collapsed) in a triangular mesh. 
 

.. seealso::

    * :mod:`brg.datastructures.mesh.operations` 

