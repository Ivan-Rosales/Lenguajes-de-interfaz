from PyQt5.QtWidgets import QMessageBox

class Notificacion(QMessageBox):
    def __init__(self):
        super().__init__()

    def set_message(self, title, string):
        self.about(self, str(title), str(string))