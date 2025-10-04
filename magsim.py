import sys
import math

from Coil import Coil
from TourqueSimulation import TorqueSimulation
from TrippleAxisSimulation import TripleAxisSimulation

from PySide6.QtCore import Qt
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

        # Parameter inputs: two columns (labels | line edits)
        params_layout = QHBoxLayout()
        label_column = QVBoxLayout()
        line_column = QVBoxLayout()
        params_layout.addLayout(label_column)
        params_layout.addLayout(line_column)
        params_layout.setSpacing(12)
        label_column.setSpacing(6)
        line_column.setSpacing(6)

        # helper to add a labelled field with matching widths
        def add_param(label_text, widget, fixed_width=220):
            lbl = QLabel(label_text)
            lbl.setFixedWidth(fixed_width)
            widget.setFixedWidth(fixed_width)
            label_column.addWidget(lbl)
            line_column.addWidget(widget)
            return lbl, widget

        # create fields and add them to the two columns
        self.coil_length = QLineEdit()
        add_param("Coil Length (mm):", self.coil_length)

        self.coil_width = QLineEdit()
        add_param("Coil Width (mm):", self.coil_width)

        self.coil_current = QLineEdit()
        add_param("Coil current (A):", self.coil_current)

        self.vector_angle = QLineEdit()
        add_param("Vector Angle (°):", self.vector_angle)

        self.num_loops = QLineEdit()
        add_param("Number of Loops:", self.num_loops)

        self.min_spacing = QLineEdit()
        add_param("Minimum Trace Clearance (thousands of an inch):", self.min_spacing)

        self.trace_width = QLineEdit()
        add_param("Trace Width (thousands of an inch):", self.trace_width)

        self.edge_clearance = QLineEdit()
        add_param("Edge Clearance (mm):", self.edge_clearance)

        layout.addLayout(params_layout)

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
        self.coil.length            = float(self.coil_length.text())
        self.coil.width             = float(self.coil_width.text())
        self.coil.num_loops         = float(self.num_loops.text())
        self.coil.min_spacing       = float(self.min_spacing.text()) + max(1,float(self.trace_width.text())) # Trace clearance muyst consider trace width
        self.coil.trace_width       = float(self.trace_width.text())
        self.coil.edge_clearance    = float(self.edge_clearance.text())

        # Render coil image
        pixmap = self.coil.render_coil_circular()
        self.preview.setPixmap(pixmap.scaled(self.preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


window = MainWindow()
window.show()

app.exec()