import sys

import pymysql
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from mydesign import Ui_MainWindow
from test import Vector


class Book(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.vector = Vector()
        self.start()
        self.checkin_completion = 0
        self.widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.ui.scrollAreaWidgetContents.setLayout(self.vbox)
        self.ui.scrollArea.verticalScrollBar().update()
        self.ui.textEdit.textChanged.connect(lambda:self.enter())

    def start(self):
        self.ui.pushButton.clicked.connect(lambda: self.text_searche())

    def enter(self):
        if self.ui.textEdit.toPlainText() == "\n":
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Введите описание книги! ")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        elif "\n" in self.ui.textEdit.toPlainText():
            self.text_searche()

    def clearvbox(self, L=False):
        if not L:
            L = self.vbox
        if L is not None:
            while L.count():
                item = L.takeAt(0)

                widget = item.widget()

                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearvbox(item.layout())

    def text_searche(self):
        con = pymysql.connect(host='localhost', user='root', password='nlp2', database='books')
        cur = con.cursor()
        cur.close()
        try:
            self.clearvbox()
            text = self.ui.textEdit.toPlainText()
            self.ui.textEdit.setText("")
            reternn = self.vector.similarity(text)
            self.ui.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)


        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Что то пошло не так ")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()


if __name__ == '__main__':
    app = QApplication([])
    application = Book()
    application.show()
    sys.exit(app.exec())