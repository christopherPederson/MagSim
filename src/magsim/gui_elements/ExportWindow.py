from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)

class ExportWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)

        label = QLabel("Export Window")
        layout.addWidget(label)