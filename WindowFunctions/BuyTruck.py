import datetime
import sys
import pymysql
from PyQt5 import QtCore, QtWidgets
from Designer.BuyTruckWindow import Ui_BuyTruckWindow
from ButtonFunctions.BuyTruckFuncs import insert_truck
from ButtonFunctions.BuyTruckFuncs import insert_purchase
from ButtonFunctions.BuyTruckFuncs import insert_protocol

class BuyTruckWindow(QtWidgets.QWidget):
    def __init__(self, connection):
        super(BuyTruckWindow, self).__init__()
        self.ui = Ui_BuyTruckWindow()
        self.ui.setupUi(self)
        self.connection = connection
        self.ui.PurchaseButton.clicked.connect(self.PurchaseButton_slot)
        self.CapacitySpinBoxValue = self.ui.CapacitySpinBox.minimum()
        self.ui.CapacitySpinBox.valueChanged.connect(self.CapacitySpinBox_slot)
        self.PriceSpinBoxValue = self.ui.PriceSpinBox.minimum()
        self.ui.PriceSpinBox.valueChanged.connect(self.PriceSpinBox_slot)
        self.RouteCostsSpinBoxValue = self.ui.RouteCostsSpinBox.minimum()
        self.ui.RouteCostsSpinBox.valueChanged.connect(self.RouteCostsSpinBox_slot)
        self.DowntimeCostsSpinBoxValue = self.ui.DowntimeCostsSpinBox.minimum()
        self.ui.DowntimeCostsSpinBox.valueChanged.connect(self.DowntimeCostsSpinBox_slot)
        self.EmptyCostsSpinBoxValue = self.ui.EmptyCostsSpinBox.minimum()
        self.ui.EmptyCostsSpinBox.valueChanged.connect(self.EmptyCostsSpinBox_slot)
        self.SellerEditText = 'Enter Name'
        self.ui.SellerEdit.setText(self.SellerEditText)
        self.ui.SellerEdit.textEdited.connect(self.SellerEdit_slot)
        self.CityComboBox_update()
        self.CityComboBoxIndex = 1
        self.ui.CityComboBox.currentIndexChanged.connect(self.CityComboBox_slot)
        self.ui.PurchaseDateEdit.setDate(datetime.date.today())
        self.ui.PurchaseDateEdit.setMinimumDate(datetime.date.today())
        self.ui.PurchaseDateEdit.setCalendarPopup(True)
        self.PurchaseDateEditDate = datetime.date.today()
        self.ui.PurchaseDateEdit.dateChanged.connect(self.PurchaseDateEdit_slot)
        self.CargoTypeComboBox_update()
        self.CargoTypeComboBoxIndex = 1
        self.ui.CargoTypeComboBox.currentIndexChanged.connect(self.CargoTypeComboBox_slot)
        self.RegisterNumberEditText = 'Enter register number'
        self.ui.RegisterNumberEdit.setText(self.RegisterNumberEditText)
        self.ui.RegisterNumberEdit.textEdited.connect(self.RegisterNumberEdit_slot)
    def RegisterNumberEdit_slot(self, text):
        self.RegisterNumberEditText = text
    def CargoTypeComboBox_slot(self, index):
        self.CargoTypeComboBoxIndex = index + 1
    def CargoTypeComboBox_update(self):
        cur = self.connection.cursor()
        cur.execute('SELECT Id, Type FROM Cargo_types ORDER BY Id')
        types = cur.fetchall()
        for type in types:
            self.ui.CargoTypeComboBox.insertItem(type[0], type[1])
    def PurchaseDateEdit_slot(self, date):
        self.PurchaseDateEditDate = QtCore.QDate.toPyDate(date)
    def CityComboBox_slot(self, index):
        self.CityComboBoxIndex = index + 1
    def CityComboBox_update(self):
        cur = self.connection.cursor()
        cur.execute('SELECT Id, Name FROM Cities ORDER BY Id')
        cities = cur.fetchall()
        for city in cities:
            self.ui.CityComboBox.insertItem(city[0], city[1])
    def SellerEdit_slot(self, text):
        self.SellerEditText = text
    def EmptyCostsSpinBox_slot(self, value):
        self.EmptyCostsSpinBoxValue = value
    def DowntimeCostsSpinBox_slot(self, value):
        self.DowntimeCostsSpinBoxValue = value
    def RouteCostsSpinBox_slot(self, value):
        self.RouteCostsSpinBoxValue = value
    def CapacitySpinBox_slot(self, value):
        self.CapacitySpinBoxValue = value
    def PriceSpinBox_slot(self, value):
        self.PriceSpinBoxValue = value
    def PurchaseButton_slot(self):
        msgbox = QtWidgets.QMessageBox()
        try:
            insert_truck(self.connection, self.RegisterNumberEditText, self.PriceSpinBoxValue, self.CapacitySpinBoxValue,
                         self.CargoTypeComboBoxIndex, self.DowntimeCostsSpinBoxValue,
                         self.RouteCostsSpinBoxValue, self.EmptyCostsSpinBoxValue)
            insert_purchase(self.connection, self.PriceSpinBoxValue,
                            self.SellerEditText, self.PurchaseDateEditDate, self.RegisterNumberEditText)
            insert_protocol(self.connection, self.CityComboBoxIndex,
                            self.PurchaseDateEditDate, self.RegisterNumberEditText)
        except:
            message = 'Что-то пошло не так...' \
                      'Возможно данные были введены неверно...'
            msgbox.setIcon(QtWidgets.QMessageBox.Critical)
            msgbox.setWindowTitle('ERROR')
            msgbox.setText(message)
        else:
            message = 'Грузовик был успешно куплен!'
            msgbox.setIcon(QtWidgets.QMessageBox.Information)
            msgbox.setWindowTitle('OK')
            msgbox.setText(message)
        msgbox.exec()

if __name__ == '__main__':
    MyDB = pymysql.connect(user='root', host='127.0.0.1', password='TeamSpirit2021', db='logistics')
    app = QtWidgets.QApplication([])
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    application = BuyTruckWindow(MyDB)
    application.show()

    sys.exit(app.exec())
