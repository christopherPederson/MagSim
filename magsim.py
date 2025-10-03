import sys
import math

from PySide6.QtGui import QImage, QPainter, QPen, QColor, QPixmap
from PySide6.QtCore import QSize, Qt, QRectF
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget
)

# -- GUI Definitions -- #
app = QApplication(sys.argv)

# -- Constants Definitions -- #
EARTH_FIELD_STRENGTH = 45e-6  # Tesla

class Coil:
    def __init__(self):
        self.length = None             # millimeters
        self.width = None              # millimeters
        self.num_loops = None
        self.min_spacing = None        # thousands of an inch
        self.min_current = None        # Amps
        self.max_current = None        # Amps
        self.copper_thickness = None   # Oz per square foot
        self.trace_width = None        # thousands of an inch
        self.edge_clearance = None     # millimeters

    def calc_magnetic_dipole_moment(self, current):
        return self.num_loops * current * (self.length * 1e-3) * (self.width * 1e-3)
    
    def render_coil(self):

        # define image size with porportional scaling based off desired 600px reference image width
        ref_img_x_size = 300
        # scaling factor for px/mm
        px_scaling = math.floor(ref_img_x_size / self.width)
        img_x_size = px_scaling * self.width
        img_y_size = px_scaling * self.length

        # instanciate QImage object
        img = QImage(img_x_size, img_y_size, QImage.Format_ARGB32)
        img.fill(Qt.white)

        img_length = (self.length - self.edge_clearance) * px_scaling
        img_width = (self.width - self.edge_clearance) * px_scaling

        pen_width = max(1, math.floor((self.trace_width / 39.3701) * px_scaling)) # convert thousands of an inch to mm then to px, minimum 1px pen width

        painter = QPainter(img)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(img_x_size / 2, img_y_size / 2)  # Move origin to center of image

        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(pen_width)
        pen.setCapStyle(Qt.FlatCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)

        pitch_px = (self.min_spacing / 39.3701) * px_scaling
        inset0   = pen_width / 2.0  # so the stroke isn’t clipped

        for k in range(int(self.num_loops)):
            x = inset0 + k * pitch_px
            y = inset0 + k * pitch_px
            w = img_length - 2*x
            h = img_width - 2*y
            if w <= 0 or h <= 0:
                break
            # Center the rectangle at (0, 0)
            painter.drawRect(QRectF(-w/2, -h/2, w, h))

        painter.end()
        return QPixmap.fromImage(img)



class TorqueSimulation:
    def __init__(self, coil):
        self.coil = coil                # Coil object

    def calc_torque(self, current, angle):
        return self.coil.calc_magnetic_dipole_moment(current) * EARTH_FIELD_STRENGTH * math.sin(math.radians(angle))
    
class TripleAxisSimulation:
    def __init__(self, coil_x, coil_y, coil_z):
        self.coil_x = coil_x              # Coil object
        self.coil_y = coil_y              # Coil object
        self.coil_z = coil_z              # Coil object

    def calc_torque(self, current_x, current_y, current_z, angle_x, angle_y, angle_z):
        torque_x = self.coil_x.calc_magnetic_dipole_moment(current_x) * EARTH_FIELD_STRENGTH * math.sin(math.radians(angle_x))
        torque_y = self.coil_y.calc_magnetic_dipole_moment(current_y) * EARTH_FIELD_STRENGTH * math.sin(math.radians(angle_y))
        torque_z = self.coil_z.calc_magnetic_dipole_moment(current_z) * EARTH_FIELD_STRENGTH * math.sin(math.radians(angle_z))
        return (torque_x, torque_y, torque_z)

class MainWindow(QMainWindow):
    def __init__(self):                         # Constructor on the MainWindow class
        super().__init__()                      # super() is used to call the constructor of any parent classes

        # Define coil for simulation
        self.coil = Coil()
        self.inst_tourque = 0.0

        # Setup the main window
        self.setWindowTitle("MagSim.py")        # sets the window title of the class instance
        self.setCentralWidget(QWidget())        # sets the central widget of the window to a basic QWidget instance

        # -- Define GUI Layout -- #
        layout = QVBoxLayout()                  # Create a vertical box layout

        # Coil Image Display
        self.preview = QLabel()
        self.preview.setFixedSize(350, 350)
        self.preview.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.preview)

        # Generate Coil Image Button
        self.gen_coil_button = QPushButton("Generate Coil Image")
        layout.addWidget(self.gen_coil_button)

        self.gen_coil_button.clicked.connect(self.update_coil_image)

        # Coil Length row
        length_row = QHBoxLayout()
        length_label = QLabel("Coil Length (mm):")
        self.coil_length = QLineEdit()
        length_row.addWidget(length_label)
        length_row.addWidget(self.coil_length)
        layout.addLayout(length_row)

        # Coil Width row
        width_row = QHBoxLayout()
        width_label = QLabel("Coil Width (mm):")
        self.coil_width = QLineEdit()
        width_row.addWidget(width_label)
        width_row.addWidget(self.coil_width)
        layout.addLayout(width_row)

        # Current Input row
        current_row = QHBoxLayout()
        current_label = QLabel("Coil current (A):")
        self.coil_current = QLineEdit()
        current_row.addWidget(current_label)
        current_row.addWidget(self.coil_current)
        layout.addLayout(current_row)

        # Vector angle row
        angle_row = QHBoxLayout()
        angle_label = QLabel("Vector Angle (°):")
        self.vector_angle = QLineEdit()
        angle_row.addWidget(angle_label)
        angle_row.addWidget(self.vector_angle)
        layout.addLayout(angle_row)

        # Nunmber of Loops row
        loops_row = QHBoxLayout()
        loops_label = QLabel("Number of Loops:")
        self.num_loops = QLineEdit()
        loops_row.addWidget(loops_label)
        loops_row.addWidget(self.num_loops)
        layout.addLayout(loops_row)

        # Calculate Button
        self.button = QPushButton("Calculate Instantaneous Torque")
        layout.addWidget(self.button)

        # Instantaneous Torque Display
        inst_torque_row = QHBoxLayout()
        inst_torque_label = QLabel(f"Instantaneous Torque (Nm):")
        self.inst_torque_display = QLineEdit()
        self.inst_torque_display.setReadOnly(True)
        inst_torque_row.addWidget(inst_torque_label)
        inst_torque_row.addWidget(self.inst_torque_display)
        layout.addLayout(inst_torque_row)

        self.button.clicked.connect(self.calculate_torque)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        # -- Define GUI Layout -- #

    def calculate_torque(self):
        # Get user inputs
        self.coil.length    = float(self.coil_length.text())
        self.coil.width     = float(self.coil_width.text())
        self.coil.num_loops = float(self.num_loops.text())
        current             = float(self.coil_current.text())
        angle               = float(self.vector_angle.text())

        # Perform torque calculation
        simulation          = TorqueSimulation(self.coil)
        self.inst_tourque   = simulation.calc_torque(current, angle)

        # Update display
        self.inst_torque_display.setText(f"{self.inst_tourque:.8g}")

    def update_coil_image(self):
        # Get user inputs
        self.coil.length    = float(self.coil_length.text())
        self.coil.width     = float(self.coil_width.text())
        self.coil.num_loops = float(self.num_loops.text())
        self.coil.min_spacing = 50.0          # default 10 thousands of an inch
        self.coil.trace_width = 10.0           # default 10 thousands of an inch
        self.coil.edge_clearance = 2.0         # default 2 mm

        # Render coil image
        pixmap = self.coil.render_coil()
        self.preview.setPixmap(pixmap.scaled(self.preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


window = MainWindow()
window.show()

app.exec()