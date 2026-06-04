import serial
import serial.tools.list_ports
import time
import re

class Model:
    def __init__(self):
        self.ports = []
        self.COM_config = dict
        self.MODBUS_settings = dict
        self.serial_port = serial.Serial()
        self.MODBUS_port = serial.Serial()
        self.terminators_list = {"None": b"", "CR": b"\r", "LR": b"\n", "CR-LF": b"\r\n"}
        self.terminator = b""
        self.ping_repeat = 5
        self.ping_count = self.ping_repeat

    def COM_ports_find(self):
        found = []
        found = [port.device for port in serial.tools.list_ports.comports()]
        self.ports = sorted(found, key=lambda p: int(p[3:]))
        return self.ports
    
    def set_COM_config(self, COM_config):
        if self.serial_port.is_open:
            self.serial_port.close()
        if self.MODBUS_port.is_open:
            self.MODBUS_port.close()
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
        self.terminator = self.terminators_list.get(self.COM_config["Terminator"],
                                                    self.COM_config["Terminator"].encode())
        self.serial_port.timeout = 1
        self.serial_port.write_timeout = 1
        print(self.serial_port)
        self.serial_port.open()

    def get_COM_config(self):
        return self.COM_config
    
    def set_MODBUS_settings(self, modbus_settings: dict):
        self.MODBUS_settings = modbus_settings
        print(self.MODBUS_settings)

    def get_MODBUS_settings(self):
        return self.MODBUS_settings

    def send_COM_message(self, text: str):
        print(text)
        check_text = text.lower()
        if check_text == "ping":
            print(time.time_ns())
            text = "ping"+str(time.time_ns())
        self.serial_port.write(text.encode() + self.terminator)

        """how ping works

        sender sends:
        ping
        this gets changed to:
        pingMM:SS:
        """

    def send_MODBUS_message(self, text: str, master: bool):
        print(text)
        check_text = text.lower()
        
        self.serial_port.write(text.encode() + self.terminator)

        """how ping works

        sender sends:
        ping
        this gets changed to:
        pingMM:SS:
        """
 
    def read_COM_message(self):
        data = self.serial_port.read_until(self.terminator)
        if not data:
            pass
            #print("none")
        data = data.strip()
        if data.startswith(b"ping"):
            matches = re.findall(r'\d{15,19}', data.decode('utf-8', errors='replace'))
            count = len(matches)
            if count == 1:
                # Someone send us the ping
                self.send_COM_message(data.decode('utf-8', errors='replace') + str(time.time_ns()))
                return
            elif count == 2:
                values = [int(m) for m in matches]
                return f"PING {(values[1] - values[0])//1000000} ms"

        print(repr(data))
        return data
    
    def close_port(self):
        self.serial_port.close()
