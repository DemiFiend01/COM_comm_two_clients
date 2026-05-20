import serial
import serial.tools.list_ports
class Model:
    def __init__(self):
        self.ports = []
        pass

    def COM_ports_find(self):
        found = []
        found = [port.device for port in serial.tools.list_ports.comports()]
        self.ports = sorted(found, key=lambda p: int(p[3:]))
        
        return self.ports