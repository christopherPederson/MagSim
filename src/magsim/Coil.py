import math
from PySide6.QtGui import QImage, QPainter, QPen, QColor, QPixmap
from PySide6.QtCore import Qt

# -- Constants Definitions -- #
EARTH_FIELD_STRENGTH = 45e-6  # Tesla 

class Coil:
    def __init__(self):
        self.length             = None # millimeters
        self.width              = None # millimeters
        self.num_loops          = None
        self.min_spacing        = None # thousands of an inch
        self.min_current        = None # Amps
        self.max_current        = None # Amps
        self.copper_thickness   = None # Oz per square foot
        self.trace_width        = None # thousands of an inch
        self.edge_clearance     = None # millimeters
        self.coil_type          = None # 'circular' or 'rectangular'
        self.overlapped         = False # True if coil traces overlap due to geometry

    def calc_magnetic_dipole_moment(self, current):

        if (self.coil_type != 'circular' and self.coil_type != 'rectangular'):
            raise ValueError("Coil type must be 'circular' or 'rectangular'")
        
        elif (self.coil_type == 'rectangular'):

            # this needs to change as it is not correct for rectangular coils
            return self.num_loops * current * (self.length * 1e-3) * (self.width * 1e-3)
        
        elif (self.coil_type == 'circular'):

            # Calculating area of archimedean spiral
            #
            # Area = pi * (Rout^2 - Rin^2)
            #
            # Rout = outer radius of coil (m)
            # Rin  = inner radius of coil (m)
            # s    = spacing between traces (m)

            Rout = 0.5*min(self.length, self.width) - self.edge_clearance*1e-3 - (self.trace_width/39_370.1)*0.5
            s    = (self.trace_width + (self.min_spacing - self.trace_width)) / 39_370.1  # if you stored spacing+width together, use pitch directly
            Rin  = max(0.0, Rout - self.num_loops * s)

            # Magnetic Dipole Moment
            #
            # mu = N * I * A
            #
            # mu = magnetic dipole moment (A*m^2)
            # N  = number of loops
            # I  = current (A)
            # A  = area of coil (m^2)

            mu   = math.pi * (Rout**2 - Rin**2) * current

            return mu
    
    def render_coil_circular(self):
        # define image size with proportional scaling based off desired reference image width
        ref_img_size = 400
        # scaling factor for px/mm (use max dimension to ensure coil fits in square)
        px_scaling = max(1, math.floor(ref_img_size / max(self.width, self.length)))
        img_size = px_scaling * max(self.width, self.length)

        # instantiate square QImage with white background
        img = QImage(img_size, img_size, QImage.Format_ARGB32)
        img.fill(Qt.white)

        # compute drawable coil dimensions (px)
        img_length = (self.length - ( 2* self.edge_clearance)) * px_scaling
        img_width = (self.width - ( 2* self.edge_clearance)) * px_scaling

        pen_width = max(1, math.floor((self.trace_width / 39.3701) * px_scaling)) # convert thousands of an inch to mm then to px, minimum 1px pen width

        painter = QPainter(img)
        painter.setRenderHint(QPainter.Antialiasing)

        # Move origin to center of square image
        painter.translate(img_size / 2.0, img_size / 2.0)

        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(pen_width)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)

        min_radius_px = min(img_length, img_width) / 2.0
        theta = 0.0
        theta_end = 2 * math.pi * self.num_loops
        # choose step so lines are reasonably smooth
        dtheta = max(1e-6, theta_end / (max(1, int(min_radius_px)) * 2 * max(1, int(self.num_loops))))

        last_x = min_radius_px
        last_y = 0.0
        x = last_x
        y = last_y

        trace_spacing_px = (self.min_spacing / 39.3701) * px_scaling
        trace_width_px = (self.trace_width / 39.3701) * px_scaling

        self.overlapped = False # reset overlapped status

        while theta <= theta_end:
            hypotenuse = (min_radius_px - ((trace_width_px + trace_spacing_px) * (theta / (2 * math.pi))))  # radius at current theta

            # check to make sure the siral does not go negative and overlap
            if hypotenuse < 0:
                self.overlapped = True
                break

            x = hypotenuse * math.cos(theta)
            y = hypotenuse * math.sin(theta)

            # draw line connecting previous point to current (coordinates centered)
            painter.drawLine(last_x, last_y, x, y)
            last_x, last_y = x, y
            theta += dtheta

        painter.end()
        return QPixmap.fromImage(img)