from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)

class SimWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        layout = QHBoxLayout(self)

        label = QLabel("Simulation Window")
        layout.addWidget(label)