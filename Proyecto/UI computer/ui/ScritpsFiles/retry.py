from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from PyQt5 import uic


class Retry(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 133)
        self.setWindowIcon(QIcon("ui/Images/128.png"))
        uic.loadUi("./ui/UiFiles/retry.ui", self)

