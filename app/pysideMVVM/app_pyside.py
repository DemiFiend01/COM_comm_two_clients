from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow )
from PySide6.QtGui import QIcon
import sys
from pysideMVVM.viewmodel import PysideViewModel
from pysideMVVM.view import PysideView
from pathlib import Path
from qt_material import apply_stylesheet

class App:
    def __init__(self, viewmodel: PysideViewModel):
        self.qt_app = QApplication(sys.argv)
        self.window = PysideView(viewmodel= viewmodel)    
        size = self.window.size().toTuple()
        screen = (self.window.screen().geometry().width(), 
                  self.window.screen().geometry().height())
        move_by = (screen[0]/2 - size[0]/2, screen[1]/2 - size[1]/2)
        self.window.move(move_by[0], move_by[1])

        apply_stylesheet(self.window, theme="dark_cyan.xml")

        icon_path = Path(__file__).parent / "icon.png"
        my_icon = QIcon()
        my_icon.addFile(str(icon_path))
        self.window.setWindowIcon(my_icon)
        self.window.show()
        self.qt_app.aboutToQuit.connect(self._cleanup)

    def run(self):
        self.qt_app.exec()

    def _cleanup(self):
        self.window.viewmodel.serial_worker_thread.stop()
        self.window.viewmodel.receive_thread.quit()
        self.window.viewmodel.receive_thread.wait()