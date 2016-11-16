__author__     = ['Matthias Rippmann <rippmann@ethz.ch>', ]
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Nov 11, 2016'


import time
import rhinoscriptsyntax as rs  
import math
from brg_rhino.datastructures.mesh import RhinoMesh
from brg_rhino.conduits.lines import LinesConduit
import brg_rhino.utilities as rhino

import subdivision_uf
from brg.datastructures.mesh.operations.split import split_edge
from brg.datastructures.mesh.algorithms.orientation import mesh_unify_cycle_directions





