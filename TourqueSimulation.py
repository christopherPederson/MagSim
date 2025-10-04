import math
from PySide6.QtCore import Qt

# -- Constants Definitions -- #
EARTH_FIELD_STRENGTH = 45e-6  # Tesla 

class TorqueSimulation():
    def __init__(self, coil):
        self.coil = coil                # Coil object

    def calc_torque(self, current, angle):
        return self.coil.calc_magnetic_dipole_moment(current) * EARTH_FIELD_STRENGTH * math.sin(math.radians(angle))
