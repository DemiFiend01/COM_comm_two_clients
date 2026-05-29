from pysideMVVM.viewmodel import PysideViewModel
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QLineEdit, QTextEdit, QRadioButton, QComboBox, QButtonGroup,
    QHBoxLayout, QVBoxLayout, QFrame
)
from PySide6.QtCore import Qt

class ViewCOMConfig(QWidget):
    def __init__(self, viewmodel: PysideViewModel, switch_display):
        self.viewmodel = viewmodel
        self.switch_display = switch_display
        self._build()
        
    def _build(self):
        pass