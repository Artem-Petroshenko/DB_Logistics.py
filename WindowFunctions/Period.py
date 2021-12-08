import datetime
import sys
import pymysql
from PyQt5 import QtCore, QtWidgets
from Designer.PeriodWindow import Ui_Period
from Reports import useless_run_koef
from Reports import downtime_koef

class PeriodWindow(QtWidgets.QWidget):
    def FromDateEdit_slot(self, date):
        self.FromDateEditDate = QtCore.QDate.toPyDate(date)
    def ToDateEdit_slot(self, date):
        self.ToDateEditDate = QtCore.QDate.toPyDate(date)
    def ReportButton_slot(self):
        if self.rep == 1:
            useless_run_koef(self.connection, 'useless_koef.csv',
                             self.FromDateEditDate, self.ToDateEditDate)
        else:
            downtime_koef(self.connection, 'downtime_koef.csv',
                          self.FromDateEditDate, self.ToDateEditDate)
    def __init__(self, connection, rep):
        super(PeriodWindow, self).__init__()
        self.ui = Ui_Period()
        self.ui.setupUi(self)
        self.connection = connection
        self.rep = rep
        self.FromDateEditDate = datetime.date.today()
        self.ui.FromDateEdit.setDate(self.FromDateEditDate)
        self.ui.FromDateEdit.setCalendarPopup(1)
        self.ui.FromDateEdit.dateChanged.connect(self.FromDateEdit_slot)
        self.ToDateEditDate = datetime.date.today()
        self.ui.ToDateEdit.setDate(self.ToDateEditDate)
        self.ui.ToDateEdit.setCalendarPopup(1)
        self.ui.ToDateEdit.dateChanged.connect(self.FromDateEdit_slot)
        self.ui.ReportButton.clicked.connect(self.ReportButton_slot)

if __name__ == '__main__':
    MyDB = pymysql.connect(user='root', host='127.0.0.1', password='TeamSpirit2021', db='logistics')
    app = QtWidgets.QApplication([])
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    application = PeriodWindow(MyDB)
    application.show()

    sys.exit(app.exec())