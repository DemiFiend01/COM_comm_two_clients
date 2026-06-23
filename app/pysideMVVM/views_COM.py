from pysideMVVM.viewmodel import PysideViewModel
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSpinBox, QWidget, QLabel, QPushButton,
    QLineEdit, QTextEdit, QRadioButton, QComboBox, QButtonGroup,
    QHBoxLayout, QVBoxLayout, QFrame, QFormLayout, QSizePolicy
)
from PySide6.QtCore import Qt

class ViewCOMConfig(QWidget):
    def __init__(self, viewmodel: PysideViewModel, switch_display, saved_config = None):
        super().__init__()
        self.viewmodel = viewmodel
        self.switch_display = switch_display
        self._build()
        if saved_config:
            self._restore(saved_config)
        
    def _build(self):
        self.vbox_layout = QVBoxLayout()

        l0 = QLabel("Properties (Default for MODBUS):")
        self.vbox_layout.addWidget(l0)

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
        port_row.addStretch()
        self.vbox_layout.addLayout(port_row)

        bitrate_row = QHBoxLayout()
        l2 = QLabel("Bitrate (from 150 bits/s to 115 kb/s):")
        self.bitrate_input = QLineEdit()
        self.bitrate_input.setText("96")
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
        self.PDU_8_bits = QRadioButton("8 bits data field")
        self.PDU_8_bits.setChecked(True)
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
        self.PDU_stop_bits_group.addButton(self.PDU_stop_bit_1, 1)
        self.PDU_stop_bits_group.addButton(self.PDU_stop_bit_2, 2)
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

        buttons_row = QHBoxLayout()
        l9 = QLabel("Choose mode and continue:")
        com_comm_button = QPushButton("COM comm")
        com_comm_button.clicked.connect(lambda: self.COM_verify_inputs(modbus = False))
        com_comm_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        modbus_button = QPushButton("Modbus")
        modbus_button.clicked.connect(lambda: self.COM_verify_inputs(modbus= True))
        modbus_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.vbox_layout.addWidget(l9)
        buttons_row.addWidget(com_comm_button)
        buttons_row.addWidget(modbus_button)
        self.vbox_layout.addLayout(buttons_row)

        self.vbox_layout.addStretch()
        self.setLayout(self.vbox_layout)

    def show_error(self, text: str):
        self.error_label.setText(text)

    def _refresh_ports(self):
        self.COM_combobox.clear()
        self.COM_combobox.addItems(self.viewmodel.COM_ports_list())

    def _restore(self, saved_config):
        self.COM_combobox.setCurrentText(saved_config["COM_port"])
        self.bitrate_input.setText(saved_config["bitrate_value"])
        if saved_config["bitrate_unit"] == "bit":
            self.bitrate_bit.setChecked(True)
        else:
            self.bitrate_kb.setChecked(True)
        if saved_config["PDU_bits"] == 7:
            self.PDU_7_bits.setChecked(True)
        else:
            self.PDU_8_bits.setChecked(True)
        if saved_config["PDU_stop"] == 1:
            self.PDU_stop_bit_1.setChecked(True)
        else:
            self.PDU_stop_bit_2.setChecked(True)

        self.PDU_parity_combobox.setCurrentText(saved_config["PDU_parity"])
        self.data_flow_combobox.setCurrentText(saved_config["Data_flow_control"])
        self.terminator_combobox.setCurrentText(saved_config["Terminator"])
        
    def COM_verify_inputs(self, modbus: bool):
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
        
        print(COM_values_dict["PDU_stop"])
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
        
        self.viewmodel.save_COM_config(COM_values_dict, modbus = modbus)
        if modbus:
            self.switch_display(new_display=ViewMODBUSconfig(viewmodel=self.viewmodel, switch_display = self.switch_display))
        else:
            self.switch_display(new_display=ViewCOMcomm(viewmodel=self.viewmodel, switch_display = self.switch_display))

class ViewMODBUSconfig(QWidget):
    def __init__(self, viewmodel: PysideViewModel, switch_display):
        super().__init__()
        self.viewmodel = viewmodel
        self.switch_display = switch_display
        self._build()

    def _build(self):
        self.vbox_layout = QVBoxLayout()

        l0 = QLabel("MODBUS choice:")
        self.vbox_layout.addWidget(l0)

        modbus_choice_row = QHBoxLayout()
        self.modbus_master = QRadioButton("Master")
        self.modbus_master.setChecked(True)
        self.modbus_slave = QRadioButton("Slave")
        self.modbus_choice_group = QButtonGroup()
        self.modbus_choice_group.addButton(self.modbus_master)
        self.modbus_choice_group.addButton(self.modbus_slave)
        modbus_choice_row.addWidget(self.modbus_master)
        modbus_choice_row.addWidget(self.modbus_slave)
        modbus_choice_row.addStretch()
        self.vbox_layout.addLayout(modbus_choice_row)

        buttons_row = QHBoxLayout()

        go_back_button = QPushButton("Go Back")
        go_back_button.clicked.connect(lambda: self.switch_display(new_display=ViewCOMConfig(viewmodel = self.viewmodel, 
                                                       switch_display = self.switch_display)))
        go_back_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        continue_button = QPushButton("MODBUS continue")
        continue_button.clicked.connect(lambda: self.switch_display(new_display=ViewMODBUScomm(viewmodel = self.viewmodel, 
                                                       switch_display = self.switch_display, 
                                                       master = self.modbus_master.isChecked())))
        continue_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        buttons_row.addWidget(go_back_button)
        buttons_row.addWidget(continue_button)
        self.vbox_layout.addLayout(buttons_row)
        self.vbox_layout.addStretch()

        self.setLayout(self.vbox_layout)

class ViewCOMcomm(QWidget):
    def __init__(self, viewmodel: PysideViewModel, switch_display):
        super().__init__()
        self.viewmodel = viewmodel
        self.switch_display = switch_display
        self._build()

    def _build(self):
        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.setContentsMargins(30, 20, 30, 20)
        self.vbox_layout.setSpacing(12)

        transmission_col = QVBoxLayout()
        receive_col = QVBoxLayout()
        comm_row = QHBoxLayout()
        l1 = QLabel("Transmission window in HEX:")
        l2 = QLabel("Receive window in HEX:")

        self.trans_window = QTextEdit()
        self.receive_window = QTextEdit()
        self.receive_window.setReadOnly(True)
        self.viewmodel.message_received.connect(self.receive_window.append)

        transmission_col.addWidget(l1)
        transmission_col.addWidget(self.trans_window)
        receive_col.addWidget(l2)
        receive_col.addWidget(self.receive_window)
        comm_row.addLayout(transmission_col)
        comm_row.addLayout(receive_col)
        #comm_row.addStretch()
        self.vbox_layout.addLayout(comm_row)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("" \
            "QLabel {" \
            "   color: red;" \
            "}" \
            "")
        self.vbox_layout.addWidget(self.error_label)

        button_row = QHBoxLayout()
        go_back_button = QPushButton("Go back")
        go_back_button.clicked.connect(lambda: self.go_back())
        send_button = QPushButton("Send")
        send_button.clicked.connect(lambda:self.viewmodel.send_COM_message(self.trans_window.toPlainText().strip()))
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda:self.receive_window.clear())
        button_row.addWidget(go_back_button)
        button_row.addWidget(send_button)
        button_row.addWidget(clear_button)
        self.vbox_layout.addLayout(button_row)

        self.vbox_layout.addStretch()
        self.setLayout(self.vbox_layout)

    def go_back(self):
        self.viewmodel.stop_thread()
        self.viewmodel.model.close_port()
        self.switch_display(new_display=ViewCOMConfig(
            viewmodel=self.viewmodel,
            switch_display=self.switch_display,
            saved_config=self.viewmodel.model.COM_config
        ))

class ViewMODBUScomm(QWidget):
    def __init__(self, viewmodel: PysideViewModel, switch_display, master: bool):
        super().__init__()
        self.viewmodel = viewmodel
        self.switch_display = switch_display
        self.master = master
        self._build()

    def _build(self):
        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.setContentsMargins(30, 20, 30, 20)
        self.vbox_layout.setSpacing(12)

        transmission_col = QVBoxLayout()
        receive_col = QVBoxLayout()
        comm_row = QHBoxLayout()
        l1 = QLabel("Transmission window in HEX:")
        l2 = QLabel("Receive window in HEX:")

        self.trans_window = QTextEdit()
        self.receive_window = QTextEdit()
        self.receive_window.setReadOnly(True)
        self.viewmodel.message_received.connect(self.receive_window.append)

        transmission_col.addWidget(l1)
        transmission_col.addWidget(self.trans_window)
        receive_col.addWidget(l2)
        receive_col.addWidget(self.receive_window)
        comm_row.addLayout(transmission_col)
        comm_row.addLayout(receive_col)
        #comm_row.addStretch()
        self.vbox_layout.addLayout(comm_row)
        
        if self.master:
            master_settings_row = QHBoxLayout()

            left_joined_row = QHBoxLayout()
            leftside_col = QVBoxLayout()
            rightside_col = QVBoxLayout()

            slave_addr_col = QVBoxLayout()
            l3 = QLabel("Slave (unit) address (set from 0 (BC) to 127): ")
            l3.setWordWrap(True)
            self.slave_addr = QSpinBox()
            self.slave_addr.setMinimum(0) # 0 For broadcast
            self.slave_addr.setMaximum(247)
            self.slave_addr.setSingleStep(1)
            self.slave_addr.setValue(1)
            slave_addr_col.addWidget(l3)
            slave_addr_col.addWidget(self.slave_addr)
            slave_addr_col.addStretch()
            leftside_col.addLayout(slave_addr_col)

            transation_timeout_col = QVBoxLayout()
            l4 = QLabel("Transaction (whole) timeout (0 - 10 s), resolution 100 ms")
            l4.setWordWrap(True)
            self.transaction_timeout = QSpinBox()
            self.transaction_timeout.setMinimum(0)
            self.transaction_timeout.setMaximum(10000)
            self.transaction_timeout.setSingleStep(100)
            self.transaction_timeout.setSuffix(" ms")
            self.transaction_timeout.setValue(10000)
            transation_timeout_col.addWidget(l4)
            transation_timeout_col.addWidget(self.transaction_timeout)
            leftside_col.addLayout(transation_timeout_col)
            leftside_col.addStretch()
            left_joined_row.addLayout(leftside_col,1)

            retransmission_row = QVBoxLayout()
            l5 = QLabel("Number of retransmissions (0 - 5)")
            l5.setWordWrap(True)
            self.retrans_number = QSpinBox()
            self.retrans_number.setMinimum(0)
            self.retrans_number.setMaximum(5)
            self.retrans_number.setSingleStep(1)
            self.retrans_number.setValue(1)
            retransmission_row.addWidget(l5)
            retransmission_row.addWidget(self.retrans_number)
            rightside_col.addLayout(retransmission_row)

            character_timeout_row = QVBoxLayout()
            l6 = QLabel("Between characters timeout (0 or 1 s), resolution 10 ms")
            l6.setWordWrap(True)
            self.character_timeout = QSpinBox()
            self.character_timeout.setMinimum(0)
            self.character_timeout.setMaximum(1000)
            self.character_timeout.setSingleStep(10)
            self.character_timeout.setSuffix(" ms")
            self.character_timeout.setValue(1000)
            character_timeout_row.addWidget(l6)
            character_timeout_row.addWidget(self.character_timeout)
            rightside_col.addLayout(character_timeout_row)
            rightside_col.addStretch()
            left_joined_row.addLayout(rightside_col,1)
            master_settings_row.addLayout(left_joined_row,1)

            right_joined_col = QVBoxLayout()

            operation_joined_col = QVBoxLayout()
            operation_row = QHBoxLayout()
            l7 = QLabel("Operation modes:")
            l7.setWordWrap(True)
            self.command_1 = QRadioButton("Send from Master to Slave")
            self.command_1.setChecked(True)
            self.command_2 = QRadioButton("Read from Slave")
            operation_modes_group = QButtonGroup()
            operation_modes_group.addButton(self.command_1)
            operation_modes_group.addButton(self.command_2)
            operation_joined_col.addWidget(l7)
            operation_row.addWidget(self.command_1)
            operation_row.addWidget(self.command_2)
            operation_row.addStretch()
            operation_joined_col.addLayout(operation_row)
            operation_joined_col.addStretch()
            right_joined_col.addLayout(operation_joined_col)
            right_joined_col.addStretch()

            set_button = QPushButton("Set settings")
            set_button.clicked.connect(self.check_master_settings)
            right_joined_col.addWidget(set_button)
            right_joined_col.addStretch()

            master_settings_row.addLayout(right_joined_col,1)
            master_settings_row.addStretch()
            self.vbox_layout.addLayout(master_settings_row)  
            
            self.check_master_settings()            
        else:
            l3 = QLabel("Slave (unit) address: ")
            l3.setWordWrap(True)
            self.slave_addr = QSpinBox()
            self.slave_addr.setMinimum(1)
            self.slave_addr.setMaximum(247)
            self.slave_addr.setSingleStep(1)
            self.slave_addr.setValue(1)
            self.vbox_layout.addWidget(l3)
            self.vbox_layout.addWidget(self.slave_addr)

            l4 = QLabel("Between characters timeout (0 - 1 s), resolution 10 ms")
            l4.setWordWrap(True)
            self.character_timeout = QSpinBox()
            self.character_timeout.setMinimum(0)
            self.character_timeout.setMaximum(1000)
            self.character_timeout.setSingleStep(10)
            self.character_timeout.setSuffix(" ms")
            self.character_timeout.setValue(1000)
            self.vbox_layout.addWidget(l4)
            self.vbox_layout.addWidget(self.character_timeout)

            set_button = QPushButton("Set settings")
            set_button.clicked.connect(self.check_slave_settings)
            self.vbox_layout.addWidget(set_button)

            self.check_slave_settings()

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("" \
            "QLabel {" \
            "   color: red;" \
            "}" \
            "")
        self.vbox_layout.addWidget(self.error_label)

        button_row = QHBoxLayout()
        go_back_button = QPushButton("Go back")
        go_back_button.clicked.connect(lambda: self.go_back())
        send_button = QPushButton("Send")
        send_button.clicked.connect(lambda:self.viewmodel.send_MODBUS_message(self.trans_window.toPlainText().strip(), master = self.master))
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda:self.receive_window.clear())
        button_row.addWidget(go_back_button)
        button_row.addWidget(send_button)
        button_row.addWidget(clear_button)
        self.vbox_layout.addLayout(button_row)

        self.vbox_layout.addStretch()
        self.setLayout(self.vbox_layout)

    def go_back(self):
        self.viewmodel.stop_thread()
        self.viewmodel.model.close_port()
        self.switch_display(new_display=ViewCOMConfig( #on purpose, too much to save
            viewmodel=self.viewmodel,
            switch_display=self.switch_display,
            saved_config=self.viewmodel.model.COM_config
        ))

    def show_error(self, text: str):
        self.error_label.setText(text)

    def check_master_settings(self):
        master_settings = [
            ["Master", True],
            ["Slave_address",self.slave_addr.value()], # 0 to 247
            ["Transmission_timeout",self.transaction_timeout.value()], # 1 to 10 s resolution 100ms
            ["Number_of_retransmissions", self.retrans_number.value()], # 0 to 5
            ["Character_timeout", self.character_timeout.value()], # 0 to 1 s resolution 10ms
            ["Master_To_Slave", True if self.command_1.isChecked() else False]
        ]
        master_settings_dict = dict(master_settings)
        if master_settings_dict["Slave_address"] < 0 or master_settings_dict["Slave_address"] > 248:
            self.show_error("No slave address has been selected")
            return
        if not master_settings_dict["Transmission_timeout"]:
            self.show_error("No transmission timeout has been selected")
            return
        if not master_settings_dict["Number_of_retransmissions"]:
            self.show_error("No number of retransmissions has been selected")
            return
        if not master_settings_dict["Character_timeout"]:
            self.show_error("No character timeout has been selected")
            return
        if master_settings_dict["Master_To_Slave"] is None:
            self.show_error("No operation mode has been selected")
            return
        
        self.viewmodel.save_MODBUS_settings(master_settings_dict)

    def check_slave_settings(self):
        slave_settings = [
            ["Master", False],
            ["Slave_address",self.slave_addr.value()], # 1 to 247
            ["Character_timeout", self.character_timeout.value()] # 0 to 1 s resolution 10ms
        ]
        slave_settings_dict = dict(slave_settings)
        if not slave_settings_dict["Slave_address"]:
            self.show_error("No slave address has been selected")
            return
        if not slave_settings_dict["Character_timeout"]:
            self.show_error("No character timeout has been selected")
            return
        self.viewmodel.save_MODBUS_settings(MODBUS_settings=slave_settings_dict)