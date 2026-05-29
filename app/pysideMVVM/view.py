import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QLineEdit, QTextEdit, QRadioButton, QComboBox, QButtonGroup,
    QHBoxLayout, QVBoxLayout, QFrame
)
from PySide6.QtCore import Qt
from pysideMVVM.viewmodel import PysideViewModel
from pysideMVVM.view_COM_config import ViewCOMConfig

class PysideView(QMainWindow):
    def __init__(self, viewmodel: PysideViewModel):
        super().__init__()
        self.setWindowTitle("CSI laboratory")
        self.viewmodel = viewmodel
        self.bg_colour="azure"
        self.switch_display(ViewCOMConfig(viewmodel=self.viewmodel))
    
    def switch_display(self, new_display: QWidget):
        self.setCentralWidget(new_display)

    def show_error(self, text: str):
        self.error_label.config(text=text)
        
    def COM_verify_inputs(self):
        COM_values = [
            ["COM_port",self.COM_port_combobox.get().strip()],
            ["bitrate_value",self.bitrate_spinbox.get().strip()],
            ["bitrate_unit", self.bitrate_unit.get().strip()],
            ["PDU_bits", self.PDU_bits.get()],
            ["PDU_stop", self.PDU_stop_bits.get()],
            ["PDU_parity", self.PDU_combobox.get().strip()],
            ["Data_flow_control", self.Data_flow_control.get().strip()],
            ["Terminator", self.terminator_choice.get().strip()]
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
        self.switch_display(new_display=self.COM_communication_screen)

    def COM_communication_screen(self):
        self.clear_screen(self.window)

        self.comm_frame = tk.Frame(
            self.window, bg=self.bg_colour
        )
        self.comm_frame.pack(pady=5)
        self.trans_frame = tk.Frame(
            self.comm_frame, bg=self.bg_colour
        )
        frame_seperator = ttk.Separator(
            self.comm_frame, orient="vertical"
        )
        self.receive_frame = tk.Frame(
            self.comm_frame, bg=self.bg_colour
        )
        self.trans_frame.pack(side="left",padx = 10)
        frame_seperator.pack(side="left", fill="y", padx=15)
        self.receive_frame.pack(side="left",padx=10)

        trans_label = tk.Label(
            self.trans_frame, text="Transmission window in HEX", bg=self.bg_colour
        )
        self.trans_window = tk.Text (
            self.trans_frame, width = 30, height=20
        )
        trans_label.pack(side="top")
        self.trans_window.pack(padx=10)
        
        receive_label = tk.Label(
            self.receive_frame, text="Receive window in HEX", bg=self.bg_colour
        )
        self.receive_window = tk.Text(
            self.receive_frame, width = 30, height=20, state="disabled"
        )
        receive_label.pack(side="top")
        self.receive_window.pack()

        self.buttons_frame = tk.Frame(
            self.window, bg=self.bg_colour
        )
        self.buttons_frame.pack(pady=10)
        go_back_button = tk.Button(
            self.buttons_frame, text="Go back", bg=self.bg_colour, command=lambda:self.switch_display(self.COM_config_screen)
        )
        go_back_button.pack(side="left",padx=30)

        send_button = tk.Button(
            self.buttons_frame, text="Send", bg=self.bg_colour, command=lambda:self.viewmodel.send_COM_message(self.trans_window.get())
        )
        send_button.pack(side="right",padx=30)