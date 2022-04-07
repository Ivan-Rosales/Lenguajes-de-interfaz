"""from cgi import test
from cgitb import text
from distutils.log import error
from re import S
import sqlite3
import sys
from tkinter.messagebox import NO

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic


class init:
    con = sqlite3.connect("app.db")
    cur = con.cursor()

    def __init__(self):
        app = QApplication(sys.argv)
        self.main = QMainWindow()
        uic.loadUi("./main.ui", self.main)
        self.main.show()

        self.con_funct()
        self.load_data()

        sys.exit(app.exec_())

    def load_data(self):
        users = self.cur.execute(f"SELECT * FROM user").fetchall()
        if not self.main.numCon.count() == 0:
            self.main.numCon.clear()
        self.main.numCon.addItems(user[0] for user in users)

    def con_funct(self):
        self.main.numCon.currentTextChanged.connect(self.changeStudent)
        self.main.submit.clicked.connect(self.insert_or_update)

    def changeStudent(self):
        numCom = self.main.numCon.currentText()
        alumno = self.cur.execute(
            f"SELECT * FROM user WHERE num_control='{numCom}'")
        try:
            self.actual_alumno = alumno.fetchall()[0]
            self.main.name.setText(self.actual_alumno[1])
        except IndexError:
            self.actual_alumno = None
            self.main.name.setText("")

    def insert_or_update(self):
        num_control = self.main.numCon.currentText()
        name = self.main.name.text()
        password = self.main.password.text()
        cpassword = self.main.cpassword.text()

        if password == cpassword:
            exist_user = self.cur.execute(
                f"SELECT * FROM user WHERE num_control = {num_control}")
            if len(exist_user.fetchall()) == 1:
                query = f"UPDATE User SET 'username' = '{name}', 'password' = '{password}' WHERE num_control = {num_control}"
                print(query)
                self.cur.execute(query)
            else:
                self.cur.execute(
                    f"INSERT INTO User ('num_control', 'username', 'password') VALUES ({num_control}, '{name}', '{password}')")
                self.load_data()
            self.con.commit()
        else:
            error("no coinciden las contraseñas")
"""
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

from database.database import DB
from ui.config import config


class init:
    def __init__(self, con):
        self.con: DB = con
        self.app = QApplication(sys.argv)
        self.main = QMainWindow()
        uic.loadUi("./ui/main.ui", self.main)
        self.connect_functions()

    def start(self):
        self.main.show()
        sys.exit(self.app.exec_())

    def connect_functions(self):
        self.main.pushButton.clicked.connect(lambda: self.change_window(0))

    def change_window(self, i):
        app = config()
        app.start()

    def set_string(self, res):
        request = self.con.searchStudent(res['num_control'], res['password'])
        print(request)
        if request:
            self.main.state.setText(
                f"Num. Control: {request[0]}\n"\
                f"Bienvenido, {request[1]}"
            )
        else:
            self.main.state.setText(
                f"Acceso denegado"
            )
        time.sleep(2)
        self.main.state.clear()
