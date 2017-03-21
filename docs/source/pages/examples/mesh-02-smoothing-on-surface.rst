.. _examples_mesh-smoothing-on-surface:

********************************************************************************
Mesh smoothing on surface
********************************************************************************

.. raw:: html
    
    <div class="video-wrapper">
        <video width="100%" height="auto" controls>
            <source src="../../_videos/mesh-modeling-relaxation.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>


:download:`geometry.3dm </_downloads/geometry_tests.3dm>`

.. literalinclude:: /../../examples/mesh-smoothing-on-surface.py

.. seealso::

    * :func:`brg.datastructures.mesh.algorithms.smooth_mesh_centroid`
    * :func:`brg.datastructures.mesh.algorithms.smooth_mesh_centerofmass`
    * :func:`brg.datastructures.mesh.algorithms.smooth_mesh_length`
    * :func:`brg.datastructures.mesh.algorithms.smooth_mesh_area` 
    * :func:`brg.datastructures.mesh.algorithms.smooth_mesh_angle` 
    * :mod:`brg_rhino.conduits.mesh`    
