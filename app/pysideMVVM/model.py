import serial
import serial.tools.list_ports

class Model:
    def __init__(self):
        self.ports = []
        self.COM_config = dict

    def COM_ports_find(self):
        found = []
        found = [port.device for port in serial.tools.list_ports.comports()]
        self.ports = sorted(found, key=lambda p: int(p[3:]))
        return self.ports
    
    def set_COM_config(self, COM_config):
        self.COM_config = COM_config        

    def send_COM_message(self, text):
        print(text)