import sys
import pymysql
from PyQt5 import QtCore, QtWidgets
from Designer.MainWindow import Ui_MainWindow
from WindowFunctions.BuyTruck import BuyTruckWindow
from WindowFunctions.SellTruck import SellTruckWindow
from WindowFunctions.Order import OrderWindow
from WindowFunctions.Period import PeriodWindow
from WindowFunctions.Year import EnterYear
from Reports import city_activity
from Reports import cargo_popularity

class MainWindow(QtWidgets.QWidget):
    def BuyButton_slot(self):
        self.BuyTruckWindow.show()
    def SellButton_slot(self):
        self.SellTruckWindow.show()
        self.SellTruckWindow.TruckIdComboBox_update()
    def OrderButton_slot(self):
        self.OrderWindow.show()
    def MileageButton_slot(self):
        self.PeriodWindow = PeriodWindow(self.connection, 1)
        self.PeriodWindow.show()
    def DowntimeButton_slot(self):
        self.PeriodWindow = PeriodWindow(self.connection, 0)
        self.PeriodWindow.show()
    def CityActivityButton_slot(self):
        city_activity(self.connection, 'city_activity.csv')
    def CargoPopularityButton_slot(self):
        cargo_popularity(self.connection, 'cargo_popularity.csv')
    def FinancialReportButton_slot(self):
        self.YearWindow.show()
    def __init__(self, connection):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connection = connection
        self.BuyTruckWindow = BuyTruckWindow(connection)
        self.ui.BuyButton.clicked.connect(self.BuyButton_slot)
        self.SellTruckWindow = SellTruckWindow(connection)
        self.ui.SellButton.clicked.connect(self.SellButton_slot)
        self.OrderWindow = OrderWindow(connection)
        self.ui.OrderButton.clicked.connect(self.OrderButton_slot)
        self.ui.MileageButton.clicked.connect(self.MileageButton_slot)
        self.ui.DowntimeButton.clicked.connect(self.DowntimeButton_slot)
        self.ui.CityActivityButton.clicked.connect(self.CityActivityButton_slot)
        self.ui.CargoPopularityButton.clicked.connect(self.CargoPopularityButton_slot)
        self.YearWindow = EnterYear(connection)
        self.ui.FinancialReportButton.clicked.connect(self.FinancialReportButton_slot)

if __name__ == '__main__':
    MyDB = pymysql.connect(user='root', host='127.0.0.1', password='TeamSpirit2021', db='logistics')
    app = QtWidgets.QApplication([])
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    application = MainWindow(MyDB)
    application.show()

    sys.exit(app.exec())
