from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from database.database import DB
from ui.ScritpsFiles.notificacion import Notificacion


class Config(QWidget):
    def __init__(self, con):
        super().__init__()
        self.setFixedSize(500, 247)
        self.setWindowIcon(QIcon("ui/Images/128.png"))
        uic.loadUi("./ui/UiFiles/crud.ui", self)
        self.con: DB = con
        self.notification = Notificacion()
        self.connect_functions()
        self.load_data()

    def load_data(self):
        self.comboBox.clear()
        self.comboBox.addItems(user[0] for user in self.con.getAllStudents())

    def connect_functions(self):
        self.pushButton.clicked.connect(self.inset_or_update)
        self.pushButton_2.clicked.connect(self.delete)
        self.comboBox.currentTextChanged.connect(self.studend_changed)

    def inset_or_update(self):
        if self.lineEdit_3.text() == self.lineEdit_4.text():
            num_control = self.comboBox.currentText()
            name = self.lineEdit_2.text()
            password = self.lineEdit_3.text()

            if self.con.getStudent(num_control):
                self.con.updateStudent(num_control, name, password)
                self.load_data()
                self.comboBox.setCurrentText(num_control)
                self.notification.set_message(
                    'Actualizar', f"Se actualizo el usuario: {num_control}, {name}")
            else:
                self.con.storeStudent(num_control, name, password)
                self.load_data()
                self.comboBox.setCurrentText(num_control)
                self.notification.set_message(
                    'Añadir', f"Se añadio un nuevo usuario: {num_control}, {name}")

    def delete(self):
        self.actual_student = self.con.getStudent(self.comboBox.currentText())
        if self.actual_student:
            num_control = self.actual_student[0]
            name = self.actual_student[1]

            self.con.deleteStudent(num_control)
            self.load_data()
            self.notification.set_message(
                'Eliminar', f"Se elimino el usuario: {num_control}, {name}")

    def studend_changed(self):
        self.actual_student = self.con.getStudent(self.comboBox.currentText())
        if self.actual_student:
            self.lineEdit_2.setText(self.actual_student[1])
