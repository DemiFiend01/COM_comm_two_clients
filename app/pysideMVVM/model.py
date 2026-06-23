import serial
import serial.tools.list_ports
import time
import re

class Model:
    MODBUS_START = b":" # always :
    MODBUS_TERMINATOR = b"\r\n" # always like this
    BROADCAST_ADDRESS = 0
    def __init__(self):
        self.ports = []
        self.COM_config = {}
        self.MODBUS_settings = {}
        self.serial_port = serial.Serial()
        self.MODBUS_port = serial.Serial()
        self.terminators_list = {"None": b"", "CR": b"\r", "LR": b"\n", "CR-LF": b"\r\n"}
        self.terminator = b""
        self.ping_repeat = 5
        self.ping_count = self.ping_repeat

        # MODBUS ASCII
        self.MODBUS_pending_frame = None   # last query the Master sent, awaiting a response
        self.MODBUS_pending_time = None
        self.MODBUS_retrans_left = 0
        self.MODBUS_text_to_send = ""

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
        if self.COM_config["PDU_stop"] == 2:
            self.serial_port.stopbits = serial.STOPBITS_TWO

        self.serial_port.parity = serial.PARITY_NONE
        match self.COM_config["PDU_parity"]:
            case "Even parity":
                self.serial_port.parity = serial.PARITY_EVEN
            case "Odd parity":
                self.serial_port.parity = serial.PARITY_ODD

        self.serial_port.dsrdtr = False
        self.serial_port.rtscts = False
        self.serial_port.xonxoff = False
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

        if data.endswith(self.terminator):
            data = data[:data.find(self.terminator)]
        print(repr(data))
        return data

    def close_port(self):
        self.serial_port.close()
        self.MODBUS_port.close()

    def _LRC(self, data: bytes) -> int:
        """Standard MODBUS LRC: two's complement of the sum of all bytes, mod 256."""
        return (-(sum(data) & 0xFF)) & 0xFF

    def build_MODBUS_frame(self, address: int, modbus_mode: int, data: bytes = b"") -> bytes:
        """':' + hex(addr + func + data + LRC) + CRLF. MODBUS-ASCII frame."""
        payload = bytes([address & 0xFF, modbus_mode & 0xFF]) + data
        lrc = self._LRC(payload)
        hex_payload = (payload + bytes([lrc])).hex().upper().encode("ascii")
        return self.MODBUS_START + hex_payload + self.MODBUS_TERMINATOR

    def build_MODBUS_exception(self, address: int, modbus_mode: int, exception_code: int = 1) -> bytes:
        """Exception response: modbus_mode code with the MSB set + one data byte."""
        return self.build_MODBUS_frame(address, modbus_mode | 0x80, bytes([exception_code]))

    def parse_MODBUS_frame(self, frame: bytes):
        """Parses a raw ':'...CRLF frame. Returns dict or None if malformed."""
        frame = frame.strip()
        if not frame.startswith(self.MODBUS_START):
            return None # Wrong start
        try:
            raw = bytes.fromhex(frame[1:].decode("ascii"))
        except ValueError:
            return None
        if len(raw) < 3:  # address + modbus_mode + LRC, minimum
            return None #Too short
        address, modbus_mode, data, received_lrc = raw[0], raw[1], raw[2:-1], raw[-1] #stripping
        return {
            "address": address,
            "modbus_mode": modbus_mode,
            "data": data,
            "lrc_ok": received_lrc == self._LRC(raw[:-1]), #checking
        }

    def _read_MODBUS_frame(self):
        """Reads one ':'...CRLF frame, honouring the inter-character timeout."""
        char_timeout_ms = self.MODBUS_settings.get("Character_timeout", 1000)
        self.serial_port.timeout = max(char_timeout_ms, 1) / 1000.0
        first = self.serial_port.read(1)
        if first != self.MODBUS_START:
            return None  # nothing arrived or noise
        buffer = bytearray(first)
        while not buffer.endswith(self.MODBUS_TERMINATOR):
            byte = self.serial_port.read(1)
            if not byte:
                return None  # TIMEOUT
            buffer += byte # Create the frame
        return bytes(buffer)

    def send_MODBUS_message(self, text: str, master: bool):
        if not self.MODBUS_settings:
            return
        if master:
            broadcast = self.MODBUS_settings.get("Broadcast", False)
            modbus_mode = 1 if self.MODBUS_settings.get("Master_To_Slave", True) else 2
            if modbus_mode == 2 and broadcast:
                broadcast = False  # "read" can only be an addressed transaction
            address = self.BROADCAST_ADDRESS if broadcast else self.MODBUS_settings.get("Slave_address", 1)
            data = text.encode("utf-8", errors="replace") if modbus_mode == 1 else b""

            frame = self.build_MODBUS_frame(address, modbus_mode, data) # modbus_mode is master to slave or slave to master
            self.serial_port.write(frame)
            print("MODBUS TX:", frame)

            self.MODBUS_pending_frame = frame
            self.MODBUS_pending_time = time.time()
            self.MODBUS_retrans_left = self.MODBUS_settings.get("Number_of_retransmissions", 0)
        else:
            # A Slave doesn't transmit on its own initiative — this just stores the text
            # to hand back the next time a Master sends a "read" (command 2) request.
            self.MODBUS_text_to_send = text

    def read_MODBUS_message(self):
        if not self.MODBUS_settings:
            return None
        if self.MODBUS_settings.get("Master", True):
            return self._handle_master_poll()
        return self._handle_slave_poll()

    def _handle_master_poll(self):
        frame = self._read_MODBUS_frame()

        if frame is None:
            if self.MODBUS_pending_frame is not None:
                timeout_s = self.MODBUS_settings.get("Transmission_timeout", 1000) / 1000.0
                if time.time() - self.MODBUS_pending_time > timeout_s:
                    if self.MODBUS_retrans_left > 0:
                        self.serial_port.write(self.MODBUS_pending_frame)
                        self.MODBUS_retrans_left -= 1
                        self.MODBUS_pending_time = time.time()
                        return "MODBUS: response timeout, retransmitting query"
                    self.MODBUS_pending_frame = None
                    return "MODBUS: transaction failed (no response from slave)"
            return None

        parsed = self.parse_MODBUS_frame(frame)
        self.MODBUS_pending_frame = None
        if parsed is None or not parsed["lrc_ok"]:
            return f"MODBUS RX (corrupted frame): {frame.hex().upper()}"

        if parsed["modbus_mode"] & 0x80:
            code = parsed["data"][0] if parsed["data"] else None
            return f"MODBUS exception response (code {code})"
        if parsed["modbus_mode"] == 2:
            text = parsed["data"].decode("utf-8", errors="replace")
            return f"Text received from slave: {text}"
        return "MODBUS: write acknowledged by slave"

    def _handle_slave_poll(self):
        frame = self._read_MODBUS_frame()
        if frame is None:
            return None

        parsed = self.parse_MODBUS_frame(frame)
        if parsed is None or not parsed["lrc_ok"]:
            return f"MODBUS RX (corrupted frame): {frame.hex().upper()}"

        own_address = self.MODBUS_settings.get("Slave_address", 1)
        broadcast = parsed["address"] == self.BROADCAST_ADDRESS # 0
        if parsed["address"] != own_address and not broadcast:
            return None

        if parsed["modbus_mode"] == 1:
            text = parsed["data"].decode("utf-8", errors="replace")
            self.MODBUS_text_to_send = text
            if not broadcast:
                self.serial_port.write(self.build_MODBUS_frame(own_address, 1, b""))
            return f"Text received from master: {text}"

        if parsed["modbus_mode"] == 2:
            if broadcast:
                return None  # "read" cannot be broadcast
            data = self.MODBUS_text_to_send.encode("utf-8", errors="replace")
            self.serial_port.write(self.build_MODBUS_frame(own_address, 2, data))
            return "MODBUS: sent stored text to master"

        if not broadcast:
            self.serial_port.write(self.build_MODBUS_exception(own_address, parsed["modbus_mode"]))
        return f"MODBUS: unknown command {parsed['modbus_mode']}, exception sent"
