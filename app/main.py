import pysideMVVM.view as v
import pysideMVVM.app_pyside as app
import pysideMVVM.viewmodel as vm
import pysideMVVM.model as m
import tkinter as tk

def init():
    print("Start")
    model = m.Model()
    viewmodel = vm.PysideViewModel(model=model)
    pyside_app = app.App(viewmodel=viewmodel)
    pyside_app.run()
 
#setup manually or read from given file

if __name__ == "__main__":
    init()