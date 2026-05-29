from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow )
import sys
from pysideMVVM.viewmodel import PysideViewModel
from pysideMVVM.view import PysideView

class App:
    def __init__(self, viewmodel: PysideViewModel):
        self.qt_app = QApplication(sys.argv)
        self.window = PysideView(viewmodel= viewmodel)

    def run(self):
        self.qt_app.exec()