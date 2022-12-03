import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

con = sqlite3.connect("coffee.sqlite")
cur = con.cursor()


class SecondForm(QMainWindow):
    def __init__(self, arg, b):
        super().__init__()
        self.b = b
        self.modified = {}
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.titles = None
        self.pushButton_2.clicked.connect(self.save)
        res = cur.execute("""SELECT * FROM coffe""").fetchall()
        title = ['ID', 'сорт', 'Обжарка', 'молотый/в зернах',
                 'описание вкуса', 'цена в рублях', 'объем в граммах']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.itemChanged.connect(self.item_changed)
        if arg == 'CREATE':
            self.tableWidget.hide()
            self.label_2.hide()
            self.pushButton.clicked.connect(self.clicked)
        else:
            self.label.hide()
            self.pushButton.hide()
            self.lineEdit.hide()
            self.lineEdit_2.hide()
            self.lineEdit_3.hide()
            self.lineEdit_4.hide()
            self.lineEdit_5.hide()
            self.lineEdit_6.hide()

    def clicked(self):
        if self.lineEdit.text().isalpha() and self.lineEdit_2.text().isalpha() \
                and self.lineEdit_3.text().isalpha() and self.lineEdit_4.text().isalpha() \
                and self.lineEdit_5.text().isdigit() and self.lineEdit_6.text().isdigit():
            self.label_3.setText('')
            cur.execute("""INSERT INTO coffe (sort, roasting,
                                                ground_or_grains, deskription, 
                                                cost_rubles, packing_volume_grams) VALUES (?, ?, ?, ?, ?, ?)""",
                        (self.lineEdit.text(), self.lineEdit_2.text(),
                         self.lineEdit_3.text(), self.lineEdit_4.text(),
                         int(self.lineEdit_5.text()), int(self.lineEdit_6.text()))).fetchall()
            con.commit()
            res = cur.execute("""SELECT * FROM coffe""").fetchall()
            title = ['ID', 'сорт', 'Обжарка', 'молотый/в зернах',
                     'описание вкуса', 'цена в рублях', 'объем в граммах']
            self.b.setColumnCount(len(title))
            self.b.setHorizontalHeaderLabels(title)
            self.b.setRowCount(0)
            for i, row in enumerate(res):
                self.b.setRowCount(
                    self.b.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.b.setItem(
                        i, j, QTableWidgetItem(str(elem)))
            self.close()
        else:
            self.label_3.setText('INCORRECT DATA')

    def item_changed(self, item):
        # Если значение в ячейке было изменено,
        if self.tableWidget.item(item.row(), 0) and self.tableWidget.item(item.row(), 1) \
                and self.tableWidget.item(item.row(), 2)\
                and self.tableWidget.item(item.row(), 3) and self.tableWidget.item(item.row(), 4) \
                and self.tableWidget.item(item.row(), 5)\
                and self.tableWidget.item(item.row(), 6):
            id = int(self.tableWidget.item(item.row(), 0).text())
            s = self.tableWidget.item(item.row(), 1).text()
            r = self.tableWidget.item(item.row(), 2).text()
            g = self.tableWidget.item(item.row(), 3).text()
            d = self.tableWidget.item(item.row(), 4).text()
            c = int(self.tableWidget.item(item.row(), 5).text())
            p = int(self.tableWidget.item(item.row(), 6).text())
            cur.execute("""UPDATE coffe SET sort = ?, roasting = ?, ground_or_grains = ?, 
            deskription = ?, cost_rubles = ?, packing_volume_grams = ? WHERE ID = ?""",
                        (s, r, g, d, c, p, id,)).fetchall()
            con.commit()
            res = cur.execute("""SELECT * FROM coffe WHERE ID = ?""",
                        (id,)).fetchall()
            print(res)

    def save(self):
        res = cur.execute("""SELECT * FROM coffe""").fetchall()
        title = ['ID', 'сорт', 'Обжарка', 'молотый/в зернах',
                 'описание вкуса', 'цена в рублях', 'объем в граммах']
        self.b.setColumnCount(len(title))
        self.b.setHorizontalHeaderLabels(title)
        self.b.setRowCount(0)
        for i, row in enumerate(res):
            self.b.setRowCount(
                self.b.rowCount() + 1)
            for j, elem in enumerate(row):
                self.b.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.close()


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        res = cur.execute("""SELECT * FROM coffe""").fetchall()
        title = ['ID', 'сорт', 'Обжарка', 'молотый/в зернах',
                 'описание вкуса', 'цена в рублях', 'объем в граммах']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeRowsToContents()
        self.pushButton.clicked.connect(self.clicked)
        self.pushButton_2.clicked.connect(self.clicked)

    def clicked(self):
        self.second_form = SecondForm(self.sender().text(), self.tableWidget)
        self.second_form.show()
        res = cur.execute("""SELECT * FROM coffe""").fetchall()
        title = ['ID', 'сорт', 'Обжарка', 'молотый/в зернах',
                 'описание вкуса', 'цена в рублях', 'объем в граммах']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())
