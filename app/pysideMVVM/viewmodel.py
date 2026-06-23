#callbacks go from view to viewmodel which receives an instance of model and communicates with it
from pysideMVVM.model import Model
from pysideMVVM.thread_receive import SerialThread
from PySide6.QtCore import QObject, QThread, Signal


class PysideViewModel(QObject):
    message_received = Signal(str)

    def __init__(self, model:Model):
        super().__init__()
        self.model = model
        self.receive_thread = QThread()
        self.serial_worker_thread = SerialThread(model = self.model, modbus= False)
        self.serial_worker_thread.moveToThread(self.receive_thread)

        self.receive_thread.started.connect(self.serial_worker_thread.run)
        # self.serial_worker_thread.finished.connect(self.receive_thread.quit)
        self.serial_worker_thread.message_received.connect(self.message_received)

    def COM_ports_list(self):
        return self.model.COM_ports_find()

    def save_COM_config(self, COM_config: dict, modbus: bool):
        self.model.set_COM_config(COM_config)
        self.serial_worker_thread.set_MODBUS(modbus)
        self.receive_thread.start()

    def save_MODBUS_settings(self, MODBUS_settings: dict):
        #self.receive_thread.set_MODBUS(modbus= True)
        self.model.set_MODBUS_settings(modbus_settings=MODBUS_settings)
    
    def get_COM_config(self):
        return self.model.get_COM_config()

    def send_COM_message(self, text):
        self.model.send_COM_message(text)

    def send_MODBUS_message(self, text, master: bool):
        self.model.send_MODBUS_message(text, master=master)

    def stop_thread(self):
        self.serial_worker_thread.stop()
        self.receive_thread.quit()
        self.receive_thread.wait()