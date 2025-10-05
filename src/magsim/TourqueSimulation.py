import math
from .FieldLib import get_B_field

# -- Constants Definitions -- #
EARTH_FIELD_STRENGTH = get_B_field()

class TorqueSimulation():
    def __init__(self, coil):
        self.coil = coil                # Coil object

    def calc_torque(self, current, angle):
        return self.coil.calc_magnetic_dipole_moment(current) * EARTH_FIELD_STRENGTH * math.sin(math.radians(angle))
