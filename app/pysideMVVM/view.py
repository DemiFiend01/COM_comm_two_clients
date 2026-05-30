from PySide6.QtWidgets import (
    QMainWindow, QWidget
)
from PySide6.QtCore import Qt
from pysideMVVM.viewmodel import PysideViewModel
from pysideMVVM.views_COM import ViewCOMConfig

class PysideView(QMainWindow):
    def __init__(self, viewmodel: PysideViewModel):
        super().__init__()
        self.setWindowTitle("CSI laboratory")
        self.setGeometry(10,10,600,500)
        self.viewmodel = viewmodel
        self.bg_colour="azure"
        self.switch_display(ViewCOMConfig(viewmodel=self.viewmodel, 
                                          switch_display=self.switch_display))
    
    def switch_display(self, new_display: QWidget):
        self.setCentralWidget(new_display)