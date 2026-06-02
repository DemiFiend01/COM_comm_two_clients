from PySide6.QtCore import QObject, QThread, Signal
from pysideMVVM.model import Model

class SerialThread(QObject):
    message_received = Signal(str)
    finished = Signal()

    def __init__(self, model: Model):
        super().__init__()
        self.model = model
        self._running = True

    def run(self):
        while self._running:
            try:
                data = self.model.read_COM_message()
                if data:
                    if isinstance(data, bytes):
                        self.message_received.emit(data.decode('utf-8', errors='replace'))
                    else:
                        self.message_received.emit(data)
            except Exception as e:
                print(repr(e))
                break
        self.finished.emit()

    def stop(self):
        self._running = False