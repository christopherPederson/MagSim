from PySide6.QtGui import QPalette
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
    QScrollArea,
)

from ..obj_elements.Coil import Coil



class PCBWindow(QWidget):

    def add_param(self, label_text, widget):
        lbl = QLabel(label_text)
        self.label_column.addWidget(lbl)
        self.line_column.addWidget(widget)

    def refresh_coil_display(self, display: QLabel):
        # update the coil display based on the selected layer
        index = self.current_layer.currentIndex()
        if self.layer_array[index] == Coil:
            self.update_coil_image()

    def update_coil_image(self):
        # Get user inputs
        coil_obj = self.layer_array[self.current_layer.currentIndex()]

        coil_obj.length                = float(self.coil_length.text())
        coil_obj.width                 = float(self.coil_width.text())  
        coil_obj.num_loops             = int(self.num_loops.text())
        coil_obj.min_spacing           = float(self.min_spacing.text())
        coil_obj.trace_width_min      = float(self.trace_width_min.text())
        coil_obj.trace_width_max      = float(self.trace_width_max.text())
        coil_obj.edge_clearance        = float(self.edge_clearance.text())
        coil_obj.coil_shape            = self.coil_shape.currentText().lower()

        # Render coil image
        pixmap = coil_obj.render_coil_circular()

        if coil_obj.overlapped:
            self.coil_display.setText("Error: Coil traces overlap due to geometry.\nPlease adjust parameters.")
        else:
            self.coil_display.setPixmap(pixmap.scaled(self.coil_display.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    
    def refresh_coil_layer_combo(self):
        # repopulate the combobox 
        self.current_layer.clear()
        for i in range(len(self.layer_array)):
            if self.layer_array[i] != 'Select':
                if isinstance(self.layer_array[i], Coil):
                    text = "Coil"
                else:
                    text = self.layer_array[i]
                self.current_layer.addItem(f"Layer {i+1} — {text}")
        if self.layer_array:
            self.current_layer.setCurrentIndex(0)

    def handle_add_layer(self, index, raw_text):

        if raw_text == 'Coil':
            self.layer_array[index] = Coil()
        else:
            self.layer_array[index] = raw_text
        self.refresh_coil_layer_combo()

    def add_layer(self, view, layer_num: int):

        self.layer_count += 1

        layer_index = len(self.layer_array)
        self.layer_array.append('Select')  # placeholder; hidden until chosen

        layer_widget = QWidget()
        layer_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layer = QHBoxLayout(layer_widget)

        layer_label = QLabel(f'Layer {layer_num}')
        layer_type = QComboBox()
        layer_type.addItems(['Select','Coil', 'Ground', 'Signal'])

        layer_type.currentTextChanged.connect(
            lambda text, i=layer_index: self.handle_add_layer(i, text)
        )

        layer_thickness = QLineEdit()
        layer_thickness.setPlaceholderText("Copper Thickness (Oz)")

        layer.addWidget(layer_label)
        layer.addWidget(layer_type)
        layer.addWidget(layer_thickness)

        view.addWidget(layer_widget)
        self.refresh_coil_layer_combo()

    def config_stack_view(self, view):
        view_label = QLabel("PCB Stack View")
        view.addWidget(view_label)

        add_layer_btn = QPushButton("+ Add Layer")
        add_layer_btn.clicked.connect(lambda: self.add_layer(view, self.layer_count))
        view.addWidget(add_layer_btn)
        
        self.add_layer(view, self.layer_count)

    def config_coil_view(self, view):
        view_label = QLabel("Layer Preview")
        view.addWidget(view_label)

        self.param_columns = QHBoxLayout()
        self.label_column = QVBoxLayout()
        self.line_column = QVBoxLayout()

        self.param_columns.addLayout(self.label_column)
        self.param_columns.addLayout(self.line_column)

        self.current_layer.setCurrentIndex(0)

        # create fields and add them to the two columns
        self.coil_length = QLineEdit()
        self.add_param("Coil Length (mm):", self.coil_length)

        self.coil_width = QLineEdit()
        self.add_param("Coil Width (mm):", self.coil_width)

        self.num_loops = QLineEdit()
        self.add_param("Number of Loops:", self.num_loops)

        self.coil_current = QLineEdit()
        self.add_param("Coil current (A):", self.coil_current)

        self.vector_angle = QLineEdit()
        self.add_param("Vector Angle (°):", self.vector_angle)

        self.min_spacing = QLineEdit()
        self.add_param("Trace Clearance (mil):", self.min_spacing)

        self.trace_width_min = QLineEdit()
        self.add_param("Trace Width Minimum (mil):", self.trace_width_min)

        self.trace_width_max = QLineEdit()
        self.add_param("Trace Width Maximum (mil):", self.trace_width_max)

        self.edge_clearance = QLineEdit()
        self.add_param("Edge Clearance (mm):", self.edge_clearance)

        self.coil_shape = QComboBox()
        self.coil_shape.addItems(["Circular", "Rectangular"])
        self.add_param("Coil Shape:", self.coil_shape)

        view.addWidget(self.current_layer)
        view.addLayout(self.param_columns)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.layer_count = 1 # Keep track of the number of layers, minimum is 1
        self.layer_array = []
        
        layout = QHBoxLayout(self)

        stack_view_widget = QWidget()
        stack_view = QVBoxLayout(stack_view_widget)
        stack_view_widget.setObjectName("stack_view")

        coil_display_widget = QWidget()
        coil_display_widget.setObjectName("coil_display")
        self.coil_display = QLabel()
        coil_display_layout = QVBoxLayout(coil_display_widget)
        coil_display_layout.addWidget(self.coil_display)

        coil_view_widget = QWidget()
        coil_view = QVBoxLayout(coil_view_widget)
        coil_view_widget.setObjectName("coil_view")
        self.current_layer = QComboBox()
        self.current_layer.currentIndexChanged.connect(lambda: self.refresh_coil_display(self.coil_display))

        self.config_stack_view(stack_view)
        self.config_coil_view(coil_view)

        layout.addWidget(stack_view_widget)
        layout.addWidget(coil_view_widget)
        layout.addWidget(coil_display_widget)

        # Set Styles
        stack_view_widget.setFixedWidth(300)
        stack_view_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        stack_view_widget.setStyleSheet("""
            #stack_view{
                border-radius: 5px;
                border: 1px solid palette(button);
            }
        """)

        stack_view.setAlignment(Qt.AlignTop)
        stack_view.setSpacing(10)
        stack_view.setContentsMargins(10, 10, 10, 10)

        coil_view_widget.setFixedWidth(300)
        coil_view_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        coil_view_widget.setStyleSheet("""
            #coil_view{
                border-radius: 5px;
                border: 1px solid palette(button);
            }
        """)

        coil_view.setAlignment(Qt.AlignTop)
        coil_view.setSpacing(10)
        coil_view.setContentsMargins(10, 10, 10, 10)

        self.param_columns.setSpacing(10)
        self.param_columns.setContentsMargins(10,10,10,10)
        self.label_column.setContentsMargins(0,0,0,0)
        self.line_column.setContentsMargins(0,0,0,0)
        self.label_column.setSpacing(6)
        self.line_column.setSpacing(6)

        coil_display_widget.setStyleSheet("""
            #coil_display{
                border-radius: 5px;
                border: 1px solid palette(button);
            }
        """)





