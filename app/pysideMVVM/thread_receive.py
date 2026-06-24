from PySide6.QtCore import QObject, QThread, Signal
from pysideMVVM.model import Model
import time

class SerialThread(QObject):
    message_received = Signal(str)
    finished = Signal()

    def __init__(self, model: Model, modbus: bool):
        super().__init__()
        self.model = model
        self.modbus = modbus
        self.bin_mode = False
        self._running = True

    def set_bin_mode(self, bin: bool):
        self.bin_mode = bin

    def set_MODBUS(self, modbus: bool):
        self.modbus = modbus

    def run(self):
        self._running = True
        while self._running:
            try:
                if self.modbus:
                    data = self.model.read_MODBUS_message()
                else:
                    data = self.model.read_COM_message(bin=self.bin_mode)
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