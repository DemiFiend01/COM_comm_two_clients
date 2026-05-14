import tkinterMVVM.view as v
import tkinterMVVM.viewmodel as vm
import tkinterMVVM.model as m
import tkinter as tk

def init():
    print("Start")
    root = tk.Tk()
    model = m.Model()
    viewmodel = vm.TkinterViewModel(model=model)
    start = v.TkinterView(window= root, viewmodel=viewmodel)
 
#setup manually or read from given file

if __name__ == "__main__":
    init()