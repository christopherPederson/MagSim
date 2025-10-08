from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
    QHBoxLayout,
)

class NavBar(QWidget):
    page_index = Signal(int) # 0 = PCB Window, 1 = Simulation Window, 2 = Export Window

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        
        self.setObjectName("navbar")
        self.setAttribute(Qt.WA_StyledBackground, True)

        row = QHBoxLayout(self)

        pcb_window_btn = QPushButton("PCB Design")
        sim_window_btn = QPushButton("Simulation")
        export_window_btn = QPushButton("Export")

        pcb_window_btn.clicked.connect(lambda: self.page_index.emit(0))
        sim_window_btn.clicked.connect(lambda: self.page_index.emit(1))
        export_window_btn.clicked.connect(lambda: self.page_index.emit(2))

        row.addWidget(pcb_window_btn)
        row.addWidget(sim_window_btn)
        row.addWidget(export_window_btn)

        # Set Styles
        self.setStyleSheet("""
            #navbar{
                border-radius: 5px;
                border: 1px solid palette(button);
            }

        """)