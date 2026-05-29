#callbacks go from view to viewmodel which receives an instance of model and communicates with it
from pysideMVVM.model import Model

class PysideViewModel:
    def __init__(self, model:Model):
        self.model = model
        pass

    def COM_ports_list(self):
        return self.model.COM_ports_find()

    def save_COM_config(self, COM_config: dict):
        self.model.set_COM_config(COM_config)

    def send_COM_message(self, text):
        self.model.send_COM_message(text)
