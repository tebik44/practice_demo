import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel, QPixmap

from model.conn import Model
import card_view

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('Screens/login.ui', self)
        self.setWindowIcon(QIcon('img/icon.png'))
        self.setWindowTitle('Окно входа')
        self.label.hide()
        
        self.pushButton = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.pushButton.clicked.connect(self.log)
        
    def log(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        
        if not (login and password):
            self.label.setText('Заполните все поля')
            self.label.show()
        else:
            conn = Model().conn
            cur = conn.cursor()
            cur.execute('select * from user where login = %s and password = %s', 
                        (login, password))
            data = cur.fetchone()
            if data:
                QMessageBox.information(self, 'Ok', f'привет {data[1]}')
                self.table = card_view.CardApp()
                self.table.show()
                self.hide()
            else:
                QMessageBox.information(self, 'Не ок', 'пользователь не найден')
                
                
class Table(QMainWindow):
    def __init__(self):
        super(Table, self).__init__()
        uic.loadUi('Screens/table.ui', self)
        
        self.tableView = self.findChild(QtWidgets.QTableView, 'tableView')
        self.table_model = QStandardItemModel()
        self.tableView.setModel(self.table_model)
        
        conn = Model().conn
        cur = conn.cursor()
        cur.execute('select * from user')
        full_query = cur.fetchall()
        fields_name = [item[0] for item in cur.description]
        self.load_data(full_query, fields_name)
        
        self.pushButton.clicked.connect(self.exit)
        self.lineEdit.textChanged.connect(self.search)
        
        
    def load_data(self, data, data_columns):
        self.table_model.clear()
        self.table_model.setHorizontalHeaderLabels(data_columns)
        self.table_model.setVerticalHeaderLabels([str(item[0]) for item in data])
        
        for row_index, row_data in enumerate(data):
            for column_index, column_data in enumerate(data_columns):
                item = QStandardItem(str(row_data[column_index]))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table_model.setItem(row_index, column_index, item)


    def search(self):
        conn = Model().conn
        cur = conn.cursor()
        search_text = self.lineEdit.text().lower()
        filtered_data = []
        data = cur.execute('select * from user')
        data = cur.fetchall()
        for row_data in data:
            if any(search_text in str(item).lower() for item in row_data):
                filtered_data.append(row_data)

        self.load_data(filtered_data, [item[0] for item in cur.description])


    def exit(self):
        self.login = Login()
        self.login.show()
        self.hide()






if __name__ == '__main__':
    conn = Model().conn
    app = QtWidgets.QApplication([])
    # login = Login()
    login = card_view.CardApp()
    login.show()
    sys.exit(app.exec_())