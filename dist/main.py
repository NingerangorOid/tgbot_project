from PyQt5.QtGui import QPixmap
import random
import sys
import sqlite3
import hashlib
from PyQt5.QtCore import QTimer
from PyQt5.Qt import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, \
    QColorDialog, QTableWidgetItem
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtGui, QtWidgets
from tableform_ui import Ui_MainWindow
import os
DB = 'database/db.db'


class MainWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.screensize = [1900, 1000]
        self.setGeometry(0, 0, *self.screensize)
        self.setFixedSize(*self.screensize)
        self.username = username
        self.initUi()

    def initUi(self):
        self.background_color = open('backgroundcolor.txt', 'r', encoding='utf-8').read()
        self.buttons_color = open('buttonscolor.txt', 'r', encoding='utf-8').read()
        self.setStyleSheet(f"background-color: {self.background_color}")
        self.difflevel_color = open('textcolor.txt', 'r', encoding='utf-8').read()

        self.font_size = int(open('fontsize.txt', 'r', encoding='utf-8').read())

        self.my_font = QFont("Calibri", self.font_size)

        self.playbtn = QPushButton('Начать', self)
        self.playbtn.setGeometry(200, 100, 100, 50)
        self.playbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                   f"color: {self.difflevel_color}")
        self.playbtn.clicked.connect(self.game)
        self.playbtn.setFont(self.my_font)

        self.hello_label = QLabel(f'Здравствуй, {self.username}', self)
        self.hello_label.setFont(self.my_font)
        self.hello_label.setStyleSheet(f"color: {self.difflevel_color}")
        self.hello_label.setGeometry(200, 50, 150, 20)

        self.exitbtn = QPushButton("Выход", self)
        self.exitbtn.setGeometry(200, 300, 100, 50)
        self.exitbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                   f"color: {self.difflevel_color}")
        self.exitbtn.clicked.connect(self.exit)
        self.exitbtn.setFont(self.my_font)

        self.optionsbtn = QPushButton("Настройки", self)
        self.optionsbtn.setGeometry(200, 200, 100, 50)
        self.optionsbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                      f"color: {self.difflevel_color}")
        self.optionsbtn.clicked.connect(self.options)
        self.optionsbtn.setFont(self.my_font)

    def exit(self):
        sys.exit()

    def options(self):
        self.op = Options(self.username)
        self.op.show()
        self.close()

    def game(self):
        self.game = GameWindow(self.username)
        self.game.show()
        self.close()


class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()


class GameWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        # версия через размер картинки
        self.screensize = [1900, 1000]
        self.setGeometry(0, 0, *self.screensize)
        self.setFixedSize(*self.screensize)
        self.diflevel = int(open('diflevel.txt', encoding='utf-8').read())
        self.username = username
        self.imagesize = [50, 50]
        self.initUI()

    def exit(self):
        self.close()
        self.ex = MainWindow(self.username)
        self.ex.show()

    def initUI(self):
        self.a = open('picname.txt', encoding='utf-8').read()
        self.countdown_num = 3
        self.hits_count = 0
        self.is_pic_clickable = False
        self.font_size = int(open('fontsize.txt', 'r', encoding='utf-8').read())
        self.my_font = QFont("Calibri", self.font_size)
        self.countdown_font = QFont('Calibri', 30)
        self.background_color = open('backgroundcolor.txt', 'r', encoding='utf-8').read()
        self.setStyleSheet(f"background-color: {self.background_color}")
        self.buttons_color = open('buttonscolor.txt', 'r', encoding='utf-8').read()
        self.text_color = open('textcolor.txt', 'r', encoding='utf-8').read()
        self.seconds = 120 - (self.diflevel * 6)

        self.tomainbtn = QPushButton('Назад', self)
        self.tomainbtn.setGeometry(0, 0, 100, 50)
        self.tomainbtn.clicked.connect(self.exit)
        self.tomainbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                     f"color: {self.text_color}")
        self.tomainbtn.setFont(self.my_font)

        self.countdown_Edit = QLineEdit(f'У вас осталось {self.seconds} секунд', self)
        self.countdown_Edit.setEnabled(False)
        self.countdown_Edit.setGeometry(1690, 35, 200, 30)

        self.countdown_start_label = QLabel(self)
        self.countdown_start_label.setGeometry(960, 540, 200, 50)
        self.countdown_start_label.setText(str(self.countdown_num))
        self.countdown_start_label.setStyleSheet(f"color: {self.text_color}")
        self.countdown_start_label.setFont(self.countdown_font)

        self.hits_label = QLabel(self)
        self.hits_label.setGeometry(960, 42, 150, 80)
        self.hits_label.setText(str(self.hits_count))
        self.hits_label.setStyleSheet(f"color: {self.text_color}")
        self.hits_label.setFont(self.countdown_font)

        self.infolabel = QLabel('Количество попаданий:', self)
        self.infolabel.setEnabled(False)
        self.infolabel.setGeometry(550, 50, 400, 60)
        self.infolabel.setStyleSheet(f"color: {self.text_color}")
        self.infolabel.setFont(self.countdown_font)

        self.endgame_label = QLabel(self)
        self.endgame_label.setStyleSheet(f"color: {self.text_color}")
        self.endgame_label.setGeometry(550, 550, 650, 60)
        self.endgame_label.setFont(self.countdown_font)
        self.endgame_label.hide()

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
            self.countdown_start_label.setText(str(self.countdown_num))
        else:
            self.is_pic_clickable = True
            self.timer.stop()
            self.gametimer.start(545 * (11 - self.diflevel))
            self.gametimer.timeout.connect(self.replacepic)
            self.countdown_start_label.hide()

    def hits_counter(self):
        if self.is_pic_clickable:
            self.hits_count += 1
            self.hits_label.setText(str(self.hits_count))

    def replacepic(self):
        self.seconds -= (1000 // 545 * (11 - self.diflevel))
        if self.seconds <= 0:
            self.countdown_Edit.setText("У вас осталось 0 секунд")
            self.is_pic_clickable = False
            self.gametimer.stop()

            if str(self.hits_count)[-1] in ['5', '6', '7', '8', '9', '0']:
                self.endgame_label.setText(f'Игра окончена, вы набрали {self.hits_count} очков')
            elif str(self.hits_count)[-1] in ['2', '3', '4']:
                self.endgame_label.setText(f'Игра окончена, вы набрали {self.hits_count} очка')
            elif str(self.hits_count)[-1] == '1':
                self.endgame_label.setText(f'Игра окончена, вы набрали {self.hits_count} очкo')
            self.endgame_label.show()
            self.image.hide()
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute('SELECT highscore FROM users WHERE user_name = ?', (self.username,))
            user = cur.fetchone()
            if user[0] < self.hits_count:
                cur.execute(f"UPDATE users SET highscore = ? WHERE user_name = ?",
                            (self.hits_count, self.username))
                conn.commit()
                cur.close()

        self.countdown_Edit.setText(f"У вас осталось {round(self.seconds)} секунд")
        self.image.move(random.randint(0, self.screensize[0] - self.imagesize[0] * 2),
                        random.randint(0, self.screensize[1] - self.imagesize[1] * 2 - 20))


class Options(QWidget):
    def __init__(self, username):
        super().__init__()
        self.screensize = [1900, 1000]
        self.setGeometry(0, 0, *self.screensize)
        self.setFixedSize(*self.screensize)
        self.background_color = open('backgroundcolor.txt', 'r', encoding='utf-8').read()
        self.buttons_color = open('buttonscolor.txt', 'r', encoding='utf-8').read()
        self.text_color = open('textcolor.txt', 'r', encoding='utf-8').read()
        self.username = username
        self.initUI()

    def initUI(self):
        self.difflevel = int(open('diflevel.txt', encoding='utf-8').read())
        self.setStyleSheet(f"background-color: {self.background_color}")
        self.font_size = int(open('fontsize.txt', 'r', encoding='utf-8').read())
        self.my_font = QFont("Calibri", self.font_size)
        self.good_font = QFont("Calibri", 16)

        self.exit_btn = QPushButton('Выход', self)

        self.exit_btn.resize(100, 50)
        self.exit_btn.clicked.connect(self.exit)
        self.exit_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                    f"color: {self.text_color}")
        self.exit_btn.setFont(self.my_font)

        self.difupbtn = QPushButton('︿', self)
        self.difupbtn.setGeometry(240, 280, 30, 20)
        self.difupbtn.clicked.connect(self.changedif)
        self.difupbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                    f"color: {self.text_color}")
        self.difupbtn.setFont(self.my_font)

        self.difmaxbtn = QPushButton('︽', self)
        self.difmaxbtn.setGeometry(280, 280, 30, 20)
        self.difmaxbtn.clicked.connect(self.changedif)
        self.difmaxbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                     f"color: {self.text_color}")
        self.difmaxbtn.setFont(self.my_font)

        self.difminbtn = QPushButton('︾', self)
        self.difminbtn.setGeometry(280, 320, 30, 20)
        self.difminbtn.clicked.connect(self.changedif)
        self.difminbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                     f"color: {self.text_color}")
        self.difminbtn.setFont(self.my_font)

        self.difdownbtn = QPushButton('﹀', self)
        self.difdownbtn.setGeometry(240, 320, 30, 20)
        self.difdownbtn.clicked.connect(self.changedif)
        self.difdownbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                      f"color: {self.text_color}")
        self.difdownbtn.setFont(self.my_font)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setGeometry(200, 300, 20, 20)
        self.lineEdit.setStyleSheet(f"color: {self.text_color}")
        self.lineEdit.setText(str(self.difflevel))
        self.lineEdit.setFont(self.my_font)

        self.picbtn = QPushButton("Выберите картинку", self)
        self.picbtn.setGeometry(200, 400, 110, 50)
        self.picbtn.clicked.connect(self.setpicture)
        self.picbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                  f"color: {self.text_color}")
        self.picbtn.setFont(self.my_font)

        self.background_color_btn = QPushButton('Выберите цвет фона', self)
        self.background_color_btn.setGeometry(200, 475, 150, 50)
        self.background_color_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                                f"color: {self.text_color}")
        self.background_color_btn.clicked.connect(self.background_setcolor)
        self.background_color_btn.setFont(self.my_font)

        self.buttons_color_btn = QPushButton('Выберите цвет кнопок', self)
        self.buttons_color_btn.setGeometry(200, 550, 150, 50)
        self.buttons_color_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                             f"color: {self.text_color}")
        self.buttons_color_btn.clicked.connect(self.difflevel_setcolor)
        self.buttons_color_btn.setFont(self.my_font)

        self.text_color_btn = QPushButton('Выберите цвет текста', self)
        self.text_color_btn.setGeometry(200, 625, 200, 50)
        self.text_color_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                          f"color: {self.text_color}")
        self.text_color_btn.clicked.connect(self.difflevel_setcolor)
        self.text_color_btn.setFont(self.my_font)

        self.font_size_btn = QPushButton('Изменить размер шрифта', self)
        self.font_size_btn.setGeometry(200, 700, 200, 50)
        self.font_size_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                         f"color: {self.text_color}")
        self.font_size_btn.clicked.connect(self.setfontsize)
        self.font_size_btn.setFont(self.my_font)

        self.show_globals = QPushButton('Увидеть глобальные рекорды', self)
        self.show_globals.setGeometry(200, 775, 200, 50)
        self.show_globals.setStyleSheet(f"background-color: {self.buttons_color};"
                                        f"color: {self.text_color}")
        self.show_globals.clicked.connect(self.globals)
        self.show_globals.setFont(self.my_font)

        self.conn = sqlite3.connect(DB)
        self.cur = self.conn.cursor()
        self.cur.execute(f"""SELECT highscore FROM users WHERE user_name = '{self.username}'""")
        self.record = self.cur.fetchone()[0]

        self.record_Label = QLabel(f"Ваш рекорд: {self.record}", self)
        self.record_Label.setGeometry(500, 290, 200, 20)
        self.record_Label.setStyleSheet(f"color: {self.text_color}")
        self.record_Label.setFont(self.good_font)

    def globals(self):
        self.ex = Globals()
        self.ex.show()

    def setfontsize(self):
        self.ex = Fontchange(self.username)
        self.ex.show()
        self.close()

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
        self.ex = MainWindow(self.username)
        self.ex.show()
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
        self.text_color = open('textcolor.txt', 'r', encoding='utf-8').read()

        self.picbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                  f"color: {self.text_color}")
        self.text_color_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                          f"color: {self.text_color}")
        self.exit_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                    f"color: {self.text_color}")
        self.difupbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                    f"color: {self.text_color}")
        self.difmaxbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                     f"color: {self.text_color}")
        self.difminbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                     f"color: {self.text_color}")
        self.difdownbtn.setStyleSheet(f"background-color: {self.buttons_color};"
                                      f"color: {self.text_color}")
        self.background_color_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                                f"color: {self.text_color}")
        self.buttons_color_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                             f"color: {self.text_color}")
        self.lineEdit.setStyleSheet(f"color: {self.text_color}")
        self.font_size_btn.setStyleSheet(f"background-color: {self.buttons_color};"
                                         f"color: {self.text_color}")
        self.show_globals.setStyleSheet(f"background-color: {self.buttons_color};"
                                        f"color: {self.text_color}")
        self.record_Label.setStyleSheet(f"color: {self.text_color}")

    def difflevel_setcolor(self):
        self.a = QColorDialog.getColor().name()
        if self.sender() is self.text_color_btn:
            with open("textcolor.txt", "w", encoding='utf-8') as f:
                f.write(self.a)
        else:
            with open("buttonscolor.txt", "w", encoding='utf-8') as f:
                f.write(self.a)
        self.setcolor()


class Fontchange(QWidget):
    def __init__(self, username):
        super().__init__()
        self.screensize = [1900, 1000]
        self.setGeometry(0, 0, *self.screensize)
        self.setFixedSize(*self.screensize)
        self.background_color = open('backgroundcolor.txt', 'r', encoding='utf-8').read()
        self.buttons_color = open('buttonscolor.txt', 'r', encoding='utf-8').read()
        self.text_color = open('textcolor.txt', 'r', encoding='utf-8').read()
        self.username = username
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

    def changefontsize(self):
        if self.fontsize_label.text().isdigit():
            self.a = self.fontsize_label.text()
            with open("fontsize.txt", "w", encoding='utf-8') as f:
                f.write(self.a)
            self.close()
            self.ex = Options(self.username)
            self.ex.show()
        else:
            self.warn.show()


class RegisterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(700, 400, 500, 500)
        self.login_flag, self.password_flag = False, False
        self.create_db()

        self.font_size = int(open('fontsize.txt', 'r', encoding='utf-8').read())
        self.my_font = QFont("Calibri", self.font_size)

        self.register_info = QLabel('Авторизуйтесь в системе, пожалуйста', self)
        self.register_info.setGeometry(25, 10, 250, 60)
        self.register_info.setFont(self.my_font)

        self.login_label = QLineEdit(self)
        self.login_label.setGeometry(70, 80, 100, 20)
        self.login_label.setFont(self.my_font)

        self.login_info = QLabel('Придумайте никнейм', self)
        self.login_info.setGeometry(70, 60, 150, 20)
        self.login_info.setFont(self.my_font)

        self.password_label = QLineEdit(self)
        self.password_label.setGeometry(70, 150, 100, 20)
        self.password_label.setFont(self.my_font)

        self.password_info = QLabel('Придумайте пароль', self)
        self.password_info.setGeometry(70, 130, 150, 20)
        self.password_info.setFont(self.my_font)

        self.has_account_btn = QPushButton('У меня уже есть аккаунт', self)
        self.has_account_btn.setGeometry(70, 250, 150, 20)
        self.has_account_btn.clicked.connect(self.begin)
        self.has_account_btn.setFont(self.my_font)

        self.new_account_btn = QPushButton('Зарегистрироваться', self)
        self.new_account_btn.setGeometry(70, 200, 150, 20)
        self.new_account_btn.clicked.connect(self.enter)
        self.new_account_btn.setFont(self.my_font)

        self.warn_label = QLabel(self)
        self.warn_label.setGeometry(70, 300, 200, 20)
        self.warn_label.setStyleSheet("color: red")
        self.warn_label.hide()
        self.warn_label.setFont(self.my_font)

    def enter(self):
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute('SELECT user_name FROM users WHERE user_name = ?', (self.login_label.text(),))
        user = cur.fetchone()
        cur.execute('SELECT password FROM users WHERE password = ?',
                    (hashlib.md5(bytes(self.password_label.text(), encoding='utf-8')).hexdigest(),))
        password = cur.fetchone()
        if self.login_label.text():
            if self.password_label.text():
                if user:
                    if self.login_label.text() == user[0]:
                        self.warn_label.setText('Это имя пользователя уже занято')
                        self.warn_label.show()
                else:
                    if not password:
                        self.register_user()
                        self.ex = MainWindow(self.login_label.text())
                        self.ex.show()
                        self.close()
                    else:
                        if hashlib.md5(bytes(self.password_label.text(), encoding='utf-8')).hexdigest() == password[0]:
                            self.warn_label.setText('Этот пароль уже занят')
                            self.warn_label.show()

            else:
                self.warn_label.setText('Вы забыли ввести пароль')
                self.warn_label.show()
        else:
            self.warn_label.setText('Вы забыли ввести логин')
            self.warn_label.show()

    def begin(self):
        self.ex = EnterForm()
        self.ex.show()
        self.close()

    def create_db(self):
        if not os.path.exists(DB):
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute(
                """CREATE TABLE IF NOT EXISTS users(
               user_name STRING,
               password STRING,
               highscore INTEGER
               );""")
            conn.commit()
            cur.execute(
                """CREATE TABLE IF NOT EXISTS global_records(
               user_name STRING,
               highscore STRING
               );""")
            conn.commit()

    def register_user(self):
        user_name = self.login_label.text()
        password = hashlib.md5(bytes(self.password_label.text(), encoding='utf-8')).hexdigest()
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE user_name = ?', (user_name,))
        user = cur.fetchall()
        if not user:
            cur.execute('INSERT INTO users (user_name, password, highscore) VALUES (?, ?, ?)',
                        (user_name, password, 0,))
            conn.commit()
            cur.close()


class EnterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(700, 400, 500, 500)
        self.font_size = int(open('fontsize.txt', 'r', encoding='utf-8').read())
        self.my_font = QFont("Calibri", self.font_size)

        self.login_label = QLineEdit(self)
        self.login_label.setGeometry(70, 80, 100, 20)
        self.login_label.setFont(self.my_font)

        self.login_info = QLabel('Введите никнейм', self)
        self.login_info.setGeometry(70, 60, 150, 20)
        self.login_info.setFont(self.my_font)

        self.password_label = QLineEdit(self)
        self.password_label.setGeometry(70, 150, 100, 20)
        self.password_label.setFont(self.my_font)

        self.password_info = QLabel('Введите пароль', self)
        self.password_info.setGeometry(70, 130, 150, 20)
        self.password_info.setFont(self.my_font)

        self.enter_game_btn = QPushButton('Войти', self)
        self.enter_game_btn.setGeometry(70, 200, 150, 20)
        self.enter_game_btn.clicked.connect(self.begin)
        self.enter_game_btn.setFont(self.my_font)

        self.warn_label = QLabel(self)
        self.warn_label.setGeometry(70, 300, 150, 20)
        self.warn_label.setStyleSheet("color: red")
        self.warn_label.hide()
        self.warn_label.setFont(self.my_font)

        self.register_account_btn = QPushButton('Зарегистрировать аккаунт', self)
        self.register_account_btn.setGeometry(100, 350, 200, 20)
        self.register_account_btn.clicked.connect(self.register_account)
        self.register_account_btn.hide()
        self.register_account_btn.setFont(self.my_font)

    def register_account(self):
        self.ex = RegisterForm()
        self.ex.show()
        self.close()

    def begin(self):
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute(f"""SELECT user_name FROM users WHERE user_name = '{self.login_label.text()}'""")
        self.username = cur.fetchone()
        cur.execute(f"""SELECT password FROM users WHERE user_name = '{self.login_label.text()}'""")
        self.password = cur.fetchone()
        if self.login_label.text():
            if self.password_label.text():
                if self.username != None:
                    if self.password != None:
                        self.pasword = self.password[0]
                        if self.pasword == hashlib.md5(
                                bytes(self.password_label.text(), encoding='utf-8')).hexdigest():
                            self.ex = MainWindow(self.login_label.text())
                            self.ex.show()
                            self.close()
                        else:
                            self.warn_label.setText('Неверный пароль')
                            self.warn_label.show()
                            self.register_account_btn.hide()
                    else:
                        self.warn_label.setText('Неверный пароль')
                        self.warn_label.show()
                        self.register_account_btn.hide()
                else:
                    self.warn_label.setText('Нет такого аккаунта')
                    self.warn_label.show()
                    self.register_account_btn.show()
            else:
                self.warn_label.setText('Вы забыли ввести пароль')
                self.warn_label.show()
                self.register_account_btn.hide()
        else:
            self.warn_label.setText('Вы забыли ввести логин')
            self.warn_label.show()
            self.register_account_btn.hide()


class Globals(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("database/db.db")
        cur = self.con.cursor()
        result = cur.execute(f'''select user_name, highscore from global_records''').fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.pushButton.clicked.connect(self.exit)

    def exit(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegisterForm()
    ex.show()
    sys.exit(app.exec())