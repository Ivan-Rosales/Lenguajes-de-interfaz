import sys
import time
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

from database.database import DB
from ui.config import Config


class Main(QMainWindow):    
    def __init__(self, con):
        super().__init__()
        self.con: DB = con
        uic.loadUi("./ui/main.ui", self)
        self.connect_functions()

        self.conf = Config(con)

    def set_string(self, res):
        request = self.con.searchStudent(res['num_control'], res['password'])
        if request:
            self.state.setText(
                f"Num. Control: {request[0]}\n"\
                f"Bienvenido, {request[1]}"
            )
            return request[1]
        else:
            self.state.setText(
                f"Acceso denegado\n"\
                f"Num. Control: {res['num_control']}\n"\
                f"Contraseña: {res['password']}"
            )
            return "False"

    def connect_functions(self):
        self.pushButton.clicked.connect(self.show_conf)

    def show_conf(self):
        self.conf.show()
