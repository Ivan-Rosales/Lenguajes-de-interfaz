from PyQt5.QtWidgets import QApplication

import sys

from ui.UI import Main
from uart.serial import Serial
from database.database import DB


if __name__ == '__main__':
    db = DB()
    app = QApplication(sys.argv)
    main = Main(db)
    serial = Serial("COM7", 115200, main.set_string)
    main.show()
    app.exec()
