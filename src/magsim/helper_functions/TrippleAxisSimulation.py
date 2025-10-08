import math
from .FieldLib import get_B_field

# -- Constants Definitions -- #
EARTH_FIELD_STRENGTH = get_B_field()

class TripleAxisSimulation():
    def __init__(self, coil_x, coil_y, coil_z):
        self.coil_x = coil_x              # Coil object
        self.coil_y = coil_y              # Coil object
        self.coil_z = coil_z              # Coil object

    def calc_torque(self, current_x, current_y, current_z, angle_x, angle_y, angle_z):
        torque_x = self.coil_x.calc_magnetic_dipole_moment(current_x) * EARTH_FIELD_STRENGTH * math.sin(math.radians(angle_x))
        torque_y = self.coil_y.calc_magnetic_dipole_moment(current_y) * EARTH_FIELD_STRENGTH * math.sin(math.radians(angle_y))
        torque_z = self.coil_z.calc_magnetic_dipole_moment(current_z) * EARTH_FIELD_STRENGTH * math.sin(math.radians(angle_z))
        
        return (torque_x, torque_y, torque_z)