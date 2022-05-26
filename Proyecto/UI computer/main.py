from PyQt5.QtWidgets import QApplication

import sys

from ui.UI import Main
from uart.uartClass import Uart
from database.database import DB
from ui.utilities import excepthook


if __name__ == '__main__':
    db = DB()
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    main = Main(db)
    serial = Uart("COM7", 115200, main.set_string)
    main.show()
    app.exec()
