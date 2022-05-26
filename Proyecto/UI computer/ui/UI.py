from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from database.database import DB
from ui.ScritpsFiles.config import Config


class Main(QMainWindow):
    state: QLabel = None
    states = []

    def __init__(self, con):
        super().__init__()
        self.setFixedSize(500, 230)
        self.setWindowIcon(QIcon("ui/Images/128.png"))
        uic.loadUi("./ui/UiFiles/main.ui", self)

        self.connect_functions()

        self.con: DB = con

        self.conf = Config(con)

    def set_string(self, res):
        num_control = str(res['num_control']).strip()
        password = str(res['password']).strip()

        request = self.con.searchStudent(num_control, password)
        if request:
            self.state.setText(
                self.state.text() +
                f"{datetime.now()} | Acceso permitido, Num. Control: {request[0]}\n"
            )
            return request[1]
        else:
            self.state.setText(
                self.state.text() +
                f"{datetime.now()} | Acceso denegado, Num. Control: {num_control}\n"
            )
            return "False"

    def connect_functions(self):
        self.pushButton.clicked.connect(self.show_conf)

    def show_conf(self):
        self.conf.show()
