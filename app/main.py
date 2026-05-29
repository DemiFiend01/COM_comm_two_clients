import pysideMVVM.view as v
import pysideMVVM.viewmodel as vm
import pysideMVVM.model as m
import tkinter as tk

def init():
    print("Start")
    root = tk.Tk()
    model = m.Model()
    viewmodel = vm.PysideViewModel(model=model)
    start = v.PysideView(window= root, viewmodel=viewmodel)
 
#setup manually or read from given file

if __name__ == "__main__":
    init()