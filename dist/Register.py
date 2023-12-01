import sys
import os
import sqlite3
import hashlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QScrollArea, QWidget, QVBoxLayout, \
    QFormLayout, QPushButton, QFrame, QLineEdit, QMessageBox, QColorDialog
from Mainwindow import MainWindow
from PyQt5.QtCore import QRect, QSize, QMetaObject, QCoreApplication
DB = 'database/db.db'


class RegisterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(700, 400, 500, 500)
        self.login_flag, self.password_flag = False, False
        self.create_db()

        self.register_info = QLabel('Авторизуйтесь в системе, пожалуйста', self)
        self.register_info.setGeometry(25, 10, 200, 60)

        self.login_label = QLineEdit(self)
        self.login_label.setGeometry(70, 80, 100, 20)

        self.login_info = QLabel('Придумайте никнейм', self)
        self.login_info.setGeometry(70, 60, 150, 20)

        self.password_label = QLineEdit(self)
        self.password_label.setGeometry(70, 150, 100, 20)

        self.password_info = QLabel('Придумайте пароль', self)
        self.password_info.setGeometry(70, 130, 150, 20)

        self.has_account_btn = QPushButton('У меня уже есть аккаунт', self)
        self.has_account_btn.setGeometry(70, 250, 150, 20)
        self.has_account_btn.clicked.connect(self.begin)

        self.new_account_btn = QPushButton('Зарегистрироваться', self)
        self.new_account_btn.setGeometry(70, 200, 150, 20)
        self.new_account_btn.clicked.connect(self.enter)

        self.warn_label = QLabel(self)
        self.warn_label.setGeometry(70, 300, 200, 20)
        self.warn_label.setStyleSheet("color: red")
        self.warn_label.hide()

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
                        self.ex = MainWindow()
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
               password STRING
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
            cur.execute('INSERT INTO users (user_name, password) VALUES (?, ?)', (user_name, password,))
            conn.commit()
            cur.close()


class EnterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(700, 400, 500, 500)
        self.login_flag, self.password_flag = False, False

        self.login_label = QLineEdit(self)
        self.login_label.setGeometry(70, 80, 100, 20)

        self.login_info = QLabel('Введите никнейм', self)
        self.login_info.setGeometry(70, 60, 150, 20)

        self.password_label = QLineEdit(self)
        self.password_label.setGeometry(70, 150, 100, 20)

        self.password_info = QLabel('Введите пароль', self)
        self.password_info.setGeometry(70, 130, 150, 20)

        self.enter_game_btn = QPushButton('Войти', self)
        self.enter_game_btn.setGeometry(70, 200, 150, 20)
        self.enter_game_btn.clicked.connect(self.begin)

        self.warn_label = QLabel(self)
        self.warn_label.setGeometry(70, 300, 150, 20)
        self.warn_label.setStyleSheet("color: red")
        self.warn_label.hide()

        self.register_account_btn = QPushButton('Зарегистрировать аккаунт', self)
        self.register_account_btn.setGeometry(100, 350, 200, 20)
        self.register_account_btn.clicked.connect(self.register_account)
        self.register_account_btn.hide()

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
                            self.ex = MainWindow()
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegisterForm()
    ex.show()
    sys.exit(app.exec())