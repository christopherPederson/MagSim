import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
)

from .gui_elements.NavBar import NavBar
from .gui_elements.PCBWindow import PCBWindow
from .gui_elements.SimWindow import SimWindow
from .gui_elements.ExportWindow import ExportWindow

# -- GUI Definitions -- #
app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self):                         # Constructor on the MainWindow class
        super().__init__()                      # super() is used to call the constructor of any parent classes

        self.setWindowTitle("MagSim")

        # Define the layout
        self.central_widget = QWidget()                     # Central widget that contains all contents
        self.root = QVBoxLayout(self.central_widget)        # Central widget that contains all contents
        self.navbar_main = NavBar()                         # navigation bar at the top of the root

        # set the root as the layout of the central widget
        self.central_widget.setLayout(self.root)

        # stacked widget to hold the pages
        self.stack = QStackedWidget()
        self.stack.addWidget(PCBWindow())       # index 0
        self.stack.addWidget(SimWindow())       # index 1
        self.stack.addWidget(ExportWindow())    # index 2

        self.root.addWidget(self.navbar_main)
        self.root.addWidget(self.stack)
        self.setCentralWidget(self.central_widget)

        # Connect the navigation bar signals to change the displayed page
        self.navbar_main.page_index.connect(self.stack.setCurrentIndex)


window = MainWindow()
window.showMaximized() # Show window in full screen

app.exec()