import sys
import os
import sqlite3
import hashlib

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QScrollArea, QWidget, QVBoxLayout, \
    QFormLayout, QPushButton, QFrame, QLineEdit, QMessageBox, QColorDialog

from PyQt5.QtCore import QRect, QSize, QMetaObject, QCoreApplication
from PyQt5.QtGui import QColor, QCursor, QPixmap

DB = 'databases/db.db'

class Register(QWidget):
    def __init__(self, parent=None):
        super(Register, self).__init__(parent, QtCore.Qt.Window)

    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(373, 204)
        Dialog.setMaximumSize(QtCore.QSize(373, 204))
        Dialog.setStyleSheet("font: 75 11pt \"Rubik\";")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 161, 106))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(170, 0, 201, 101))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.textChanged.connect(self.check_input)
        self.lineEdit.EchoMode(QLineEdit.Password)
        self.lineEdit.setPlaceholderText('Придумайте имя')
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setMaxLength(30)
        self.verticalLayout_3.addWidget(self.lineEdit)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.EchoMode(QLineEdit.Password)
        self.lineEdit_2.textChanged.connect(self.check_input)
        self.lineEdit_2.setPlaceholderText('Придумайте пароль')
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_3.addWidget(self.lineEdit_2)

        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 110, 351, 91))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.register_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.register_btn.setObjectName("register_button")
        self.register_btn.clicked.connect(self.register_user)
        self.register_btn.setEnabled(False)
        self.register_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.verticalLayout_4.addWidget(self.register_btn)

        self.login_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.login_btn.setObjectName("login_button")
        self.login_btn.clicked.connect(self.open_log_window)
        self.login_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.verticalLayout_4.addWidget(self.login_btn)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def register_user(self):
        user_name = self.lineEdit.text()
        password = hashlib.md5(bytes(self.lineEdit_2.text(), encoding='utf-8')).hexdigest()

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE user_name = ?', (user_name,))
        user = cur.fetchall()
        if not user:
            cur.execute('INSERT INTO users (user_name, password) VALUES (?, ?)', (user_name, password,))
            conn.commit()
            cur.close()

            self.MainWindow = QtWidgets.QMainWindow()
            self.ui = NotesMainMenu(user_name)
            self.ui.setupUi(self.MainWindow)
            self.MainWindow.show()
            self.Dialog.close()
        else:
            QMessageBox.critical(self, 'Ошибка регистрации!', 'Это имя уже занято!')

    def open_log_window(self):
        self.prog = Login()
        self.Dialog1 = QtWidgets.QDialog()
        self.prog.setupUi(self.Dialog1)
        self.Dialog1.show()
        self.Dialog.close()

    def check_input(self):
        if self.lineEdit.text() and self.lineEdit_2.text():
            self.register_btn.setEnabled(True)
        else:
            self.register_btn.setEnabled(False)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Регистрация"))
        self.label.setText(_translate("Dialog", "Имя: "))
        self.label_2.setText(_translate("Dialog", "Пароль: "))
        self.register_btn.setText(_translate("Dialog", "Зарегистрироваться"))
        self.login_btn.setText(_translate("Dialog", "У меня есть аккаунт"))


class Login(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(373, 204)
        Dialog.setMaximumSize(QtCore.QSize(373, 204))
        Dialog.setMinimumSize(QtCore.QSize(373, 204))
        Dialog.setStyleSheet("font: 75 11pt \"Rubik\";")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 161, 106))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(170, 0, 201, 101))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.textChanged.connect(self.check_input)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_3.addWidget(self.lineEdit)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_2.textChanged.connect(self.check_input)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_3.addWidget(self.lineEdit_2)

        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 110, 351, 91))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.login_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.login_btn.setObjectName("login_button")
        self.login_btn.clicked.connect(self.login_user)
        self.login_btn.setEnabled(False)
        self.login_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.verticalLayout_4.addWidget(self.login_btn)

        self.register_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.register_btn.setObjectName("register_button")
        self.register_btn.clicked.connect(self.open_reg_window)
        self.register_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.verticalLayout_4.addWidget(self.register_btn)

        self.create_db()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def login_user(self):
        self.user_name = self.lineEdit.text()
        self.password = hashlib.md5(bytes(self.lineEdit_2.text(), encoding='utf-8')).hexdigest()

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE user_name = ?', (self.user_name,))
        user = cur.fetchall()
        if user:
            cur.execute('SELECT password FROM users WHERE user_name =  (?)', (self.user_name,))
            right_password = str(cur.fetchall()[0][0])
            if right_password == self.password:
                self.MainWindow = QtWidgets.QMainWindow()
                self.ui = NotesMainMenu(self.user_name)
                self.ui.setupUi(self.MainWindow)
                self.MainWindow.show()
                self.Dialog.close()
            else:
                QMessageBox.critical(self, 'Ошибка входа!', 'Неправильный пароль!')
        else:
            QMessageBox.critical(self, 'Ошибка входа!', 'Такого аккаунта нет!')

    def open_reg_window(self):
        self.Dialog.close()
        self.prog = Register()
        self.Dialog1 = QtWidgets.QDialog()
        self.prog.setupUi(self.Dialog1)
        self.Dialog1.show()
        self.close()

    def check_input(self):
        if self.lineEdit.text() and self.lineEdit_2.text():
            self.login_btn.setEnabled(True)
        else:
            self.login_btn.setEnabled(False)

    def create_db(self):
        if not os.path.exists(DB):
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute(
                """CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY,
               user_name STRING,
               password STRING
               );""")
            conn.commit()
            cur.execute(
                """CREATE TABLE IF NOT EXISTS notes(
               id INTEGER PRIMARY KEY,
               user STRING,
               note_name STRING,
               note_description TEXT,
               note_color STRING
               );""")
            conn.commit()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Вход"))
        self.label.setText(_translate("Dialog", "Имя: "))
        self.label_2.setText(_translate("Dialog", "Пароль: "))
        self.login_btn.setText(_translate("Dialog", "Войти"))
        self.register_btn.setText(_translate("Dialog", "У меня нет аккаунта"))


class NotesMainMenu(QtWidgets.QMainWindow):
    def __init__(self, user_name):
        super().__init__()
        self.note_list = []
        self.notes_windows_dict = dict()
        self.user_name = user_name

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 620)
        MainWindow.setMaximumSize(QtCore.QSize(640, 620))
        MainWindow.setMinimumSize(QtCore.QSize(640, 620))
        MainWindow.setStyleSheet("font: 75 14pt \"Rubik\";\n")
        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.scrollLayout = QFormLayout()

        self.scrollWidget = QWidget(self.centralwidget)
        self.scrollWidget.setLayout(self.scrollLayout)
        self.scrollWidget.setStyleSheet('background:transparent;')

        self.name_lbl = QLabel(f'Здравствуй, {self.user_name}', self.centralwidget)
        self.name_lbl.setGeometry(QRect(35, 5, 640, 25))

        self.pixmap = QPixmap('images/resized_note_logo.png')
        self.image = QLabel(self.centralwidget)
        self.image.move(5, 5)
        self.image.resize(25, 25)
        self.image.setPixmap(self.pixmap)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setGeometry(QRect(10, 30, 620, 530))

        self.show_note_btn = QPushButton('Показать', self.centralwidget)
        self.show_note_btn.setGeometry(QRect(10, 570, 200, 40))
        self.show_note_btn.clicked.connect(self.create_new_window)
        self.show_note_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.logout_btn = QtWidgets.QPushButton('Выйти', self.centralwidget)
        self.logout_btn.clicked.connect(self.logout_user)
        self.logout_btn.setGeometry(QRect(545, 5, 85, 25))

        self.create_note_btn = QPushButton('Добавить', self.centralwidget)
        self.create_note_btn.setGeometry(QRect(220, 570, 200, 40))
        self.create_note_btn.clicked.connect(self.update_or_create_note)
        self.create_note_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.update_note_btn = QPushButton('Обновить список', self.centralwidget)
        self.update_note_btn.setGeometry(QRect(430, 570, 200, 40))
        self.update_note_btn.clicked.connect(self.get_list_of_note)
        self.update_note_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        MainWindow.setCentralWidget(self.centralwidget)

        self.get_list_of_note()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def update_or_create_note(self):
        if self.sender().text().lower() == 'настроить':
            self.Dialog = QtWidgets.QDialog()
            self.prog = CreateOrUpdateNote(self.user_name, int(self.sender().objectName().split('_')[1]))
            self.prog.setupUi(self.Dialog)
            self.Dialog.show()
        else:
            self.Dialog = QtWidgets.QDialog()
            self.prog = CreateOrUpdateNote(self.user_name, -1)
            self.prog.setupUi(self.Dialog)
            self.Dialog.show()

    def create_new_window(self):
        self.create_txt()
        for i in range(len(self.note_list)):
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute('SELECT note_name FROM notes WHERE id = (?)', (self.note_list[i].split('_')[1],))
            self.note_name = cur.fetchall()[0][0]
            cur.execute('SELECT note_description FROM notes WHERE id = (?)', (self.note_list[i].split('_')[1],))
            self.note_description = cur.fetchall()[0][0]
            cur.execute('SELECT note_color FROM notes WHERE id = (?)', (self.note_list[i].split('_')[1],))
            self.note_color = cur.fetchall()[0][0]

            self.new_window = Note(note_name=self.note_name, note_description=self.note_description,
                                   note_color=self.note_color)
            self.Dialog = QtWidgets.QDialog()
            self.new_window.setupUi(self.Dialog)
            self.notes_windows_dict[i] = self.Dialog
        for i in range(len(self.notes_windows_dict)):
            self.notes_windows_dict[i].show()

    def get_new_windows(self):
        if self.sender().isChecked():
            self.note_list.append(self.sender().objectName())
        else:
            self.note_list.remove(self.sender().objectName())

    def create_txt(self):
        if len(self.note_list) >= 1:
            if os.path.exists('selected_notes.txt'):
                os.remove('selected_notes.txt')
            file = open('selected_notes.txt', mode='w', encoding='utf-8')
            file.write(f'Ранее открытые стикеры пользователя {self.user_name}: \n')
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            for i in self.note_list:
                cur.execute("SELECT note_name FROM notes WHERE id = (?)", (i.split('_')[1],))
                selected_note_name = cur.fetchall()[0][0]
                file.write(str(selected_note_name) + '\n')
            file.close()

    def logout_user(self):
        self.MainWindow.close()
        self.prog = Login()
        self.Dialog1 = QtWidgets.QDialog()
        self.prog.setupUi(self.Dialog1)
        self.Dialog1.show()

    def delete_note(self):
        self.selected_note_id = self.sender().objectName().split('_')[-1]

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT note_name FROM notes WHERE id = (?)", (self.selected_note_id,))
        self.selected_note = cur.fetchall()[0][0]

        valid = QMessageBox.question(
            self, 'Удаление', "Вы деуствительно хотите удалить заметку: " + self.selected_note,
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute("DELETE FROM notes WHERE id = (?)", (self.selected_note_id,))
            conn.commit()

    def get_list_of_note(self):
        self.note_list = []
        self.notes_windows_dict = dict()
        for i in reversed(range(self.scrollLayout.count())):
            self.scrollLayout.itemAt(i).widget().deleteLater()

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute('SELECT note_name, id FROM notes WHERE user = (?) ORDER BY id DESC', (self.user_name,))
        notes = cur.fetchall()

        self.horisontalLayoutWidget = QWidget(self.scrollWidget)
        self.horisontalLayoutWidget.setObjectName(u"horisontalLayoutWidget")
        self.horisontalLayoutWidget.resize(200, 700)

        self.verticalLayoutWidget = QWidget(self.horisontalLayoutWidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.resize(200, 100)

        self.list_vertical_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.list_horisontal_layout = QtWidgets.QHBoxLayout(self.horisontalLayoutWidget)


        for i in reversed(range(self.list_vertical_layout.count())):
            self.scrollLayout.itemAt(i).widget().deleteLater()

        for i in reversed(range(self.list_horisontal_layout.count())):
            self.scrollLayout.itemAt(i).widget().deleteLater()


        for text, id in notes:
            self.checkBox = QCheckBox(str(text), self.verticalLayoutWidget)
            self.checkBox.setObjectName(u"checkBox_" + str(id))
            self.checkBox.setStyleSheet('background:transparent;')
            self.checkBox.clicked.connect(self.get_new_windows)
            self.checkBox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

            self.push_btn = QPushButton('Настроить', self.verticalLayoutWidget)
            self.push_btn.setObjectName('pushButton_' + str(id))
            self.push_btn.clicked.connect(self.update_or_create_note)
            self.push_btn.setStyleSheet('font: 75 10pt \"Rubik\";')
            self.push_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            self.push_btn.setStyleSheet('border: 2px solid grey;')

            self.delete_btn = QPushButton('Удалить', self.verticalLayoutWidget)
            self.delete_btn.setObjectName('deleteButton_' + str(id))
            self.delete_btn.clicked.connect(self.delete_note)
            self.delete_btn.setStyleSheet('font: 75 10pt \"Rubik\";')
            self.delete_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            self.delete_btn.setStyleSheet('border: 2px solid grey;')

            self.list_vertical_layout.addWidget(self.checkBox)
            self.list_vertical_layout.addWidget(self.push_btn)
            self.list_vertical_layout.addWidget(self.delete_btn)
            self.list_horisontal_layout.addWidget(self.verticalLayoutWidget)
        self.scrollLayout.addWidget(self.horisontalLayoutWidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Меню"))


class Note(QWidget):
    def __init__(self, note_name, note_description, note_color):
        super(Note, self).__init__()

        self.note_name = note_name
        self.note_description = note_description
        self.note_color = note_color

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 300)
        Dialog.setMaximumSize(QtCore.QSize(300, 300))
        Dialog.setMinimumSize(QtCore.QSize(300, 300))
        Dialog.setStyleSheet("font: 75 11pt \"Rubik\";\n"
                             f"background-color: rgb{tuple(int(self.note_color[1:][i:i + 2], 16) for i in (0, 2, 4))};")
        Dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.centralwidget = QtWidgets.QWidget(Dialog)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 281, 21))
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label.setStyleSheet("font: 75 13pt \"Rubik\";")
        self.label.setObjectName("label")
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(0, 30, 231, 21))
        self.line.setStyleSheet("color: rgb(180, 174, 5);")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.label_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)

        self.scrollLayout = QFormLayout()
        self.scrollWidget = QWidget(self.centralwidget)
        self.scrollWidget.setLayout(self.scrollLayout)
        self.scrollWidget.setStyleSheet('background:transparent;')
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setGeometry(QRect(-10, 40, 301, 271))
        self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().maximum())
        self.scrollArea.horizontalScrollBar().setEnabled(False)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollLayout.addWidget(self.label_2)
        self.scrollArea.setStyleSheet('border: 1px solid transparent;')


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def description_change(self):
        if len(self.note_description) > 28:
            description_list = self.note_description.split('\n')
            for i in range(len(description_list)):
                if description_list[i] == '':
                    description_list[i] = '\n'
            for i in range(len(description_list)):
                if description_list[i] != '\n':
                    description_list[i] += '\n'
                if len(description_list[i]) > 30:
                    description_list[i] = description_list[i][:30] + '\n' + description_list[i][30:]
                    print(description_list)
            self.note_description = "".join(description_list)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Заметка"))
        self.label.setText(_translate("Dialog", str(self.note_name)))
        self.description_change()
        self.label_2.setText(_translate("Dialog", str(self.note_description)))


class CreateOrUpdateNote(QWidget):
    def __init__(self, user_name, note_id):
        super().__init__()
        self.user_name = user_name
        self.note_id = note_id
        self.note_color = '#fff808'

    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(325, 482)
        Dialog.setMaximumSize(325, 482)
        Dialog.setMinimumSize(325, 482)
        Dialog.setStyleSheet("font: 75 12pt \"Rubik\";")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 13, 305, 421))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")

        self.verticalLayout.addWidget(self.label)
        self.line_edit_title = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.line_edit_title.setMaxLength(35)

        self.line_edit_title.setAlignment(QtCore.Qt.AlignCenter)
        self.line_edit_title.setObjectName("line_edit_title")
        self.verticalLayout.addWidget(self.line_edit_title)

        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.line_edit_description = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.line_edit_description.setObjectName("line_edit_description")
        self.verticalLayout.addWidget(self.line_edit_description)

        self.save_btn = QtWidgets.QPushButton(Dialog)
        self.save_btn.setGeometry(QtCore.QRect(165, 440, 150, 30))
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_note)

        self.colorpicker_btn = QtWidgets.QPushButton(Dialog)
        self.colorpicker_btn.setGeometry(QtCore.QRect(10, 440, 150, 30))
        self.colorpicker_btn.setObjectName("colorpicker_btn")
        self.colorpicker_btn.clicked.connect(self.get_new_color)

        if self.note_id > -1:
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute('SELECT note_name FROM notes WHERE id = (?)', (self.note_id,))
            self.note_title1 = cur.fetchall()[0][0]
            self.line_edit_title.setText(self.note_title1)
            cur.execute('SELECT note_description FROM notes WHERE id = (?)', (self.note_id,))
            self.note_description1 = cur.fetchall()[0][0]
            self.line_edit_description.setText(self.note_description1)
            cur.execute('SELECT note_color FROM notes WHERE id = (?)', (self.note_id,))
            self.note_color = cur.fetchall()[0][0]

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def get_new_color(self):
        self.selected_color = QColorDialog.getColor().name()
        if self.selected_color != '#000000':
            self.note_color = self.selected_color

    def save_note(self):
        self.note_title = self.line_edit_title.text()
        self.note_description = self.line_edit_description.toPlainText()
        if self.note_id > -1:
            conn = sqlite3.connect(DB)
            cur = conn.cursor()

            cur.execute('UPDATE notes SET (note_name, note_description, note_color) = (?, ?, ?) WHERE id = (?)',
                        (self.note_title, self.note_description, self.note_color, self.note_id))
            conn.commit()
            cur.close()
            QMessageBox.information(self, 'Успешно', f'Заметка {self.note_title} успешно обновлена.', QMessageBox.Ok)
        else:

            conn = sqlite3.connect(DB)
            cur = conn.cursor()

            cur.execute('INSERT INTO notes (user, note_name, note_description, note_color) VALUES (?, ?, ?, ?)',
                        (self.user_name, self.note_title, self.note_description, self.note_color))
            conn.commit()
            cur.close()
            QMessageBox.information(self, 'Успешно', f'Заметка {self.note_title} успешно добавлена.', QMessageBox.Ok)
        self.Dialog.close()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        if self.note_id != -1:
            Dialog.setWindowTitle(_translate("Dialog", "Изменение"))
        else:
            Dialog.setWindowTitle(_translate("Dialog", "Добавление"))
        self.label.setText(_translate("Dialog", "Заголовок заметки:"))
        self.label_2.setText(_translate("Dialog", "Описание:"))
        self.save_btn.setText(_translate("Dialog", "Сохранить"))
        self.colorpicker_btn.setText(_translate("Dialog", "Выбрать цвет"))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    prog = Login()
    Dialog = QtWidgets.QDialog()
    prog.setupUi(Dialog)
    Dialog.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
