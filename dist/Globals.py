import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidgetItem
from tableform_ui import Ui_MainWindow
import sqlite3


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


def main():
    app = QApplication(sys.argv)
    ex = Globals()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()