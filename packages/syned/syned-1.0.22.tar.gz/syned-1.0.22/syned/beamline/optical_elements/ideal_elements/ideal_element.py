
from syned.beamline.optical_element import OpticalElement
from syned.beamline.shape import BoundaryShape

class IdealElement(OpticalElement):
    def __init__(self, name="Undefined", boundary_shape=BoundaryShape()):
        OpticalElement.__init__(self, name=name, boundary_shape=boundary_shape)