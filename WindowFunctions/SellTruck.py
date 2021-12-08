import datetime
import sys
import pymysql
from PyQt5 import QtCore, QtWidgets
from Designer.SellTruckWindow import Ui_SellTruckWindow
from ButtonFunctions.SellTruckFuncs import insert_sell_truck
from ButtonFunctions.SellTruckFuncs import update_truck
from ButtonFunctions.SellTruckFuncs import update_protocols

class SellTruckWindow(QtWidgets.QWidget):
    def __init__(self, connection):
        super(SellTruckWindow, self).__init__()
        self.ui = Ui_SellTruckWindow()
        self.ui.setupUi(self)
        self.connection = connection
        self.CustomerEditText = 'Enter Name'
        self.ui.CustomerEdit.setText(self.CustomerEditText)
        self.ui.CustomerEdit.textEdited.connect(self.CustomerEdit_slot)
        self.TruckIdComboBox_update()
        self.ui.TruckIdComboBox.currentTextChanged.connect(self.TruckIdComboBox_slot)
        self.SellDateEditDate = datetime.date.today()
        self.ui.SellDateEdit.setDate(datetime.date.today())
        self.ui.SellDateEdit.setCalendarPopup(1)
        self.ui.SellDateEdit.dateChanged.connect(self.SellDateEdit_slot)
        self.ui.SellButton.clicked.connect(self.SellButton_slot)
    def CustomerEdit_slot(self, text):
        self.CustomerEditText = text
    def TruckIdComboBox_slot(self, text):
        self.TruckIdComboBoxIndex = text
    def TruckIdComboBox_update(self):
        self.ui.TruckIdComboBox.clear()
        cur = self.connection.cursor()
        cur.execute('SELECT Trucks.Id FROM Trucks '
                    'JOIN Protocol_truck_city ON Trucks.Id = Truck_Id '
                    'WHERE End_downtime IS NULL '
                    'ORDER BY Trucks.Id')
        ids = cur.fetchall()
        self.TruckIdComboBoxIndex = ids[0][0]
        for id in ids:
            self.ui.TruckIdComboBox.insertItem(id[0], '{}'.format(id[0]))
    def SellDateEdit_slot(self, date):
        self.SellDateEditDate = QtCore.QDate.toPyDate(date)
    def SellButton_slot(self):
        insert_sell_truck(self.connection, self.TruckIdComboBoxIndex,
                          self.CustomerEditText, self.SellDateEditDate)
        update_truck(self.connection, self.TruckIdComboBoxIndex)
        update_protocols(self.connection, self.TruckIdComboBoxIndex)
        self.TruckIdComboBox_update()

if __name__ == '__main__':
    MyDB = pymysql.connect(user='root', host='127.0.0.1', password='TeamSpirit2021', db='logistics')
    app = QtWidgets.QApplication([])
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    application = SellTruckWindow(MyDB)
    application.show()

    sys.exit(app.exec())