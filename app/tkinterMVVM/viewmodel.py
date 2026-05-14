#callbacks go from view to viewmodel which receives an instance of model and communicates with it
from tkinterMVVM.model import Model

class TkinterViewModel:
    def __init__(self, model:Model):
        self.model = model
        pass

    def COM_ports_list(self):
        return self.model.COM_ports_find()


    #mapping of inputs to view