import serial
import serial.tools.list_ports

# COM_values = [
#             ["COM_port"],
#             ["bitrate_value"],
#             ["bitrate_unit"],
#             ["PDU_bits"],
#             ["PDU_stop"],
#             ["PDU_parity"],
#             ["Data_flow_control"],
#             ["Terminator"]
#         ]
class Model:
    def __init__(self):
        self.ports = []
        self.COM_config = dict
        self.serial_port = serial.Serial()

    def COM_ports_find(self):
        found = []
        found = [port.device for port in serial.tools.list_ports.comports()]
        self.ports = sorted(found, key=lambda p: int(p[3:]))
        return self.ports
    
    def set_COM_config(self, COM_config):
        self.COM_config = COM_config      
        self.serial_port.port = self.COM_config["COM_port"]
        self.serial_port.baudrate = int(self.COM_config["bitrate_value"])
        if self.COM_config["bitrate_unit"] == "kb":
            self.serial_port.baudrate *= 1000
        self.serial_port.bytesize = self.COM_config["PDU_bits"]

        self.serial_port.stopbits = serial.STOPBITS_ONE
        if self.COM_config["PDU_stop"] == 8:
            self.serial_port.stopbits = serial.STOPBITS_TWO

        self.serial_port.parity = serial.PARITY_NONE
        match self.COM_config["PDU_parity"]:
            case "Even parity":
                self.serial_port.parity = serial.PARITY_EVEN
            case "Odd parity":
                self.serial_port.parity = serial.PARITY_ODD

        match self.COM_config["Data_flow_control"]:
            case "DTR/DSR handshake":
                self.serial_port.dsrdtr = True
            case "RTS/CTS handshake":
                self.serial_port.rtscts = True
            case "XON/XOFF protocol":
                self.serial_port.xonxoff = True

        print(self.serial_port)
    
    def get_COM_config(self):
        return self.COM_config

    def send_COM_message(self, text):

        print(text)
        self.serial_port.write(text.encode() + "cd")
