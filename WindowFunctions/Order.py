import datetime
import sys
import pymysql
from PyQt5 import QtCore, QtWidgets
from Designer.OrderWindow import Ui_OrderWindow
from ButtonFunctions.OrderFuncs import insert_order
from ButtonFunctions.OrderFuncs import send_truck
from ButtonFunctions.OrderFuncs import update_cargo
from ButtonFunctions.OrderFuncs import update_cities

class OrderWindow(QtWidgets.QWidget):
    def __init__(self, connection):
        super(OrderWindow, self).__init__()
        self.ui = Ui_OrderWindow()
        self.ui.setupUi(self)
        self.connection = connection
        self.OrderDateEditDate = datetime.date.today()
        self.ui.OrderDateEdit.setMinimumDate(self.OrderDateEditDate)
        self.ui.OrderDateEdit.setCalendarPopup(1)
        self.ui.OrderDateEdit.dateChanged.connect(self.OrderDateEdit_slot)
        self.CustomerEditText = 'Enter Name'
        self.ui.CustomerEdit.setText(self.CustomerEditText)
        self.DepartureComboBox_update()
        self.ui.DepartureComboBox.currentTextChanged.connect(self.DepartureComboBox_slot)
        self.ArrivalComboBox_update()
        self.ui.ArrivalComboBox.currentTextChanged.connect(self.ArrivalComboBox_slot)
        self.CargoTypeComboBox_update()
        self.ui.CargoTypeComboBox.currentIndexChanged.connect(self.CargoTypeComboBox_slot)
        self.CargoComboBox_update()
        self.ui.CargoComboBox.currentIndexChanged.connect(self.CargoComboBox_slot)
        self.WeightSpinBoxValue = self.ui.WeightSpinBox.minimum()
        self.ui.WeightSpinBox.valueChanged.connect(self.WeightSpinBox_slot)
        self.ui.OrderButton.clicked.connect(self.OrderButton_slot)

    def OrderButton_slot(self):
        insert_order(self.connection, self.OrderDateEditDate)
        send_truck(self.connection, self.DepartureComboBoxName,
                   self.ArrivalComboBoxName, self.CargoComboBoxIndex,
                   self.WeightSpinBoxValue, self.OrderDateEditDate)
        update_cargo(self.connection, self.CargoComboBoxIndex, self.WeightSpinBoxValue)
        update_cities(self.connection, self.DepartureComboBoxName,
                      self.ArrivalComboBoxName, self.WeightSpinBoxValue)
    def WeightSpinBox_slot(self, value):
        self.WeightSpinBoxValue = value
    def OrderDateEdit_slot(self, date):
        self.OrderDateEditDate = date
    def CargoComboBox_slot(self, index):
        self.CargoComboBoxIndex = index + 1
    def CargoComboBox_update(self):
        cur = self.connection.cursor()
        cur.execute('SELECT Id, Name FROM Cargo '
                    f'WHERE Cargo_type_Id = {self.CargoTypeComboBoxIndex} '
                    'ORDER BY Id')
        cargoes = cur.fetchall()
        self.CargoComboBoxIndex = cargoes[0][0]
        for cargo in cargoes:
            self.ui.CargoComboBox.insertItem(cargo[0], "{}".format(cargo[1]))
    def CargoTypeComboBox_slot(self, index):
        self.CargoTypeComboBoxIndex = index + 1
        self.ui.CargoComboBox.clear()
        self.CargoComboBox_update()
    def CargoTypeComboBox_update(self):
        cur = self.connection.cursor()
        cur.execute('SELECT Id, Type FROM Cargo_types '
                    'ORDER BY Id')
        types = cur.fetchall()
        self.CargoTypeComboBoxIndex = types[0][0]
        for type in types:
            self.ui.CargoTypeComboBox.insertItem(type[0], "{}".format(type[1]))
    def ArrivalComboBox_update(self):
        cur = self.connection.cursor()
        cur.execute('SELECT Id, Name FROM Cities '
                    f'WHERE Name != "{self.DepartureComboBoxName}" ' 
                    'ORDER BY Id')
        cities = cur.fetchall()
        self.ArrivalComboBoxName = cities[0][1]
        for city in cities:
            self.ui.ArrivalComboBox.insertItem(city[0], "{}".format(city[1]))
    def ArrivalComboBox_slot(self, text):
        self.ArrivalComboBoxName = text
    def DepartureComboBox_update(self):
        cur = self.connection.cursor()
        cur.execute('SELECT Id, Name FROM Cities '
                    'ORDER BY Id')
        cities = cur.fetchall()
        self.DepartureComboBoxName = cities[0][1]
        for city in cities:
            self.ui.DepartureComboBox.insertItem(city[0], "{}".format(city[1]))
    def DepartureComboBox_slot(self, text):
        self.DepartureComboBoxName = text
        self.ui.ArrivalComboBox.clear()
        self.ArrivalComboBox_update()

if __name__ == '__main__':
    MyDB = pymysql.connect(user='root', host='127.0.0.1', password='TeamSpirit2021', db='logistics')
    app = QtWidgets.QApplication([])
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    application = OrderWindow(MyDB)
    application.show()

    sys.exit(app.exec())