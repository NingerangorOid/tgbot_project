import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QColorDialog
from OptionWindow import Options
from Gamewindow import GameWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.screensize = [1900, 1000]
        self.setGeometry(0, 0, *self.screensize)
        self.setFixedSize(*self.screensize)
        self.initUi()

    def initUi(self):
        self.background_color = open('backgroundcolor.txt', 'r', encoding='utf-8').read()
        self.buttons_color = open('buttonscolor.txt', 'r', encoding='utf-8').read()
        self.setStyleSheet(f"background-color: {self.background_color}")

        self.playbtn = QPushButton('Начать', self)
        self.playbtn.setGeometry(200, 100, 100, 50)
        self.playbtn.setStyleSheet(f"background-color: {self.buttons_color}")
        self.playbtn.clicked.connect(self.game)

        self.exitbtn = QPushButton("Выход", self)
        self.exitbtn.setGeometry(200, 300, 100, 50)
        self.exitbtn.setStyleSheet(f"background-color: {self.buttons_color}")
        self.exitbtn.clicked.connect(self.exit)

        self.optionsbtn = QPushButton("Настройки", self)
        self.optionsbtn.setGeometry(200, 200, 100, 50)
        self.optionsbtn.setStyleSheet(f"background-color: {self.buttons_color}")
        self.optionsbtn.clicked.connect(self.options)

    def exit(self):
        sys.exit()

    def options(self):
        self.op = Options()
        self.op.show()


    def game(self):
        self.game = GameWindow()
        self.game.show()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())