import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
import random
from PyQt5.Qt import pyqtSignal
from PyQt5.QtCore import QTimer


class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        # версия через размер картинки
        self.screensize = [1900, 1000]
        self.setGeometry(0, 0, *self.screensize)
        self.setFixedSize(*self.screensize)
        self.diflevel = int(open('diflevel.txt', encoding='utf-8').read())
        if self.diflevel == 1:
            self.imagesize = [250, 250]
        else:
            self.imagesize = [250 // (self.diflevel // 2), 250 // (self.diflevel // 2)]
        self.initUI()

    def exit(self):
        self.close()

    def initUI(self):
        self.a = open('picname.txt', encoding='utf-8').read()
        self.countdown_num = 3
        self.hits_count = 0
        self.is_pic_clickable = False
        self.background_color = open('backgroundcolor.txt', 'r', encoding='utf-8').read()
        self.setStyleSheet(f"background-color: {self.background_color}")
        self.buttons_color = open('buttonscolor.txt', 'r', encoding='utf-8').read()
        self.text_color = open('textcolor.txt', 'r', encoding='utf-8').read()

        self.tomainbtn = QPushButton('Назад', self)
        self.tomainbtn.setGeometry(0, 0, 100, 50)
        self.tomainbtn.clicked.connect(self.exit)
        self.tomainbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                          f"color: {self.text_color}")

        self.countdown_label = QLabel(self)
        self.countdown_label.setGeometry(960, 540, 200, 50)
        self.countdown_label.setText(str(self.countdown_num))
        self.countdown_label.setStyleSheet(f"color: {self.text_color}")

        self.hits_label = QLabel(self)
        self.hits_label.setGeometry(1000, 55, 20, 10)
        self.hits_label.setText(str(self.hits_count))
        self.hits_label.setStyleSheet(f"color: {self.text_color}")

        self.infolabel = QLabel('Количество попаданий:', self)
        self.infolabel.setEnabled(False)
        self.infolabel.setGeometry(850, 50, 130, 20)
        self.infolabel.setStyleSheet(f"color: {self.text_color}")

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.countdown)

        self.gametimer = QTimer(self)
        self.pixmap = QPixmap(self.a)
        self.image = ClickedLabel(self)
        self.image.clicked.connect(self.hits_counter)
        self.image.move(random.randint(0, self.screensize[0] - self.imagesize[0] * 2),
                        random.randint(0, self.screensize[1] - self.imagesize[1] * 2 - 20))
        self.image.resize(*self.imagesize)
        self.image.setScaledContents(True)
        self.image.setPixmap(self.pixmap)

    def countdown(self):
        if self.countdown_num > 0:
            self.countdown_num -= 1
            self.countdown_label.setText(str(self.countdown_num))
        else:
            self.is_pic_clickable = True
            self.timer.stop()
            self.gametimer.start(545 * (11 - self.diflevel))
            self.gametimer.timeout.connect(self.replacepic)
            self.countdown_label.hide()

    def hits_counter(self):
        if self.is_pic_clickable:
            self.hits_count += 1
            self.hits_label.setText(str(self.hits_count))

    def replacepic(self):
        self.image.move(random.randint(0, self.screensize[0] - self.imagesize[0] * 2),
                        random.randint(0, self.screensize[1] - self.imagesize[1] * 2 - 20))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    ex = GameWindow()
    ex.show()
    sys.exit(app.exec())