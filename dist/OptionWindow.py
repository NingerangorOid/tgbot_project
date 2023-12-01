import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QColorDialog


class Options(QWidget):
    def __init__(self):
        super().__init__()
        self.screensize = [1900, 1000]
        self.setGeometry(0, 0, *self.screensize)
        self.setFixedSize(*self.screensize)
        self.background_color = open('backgroundcolor.txt', 'r', encoding='utf-8').read()
        self.buttons_color = open('buttonscolor.txt', 'r', encoding='utf-8').read()
        self.difflevel_color = open('textcolor.txt', 'r', encoding='utf-8').read()
        self.initUI()

    def initUI(self):
        self.difflevel = int(open('diflevel.txt', encoding='utf-8').read())
        self.setStyleSheet(f"background-color: {self.background_color}")

        self.exit_btn = QPushButton('Выход', self)
        self.exit_btn.resize(100, 50)
        self.exit_btn.clicked.connect(self.exit)
        self.exit_btn.setStyleSheet(f"background-color: {self.buttons_color}")

        self.difupbtn = QPushButton('︿', self)
        self.difupbtn.setGeometry(240, 280, 30, 20)
        self.difupbtn.clicked.connect(self.changedif)
        self.difupbtn.setStyleSheet(f"background-color: {self.buttons_color}")

        self.difmaxbtn = QPushButton('︽', self)
        self.difmaxbtn.setGeometry(280, 280, 30, 20)
        self.difmaxbtn.clicked.connect(self.changedif)
        self.difmaxbtn.setStyleSheet(f"background-color: {self.buttons_color}")

        self.difminbtn = QPushButton('︾', self)
        self.difminbtn.setGeometry(280, 320, 30, 20)
        self.difminbtn.clicked.connect(self.changedif)
        self.difminbtn.setStyleSheet(f"background-color: {self.buttons_color}")

        self.difdownbtn = QPushButton('﹀', self)
        self.difdownbtn.setGeometry(240, 320, 30, 20)
        self.difdownbtn.clicked.connect(self.changedif)
        self.difdownbtn.setStyleSheet(f"background-color: {self.buttons_color}")

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setGeometry(200, 300, 20, 20)
        self.lineEdit.setStyleSheet(f"color: {self.difflevel_color}")
        self.lineEdit.setText(str(self.difflevel))

        self.picbtn = QPushButton("Выберите картинку", self)
        self.picbtn.setGeometry(200, 400, 110, 50)
        self.picbtn.clicked.connect(self.setpicture)
        self.picbtn.setStyleSheet(f"background-color: {self.buttons_color}")

        self.background_color_btn = QPushButton('Выберите цвет фона', self)
        self.background_color_btn.setGeometry(200, 475, 150, 50)
        self.background_color_btn.setStyleSheet(f"background-color: {self.buttons_color}")
        self.background_color_btn.clicked.connect(self.background_setcolor)

        self.buttons_color_btn = QPushButton('Выберите цвет кнопок', self)
        self.buttons_color_btn.setGeometry(200, 550, 150, 50)
        self.buttons_color_btn.setStyleSheet(f"background-color: {self.buttons_color}")
        self.buttons_color_btn.clicked.connect(self.difflevel_setcolor)

        self.text_color_btn = QPushButton('Выберите цвет текста', self)
        self.text_color_btn.setGeometry(200, 625, 200, 50)
        self.text_color_btn.setStyleSheet(f"background-color: {self.buttons_color}")
        self.text_color_btn.clicked.connect(self.difflevel_setcolor)

    def changedif(self):
        if self.sender() is self.difupbtn:
            self.difflevel += 1
        elif self.sender() is self.difdownbtn:
            self.difflevel -= 1
        elif self.sender() is self.difminbtn:
            self.difflevel = 1
        elif self.sender() == self.difmaxbtn:
            self.difflevel = 10
        if self.difflevel == 0:
            self.difflevel += 1
        elif self.difflevel == 11:
            self.difflevel -= 1
        self.lineEdit.setText(str(self.difflevel))
        s = open('diflevel.txt', 'w', encoding='utf-8')
        s.write(str(self.difflevel))

    def exit(self):

        self.close()

    def setpicture(self):
        self.a = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        with open("picname.txt", "w", encoding='utf-8') as f:
            f.write(self.a)

    def background_setcolor(self):
        self.a = QColorDialog.getColor().name()
        with open("backgroundcolor.txt", "w", encoding='utf-8') as f:
            f.write(self.a)
        self.setStyleSheet(f"background-color: {open('backgroundcolor.txt', 'r', encoding='utf-8').read()}")

    def setcolor(self):
        self.buttons_color = open('buttonscolor.txt', 'r', encoding='utf-8').read()
        self.difflevel_color = open('textcolor.txt', 'r', encoding='utf-8').read()

        self.picbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                  f"color: {self.difflevel_color}")
        self.text_color_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                  f"color: {self.difflevel_color}")
        self.exit_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                  f"color: {self.difflevel_color}")
        self.difupbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                  f"color: {self.difflevel_color}")
        self.difmaxbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                  f"color: {self.difflevel_color}")
        self.difminbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                  f"color: {self.difflevel_color}")
        self.difdownbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                  f"color: {self.difflevel_color}")
        self.background_color_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                  f"color: {self.difflevel_color}")
        self.buttons_color_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                  f"color: {self.difflevel_color}")
        self.lineEdit.setStyleSheet(f"color: {self.difflevel_color}")

    def difflevel_setcolor(self):
        self.a = QColorDialog.getColor().name()
        if self.sender() is self.text_color_btn:
            with open("textcolor.txt", "w", encoding='utf-8') as f:
                f.write(self.a)
        else:
            with open("buttonscolor.txt", "w", encoding='utf-8') as f:
                f.write(self.a)
        self.setcolor()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Options()
    ex.show()
    sys.exit(app.exec())