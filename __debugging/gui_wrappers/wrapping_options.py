import brg

from brg.datastructures.mesh import Mesh

from brg_rhino.datastructures.mixins import DrawMixin
from brg_rhino.datastructures.mixins import EditAttributesMixin
from brg_rhino.datastructures.mixins import DisplayLabelsMixin
from brg_rhino.datastructures.mixins import SelectComponentsMixin


class Mesh(DrawMixin,
           EditAttributesMixin,
           DisplayLabelsMixin,
           SelectComponentsMixin,
           Mesh):
    pass


mesh = Mesh.from_obj(brg.find_resource('faces.obj'))

mesh.draw()
