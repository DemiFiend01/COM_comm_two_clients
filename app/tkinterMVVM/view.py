import tkinter as tk
from tkinter import ttk as ttk
from tkinterMVVM.viewmodel import TkinterViewModel

class TkinterView:
    def __init__(self, window: tk.Tk, viewmodel: TkinterViewModel):
        self.window = window
        self.viewmodel = viewmodel
        self.running = True
        self.bg_colour="azure"
        self.start()

    def clear_screen(self, win: tk.Tk):
        for widget in win.winfo_children():
            widget.destroy()
    
    def update(self):
        self.window.update_idletasks()
        self.window.update()
        if self._needs_render:
            self.render()

    def render(self):
        self.current_display()
        self._needs_render = False
    
    def switch_display(self, new_display):
        self.current_display = new_display
        self._needs_render = True
        self.render()

    def start(self):
        self.window_init(self.window)
        self.current_display = self.COM_config_screen
        self._needs_render = True
        while self.running:
            self.update()
            
    def window_init(self, win) -> tk.Tk:
        win.configure(bg=self.bg_colour)
        win.title("CSI laboratory 1")
        win.geometry("680x520")
        return win
    
    def COM_config_screen(self) -> tk.Tk:
        self.clear_screen(self.window)
        # COM port selection (combo box)
        # bit rate (can input number in a range)
        # protocol data (combo box)
        # data flow control (radio buttons or combo box)
        # terminator setting (combo box + optional custom)
        # callbacks to viewmodel
        self.COM_frame = tk.Frame (
            self.window, bg=self.bg_colour
        )
        self.COM_frame.pack(pady=10)

        COM_label = tk.Label(
            self.COM_frame, text="COM port: ", bg=self.bg_colour
        )
        self.COM_port_combobox = ttk.Combobox(
            self.COM_frame, values=self.viewmodel.COM_ports_list()
        )
        self.refresh_button = tk.Button(
            self.COM_frame, text="↺", command=lambda: self.switch_display(self.COM_config_screen)
        )
        COM_label.pack(side="left")
        self.COM_port_combobox.pack(side="left", padx=5)
        self.refresh_button.pack(side="left", padx=5)

        
        self.bitrate_frame = tk.Frame( self.window, bg=self.bg_colour)
        bitrate_label = tk.Label(
            self.bitrate_frame, text="Bitrate (from 150 bits/s to 115 kb/s):", bg=self.bg_colour
        )
        self.bitrate_frame.pack(pady=10)
        self.bitrate_spinbox = tk.Entry(
            self.bitrate_frame, width=10
        )
        self.bitrate_unit = tk.StringVar(value="bit")
        self.bitrate_bit_check = tk.Radiobutton(
            self.bitrate_frame, text="bit/s", variable = self.bitrate_unit, value="bit", bg=self.bg_colour
        )
        self.bitrate_kb_check = tk.Radiobutton(
            self.bitrate_frame, text="kb/s", variable= self.bitrate_unit, value="kb", bg=self.bg_colour
        )
        bitrate_label.pack(side="top")
        self.bitrate_spinbox.pack(side="left", padx=10)
        self.bitrate_bit_check.pack(padx=10)
        self.bitrate_kb_check.pack(padx=10)

        self.PDU_frame = tk.Frame(
            self.window, bg=self.bg_colour
        )
        self.PDU_frame.pack(pady=10)
        PDU_label = tk.Label(
            self.PDU_frame, text="PDU values:", bg=self.bg_colour
        )
        self.PDU_bits = tk.IntVar(value=7)
        self.PDU_stop_bits = tk.IntVar(value=1)
        self.PDU_bits_7 = tk.Radiobutton (
            self.PDU_frame, text="7 bits data field", variable=self.PDU_bits, value=7, bg=self.bg_colour
        )
        self.PDU_bits_8 = tk.Radiobutton (
            self.PDU_frame, text="8 bits data field", variable=self.PDU_bits, value=8, bg=self.bg_colour
        ) 
        self.PDU_combobox = ttk.Combobox (
            self.PDU_frame, values=["Even parity","Odd parity","None parity"]
        )
        self.PDU_stop_bit_1 = tk.Radiobutton (
            self.PDU_frame, text="1 stop bit", variable=self.PDU_stop_bits, value=1, bg=self.bg_colour
        )
        self.PDU_stop_bit_2 = tk.Radiobutton (
            self.PDU_frame, text="2 stop bits", variable=self.PDU_stop_bits, value=2, bg=self.bg_colour
        )

        PDU_label.pack(side="top", padx=5)
        self.PDU_bits_7.pack(side="left",padx=5)
        self.PDU_bits_8.pack(side="left",padx=5)
        self.PDU_combobox.pack(side="right",padx=5)
        self.PDU_stop_bit_1.pack(padx=5)
        self.PDU_stop_bit_2.pack(padx=5)

        self.Data_flow_frame = tk.Frame (
            self.window, bg=self.bg_colour
        )
        self.Data_flow_frame.pack(pady=10)
        Data_flow_label =  tk.Label(
            self.Data_flow_frame, text="Data flow control:", bg=self.bg_colour
        )
        self.Data_flow_control = ttk.Combobox (
            self.Data_flow_frame, 
            values=["None","DTR/DSR handshake","RTS/CTS handshake","XON/XOFF protocol"]
        )
        Data_flow_label.pack(side="left", padx=5)
        self.Data_flow_control.pack(side="right", padx=5)

        self.terminator_frame = tk.Frame(
            self.window, bg=self.bg_colour
        )
        self.terminator_frame.pack(pady=10)
        terminator_label = tk.Label (
            self.terminator_frame, text="Terminator settings, insert value if custom:", bg=self.bg_colour
        )
        self.terminator_choice = ttk.Combobox (
            self.terminator_frame, values=["None","CR","LF","CR-LF","Other - insert"]
        )
        terminator_label.pack(padx=5)
        self.terminator_choice.pack(padx=10)

        continue_button = tk.Button(
            self.window, text="Continue", bg=self.bg_colour, command=lambda:self.switch_display(new_display=self.COM_verify_inputs)
        )
        continue_button.pack()

    def show_error(self, text: str):
        error_label = tk.Label (
            self.window, text= text, bg=self.bg_colour, fg="red"
        )
        error_label.pack()

    def COM_verify_inputs(self):
        #save all values somehow
        self.COM_port = self.COM_port_combobox.get().strip()
        if not self.COM_port:
            self.show_error("No port has been selected")
            return
        #Add for all
        self.switch_display(new_display=self.COM_communication_screen)

    def COM_communication_screen(self):
        self.clear_screen(self.window)

        go_back_button = tk.Button(
            self.window, text="Go back", bg=self.bg_colour, command=lambda:self.switch_display(self.COM_config_screen)
        )
        go_back_button.pack(padx=10)