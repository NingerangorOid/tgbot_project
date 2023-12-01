from PyQt5.QtGui import QPixmap
import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QLabel


class Fontchange(QWidget):
    def __init__(self):
        super().__init__()
        self.screensize = [1900, 1000]
        self.setGeometry(0, 0, *self.screensize)
        self.setFixedSize(*self.screensize)
        self.background_color = open('backgroundcolor.txt', 'r', encoding='utf-8').read()
        self.buttons_color = open('buttonscolor.txt', 'r', encoding='utf-8').read()
        self.text_color = open('textcolor.txt', 'r', encoding='utf-8').read()
        self.initUi()

    def initUi(self):
        self.setStyleSheet(f'background-color: {self.background_color}')

        self.fontsize_label = QLineEdit(self)
        self.fontsize_label.setGeometry(200, 200, 20, 20)

        self.accept = QPushButton('Подтвердить', self)
        self.accept.clicked.connect(self.changefontsize)
        self.accept.setGeometry(250, 200, 100, 20)
        self.accept.setStyleSheet(f"background-color: {self.buttons_color};"
                                          f"color: {self.text_color}")
        self.warn = QLabel('Пожалуйста, введите целое число', self)
        self.warn.setStyleSheet('color: red')
        self.warn.setGeometry(200, 300, 250, 20)
        self.warn.hide()
        self.warn.setStyleSheet("color: red")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Fontchange()
    ex.show()
    sys.exit(app.exec())