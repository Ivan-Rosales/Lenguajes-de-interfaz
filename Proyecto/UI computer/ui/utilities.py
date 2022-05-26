import traceback

from PyQt5 import QtWidgets


def excepthook(e_type, e_message, e_traceback):
    print(''.join(traceback.format_exception(e_type, e_message, e_traceback)))
    error("Error", f'{e_type.__name__}\n{e_message}')


def error(title, text):
    msgBox = new_dialog(title, text)
    msgBox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
    msgBox.exec()


def new_dialog(title, text):
    msgBox = QtWidgets.QMessageBox()
    msgBox.setIcon(QtWidgets.QMessageBox.Icon.Information)
    msgBox.setWindowTitle(title)
    msgBox.setText(text)
    return msgBox
