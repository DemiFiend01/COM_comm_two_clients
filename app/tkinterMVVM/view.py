import tkinter as tk
from tkinter import ttk as ttk
from tkinterMVVM.viewmodel import TkinterViewModel

class TkinterView:
    def __init__(self, window: tk.Tk, viewmodel: TkinterViewModel):
        self.window = window
        self.viewmodel = viewmodel
        self.running = True
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

    def start(self):
        self.window_init(self.window)
        self.current_display = self.port_config
        self._needs_render = True
        while self.running:
            self.update()
            
    def window_init(self, win) -> tk.Tk:
        win.configure(bg="azure")
        win.title("CSI laboratory 1")
        win.geometry("480x320")
        return win
    
    def port_config(self) -> tk.Tk:
        self.clear_screen(self.window)
        # COM port selection (combo box)
        # bit rate (can input number in a range)
        # protocol data (combo box)
        # data flow control (radio buttons or combo box)
        # terminator setting (combo box + optional custom)
        # callbacks to viewmodel

        self.COM_port_combobox = ttk.Combobox(
            self.window, values=self.viewmodel.COM_ports_list()
        )
        self.refresh_button = tk.Button(
            self.window, text="↺", command=lambda: self.switch_display(self.port_config)
        )
        self.bitrate_spinbox = tk.Text(
            self.window
        )
        self.COM_port_combobox.pack(pady=10, padx=10)
        self.refresh_button.pack(pady=10, padx=10)
        self.bitrate_spinbox.pack(pady=10, padx=10)