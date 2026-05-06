import tkinter as tk

class TkinterView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg="lightgreen")
        self.root.title("CSI laboratory 1")
        self.root.geometry("480x320")
        self.root.mainloop()

        #just functions and init to show the inputs
