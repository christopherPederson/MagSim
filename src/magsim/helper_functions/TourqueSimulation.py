import math
from .FieldLib import get_B_field

# -- Constants Definitions -- #
EARTH_FIELD_STRENGTH = get_B_field()
_SIN_EPS = 1e-12                        # tolerance for “should be zero” angles

def _sin_deg(angle_deg):
    # normalize to [0, 360)
    s = math.sin(math.radians(angle_deg % 360.0))
    return 0.0 if abs(s) < _SIN_EPS else s

class TorqueSimulation():
    def __init__(self, coil):
        self.coil = coil                # Coil object

    def calc_torque(self, current, angle):
        return self.coil.calc_magnetic_dipole_moment(current) * EARTH_FIELD_STRENGTH * _sin_deg(angle)
