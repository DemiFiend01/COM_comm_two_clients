from pysideMVVM.viewmodel import PysideViewModel
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QLineEdit, QTextEdit, QRadioButton, QComboBox, QButtonGroup,
    QHBoxLayout, QVBoxLayout, QFrame, QFormLayout, QSizePolicy
)
from PySide6.QtCore import Qt

class ViewCOMConfig(QWidget):
    def __init__(self, viewmodel: PysideViewModel, switch_display):
        super().__init__()
        self.viewmodel = viewmodel
        self.switch_display = switch_display
        self._build()
        
    def _build(self):
        self.vbox_layout = QVBoxLayout()

        port_row = QHBoxLayout()
        l1 = QLabel("COM port:")
        self.COM_combobox = QComboBox()
        self.COM_combobox.addItems(self.viewmodel.COM_ports_list())
        port_refresh = QPushButton("↺")
        port_refresh.clicked.connect(self._refresh_ports)
        port_refresh.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        port_row.addWidget(l1)
        port_row.addWidget(self.COM_combobox)
        port_row.addWidget(port_refresh)
        self.vbox_layout.addLayout(port_row)

        bitrate_row = QHBoxLayout()
        l2 = QLabel("Bitrate (from 150 bits/s to 115 kb/s):")
        self.bitrate_input = QLineEdit()
        self.bitrate_input.setText("115")
        self.bitrate_bit = QRadioButton("bit/s")
        self.bitrate_kb = QRadioButton("kb/s")
        self.bitrate_kb.setChecked(True)
        self.bitrate_choice_group = QButtonGroup()
        self.bitrate_choice_group.addButton(self.bitrate_bit)
        self.bitrate_choice_group.addButton(self.bitrate_kb)
        bitrate_row.addWidget(self.bitrate_input)
        bitrate_row.addWidget(self.bitrate_bit)
        bitrate_row.addWidget(self.bitrate_kb)
        bitrate_row.addStretch()
        self.vbox_layout.addWidget(l2)
        self.vbox_layout.addLayout(bitrate_row)

        l3 = QLabel("PDU values:")

        PDU_bits_row = QHBoxLayout()
        l4 = QLabel("Data bits:")
        self.PDU_7_bits = QRadioButton("7 bits data field")
        self.PDU_7_bits.setChecked(True)
        self.PDU_8_bits = QRadioButton("8 bits data field")
        self.PDU_bits_group = QButtonGroup()
        self.PDU_bits_group.addButton(self.PDU_7_bits, 7)
        self.PDU_bits_group.addButton(self.PDU_8_bits, 8)
        PDU_bits_row.addWidget(l4)
        PDU_bits_row.addWidget(self.PDU_7_bits)
        PDU_bits_row.addWidget(self.PDU_8_bits)
        PDU_bits_row.addStretch()
        self.vbox_layout.addWidget(l3)
        self.vbox_layout.addLayout(PDU_bits_row)

        PDU_stop_bits_row = QHBoxLayout()
        l5 = QLabel("Stop bits:")
        self.PDU_stop_bit_1 = QRadioButton("1 stop bit")
        self.PDU_stop_bit_1.setChecked(True)
        self.PDU_stop_bit_2 = QRadioButton("2 stop bits")
        self.PDU_stop_bits_group = QButtonGroup()
        self.PDU_stop_bits_group.addButton(self.PDU_stop_bit_1)
        self.PDU_stop_bits_group.addButton(self.PDU_stop_bit_2)
        PDU_stop_bits_row.addWidget(l5)
        PDU_stop_bits_row.addWidget(self.PDU_stop_bit_1)
        PDU_stop_bits_row.addWidget(self.PDU_stop_bit_2)
        PDU_stop_bits_row.addStretch()
        self.vbox_layout.addLayout(PDU_stop_bits_row)

        PDU_parity_row = QHBoxLayout()
        l6 = QLabel("Parity:")
        self.PDU_parity_combobox = QComboBox()
        self.PDU_parity_combobox.addItems(["Even parity","Odd parity","None parity"])
        PDU_parity_row.addWidget(l6)
        PDU_parity_row.addWidget(self.PDU_parity_combobox)
        PDU_parity_row.addStretch()
        self.vbox_layout.addLayout(PDU_parity_row)

        data_flow_row = QHBoxLayout()
        l7 = QLabel("Data flow control:")
        self.data_flow_combobox = QComboBox()
        self.data_flow_combobox.addItems(["None","DTR/DSR handshake","RTS/CTS handshake","XON/XOFF protocol"])
        data_flow_row.addWidget(l7)
        data_flow_row.addWidget(self.data_flow_combobox)
        data_flow_row.addStretch()
        self.vbox_layout.addLayout(data_flow_row)

        terminator_row = QHBoxLayout()
        l8 = QLabel("Terminator settings, editable:")
        self.terminator_combobox = QComboBox()
        self.terminator_combobox.addItems(["None","CR","LF","CR-LF"])
        self.terminator_combobox.setEditable(True)
        terminator_row.addWidget(l8)
        terminator_row.addWidget(self.terminator_combobox)
        terminator_row.addStretch()
        self.vbox_layout.addLayout(terminator_row)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("" \
            "QLabel {" \
            "   color: red;" \
            "}" \
            "")
        self.vbox_layout.addWidget(self.error_label)

        continue_button = QPushButton("Continue")
        continue_button.clicked.connect(self.COM_verify_inputs)
        port_refresh.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.vbox_layout.addWidget(continue_button)

        self.vbox_layout.addStretch()
        self.setLayout(self.vbox_layout)

    def show_error(self, text: str):
        self.error_label.setText(text)

    def _refresh_ports(self):
        self.COM_combobox.clear()
        self.COM_combobox.addItems(self.viewmodel.COM_ports_list())
        
    def COM_verify_inputs(self):
        COM_values = [
            ["COM_port",self.COM_combobox.currentText().strip()],
            ["bitrate_value",self.bitrate_input.text().strip()],
            ["bitrate_unit", "bit" if self.bitrate_bit.isChecked() else "kb"],
            ["PDU_bits", self.PDU_bits_group.checkedId()],
            ["PDU_stop", self.PDU_stop_bits_group.checkedId()],
            ["PDU_parity", self.PDU_parity_combobox.currentText().strip()],
            ["Data_flow_control", self.data_flow_combobox.currentText().strip()],
            ["Terminator", self.terminator_combobox.currentText().strip()]
        ]
        COM_values_dict = dict(COM_values)
        if not COM_values_dict["COM_port"]:
            self.show_error("No port has been selected")
            return

        if not COM_values_dict["bitrate_unit"]:
            self.show_error("No bitrate unit has been selected")
            return
        
        if COM_values_dict["bitrate_value"]:
            if COM_values_dict["bitrate_value"].isdigit():
                if COM_values_dict["bitrate_unit"] == "bit":
                    if int(COM_values_dict["bitrate_value"]) < 150 or int(COM_values_dict["bitrate_value"]) > 115000:
                        self.show_error("Wrong bitrate value")
                        return
                else:
                    if int(COM_values_dict["bitrate_value"]) > 115:
                        self.show_error("Bitrate value is too great")
                        return
            else:
                self.show_error("Bitrate has to be a number")
                return
        else:
            self.show_error("No bitrate has been inputted")
            return
        
        if not COM_values_dict["PDU_bits"]:
            self.show_error("No PDU bits chosen")
            return
        
        if not COM_values_dict["PDU_stop"]:
            self.show_error("No stop bits chosen")
            return
        
        if not COM_values_dict["PDU_parity"]:
            self.show_error("No PDU parity option has been selected")
            return
        
        if not COM_values_dict["Data_flow_control"]:
            self.show_error("No data flow control option has been selected")
            return
        
        if COM_values_dict["Terminator"]:
            if not COM_values_dict["Terminator"] in ["None","CR","LF","CR-LF"]:
                if len(COM_values_dict["Terminator"]) > 2:
                    self.show_error("Terminator is too long (2 chars max)")
                    return
        else:
            self.show_error("No terminator has been selected")
            return

        self.viewmodel.save_COM_config(COM_values_dict)
        self.switch_display(new_display=ViewCOMcomm(viewmodel=self.viewmodel, switch_display = self.switch_display))

class ViewCOMcomm(QWidget):
    def __init__(self, viewmodel: PysideViewModel, switch_display):
        super().__init__()
        self.viewmodel = viewmodel
        self.switch_display = switch_display
        self._build()

    def _build(self):
        print("meow")
        # self.comm_frame = tk.Frame(
        #     self.window, bg=self.bg_colour
        # )
        # self.comm_frame.pack(pady=5)
        # self.trans_frame = tk.Frame(
        #     self.comm_frame, bg=self.bg_colour
        # )
        # frame_seperator = ttk.Separator(
        #     self.comm_frame, orient="vertical"
        # )
        # self.receive_frame = tk.Frame(
        #     self.comm_frame, bg=self.bg_colour
        # )
        # self.trans_frame.pack(side="left",padx = 10)
        # frame_seperator.pack(side="left", fill="y", padx=15)
        # self.receive_frame.pack(side="left",padx=10)

        # trans_label = tk.Label(
        #     self.trans_frame, text="Transmission window in HEX", bg=self.bg_colour
        # )
        # self.trans_window = tk.Text (
        #     self.trans_frame, width = 30, height=20
        # )
        # trans_label.pack(side="top")
        # self.trans_window.pack(padx=10)
        
        # receive_label = tk.Label(
        #     self.receive_frame, text="Receive window in HEX", bg=self.bg_colour
        # )
        # self.receive_window = tk.Text(
        #     self.receive_frame, width = 30, height=20, state="disabled"
        # )
        # receive_label.pack(side="top")
        # self.receive_window.pack()

        # self.buttons_frame = tk.Frame(
        #     self.window, bg=self.bg_colour
        # )
        # self.buttons_frame.pack(pady=10)
        # go_back_button = tk.Button(
        #     self.buttons_frame, text="Go back", bg=self.bg_colour, command=lambda:self.switch_display(self.COM_config_screen)
        # )
        # go_back_button.pack(side="left",padx=30)

        # send_button = tk.Button(
        #     self.buttons_frame, text="Send", bg=self.bg_colour, command=lambda:self.viewmodel.send_COM_message(self.trans_window.get())
        # )
        # send_button.pack(side="right",padx=30)