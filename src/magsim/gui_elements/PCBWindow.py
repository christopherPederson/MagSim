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
)



class PCBWindow(QWidget):
    def add_layer(self, view, layer_num: int):

        layer_widget = QWidget()
        layer = QHBoxLayout(layer_widget)

        layer_label = QLabel(f'Layer {layer_num}')
        layer_type = QComboBox()
        layer_type.addItems(['Coil', 'Ground', 'Signal'])
        layer_thickness = QLineEdit()
        layer_thickness.setPlaceholderText("Copper Thickness (Oz)")

        layer.addWidget(layer_label)
        layer.addWidget(layer_type)
        layer.addWidget(layer_thickness)

        view.addWidget(layer_widget)

    def config_stack_view(self, view):
        view_label = QLabel("PCB Stack View")
        view.addWidget(view_label)

        for i in range(1, 5):
            self.add_layer(view, i)




    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)

        stack_view_widget = QWidget()
        stack_view_widget.setObjectName("stack_view")
        stack_view = QVBoxLayout(stack_view_widget)
        self.config_stack_view(stack_view)

        # coil_view_widget = QWidget()
        # coil_view = QVBoxLayout(coil_view_widget)
        # self.config_coil_view(coil_view)
        # coil_view_widget.setLayout(coil_view)

        layout.addWidget(stack_view_widget)

        # Set Styles
        stack_view_widget.setFixedWidth(250)
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





