import sys
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

from database.database import DB


class config:
    def start(self):
        self.conf = QWidget()
        uic.loadUi("./ui/crud.ui", self.conf)
        self.conf.show()
